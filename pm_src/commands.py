from operations import copy_file_template, copy_folder_template, update_frontmatter, read_file, get_next_id
from datetime import datetime
from pathlib import Path
import re

def initialize_project(project_name: str, template_name: str, starting_date:str = str(datetime.now().date())) -> str:
    """
    Initializes a project from a template and sets the project_name and starting_date in the frontmatter.
    """
    parent_path = Path(__file__).parent.parent.parent
    # create new project-folder from template
    try:
        copy_folder_template(project_name, parent_path / "project_templates" / template_name)
    except FileExistsError:
        return "A folder with that name already exists."
    except FileNotFoundError:
        return "The specified project template was not found."
    
    #look for highest ID in the current directory and iterate by one
    next_id = get_next_id("*/Main_page.md", "PROJ", parent_path)

    # update frontmatter to match new project
    update_frontmatter(parent_path / project_name / "Main_page.md", {"id": next_id, "name": project_name, "created_on": starting_date})

    return "Project created successfully."

def add_task(project_name: str, task_name: str) -> str:
    """
    Creates a new task in a project folder from the template file in that project folder.
    Task name, id and created_on date are always modified.
    """
    parent_dir = Path(__file__).parent.parent.parent
    project_dir = parent_dir / project_name
    file_name = task_name + ".md"
    task_path = project_dir / "Tasks" / file_name
    try:
        copy_file_template(project_dir / "Templates" / "Task.md", task_path)
    except FileExistsError:
        return "A task file with that name already exists."
    except FileNotFoundError:
        return "The task template was not found."
    next_id = get_next_id("*.md", "TASK", project_dir / "Tasks")
    update_frontmatter(task_path, {"id": next_id, "created_on": datetime.now().date()})
    return "Task successfully created."

def add_task_hours(project_name: str, task_name: str, hours: str) -> str:
    """
    Adds a specified amount of hours to the current hour count.
    """
    parent_dir = Path(__file__).parent.parent.parent
    project_dir = parent_dir / project_name
    file_name = task_name + ".md"
    task_path = project_dir / "Tasks" / file_name
    meta, _ = read_file(task_path)
    current_hours = float(meta.get("time_spent", ""))
    hours = float(hours)
    hours += current_hours
    update_frontmatter(task_path, {"time_spent": hours})
    return "Hours successfully added to task."

def mark_task_done(project_name: str, task_name: str) -> str:
    """
    Updates the frontmatter fields of a task and triggers corresponding logic.
    """
    parent_dir = Path(__file__).parent.parent.parent
    project_dir = parent_dir / project_name
    file_name = task_name + ".md"
    task_path = project_dir / "Tasks" / file_name
    meta, _ = read_file(task_path)
    match = meta.get("status", "")
    if match == "done":
        return f"Task at filepath {task_path} is already marked as done."
    update_frontmatter(task_path, {"status": "done", "end_date": datetime.now().date()})
    return "Task successfully marked as done."

def add_research_note(project_name: str, note_name: str) -> str:
    """
    Creates a new research_note in a project folder from the template file in that project folder.
    Project_note name, id and created_on date are always modified.
    """
    parent_dir = Path(__file__).parent.parent.parent
    project_dir = parent_dir / project_name
    file_name = note_name + ".md"
    note_path = project_dir / "Research_notes" / file_name
    try:
        copy_file_template(project_dir / "Templates" / "Research_note.md", note_path)
    except FileExistsError:
        return "A research_note file with that name already exists."
    except FileNotFoundError:
        return "The research_note template was not found."
    next_id = get_next_id("*.md", "RES", project_dir / "Research_notes")
    update_frontmatter(note_path, {"id": next_id, "created_on": datetime.now().date()})
    return "Research_note successfully created."

def add_note_hours(project_name: str, note_name: str, hours: str) -> str:
    """
    Adds a specified amount of hours to the current hour count.
    """
    parent_dir = Path(__file__).parent.parent.parent
    project_dir = parent_dir / project_name
    file_name = note_name + ".md"
    note_path = project_dir / "Research_notes" / file_name
    meta, _ = read_file(note_path)
    current_hours = float(meta.get("time_spent", ""))
    hours = float(hours)
    hours += current_hours
    update_frontmatter(note_path, {"time_spent": hours})
    return "Hours successfully added to research note."

