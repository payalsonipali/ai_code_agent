from engine.model import AIEngine

engine = AIEngine()

language = input("Language: ")
task = input("Task: ")

print("\nGenerating...\n")
code = engine.generate_code(language, task)

print("========== OUTPUT ==========\n")
print(code)