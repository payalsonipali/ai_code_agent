SYSTEM_PROMPT = """
You are a senior software engineer.

Rules:
- Write clean, production-ready code.
- Follow best practices.
- Add meaningful comments.
- Handle edge cases.
- Return ONLY raw code.
- No markdown.
"""
def build_code_prompt(language: str, task: str) -> str:
    return f"""
{SYSTEM_PROMPT}

Language: {language}

Task:
{task}
"""