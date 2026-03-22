"""
Specification Parser - Parses natural language project requirements
and extracts structured information for project generation.
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from ai_code_agent.engine.model import AIEngine


class SpecParser:
    """Parse natural language project specifications using AI or regex patterns."""

    def __init__(self, use_ai: bool = True):
        """
        Initialize parser.

        Args:
            use_ai: Whether to use Ollama for intelligent parsing
        """
        self.use_ai = use_ai
        self.engine = AIEngine() if use_ai else None
        self.tech_keywords = {
            "nextjs": ["next.js", "next", "react", "typescript"],
            "fastapi": ["fastapi", "python api", "async api", "pydantic"],
            "django": ["django", "python web", "django orm", "drf"],
            "spring_boot": ["spring boot", "java", "spring framework"],
            "kotlin": ["kotlin", "jvm", "gradle"],
            "golang": ["go", "golang"],
            "rust": ["rust", "cargo"],
        }

        self.feature_keywords = {
            "api_routes": ["api", "rest", "endpoints", "routes"],
            "database": ["database", "db", "sql", "postgresql", "mongodb", "orm"],
            "orm": ["orm", "sqlalchemy", "django orm"],
            "auth": ["authentication", "auth", "login", "user", "jwt", "oauth"],
            "docker": ["docker", "container", "dockercompose", "kubernetes"],
            "testing": ["test", "pytest", "jest", "unit test", "integration test"],
            "tailwind": ["tailwind", "css", "styling", "design"],
            "cors": ["cors", "cross-origin"],
            "validation": ["validate", "validation", "pydantic"],
            "admin": ["admin", "dashboard", "management"],
            "rest_api": ["rest api", "restful"],
            "security": ["security", "secure"],
            "coroutines": ["async", "coroutine", "concurrent"],
            "grpc": ["grpc", "protobuf"],
            "async": ["async", "asynchronous", "concurrent"],
        }

    def parse_with_ai(self, spec_text: str) -> Dict:
        """
        Use Ollama to intelligently parse the specification.

        Args:
            spec_text: Natural language project specification

        Returns:
            dict: Parsed specification with tech, features, name, details
        """
        prompt = f"""Analyze this project specification and extract structured information.

Specification:
{spec_text}

Return a JSON response with EXACTLY this structure (no markdown, just json):
{{
    "technology": "nextjs|fastapi|django|spring_boot|kotlin|golang|rust",
    "project_name": "project-name-in-kebab-case",
    "description": "brief project description",
    "features": ["feature1", "feature2"],
    "custom_requirements": ["requirement1", "requirement2"],
    "notes": "any additional notes about the project",
    "confidence": 0.0-1.0
}}

Guidelines:
- technology: Choose the best match from: nextjs, fastapi, django, spring_boot, kotlin, golang, rust
- project_name: Extract or infer from text, make it hyphenated lowercase
- features: Include from: api_routes, database, orm, auth, docker, testing, tailwind, cors, validation, admin, rest_api, security, coroutines, grpc, async
- custom_requirements: Any special requirements not covered by standard features
- confidence: How confident you are in the parsing (0.0 to 1.0)

