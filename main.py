#from vault import read_file, update_frontmatter, copy_file_template, copy_folder_template
from commands import initialize_project, add_task, mark_task_done, add_research_note, add_purchase, add_supplier, add_hours
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

# Create a folder from a template directory
#try:
#    copy_folder_template("test_project_from_template_1")
#except FileExistsError:
#    print("A project with that name already exists.")
#except FileNotFoundError:
#    print("The template could not be found.")

# File exists error should be thrown
#try:
#    copy_folder_template("test_project_from_template_1")
#except FileExistsError:
#    print("A project with that name already exists.")
#except FileNotFoundError:
#    print("The template could not be found.")

# The template could not be found error should be thrown
#try:
#    copy_folder_template("test_project_from_template_2", PARENT_DIR / "non-existant-folder")
#except FileExistsError:
#    print("A project with that name already exists.")
#except FileNotFoundError:
#    print("The template could not be found.")


initialize_project("test_dev-proj", "Template_development")
initialize_project("test_res-proj", "Template_research")

add_task(PARENT_DIR / "test_dev-proj", "test_task_ID-should-be-001")
add_task(PARENT_DIR / "test_dev-proj", "test_task_ID-should-be-002")

add_research_note(PARENT_DIR / "test_dev-proj", "test_note_ID-should-be-001")
add_research_note(PARENT_DIR / "test_dev-proj", "test_note_ID-should-be-002")

add_research_note(PARENT_DIR / "test_res-proj", "test_note_ID-should-be-001")
add_research_note(PARENT_DIR / "test_res-proj", "test_note_ID-should-be-002")

add_supplier(PARENT_DIR / "test_res-proj", "test-supplier_ID-should-be-001")
add_supplier(PARENT_DIR / "test_res-proj", "test-supplier_ID-should-be-002")
add_supplier(PARENT_DIR / "test_res-proj", "test-supplier_ID-should-be-002") # should fail as supplier exists

add_purchase(PARENT_DIR / "test_res-proj", "test_purchase_ID-should-fail", PARENT_DIR / "test_res-proj" / "Research_notes" / "test_note_ID-should-be-000.md", PARENT_DIR / "test_res-proj" / "Suppliers" / "test-supplier_ID-should-be-001.md") # should fail, as linked task file does not exist
add_purchase(PARENT_DIR / "test_res-proj", "test_purchase_ID-should-be-001", PARENT_DIR / "test_res-proj" / "Research_notes" / "test_note_ID-should-be-001.md", PARENT_DIR / "test_res-proj" / "Suppliers" / "test-supplier_ID-should-be-001.md")
add_purchase(PARENT_DIR / "test_res-proj", "test_purchase_ID-should-be-002", PARENT_DIR / "test_res-proj" / "Research_notes" / "test_note_ID-should-be-002.md", PARENT_DIR / "test_res-proj" / "Suppliers" / "test-supplier_ID-should-be-002.md")
add_purchase(PARENT_DIR / "test_res-proj", "test_purchase_ID-should-be-002", PARENT_DIR / "test_res-proj" / "Research_notes" / "test_note_ID-should-be-002.md", PARENT_DIR / "test_res-proj" / "Suppliers" / "test-supplier_ID-should-be-003.md") # should fail, as linked supplier file does not exist

add_hours(PARENT_DIR / "test_dev-proj" / "Tasks" / "test_task_ID-should-be-001.md", 1.0)
add_hours(PARENT_DIR / "test_dev-proj" / "Tasks" / "test_task_ID-should-be-001.md", 500)

add_hours(PARENT_DIR / "test_dev-proj" / "Research_notes" / "test_note_ID-should-be-001.md", 1.0)
add_hours(PARENT_DIR / "test_dev-proj" / "Research_notes" / "test_note_ID-should-be-001.md", 500)

mark_task_done(PARENT_DIR / "test_dev-proj" / "Tasks" / "test_task_ID-should-be-001.md")
mark_task_done(PARENT_DIR / "test_dev-proj" / "Tasks" / "test_task_ID-should-be-001.md")