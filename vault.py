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

def copy_from_template(template_file: Path, destination: Path) -> None:
    """
    Copy a template file to a destination path.
    Raises FileExistsError if the destination already exists.
    Raises FileNotFoundError if the template does not exist.

    Example:
        copy_from_template(
            template_file = TEMPLATES_PATH / "default" / "README.md",
            destination   = PROJECTS_PATH / "my-project" / "README.md"
        )
    """
    if destination.exists():
        raise FileExistsError(f"File already exists: {destination}")
    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_file}")

    shutil.copy2(template_file, destination)


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