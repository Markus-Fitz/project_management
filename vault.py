import shutil
from pathlib import Path
import frontmatter

# ── Reading ───────────────────────────────────────────────────────────────────

def read_file(filepath: Path) -> tuple[dict, str]:
    """
    Read a markdown file and return its frontmatter and body separately.

    Example:
        meta, body = read_file(PROJECTS_PATH / "my-project" / "README.md")
        print(meta["status"])   # "active"
    """
    post = frontmatter.load(filepath)
    return dict(post.metadata), post.content


# ── Creating ──────────────────────────────────────────────────────────────────

def copy_file_template(template_file: Path, destination: Path) -> None:
    """
    Copy a template file to a destination path.
    Raises FileExistsError if the destination already exists.
    Raises FileNotFoundError if the template does not exist.

    Example:
        copy_from_template(
            template_file = TEMPLATES_PATH / "Template_development" / "README.md",
            destination   = PROJECTS_PATH / "my-project" / "README.md"
        )
    """
    if destination.exists():
        raise FileExistsError(f"File already exists: {destination}")
    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_file}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(template_file, destination)

def copy_folder_template(name: str, id: int, template_folder: Path = Path(__file__).parent.parent / "project_templates" / "Template_development") -> None:
    """
    Copy a template folder structure (vault) to a destination path.
    Raises FileExistsError if the destination already exists.
    Raises FileNotFoundError if the template does not exist.

    Example:
        copy_from_template(
            template_file = TEMPLATES_PATH / "Template_development"
            destination   = PROJECTS_PATH / "my-project"
        )
    """
    project_path = Path = Path(__file__).parent.parent / name
    if project_path.exists():
        raise FileExistsError(f"Project folder already exsists: {project_path}")
    if not template_folder.exists():
        raise FileNotFoundError(f"Template folder was not found: {template_folder}")
    
    shutil.copytree(template_folder, project_path)

# ── Writing ───────────────────────────────────────────────────────────────────

def update_frontmatter(filepath: Path, updates: dict) -> None:
    """
    Read a file, apply a dict of changes to its frontmatter, write it back.
    Only the fields in `updates` are changed — everything else is preserved.

    Example:
        update_frontmatter(
            filepath = PROJECTS_PATH / "my-project" / "tasks" / "my-project-001.md",
            updates  = {"status": "done", "actual_hours": 6.0}
        )
    """
    metadata, body = read_file(filepath)
    metadata.update(updates)

    post = frontmatter.Post(content=body, **metadata)
    with open(filepath, "w", encoding="utf-8") as f:
        frontmatter.dump(post, f)