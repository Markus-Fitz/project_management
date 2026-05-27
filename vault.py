# vault.py
# Responsible for reading and writing markdown files with YAML frontmatter.
# All other modules import from here when they need to touch the vault files.

import os
from pathlib import Path
import frontmatter  # pip install python-frontmatter


# ── Vault location ────────────────────────────────────────────────────────────
# Reads from environment variable, falls back to ~/vault
# Set your vault path with: export PM_VAULT_PATH="/path/to/your/vault"

VAULT_PATH = Path(os.environ.get("PM_VAULT_PATH", "~/vault")).expanduser()
PROJECTS_PATH = VAULT_PATH / "Projects"


# ── Reading ───────────────────────────────────────────────────────────────────

def read_file(filepath: Path) -> tuple[dict, str]:
    """
    Read a markdown file and return its frontmatter and body separately.

    Returns:
        frontmatter_data  -- dict of all YAML fields, e.g. {"id": "my-project", "status": "active"}
        body              -- the markdown text below the frontmatter block
    
    Example:
        meta, body = read_file(PROJECTS_PATH / "my-project" / "README.md")
        print(meta["status"])   # "active"
        print(body)             # "This project is about..."
    """
    post = frontmatter.load(filepath)
    return dict(post.metadata), post.content


# ── Writing ───────────────────────────────────────────────────────────────────

def write_file(filepath: Path, metadata: dict, body: str = "") -> None:
    """
    Write a dict of frontmatter fields and a markdown body to a file.
    Overwrites the file if it already exists.

    Example:
        write_file(
            filepath = PROJECTS_PATH / "my-project" / "README.md",
            metadata = {"id": "my-project", "status": "active"},
            body     = "This project is about building a weather station."
        )
    """
    post = frontmatter.Post(content=body, **metadata)
    with open(filepath, "wb") as f:
        frontmatter.dump(post, f)


# ── Convenience: update only frontmatter fields ───────────────────────────────

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
    write_file(filepath, metadata, body)