Return ONLY valid JSON, no explanations."""

        try:
            response = self.engine.generate_code("json", prompt)
            parsed = json.loads(response)
            return parsed
        except Exception as e:
            print(f"Warning: AI parsing failed ({e}), using keyword-based parsing")
            return self.parse_with_keywords(spec_text)

    def parse_with_keywords(self, spec_text: str) -> Dict:
        """
        Parse specification using keyword matching (fallback method).

        Args:
            spec_text: Natural language project specification

        Returns:
            dict: Parsed specification
        """
        text_lower = spec_text.lower()

        # Detect technology
        detected_tech = None
        for tech, keywords in self.tech_keywords.items():
            if any(kw in text_lower for kw in keywords):
                detected_tech = tech
                break
        detected_tech = detected_tech or "nextjs"

        # Extract project name
        project_name = self._extract_project_name(spec_text)
        if not project_name:
            project_name = "my-app"

        # Detect features
        detected_features = []
        for feature, keywords in self.feature_keywords.items():
            if any(kw in text_lower for kw in keywords):
                detected_features.append(feature)

        return {
            "technology": detected_tech,
            "project_name": project_name,
            "description": spec_text[:200],
            "features": detected_features,
            "custom_requirements": [],
            "notes": "Parsed using keyword matching",
            "confidence": 0.6,
        }

    def _extract_project_name(self, text: str) -> Optional[str]:
        """Extract project name from text."""
        # Look for quoted name
        quoted_match = re.search(r'["\']([a-zA-Z0-9\-_]+)["\']', text)
        if quoted_match:
            return quoted_match.group(1).lower().replace(" ", "-")

        # Look for "called X" pattern
        called_match = re.search(r'(?:called|named|project\s+)([a-zA-Z0-9\-_ ]+)', text, re.IGNORECASE)
        if called_match:
            return called_match.group(1).strip().lower().replace(" ", "-")

        # Look for first capitalized word after certain keywords
        for keyword in ["for", "building", "creating", "making"]:
            pattern = rf'{keyword}\s+(?:a|an|the)?\s*([A-Z][a-zA-Z0-9\s]+)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip().lower().replace(" ", "-")

        return None

    def validate_parsed_spec(self, spec: Dict) -> Tuple[bool, List[str]]:
        """
        Validate parsed specification.

        Args:
            spec: Parsed specification dict

        Returns:
            tuple: (is_valid, list_of_errors)
        """
        errors = []

        if not spec.get("technology"):
            errors.append("No technology detected")
        elif spec["technology"] not in self.tech_keywords.keys():
            errors.append(f"Unknown technology: {spec['technology']}")

        if not spec.get("project_name"):
            errors.append("No project name found")
        elif not re.match(r'^[a-z0-9_-]+$', spec["project_name"]):
            errors.append(f"Invalid project name format: {spec['project_name']}")

        if spec.get("confidence", 0) < 0.3:
            errors.append("Low confidence in parsing - consider revising specification")

        return len(errors) == 0, errors

    def parse_spec_file(self, file_path: str) -> Dict:
        """
        Parse a specification file.

        Args:
            file_path: Path to spec file

        Returns:
            dict: Parsed specification
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                spec_text = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Specification file not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading specification file: {e}")

        if self.use_ai:
            parsed = self.parse_with_ai(spec_text)
        else:
            parsed = self.parse_with_keywords(spec_text)

        # Validate
        is_valid, errors = self.validate_parsed_spec(parsed)
        if not is_valid:
            print("⚠️  Parsing warnings:")
            for error in errors:
                print(f"   - {error}")

        return parsed

    def print_parsed_spec(self, spec: Dict) -> None:
        """Print parsed specification in a readable format."""
        print("\n" + "=" * 60)
        print("📋 Parsed Project Specification")
        print("=" * 60)
        print(f"Technology: {spec.get('technology', 'unknown').upper()}")
        print(f"Project Name: {spec.get('project_name', 'unknown')}")
        print(f"Description: {spec.get('description', 'N/A')[:100]}")
        print(f"Features: {', '.join(spec.get('features', []))}")
        if spec.get("custom_requirements"):
            print(f"Custom Requirements: {', '.join(spec.get('custom_requirements', []))}")
        print(f"Confidence: {spec.get('confidence', 0):.0%}")
        print("=" * 60 + "\n")

    def confirm_spec_interactive(self, spec: Dict) -> bool:
        """
        Ask user to confirm parsed specification.

        Args:
            spec: Parsed specification

        Returns:
            bool: True if user confirms
        """
        self.print_parsed_spec(spec)

        while True:
            response = input("Does this look correct? (yes/no): ").strip().lower()
            if response in ["yes", "y"]:
                return True
            elif response in ["no", "n"]:
                return False
            else:
                print("Please enter 'yes' or 'no'")
