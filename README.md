# Project Template

An Obsidian vault template for managing hardware/maker and research projects. Designed to be cloned per-project and optionally managed via the companion Python CLI (coming soon).

## Setup

1. Clone this repo into your projects folder: `git clone <repo-url> my-project`
2. Open the `project template/` folder as a vault in Obsidian
3. In Obsidian → Settings → Templates, confirm the template folder is set to `Templates`
4. Edit `Main page.md` with your project details

## Folder Structure

```
project template/
├── Templates/          # Obsidian note templates (use Ctrl+T to insert)
├── Tasks/              # One .md file per task
├── Purchases/          # One .md file per purchase order
├── Suppliers/          # One .md file per supplier
├── Research/           # Datasheets, paper notes, reference material
├── Notes/              # General project notes
├── Documents/          # Specs, reports, formal documentation
├── Images/             # Photos, diagrams, renders
├── FreeCAD/            # CAD source files
├── Exports/            # PDFs and other exported outputs
└── Main page.md        # Project overview and log
```

## Schemas

All frontmatter is designed to be machine-readable by the Python PM tool.

### Project (`Main page.md`)

| Field | Type | Values |
|---|---|---|
| `project_id` | string | `PROJ-001` |
| `name` | string | |
| `status` | string | `planning` \| `active` \| `on-hold` \| `completed` \| `archived` |
| `created_on` | date | `YYYY-MM-DD` |
| `target_date` | date | `YYYY-MM-DD` |
| `budget` | number | total budget in project currency |

### Task (`Tasks/`)

| Field | Type | Values |
|---|---|---|
| `id` | string | `TASK-001` |
| `status` | string | `icebox` \| `backlog` \| `to-do` \| `in-progress` \| `done` \| `archived` |
| `created_on` | date | `YYYY-MM-DD` |
| `start_date` | date | `YYYY-MM-DD` — set when work actually begins |
| `parent_task` | wikilink | links to parent task, or `[[Main page]]` for top-level tasks |
| `priority` | number | 1–1000 (higher = more urgent) |
| `time_spent` | number | hours (decimal, e.g. `1.5`) |
| `dependent_on` | list | task IDs that must be `done` before this task can start |
| `purchases` | list | purchase IDs associated with this task (mirrors `purchase_task` on each purchase) |

### Purchase (`Purchases/`)

| Field | Type | Values |
|---|---|---|
| `purchase_id` | string | `PUR-0001` |
| `purchase_task` | wikilink | links to the task this purchase belongs to |
| `purchase_date` | date | `YYYY-MM-DD` |
| `arrival_date` | date | `YYYY-MM-DD` |
| `supplier_id` | string | `SUP-0001` |
| `currency` | string | ISO 4217 (e.g. `EUR`, `USD`) |
| `amount` | number | total order amount |
| `tax` | number | tax amount (optional) |

### Supplier (`Suppliers/`)

| Field | Type | Values |
|---|---|---|
| `supplier_id` | string | `SUP-0001` |
| `name` | string | |
| `website` | string | URL |
| `country` | string | ISO 3166-1 alpha-2 (e.g. `DE`, `US`) |

### Research Note (`Research/`)

| Field | Type | Values |
|---|---|---|
| `note_id` | string | `RES-001` |
| `source` | string | URL, DOI, or citation |
| `source_date` | date | `YYYY-MM-DD` |

## Python PM Interface

A companion CLI tool is planned that will read this vault structure to provide:

**Views**
- Task board grouped by status, sorted by priority
- Task tree built from `parent_task` links (top-level → sub-tasks)
- Purchase ledger with per-task and per-project cost rollup
- Time tracking summary by task, tag, or time period
- Supplier index

**Automation**
- Create new Task / Purchase / Supplier notes from templates with auto-incremented IDs
- Auto-populate `purchases` list on a task when a new purchase links to it
- Generate or refresh the `Main page.md` dashboard (task list, total time spent, total cost)

**Validation & analysis**
- Flag dependency inconsistencies (e.g. a task depends on a lower-priority task)
- Flag tasks marked `in-progress` with no `start_date`
- Cost and time rollup filtered by tag (useful for categorising effort across projects)

**Change log** *(future)*
- Record timestamped history of frontmatter field changes (status transitions, priority edits)
- Visualise when tasks were completed or how cost accumulated over time

The consistent frontmatter schemas above are designed with this tool in mind. The bidirectional `purchase_task` ↔ `purchases` link means the tool can resolve task costs without a full vault scan.
