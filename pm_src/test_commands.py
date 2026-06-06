import unittest
import shutil
import sys
import uuid
from pathlib import Path
from datetime import date
import frontmatter as fm

sys.path.insert(0, str(Path(__file__).parent))
from commands import (
    initialize_project,
    add_task,
    add_task_hours,
    mark_task_done,
    add_research_note,
    add_note_hours,
    add_supplier,
    add_purchase,
)

WORKSPACE = Path(__file__).parent.parent.parent


def unique_name() -> str:
    return f"_test_{uuid.uuid4().hex[:8]}"


class TestInitializeProject(unittest.TestCase):
    def setUp(self):
        self.name = unique_name()
        self.path = WORKSPACE / self.name

    def tearDown(self):
        if self.path.exists():
            shutil.rmtree(self.path)

    def test_creates_project_folder_in_workspace(self):
        initialize_project(self.name, "Template_development")
        self.assertTrue(self.path.exists())
        self.assertTrue((self.path / "Main_page.md").exists())

    def test_sets_project_name_in_frontmatter(self):
        initialize_project(self.name, "Template_development")
        meta = fm.load(self.path / "Main_page.md").metadata
        self.assertEqual(meta["name"], self.name)

    def test_sets_created_on_to_today(self):
        initialize_project(self.name, "Template_development")
        meta = fm.load(self.path / "Main_page.md").metadata
        self.assertEqual(meta["created_on"], str(date.today()))

    def test_assigns_proj_id(self):
        initialize_project(self.name, "Template_development")
        meta = fm.load(self.path / "Main_page.md").metadata
        self.assertRegex(str(meta["id"]), r"PROJ-\d{3}")

    def test_returns_success_message(self):
        result = initialize_project(self.name, "Template_development")
        self.assertIn("successfully", result)

    def test_returns_error_if_project_already_exists(self):
        initialize_project(self.name, "Template_development")
        original_id = fm.load(self.path / "Main_page.md").metadata["id"]
        result = initialize_project(self.name, "Template_development")
        self.assertIn("already exists", result)
        self.assertEqual(fm.load(self.path / "Main_page.md").metadata["id"], original_id)

    def test_returns_error_if_template_not_found(self):
        result = initialize_project(self.name, "NonExistentTemplate")
        self.assertIn("not found", result)
        self.assertFalse(self.path.exists())

    def test_works_with_research_template(self):
        initialize_project(self.name, "Template_research")
        self.assertTrue((self.path / "Research_notes").exists())
        self.assertTrue((self.path / "Suppliers").exists())


class TestAddTask(unittest.TestCase):
    def setUp(self):
        self.name = unique_name()
        self.path = WORKSPACE / self.name
        initialize_project(self.name, "Template_development")

    def tearDown(self):
        shutil.rmtree(self.path)

    def test_creates_task_file(self):
        add_task(self.name, "my_task")
        self.assertTrue((self.path / "Tasks" / "my_task.md").exists())

    def test_assigns_task_id(self):
        add_task(self.name, "my_task")
        meta = fm.load(self.path / "Tasks" / "my_task.md").metadata
        self.assertRegex(str(meta["id"]), r"TASK-\d{3}")

    def test_ids_increment_for_each_new_task(self):
        add_task(self.name, "task_a")
        add_task(self.name, "task_b")
        num_a = int(fm.load(self.path / "Tasks" / "task_a.md").metadata["id"].split("-")[1])
        num_b = int(fm.load(self.path / "Tasks" / "task_b.md").metadata["id"].split("-")[1])
        self.assertEqual(num_b, num_a + 1)

    def test_returns_success_message(self):
        result = add_task(self.name, "my_task")
        self.assertIn("successfully", result)

    def test_returns_error_if_task_file_already_exists(self):
        add_task(self.name, "my_task")
        original_id = fm.load(self.path / "Tasks" / "my_task.md").metadata["id"]
        result = add_task(self.name, "my_task")
        self.assertIn("already exists", result)
        self.assertEqual(fm.load(self.path / "Tasks" / "my_task.md").metadata["id"], original_id)


