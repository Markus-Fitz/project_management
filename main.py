import os
from vault import read_file, update_frontmatter, copy_file_template, copy_folder_template
from pathlib import Path

# ── Vault location ────────────────────────────────────────────────────────────

project_name = "test_project"

# Name of the parent directory everything happens in
PARENT_DIR = Path(__file__).parent.parent

# Name of the project directory which is subject to management
PROJECT_DIR = PARENT_DIR / project_name

# Paths to all the sub-directories to test manual creation of files from templates
PROJECT_TASK_DIR = PROJECT_DIR / "Tasks"
PROJECT_PURCHASE_DIR = PROJECT_DIR / "Purchases"
PROJECT_SUPPLIER_DIR = PROJECT_DIR / "Suppliers"
PROJECT_RESEARCH_NOTE_DIR = PROJECT_DIR / "Research_notes"

# Path to template directories
DEVELOPMENT_TEMPLATE_PATH = PARENT_DIR / "project_templates" / "Template_development"
RESEARCH_TEMPLATE_PATH = PARENT_DIR / "project_templates" / "Template_research"

# creating Task directory and new Task.md from template
copy_file_template(DEVELOPMENT_TEMPLATE_PATH / "Templates" / "Task.md", PROJECT_TASK_DIR / "test_task.md")
update_frontmatter(PROJECT_TASK_DIR / "test_task.md", {"status": "active", "id": "TASK-000"})

# creating Purchase directory and new Purchase.md from template
copy_file_template(DEVELOPMENT_TEMPLATE_PATH / "Templates" / "Purchase.md", PROJECT_PURCHASE_DIR / "test_purchase.md")
update_frontmatter(PROJECT_PURCHASE_DIR / "test_purchase.md", {"amount": 100, "id": "PUR-000"})

# creating Supplier directory and new Supplier.md from template
copy_file_template(DEVELOPMENT_TEMPLATE_PATH / "Templates" / "Supplier.md", PROJECT_SUPPLIER_DIR / "test_supplier.md")
update_frontmatter(PROJECT_SUPPLIER_DIR / "test_supplier.md", {"name": "Amazon", "id": "SUP-000"})

# creating Research_note directory and new Research_note.md from template
copy_file_template(DEVELOPMENT_TEMPLATE_PATH / "Templates" / "Research_note.md", PROJECT_RESEARCH_NOTE_DIR / "test_research_note.md")
update_frontmatter(PROJECT_RESEARCH_NOTE_DIR / "test_research_note.md", {"source": "www.test_source.org", "id": "RES-000"})

meta, body = read_file(PROJECT_TASK_DIR / "test_task.md")
print("Updated Task meta: \n")
print(meta)  # should show updated fields

meta, body = read_file(PROJECT_PURCHASE_DIR / "test_purchase.md")
print("Updated Purchase meta: \n")
print(meta)  # should show updated fields

meta, body = read_file(PROJECT_SUPPLIER_DIR / "test_supplier.md")
print("Updated Supplier meta: \n")
print(meta)  # should show updated fields

meta, body = read_file(PROJECT_RESEARCH_NOTE_DIR / "test_research_note.md")
print("Updated Research-note meta: \n")
print(meta)  # should show updated fields