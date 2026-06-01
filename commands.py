from vault import copy_file_template, copy_folder_template, update_frontmatter, read_file, get_next_id
from datetime import datetime
from pathlib import Path
import re

def initialize_project(project_name: str, template_name: str, starting_date:datetime.date = datetime.now().date()) -> None:
    """
    Initializes a project from a template and sets the project_name and starting_date in the frontmatter.
    """
    parent_path = Path(__file__).parent.parent
    # create new project-folder from template
    try:
        copy_folder_template(project_name, parent_path / "project_templates" / template_name)
    except FileExistsError:
        print("A folder with that name already exists.")
        return # exit out of function
    except FileNotFoundError:
        print("The specified project template was not found.")
        return # exit out of function
    
    #look for highest ID in the current directory and iterate by one
    next_id = get_next_id("*/Main_page.md", "PROJ", parent_path)

    # update frontmatter to match new project
    update_frontmatter(parent_path / project_name / "Main_page.md", {"id": next_id, "name": project_name, "created_on": str(starting_date)})

def add_task(project_dir: Path, name: str) -> None:
    """
    Creates a new task in a project folder from the template file in that project folder.
    Task name, id and created_on date are always modified.
    """
    file_name = name + ".md"
    task_path = project_dir / "Tasks" / file_name
    try:
        copy_file_template(project_dir / "Templates" / "Task.md", task_path)
    except FileExistsError:
        print("A task file with that name already exists.")
        return
    except FileNotFoundError:
        print("The task template was not found.")
        return
    next_id = get_next_id("*.md", "TASK", project_dir / "Tasks")
    update_frontmatter(task_path, {"id": next_id, "created_on": datetime.now().date()})

def add_hours(path: Path, hours: float) -> None:
    """
    Adds a specified amount of hours to the current hour count.
    """
    meta, _ = read_file(path)
    current_hours = float(meta.get("time_spent", ""))
    hours += current_hours
    update_frontmatter(path, {"time_spent": hours})

def mark_task_done(task_path: Path) -> None:
    """
    Updates the frontmatter fields of a task and triggers corresponding logic.
    """
    meta, _ = read_file(task_path)
    match = re.fullmatch(rf"done", str(meta.get("status", "")))
    if match:
        print(f"Task at filepath {task_path} is alredy marked as done.")
        return
    update_frontmatter(task_path, {"status": "done", "end_date": datetime.now().date()})

def add_research_note(project_dir: Path, name: str) -> None:
    """
    Creates a new research_note in a project folder from the template file in that project folder.
    Project_note name, id and created_on date are always modified.
    """
    file_name = name + ".md"
    research_note_path = project_dir / "Research_notes" / file_name
    try:
        copy_file_template(project_dir / "Templates" / "Research_note.md", research_note_path)
    except FileExistsError:
        print("A research_note file with that name already exists.")
        return
    except FileNotFoundError:
        print("The research_note template was not found.")
        return
    next_id = get_next_id("*.md", "RES", project_dir / "Research_notes")
    update_frontmatter(research_note_path, {"id": next_id, "created_on": datetime.now().date()})

def add_supplier(project_dir: Path, name: str) -> None:
    """
    Creates a new supplier in a project folder from the template file in that project folder.
    Supplier name, id and created_on date are always modified.
    """
    file_name = name + ".md"
    supplier_path = project_dir / "Suppliers" / file_name
    try:
        copy_file_template(project_dir / "Templates" / "Supplier.md", supplier_path)
    except FileExistsError:
        print("A supplier file with that name already exists.")
        return
    except FileNotFoundError:
        print("The supplier template was not found.")
        return
    next_id = get_next_id("*.md", "SUP", project_dir / "Suppliers")
    update_frontmatter(supplier_path, {"id": next_id, "created_on": datetime.now().date()})

def add_purchase(project_dir: Path, name: str, linked_file: Path, linked_supplier: Path) -> None:
    """
    Creates a new purchase in a project folder from the template file in that project folder.
    Purchase name, id, created_on date, linked file (Task / Research_note) and Supplier are always modified.
    """
    if not linked_file.is_file():
        print("Purchase not created, linked file does not exist.")
        return
    if not linked_supplier.is_file():
        print("Purchase not created, linked supplier does not exist.")
        return
    file_name = name + ".md"
    purchase_path = project_dir / "Purchases" / file_name
    try:
        copy_file_template(project_dir / "Templates" / "Purchase.md", purchase_path)
    except FileExistsError:
        print("A purchase file with that name already exists.")
        return
    except FileNotFoundError:
        print("The purchase template was not found.")
        return
    next_id = get_next_id("*.md", "PUR", project_dir / "Purchases")
    update_frontmatter(purchase_path, {"id": next_id, "created_on": datetime.now().date(), "purchase_linked_file": f"[[{linked_file.stem}]]", "supplier": f"[[{linked_supplier.stem}]]"})