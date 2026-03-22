"""
AI Code Agent - Main entry point
Routes to scaffolder, spec-based generation, or code generation based on arguments
"""

import sys

# Configure UTF-8 for emoji support on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from pathlib import Path
from ai_code_agent.scaffolder import ProjectScaffolder
from ai_code_agent.engine.model import AIEngine
from ai_code_agent.utils import SpecParser


def show_help():
    """Display help message."""
    print("""
AI Code Agent - Project Scaffolder & Code Generator

Usage:
    python -m ai_code_agent                         # Interactive project scaffolding
    python -m ai_code_agent --from-spec <file>     # Create project from spec file
    python -m ai_code_agent --gen                   # Code snippet generator
    python -m ai_code_agent --help                  # Show this help

Commands:
    scaffold (default)      - Interactive menu to create new project
    --from-spec <file>      - Create project from specification file
    --gen / generate        - Generate code snippets
    --help                  - Show this help message

Specification File Format:
    Write natural language project description in a .txt or .spec file:

    Example (my_project.spec):
    -------
    I need a Next.js web application called "ecommerce-store" with:
    - React components for shopping cart
    - TypeScript for type safety
    - Tailwind CSS for styling
    - Authentication system for users
    - Docker support for easy deployment
    -------

    Then run: python -m ai_code_agent --from-spec my_project.spec

Features:
    - Supports: nextjs, fastapi, django, spring_boot, kotlin, golang, rust
    - AI parses natural language descriptions (uses Ollama if available)
    - Validates project names and configurations
    - Creates production-ready boilerplate code
""")


def main():
    """Main entry point."""
    if "--help" in sys.argv or "-h" in sys.argv:
        show_help()
        return

    # Check for spec-based generation
    if "--from-spec" in sys.argv:
        try:
            spec_idx = sys.argv.index("--from-spec")
            if spec_idx + 1 >= len(sys.argv):
                print("❌ Error: --from-spec requires a file path")
                print("Usage: python -m ai_code_agent --from-spec <file>")
                return

            spec_file = sys.argv[spec_idx + 1]

            # Parse specification
            print(f"📖 Reading specification from: {spec_file}")
            parser = SpecParser(use_ai=True)

            try:
                parsed_spec = parser.parse_spec_file(spec_file)
                parser.print_parsed_spec(parsed_spec)

                # Confirm with user
                if not parser.confirm_spec_interactive(parsed_spec):
                    print("❌ Project creation cancelled")
                    return

                # Create project from spec
                scaffolder = ProjectScaffolder()
                if scaffolder.create_project_from_spec(parsed_spec):
                    print("✓ Project creation successful!")
                else:
                    print("❌ Project creation failed")

            except FileNotFoundError as e:
                print(f"❌ Error: {e}")
            except Exception as e:
                print(f"❌ Error parsing specification: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
        return

    if "--gen" in sys.argv or "generate" in sys.argv:
        # Code snippet generation mode (original functionality)
        engine = AIEngine()
        language = input("Language: ").strip()
        task = input("Task: ").strip()

        if not language or not task:
            print("❌ Language and task are required")
            return

        print("\n⏳ Generating...\n")
        try:
            code = engine.generate_code(language, task)
            print("========== OUTPUT ==========\n")
            print(code)
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        # Project scaffolding mode (interactive)
        scaffolder = ProjectScaffolder()
        scaffolder.start()


if __name__ == "__main__":
    main()
