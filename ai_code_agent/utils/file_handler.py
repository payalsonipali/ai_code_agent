import os
from pathlib import Path
from typing import Dict, List, Optional
import re


class FileHandler:
    """Utility class for safe file and directory operations."""

    @staticmethod
    def validate_project_name(name: str) -> bool:
        """Validate project name - alphanumeric, hyphens, underscores only."""
        pattern = r'^[a-zA-Z0-9_-]+$'
        return bool(re.match(pattern, name)) and len(name) > 0

    @staticmethod
    def create_project_directory(base_path: str, project_name: str) -> Path:
        """
        Create project directory and return the path.
        Raises error if directory already exists.
        """
        if not FileHandler.validate_project_name(project_name):
            raise ValueError(
                f"Invalid project name: '{project_name}'. "
                "Use only alphanumeric characters, hyphens, and underscores."
            )

        project_path = Path(base_path) / project_name

        if project_path.exists():
            raise FileExistsError(
                f"Directory '{project_name}' already exists at {project_path}"
            )

        project_path.mkdir(parents=True, exist_ok=False)
        return project_path

    @staticmethod
    def create_directory_structure(
        base_path: Path, folders: List[str]
    ) -> None:
        """Create a directory structure."""
        for folder in folders:
            folder_path = base_path / folder
            folder_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def write_files(
        base_path: Path, files: Dict[str, str]
    ) -> List[str]:
        """
        Write files to disk.

        Args:
            base_path: Base directory path
            files: Dictionary of {relative_path: content}

        Returns:
            List of created file paths
        """
        created_files = []

        for file_path, content in files.items():
            full_path = base_path / file_path

            # Create parent directories if needed
            full_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

            created_files.append(str(full_path))

        return created_files

    @staticmethod
    def get_gitignore(tech: str) -> str:
        """Get tech-specific .gitignore content."""
        gitignores = {
            "nextjs": """# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/

# Next.js
.next/
out/

# Production
build/
dist/

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.idea/
.vscode/
*.swp
*.swo
*~
.DS_Store
""",
            "fastapi": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment variables
.env
.env.local

# Testing
.pytest_cache/
.coverage
htmlcov/
""",
            "django": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# Django
*.log
local_settings.py
db.sqlite3
/media
/static

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment
.env
.env.local
""",
            "spring_boot": """# Java
*.class
*.jar
*.war
*.ear

# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup

# IDE
.vscode/
.idea/
*.iml
*.iws
*.ipr
.classpath
.project
.settings/

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db
""",
            "kotlin": """# Kotlin/Java
*.class
*.jar
*.war
*.ear

# Gradle
.gradle
build/
gradle/

# IDE
.vscode/
.idea/
*.iml
*.iws
*.ipr
.classpath
.project
.settings/

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db
""",
            "golang": """# Go
/bin
/vendor
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment
.env
.env.local
""",
            "rust": """# Rust
/target
Cargo.lock
**/*.rs.bk

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment
.env
.env.local
""",
        }

        return gitignores.get(tech, """# General
.env
.env.local
.DS_Store
Thumbs.db
""")

    @staticmethod
    def print_project_summary(project_path: Path, files_created: List[str]) -> None:
        """Print a summary of created project."""
        print(f"\n✓ Project created successfully!")
        print(f"📁 Location: {project_path}")
        print(f"📦 Files created: {len(files_created)}")
        print(f"\n📋 Next steps:")
        print(f"   1. cd {project_path.name}")
        print(f"   2. Install dependencies (npm install / pip install -r requirements.txt)")
        print(f"   3. Start development server (npm run dev / python main.py)")
