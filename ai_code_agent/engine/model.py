import ollama
import re
import json
from .prompts import build_code_prompt, build_project_prompt


class AIEngine:
    def __init__(self, model_name: str = "deepseek-r1:7b"):
        self.model_name = model_name

    def _extract_code(self, text: str) -> str:
        """Extract code from markdown code blocks."""
        pattern = r"```(?:\w+)?\n(.*?)```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()

    def _extract_json(self, text: str) -> dict:
        """Extract JSON from response, with fallback attempts."""
        # Try to parse as-is
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try to extract JSON from markdown code blocks
        json_pattern = r"```(?:json)?\n(.*?)```"
        match = re.search(json_pattern, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except json.JSONDecodeError:
                pass

        # Try to find JSON object/array in the text
        json_pattern = r'\{.*\}|\[.*\]'
        match = re.search(json_pattern, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass

        raise ValueError(f"Could not parse JSON response: {text[:200]}")

    def generate_code(self, language: str, task: str) -> str:
        """Generate code snippet for a given language and task."""
        prompt = build_code_prompt(language, task)

        response = ollama.generate(
            model=self.model_name,
            prompt=prompt,
            options={
                "temperature": 0.1,
                "top_p": 0.9,
                "num_ctx": 2048
            }
        )

        return self._extract_code(response["response"])

    def generate_project_files(
        self, tech: str, project_name: str, features: list
    ) -> dict:
        """
        Generate project files for the given technology stack.

        Returns:
            dict: {"files": {filename: content, ...}, "notes": "setup instructions"}
        """
        prompt = build_project_prompt(tech, project_name, features)

        response = ollama.generate(
            model=self.model_name,
            prompt=prompt,
            options={
                "temperature": 0.2,
                "top_p": 0.9,
                "num_ctx": 4096
            }
        )

        try:
            result = self._extract_json(response["response"])
            return result
        except Exception as e:
            print(f"Warning: Could not parse JSON, returning raw response")
            return {
                "files": {},
                "notes": f"Error: {str(e)}. Raw response: {response['response'][:500]}"
            }

    def generate_config_file(self, tech: str, filename: str, config_type: str) -> str:
        """Generate a specific configuration file for the tech stack."""
        prompt = f"""Generate a {config_type} file for {tech}.
Tech: {tech}
File: {filename}

Return ONLY the file content, no markdown blocks, no explanations."""

        response = ollama.generate(
            model=self.model_name,
            prompt=prompt,
            options={
                "temperature": 0.1,
                "top_p": 0.9,
                "num_ctx": 2048
            }
        )

        return self._extract_code(response["response"])