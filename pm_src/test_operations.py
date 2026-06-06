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


class TestReadFile(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_returns_metadata_and_body(self):
        path = write_md(self.dir, "f.md", {"id": "TASK-001", "status": "to-do"}, "# Hello")
        meta, body = read_file(path)
        self.assertEqual(meta["id"], "TASK-001")
        self.assertEqual(meta["status"], "to-do")
        self.assertIn("Hello", body)

    def test_empty_frontmatter_returns_empty_dict(self):
        path = write_md(self.dir, "f.md", {}, "just body")
        meta, body = read_file(path)
        self.assertEqual(meta, {})
        self.assertIn("just body", body)


class TestCopyFileTemplate(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())
        self.template = self.dir / "template.md"
        self.template.write_text("---\nid: TASK-###\n---\nbody text")

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_copies_file_to_destination(self):
        dest = self.dir / "output.md"
        copy_file_template(self.template, dest)
        self.assertTrue(dest.exists())
        self.assertEqual(dest.read_text(), self.template.read_text())

    def test_creates_missing_parent_directories(self):
        dest = self.dir / "subdir" / "nested" / "output.md"
        copy_file_template(self.template, dest)
        self.assertTrue(dest.exists())

    def test_raises_file_exists_error_if_destination_already_exists(self):
        dest = self.dir / "output.md"
        dest.write_text("already here")
        with self.assertRaises(FileExistsError):
            copy_file_template(self.template, dest)

    def test_raises_file_not_found_if_template_missing(self):
        with self.assertRaises(FileNotFoundError):
            copy_file_template(self.dir / "no_such_file.md", self.dir / "output.md")


class TestCopyFolderTemplate(unittest.TestCase):
    # copy_folder_template always creates the project folder at WORKSPACE/<name>
    def setUp(self):
        import uuid
        self.name = f"_test_{uuid.uuid4().hex[:8]}"
        self.project_path = WORKSPACE / self.name

    def tearDown(self):
        if self.project_path.exists():
            shutil.rmtree(self.project_path)

    def test_copies_folder_structure_to_workspace(self):
        copy_folder_template(self.name, TEMPLATE_DEV)
        self.assertTrue(self.project_path.exists())
        self.assertTrue((self.project_path / "Main_page.md").exists())
        self.assertTrue((self.project_path / "Tasks").exists())

    def test_raises_file_exists_error_if_project_already_exists(self):
        copy_folder_template(self.name, TEMPLATE_DEV)
        with self.assertRaises(FileExistsError):
            copy_folder_template(self.name, TEMPLATE_DEV)

    def test_raises_file_not_found_if_template_does_not_exist(self):
        with self.assertRaises(FileNotFoundError):
            copy_folder_template(self.name, WORKSPACE / "no_such_template")


class TestUpdateFrontmatter(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_updates_specified_field(self):
        path = write_md(self.dir, "f.md", {"id": "TASK-###", "status": "to-do"})
        update_frontmatter(path, {"id": "TASK-001"})
        meta, _ = read_file(path)
        self.assertEqual(meta["id"], "TASK-001")

    def test_preserves_unmodified_fields(self):
        path = write_md(self.dir, "f.md", {"id": "TASK-###", "status": "to-do"})
        update_frontmatter(path, {"id": "TASK-001"})
        meta, _ = read_file(path)
        self.assertEqual(meta["status"], "to-do")

    def test_adds_new_field_not_in_original(self):
        path = write_md(self.dir, "f.md", {"id": "TASK-###"})
        update_frontmatter(path, {"new_field": "hello"})
        meta, _ = read_file(path)
        self.assertEqual(meta["new_field"], "hello")

    def test_body_is_preserved_after_update(self):
        path = write_md(self.dir, "f.md", {"id": "TASK-###"}, "# My heading")
        update_frontmatter(path, {"id": "TASK-001"})
        _, body = read_file(path)
        self.assertIn("My heading", body)


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
