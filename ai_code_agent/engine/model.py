import ollama
import re
from .prompts import build_code_prompt


class AIEngine:
    def __init__(self, model_name: str = "deepseek-r1:7b"):
        self.model_name = model_name

    def _extract_code(self, text: str) -> str:
        pattern = r"```(?:\w+)?\n(.*?)```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()

    def generate_code(self, language: str, task: str) -> str:
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