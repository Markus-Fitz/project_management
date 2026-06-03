import shutil
from pathlib import Path
import frontmatter
import re

def read_file(filepath: Path) -> tuple[dict, str]:
    """
    Read a markdown file and return its frontmatter and body separately.
    """
    post = frontmatter.load(filepath)
    return dict(post.metadata), post.content

def copy_file_template(template_file: Path, destination: Path) -> None:
    """
    Copy a template file to a destination path.
    Raises FileExistsError if the destination already exists.
    Raises FileNotFoundError if the template does not exist.
    """
    if destination.exists():
        raise FileExistsError(f"File already exists: {destination}")
    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_file}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(template_file, destination)

def copy_folder_template(name: str, template_folder: Path = Path(__file__).parent.parent.parent / "project_templates" / "Template_development") -> None:
    """
    Copy a template folder structure (vault) to a destination path.
    Raises FileExistsError if the destination already exists.
    Raises FileNotFoundError if the template does not exist.
    """
    project_path = Path(__file__).parent.parent.parent / name
    if project_path.exists():
        raise FileExistsError(f"Project folder already exists: {project_path}")
    if not template_folder.exists():
        raise FileNotFoundError(f"Template folder was not found: {template_folder}")
    
    shutil.copytree(template_folder, project_path)

def update_frontmatter(filepath: Path, updates: dict) -> None:
    """
    Read a file, apply a dict of changes to its frontmatter, write it back.
    Only the fields in `updates` are changed — everything else is preserved.
    """
    metadata, body = read_file(filepath)
    metadata.update(updates)

    post = frontmatter.Post(content=body, **metadata)
    with open(filepath, "w", encoding="utf-8") as f:
        frontmatter.dump(post, f)

def get_next_id(glob_pattern: str, abbrev: str, search_dir: Path) -> str:
    """
    Looks for files matching file_name, extracts the id if it matches the format abbrev-xxx and returns the highest id + 1 in the same format.
    """
    highest = 0
    for file in search_dir.glob(glob_pattern):
        meta, _ = read_file(file)
        # looks for string with pattern "PROJ-xxx" with xxx being an integer
        # Pattern has to match "PROJ-123"; "PROJ-###" or "PROJ-123-old" does not match
        match = re.fullmatch(rf"{abbrev}-(\d+)", str(meta.get("id", "")))
        if match:
            highest = max(highest, int(match.group(1)))
    return f"{abbrev}-{highest + 1:03d}"