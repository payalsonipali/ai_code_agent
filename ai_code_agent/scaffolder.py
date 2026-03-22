"""
Project Scaffolder - Main orchestrator for generating projects.
"""

import json
from pathlib import Path
from typing import Dict, List
from ai_code_agent.engine.model import AIEngine
from ai_code_agent.templates.project_templates import get_template
from ai_code_agent.utils.file_handler import FileHandler


class ProjectScaffolder:
    """Main class for orchestrating project scaffolding."""

    def __init__(self):
        """Initialize the scaffolder."""
        self.engine = AIEngine()
        self.current_path = Path.cwd()
        self.tech_config = self._load_tech_config()

    def _load_tech_config(self) -> Dict:
        """Load technology configuration."""
        config_path = Path(__file__).parent / "templates" / "tech_config.json"
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading tech config: {e}")
            return {}

    def show_menu(self) -> str:
        """Display technology selection menu and return chosen tech."""
        print("\n" + "=" * 60)
        print("🚀 AI Code Agent - Project Scaffolder")
        print("=" * 60)
        print("\nSelect a technology stack:\n")

        techs = list(self.tech_config.get("technologies", {}).items())

        for i, (key, tech) in enumerate(techs, 1):
            print(f"  [{i}] {tech['name']}")
            print(f"      {tech['description']}")

        print(f"  [{len(techs) + 1}] Exit")

        while True:
            try:
                choice = input("\nEnter your choice (number): ").strip()
                choice_num = int(choice)

                if choice_num == len(techs) + 1:
                    print("Goodbye!")
                    exit(0)

                if 1 <= choice_num <= len(techs):
                    selected_tech = techs[choice_num - 1][0]
                    return selected_tech

                print(f"Invalid choice. Please enter a number between 1 and {len(techs) + 1}")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def get_project_details(self, tech: str) -> tuple:
        """Get project name and selected features from user."""
        print("\n" + "-" * 60)

        # Get project name
        while True:
            project_name = input("Enter project name (alphanumeric, hyphens, underscores): ").strip()
            if FileHandler.validate_project_name(project_name):
                break
            print("❌ Invalid name. Use only letters, numbers, hyphens, and underscores.")

        # Get features
        tech_info = self.tech_config["technologies"][tech]
        available_features = tech_info.get("features", [])

        if available_features:
            print(f"\nAvailable features for {tech_info['name']}:")
            for i, feature in enumerate(available_features, 1):
                print(f"  [{i}] {feature}")

            selected_features = []
            print("\nEnter feature numbers (comma-separated) or press Enter for defaults:")
            feature_input = input("Features: ").strip()

            if feature_input:
                try:
                    indices = [int(x.strip()) - 1 for x in feature_input.split(",")]
                    selected_features = [
                        available_features[i] for i in indices
                        if 0 <= i < len(available_features)
                    ]
                except ValueError:
                    print("Using default features")
                    selected_features = tech_info.get("defaults", [])
            else:
                selected_features = tech_info.get("defaults", [])

            print(f"✓ Selected features: {', '.join(selected_features)}")
        else:
            selected_features = tech_info.get("defaults", [])

        return project_name, selected_features

    def create_project(self):
        """Main orchestration method."""
        try:
            # Step 1: Show menu and get technology
            selected_tech = self.show_menu()
            tech_info = self.tech_config["technologies"][selected_tech]

            print(f"\n✓ Selected: {tech_info['name']}")

            # Step 2: Get project details
            project_name, selected_features = self.get_project_details(selected_tech)

            # Step 3: Create project directory
            print("\n" + "-" * 60)
            print(f"📁 Creating project directory...")
            try:
                project_path = FileHandler.create_project_directory(
                    self.current_path, project_name
                )
                print(f"✓ Created {project_path}")
            except FileExistsError as e:
                print(f"❌ Error: {e}")
                return

            # Step 4: Generate files using template (faster than AI)
            print(f"📝 Generating project files...")
            try:
                template_files = get_template(selected_tech, project_name, selected_features)

                # Create directory structure
                folders = tech_info.get("folders", [])
                if folders:
                    FileHandler.create_directory_structure(project_path, folders)

                # Add .gitignore
                template_files[".gitignore"] = FileHandler.get_gitignore(selected_tech)

                # Write all files
                created_files = FileHandler.write_files(project_path, template_files)
                print(f"✓ Generated {len(created_files)} files")

            except Exception as e:
                print(f"❌ Error generating files: {e}")
                return

            # Step 5: Print summary
            FileHandler.print_project_summary(project_path, created_files)

            print("\n" + "=" * 60)
            print("✓ Project created successfully!")
            print("=" * 60 + "\n")

        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
        except Exception as e:
            print(f"\n❌ Error: {e}")

    def create_project_from_spec(self, spec: Dict) -> bool:
        """
        Create project from parsed specification.

        Args:
            spec: Parsed specification dictionary

        Returns:
            bool: True if successful
        """
        try:
            selected_tech = spec.get("technology", "nextjs")
            project_name = spec.get("project_name", "my-app")
            selected_features = spec.get("features", [])

            tech_info = self.tech_config["technologies"].get(selected_tech, {})

            if not tech_info:
                print(f"❌ Unknown technology: {selected_tech}")
                return False

            print(f"\n✓ Technology: {tech_info['name']}")
            print(f"✓ Project Name: {project_name}")
            print(f"✓ Features: {', '.join(selected_features)}")

            # Step 1: Create project directory
            print("\n" + "-" * 60)
            print(f"📁 Creating project directory...")
            try:
                project_path = FileHandler.create_project_directory(
                    self.current_path, project_name
                )
                print(f"✓ Created {project_path}")
            except FileExistsError as e:
                print(f"❌ Error: {e}")
                return False

            # Step 2: Generate files
            print(f"📝 Generating project files...")
            try:
                template_files = get_template(selected_tech, project_name, selected_features)

                # Create directory structure
                folders = tech_info.get("folders", [])
                if folders:
                    FileHandler.create_directory_structure(project_path, folders)

                # Add .gitignore
                template_files[".gitignore"] = FileHandler.get_gitignore(selected_tech)

                # Write all files
                created_files = FileHandler.write_files(project_path, template_files)
                print(f"✓ Generated {len(created_files)} files")

            except Exception as e:
                print(f"❌ Error generating files: {e}")
                return False

            # Step 3: Print summary
            FileHandler.print_project_summary(project_path, created_files)

            # Step 4: Save spec for reference
            spec_file = project_path / ".project-spec.json"
            with open(spec_file, 'w') as f:
                json.dump(spec, f, indent=2)
            print(f"💾 Specification saved to: {spec_file}")

            print("\n" + "=" * 60)
            print("✓ Project created successfully!")
            print("=" * 60 + "\n")
            return True

        except Exception as e:
            print(f"\n❌ Error: {e}")
            return False

    def start(self):
        """Start the scaffolder."""
        self.create_project()


def main():
    """Entry point."""
    scaffolder = ProjectScaffolder()
    scaffolder.start()


if __name__ == "__main__":
    main()
