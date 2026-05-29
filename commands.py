from vault import copy_file_template, copy_folder_template, update_frontmatter, read_file
from datetime import datetime
from pathlib import Path

# creates a new project folder with a name 
# reads projects in the folder - checks highest id and iterates by one
def initialize_project(project_name: str, template_name: str, starting_date:datetime.date = datetime.now().date()) -> None:
    parent_path = Path(__file__).parent.parent
    
    # create new project-folder from template
    try:
        copy_folder_template(project_name, parent_path / "projectttt_templates" / template_name)
    except FileExistsError:
        print("A folder with that name already exists.")
        return # exit out of function
    except FileNotFoundError:
        print("The specified project template was not found.")
        return # exit out of function
    
    # update frontmatter to match new project
    update_frontmatter(parent_path / project_name / "Main_page.md", {"name": project_name, "created_on": str(starting_date)})