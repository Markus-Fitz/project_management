import unittest
import tempfile
import shutil
import sys
from pathlib import Path
from datetime import date
import frontmatter as fm

sys.path.insert(0, str(Path(__file__).parent))
from operations import read_file, copy_file_template, copy_folder_template, update_frontmatter, get_next_id

WORKSPACE = Path(__file__).parent.parent.parent
TEMPLATE_DEV = WORKSPACE / "project_templates" / "Template_development"


def write_md(directory: Path, filename: str, metadata: dict, body: str = "") -> Path:
    path = directory / filename
    post = fm.Post(content=body, **metadata)
    with open(path, "w") as f:
        fm.dump(post, f)
    return path


class TestGetNextId(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.dir)

    def _write_with_id(self, filename: str, id_value: str):
        write_md(self.dir, filename, {"id": id_value})

    def test_returns_001_when_directory_is_empty(self):
        self.assertEqual(get_next_id("*.md", "TASK", self.dir), "TASK-001")

    def test_returns_next_id_after_existing_files(self):
        self._write_with_id("a.md", "TASK-001")
        self._write_with_id("b.md", "TASK-002")
        self.assertEqual(get_next_id("*.md", "TASK", self.dir), "TASK-003")

    def test_finds_highest_id_not_just_last_file(self):
        self._write_with_id("a.md", "TASK-005")
        self._write_with_id("b.md", "TASK-002")
        self.assertEqual(get_next_id("*.md", "TASK", self.dir), "TASK-006")

    def test_ignores_placeholder_id(self):
        self._write_with_id("a.md", "TASK-###")
        self.assertEqual(get_next_id("*.md", "TASK", self.dir), "TASK-001")

    def test_ignores_id_with_trailing_suffix(self):
        self._write_with_id("a.md", "TASK-001-old")
        self.assertEqual(get_next_id("*.md", "TASK", self.dir), "TASK-001")

    def test_result_is_zero_padded_to_three_digits(self):
        result = get_next_id("*.md", "TASK", self.dir)
        self.assertRegex(result, r"TASK-\d{3}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