class TestAddResearchNote(unittest.TestCase):
    def setUp(self):
        self.name = unique_name()
        self.path = WORKSPACE / self.name
        initialize_project(self.name, "Template_development")

    def tearDown(self):
        shutil.rmtree(self.path)

    def test_creates_note_file(self):
        add_research_note(self.name, "my_note")
        self.assertTrue((self.path / "Research_notes" / "my_note.md").exists())

    def test_assigns_res_id(self):
        add_research_note(self.name, "my_note")
        meta = fm.load(self.path / "Research_notes" / "my_note.md").metadata
        self.assertRegex(str(meta["id"]), r"RES-\d{3}")

    def test_ids_increment_for_each_new_note(self):
        add_research_note(self.name, "note_a")
        add_research_note(self.name, "note_b")
        num_a = int(fm.load(self.path / "Research_notes" / "note_a.md").metadata["id"].split("-")[1])
        num_b = int(fm.load(self.path / "Research_notes" / "note_b.md").metadata["id"].split("-")[1])
        self.assertEqual(num_b, num_a + 1)

    def test_returns_success_message(self):
        result = add_research_note(self.name, "my_note")
        self.assertIn("successfully", result)

    def test_returns_error_if_note_already_exists(self):
        add_research_note(self.name, "my_note")
        original_id = fm.load(self.path / "Research_notes" / "my_note.md").metadata["id"]
        result = add_research_note(self.name, "my_note")
        self.assertIn("already exists", result)
        self.assertEqual(fm.load(self.path / "Research_notes" / "my_note.md").metadata["id"], original_id)


class TestAddTaskHours(unittest.TestCase):
    def setUp(self):
        self.name = unique_name()
        self.path = WORKSPACE / self.name
        initialize_project(self.name, "Template_development")
        add_task(self.name, "my_task")
        self.task_path = self.path / "Tasks" / "my_task.md"

    def tearDown(self):
        shutil.rmtree(self.path)

    def test_adds_hours_to_initial_zero(self):
        add_task_hours(self.name, "my_task", "3.5")
        meta = fm.load(self.task_path).metadata
        self.assertEqual(meta["time_spent"], 3.5)

    def test_accumulates_hours_across_calls(self):
        add_task_hours(self.name, "my_task", "1.0")
        add_task_hours(self.name, "my_task", "2.5")
        meta = fm.load(self.task_path).metadata
        self.assertEqual(meta["time_spent"], 3.5)

    def test_returns_success_message(self):
        result = add_task_hours(self.name, "my_task", "1.0")
        self.assertIn("successfully", result)


class TestAddNoteHours(unittest.TestCase):
    def setUp(self):
        self.name = unique_name()
        self.path = WORKSPACE / self.name
        initialize_project(self.name, "Template_development")
        add_research_note(self.name, "my_note")
        self.note_path = self.path / "Research_notes" / "my_note.md"

    def tearDown(self):
        shutil.rmtree(self.path)

    def test_adds_hours_to_initial_zero(self):
        add_note_hours(self.name, "my_note", "2.0")
        meta = fm.load(self.note_path).metadata
        self.assertEqual(meta["time_spent"], 2.0)

    def test_accumulates_hours_across_calls(self):
        add_note_hours(self.name, "my_note", "1.0")
        add_note_hours(self.name, "my_note", "1.5")
        meta = fm.load(self.note_path).metadata
        self.assertEqual(meta["time_spent"], 2.5)

    def test_returns_success_message(self):
        result = add_note_hours(self.name, "my_note", "1.0")
        self.assertIn("successfully", result)


class TestMarkTaskDone(unittest.TestCase):
    def setUp(self):
        self.name = unique_name()
        self.path = WORKSPACE / self.name
        initialize_project(self.name, "Template_development")
        add_task(self.name, "my_task")
        self.task_path = self.path / "Tasks" / "my_task.md"

    def tearDown(self):
        shutil.rmtree(self.path)

    def test_sets_status_to_done(self):
        mark_task_done(self.name, "my_task")
        meta = fm.load(self.task_path).metadata
        self.assertEqual(meta["status"], "done")

    def test_sets_end_date_to_today(self):
        mark_task_done(self.name, "my_task")
        meta = fm.load(self.task_path).metadata
        self.assertEqual(meta["end_date"], date.today())

    def test_returns_success_message(self):
        result = mark_task_done(self.name, "my_task")
        self.assertIn("successfully", result)

    def test_returns_error_if_already_marked_as_done(self):
        mark_task_done(self.name, "my_task")
        result = mark_task_done(self.name, "my_task")
        self.assertIn("already", result)