def add_supplier(project_name:str, supplier_name: str) -> str:
    """
    Creates a new supplier in a project folder from the template file in that project folder.
    Supplier name, id and created_on date are always modified.
    """
    parent_dir = Path(__file__).parent.parent.parent
    project_dir = parent_dir / project_name
    file_name = supplier_name + ".md"
    supplier_path = project_dir / "Suppliers" / file_name
    try:
        copy_file_template(project_dir / "Templates" / "Supplier.md", supplier_path)
    except FileExistsError:
        return "A supplier file with that name already exists."
    except FileNotFoundError:
        return "The supplier template was not found."
    next_id = get_next_id("*.md", "SUP", project_dir / "Suppliers")
    update_frontmatter(supplier_path, {"id": next_id, "created_on": datetime.now().date()})
    return "Supplier created successfully."

def get_project_structure(project_name: str) -> dict:
    """
    Returns an overview of a project: project metadata, all tasks, and all research notes.
    Files without a valid ID (e.g. README.md) are skipped.
    All date fields are returned as strings for JSON compatibility.
    """
    parent_dir = Path(__file__).parent.parent.parent
    project_dir = parent_dir / project_name

    meta, _ = read_file(project_dir / "Main_page.md")
    project_info = {
        "id":         str(meta.get("id", "")),
        "name":       str(meta.get("name", project_name)),
        "status":     str(meta.get("status", "")),
        "created_on": str(meta.get("created_on", ""))
    }

    tasks = []
    tasks_dir = project_dir / "Tasks"
    if tasks_dir.exists():
        for file in sorted(tasks_dir.glob("*.md")):
            meta, _ = read_file(file)
            if not re.fullmatch(r"TASK-\d+", str(meta.get("id", ""))):
                continue
            tasks.append({
                "name":       file.stem,
                "id":         str(meta.get("id", "")),
                "status":     str(meta.get("status", "")),
                "priority":   meta.get("priority", None),
                "time_spent": float(meta.get("time_spent", 0.0)),
                "created_on": str(meta.get("created_on", "")),
                "end_date":   str(meta.get("end_date")) if meta.get("end_date") else None
            })

    research_notes = []
    notes_dir = project_dir / "Research_notes"
    if notes_dir.exists():
        for file in sorted(notes_dir.glob("*.md")):
            meta, _ = read_file(file)
            if not re.fullmatch(r"RES-\d+", str(meta.get("id", ""))):
                continue
            research_notes.append({
                "name":       file.stem,
                "id":         str(meta.get("id", "")),
                "time_spent": float(meta.get("time_spent", 0.0)),
                "created_on": str(meta.get("created_on", ""))
            })

    return {
        "project":        project_info,
        "tasks":          tasks,
        "research_notes": research_notes
    }


def add_purchase(project_name: str, purchase_name: str, linked_file_dir: str, linked_file_name: str, linked_supplier: str) -> str:
    """
    Creates a new purchase in a project folder from the template file in that project folder.
    Purchase name, id, created_on date, linked file (Task / Research_note) and Supplier are always modified.
    """
    parent_dir = Path(__file__).parent.parent.parent
    project_dir = parent_dir / project_name
    file_name = purchase_name + ".md"
    purchase_path = project_dir / "Purchases" / file_name
    linked_file_path = project_dir / linked_file_dir / (linked_file_name + ".md")
    linked_supplier_path = project_dir / "Suppliers" / (linked_supplier + ".md")
    if not linked_file_path.is_file():
        return "Purchase not created, linked file does not exist."
    if not linked_supplier_path.is_file():
        return "Purchase not created, linked supplier does not exist."
    try:
        copy_file_template(project_dir / "Templates" / "Purchase.md", purchase_path)
    except FileExistsError:
        return "A purchase file with that name already exists."
    except FileNotFoundError:
        return "The purchase template was not found."
    next_id = get_next_id("*.md", "PUR", project_dir / "Purchases")
    update_frontmatter(purchase_path, {"id": next_id, "created_on": datetime.now().date(), "purchase_linked_file": f"[[{linked_file_path.stem}]]", "supplier": f"[[{linked_supplier_path.stem}]]"})
    return "Purchase created successfully."