from vault import copy_file_template, copy_folder_template, update_frontmatter, read_file
from datetime import datetime
from pathlib import Path
import re

def get_next_id(file_name: str, abbrev: str, search_dir: Path) -> str:
    """
    Looks for files matching file_name, extracts the id if it matches the format abbrev-xxx and returns the highest id + 1 in the same format.
    """
    highest = 0
    for file in search_dir.glob("*/" + file_name):
        meta, _ = read_file(file)
        # looks for string with pattern "PROJ-xxx" with xxx being an integer
        # Pattern has to match "PROJ-123"; "PROJ-###" or "PROJ-123-old" does not match
        match = re.fullmatch(rf"{abbrev}-(\d+)", str(meta.get("id", "")))
        if match:
            highest = max(highest, int(match.group(1)))
    return f"{abbrev}-{highest + 1:03d}"

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
    next_id = get_next_id("Main_page.md", "PROJ", parent_path)

    # update frontmatter to match new project
    update_frontmatter(parent_path / project_name / "Main_page.md", {"id": next_id, "name": project_name, "created_on": str(starting_date)})

def add_task(project_dir: Path, name: str):
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
        print("The Task template was not found.")
        return
    next_id = get_next_id("", "TASK", project_dir / "Tasks")
    update_frontmatter(task_path, {"id": next_id, "created_on": datetime.now().date()})
