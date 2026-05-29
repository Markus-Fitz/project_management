import os
from vault import read_file, update_frontmatter, copy_from_template
from pathlib import Path

# ── Vault location ────────────────────────────────────────────────────────────

project_name = "test_project"

# Name of the parent directory everything happens in
PARENT_DIR = Path(__file__).parent.parent

# Name of the project directory which is subject to management
PROJECT_DIR = PARENT_DIR / project_name
PROJECT_TASK_DIR = PROJECT_DIR / "Tasks"

# Path to template directories
DEVELOPMENT_TEMPLATE_PATH = PARENT_DIR / "project_templates" / "Template_development"
RESEARCH_TEMPLATE_PATH = PARENT_DIR / "project_templates" / "Template_research"

# creating project directory and 
PROJECT_TASK_DIR.mkdir(parents=True, exist_ok=True)
copy_from_template(DEVELOPMENT_TEMPLATE_PATH / "Templates" / "Task.md", PROJECT_DIR / "Tasks" / "test_task.md")

update_frontmatter(PROJECT_DIR / "Tasks/test_task.md", {"status": "active", "id": "test-project"})

meta, body = read_file(PROJECT_DIR / "Tasks/test_task.md")
print(meta)  # should show updated fields