class TestAddSupplier(unittest.TestCase):
    def setUp(self):
        self.name = unique_name()
        self.path = WORKSPACE / self.name
        initialize_project(self.name, "Template_research")

    def tearDown(self):
        shutil.rmtree(self.path)

    def test_creates_supplier_file(self):
        add_supplier(self.path, "supplier_a")
        self.assertTrue((self.path / "Suppliers" / "supplier_a.md").exists())

    def test_assigns_sup_id(self):
        add_supplier(self.path, "supplier_a")
        meta = fm.load(self.path / "Suppliers" / "supplier_a.md").metadata
        self.assertRegex(str(meta["id"]), r"SUP-\d{3}")

    def test_second_supplier_gets_incremented_id(self):
        add_supplier(self.path, "supplier_a")
        add_supplier(self.path, "supplier_b")
        num_a = int(fm.load(self.path / "Suppliers" / "supplier_a.md").metadata["id"].split("-")[1])
        num_b = int(fm.load(self.path / "Suppliers" / "supplier_b.md").metadata["id"].split("-")[1])
        self.assertEqual(num_b, num_a + 1)

    def test_returns_error_if_supplier_already_exists(self):
        add_supplier(self.path, "supplier_a")
        original_id = fm.load(self.path / "Suppliers" / "supplier_a.md").metadata["id"]
        result = add_supplier(self.path, "supplier_a")
        self.assertIn("already", result)
        self.assertEqual(fm.load(self.path / "Suppliers" / "supplier_a.md").metadata["id"], original_id)

    def test_returns_success_message(self):
        result = add_supplier(self.path, "supplier_a")
        self.assertIn("successfully", result)


class TestAddPurchase(unittest.TestCase):
    def setUp(self):
        self.name = unique_name()
        self.path = WORKSPACE / self.name
        initialize_project(self.name, "Template_research")
        add_research_note(self.name, "note_a")
        add_supplier(self.path, "supplier_a")

    def tearDown(self):
        shutil.rmtree(self.path)

    def test_creates_purchase_file(self):
        add_purchase(self.name, "purchase_a", "Research_notes", "note_a", "supplier_a")
        self.assertTrue((self.path / "Purchases" / "purchase_a.md").exists())

    def test_sets_linked_file_in_frontmatter(self):
        add_purchase(self.name, "purchase_a", "Research_notes", "note_a", "supplier_a")
        meta = fm.load(self.path / "Purchases" / "purchase_a.md").metadata
        self.assertIn("note_a", meta["purchase_linked_file"])

    def test_sets_supplier_in_frontmatter(self):
        add_purchase(self.name, "purchase_a", "Research_notes", "note_a", "supplier_a")
        meta = fm.load(self.path / "Purchases" / "purchase_a.md").metadata
        self.assertIn("supplier_a", meta["supplier"])

    def test_assigns_pur_id(self):
        add_purchase(self.name, "purchase_a", "Research_notes", "note_a", "supplier_a")
        meta = fm.load(self.path / "Purchases" / "purchase_a.md").metadata
        self.assertRegex(str(meta["id"]), r"PUR-\d{3}")

    def test_second_pur_gets_incremented_id(self):
        add_purchase(self.name, "purchase_a", "Research_notes", "note_a", "supplier_a")
        add_purchase(self.name, "purchase_b", "Research_notes", "note_a", "supplier_a")
        num_a = int(fm.load(self.path / "Purchases" / "purchase_a.md").metadata["id"].split("-")[1])
        num_b = int(fm.load(self.path / "Purchases" / "purchase_b.md").metadata["id"].split("-")[1])
        self.assertEqual(num_b, num_a + 1)

    def test_creates_error_if_linked_file_does_not_exist(self):
        result = add_purchase(self.name, "purchase_b", "Research_notes", "no_such", "supplier_a")
        self.assertIn("does not exist", result)
        self.assertFalse((self.path / "Purchases" / "purchase_b.md").exists())

    def test_creates_error_if_supplier_does_not_exist(self):
        result = add_purchase(self.name, "purchase_c", "Research_notes", "note_a", "no_such")
        self.assertIn("does not exist", result)
        self.assertFalse((self.path / "Purchases" / "purchase_c.md").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
