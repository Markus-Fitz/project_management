# Project management

This folder contains all the logic for managing the Obsidian template in the project_template repository. It will offer a command-line interface to create a project and update each of its parts and components.

The first goal is to create a working command skeleton, that is able to work with the structure of the project_template folders. First, basic operations like cloning a template and customizing it and creating and modifying Tasks, Research_notes, Purchases, Suppliers etc. will be implemented. Once that works, drawing information out of the frontmatter is the next step, so that task scheduling, cost and time accumulation and creating dashboards will be possible.

After that, the MCP server should be implemented, to provide a free-form interface to the project management software.

The end goal is a tool that takes all the creation and management of the project structure away from me, and just gives me blocks of white space I can use for notes etc.

## Setup

To use the project_management tool, clone this project_management repository into your projects folder containing the projects you want to manage.

Clone the project_templates repository into the same parent directory as the project_management repository. The project_management folder expects to be in the same folder as the project_template folder it uses to create new projects.

The projects it creates and modifies are also expected in the same parent folder as the project_management folder.

## LM studio interface

The project management functions are designed to be interfaced with via an LLM to make interactions more frictionless. LM studio was chosen as an implementation example here.

To make LM studio aware of the MCP server running on the same device, the following snippet has to be included in the mcp.json file.

```
    "pm_mcp_server": {
      "url": "http://127.0.0.1:5173/sse"
    }
```

Save the mcp.json file and start the MCP server by running pm_mcp_server/pm_mcp.py. The pm_mcp_server tool should appear in the LM studio GUI. When activated, the LLM will create and modify the projects in the same directory this repository is cloned into.

In Windows, navigate into this directory in the powershell, start a virtual environment

```
cd path\to\your\projects\project_management
python -m venv .venv
.venv\Scripts\activate
```

and run the MCP server

```
cd pm_mcp_server
python pm_mcp.py
```

. Again, the pm_mcp_server tool should appear in the GUI.

## Folder structure

The project management tool expects the following folder structure for the project_template folder

```
project_templates/
├── README.md
├── Template_development
│   ├── Design_electronic       # EDA source files
│   │   └── exports             # PDFs and other exported outputs
│   ├── Design_mechanical       # CAD source files
│   │   └── exports             # PDFs and other exported outputs
│   ├── Documents               # Datasheets, paper notes, reference material
│   ├── Images                  # Photos, diagrams, renders
│   ├── Main_page.md            # Project overview and log
│   ├── Purchases               # One .md file per Purchase
│   ├── Research_notes          # One .md file per Research_note
│   ├── Suppliers               # One .md file per Supplier
│   ├── Tasks                   # One .md file per Task
│   └── Templates               # Obsidian note templates
└── Template_research
    ├── Documents               # Datasheets, paper notes, reference material
    ├── Images                  # Photos, diagrams, renders
    ├── Main_page.md            # Project overview and log
    ├── Purchases               # One .md file per Purchase
    ├── Research_notes          # One .md file per Research_note
    ├── Suppliers               # One .md file per Supplier
    └── Templates               # Obsidian note templates
```

. This is the folder structure of hte project_template repo, which also can just be cloned into the parent directory.

## Frontmatter

The project manager works with the Frontmatter of the markdown-files. The expected Frontmatter-structure is shown for each file.

### Main_page

```
---
id: "PROJ-###"
name: null
status: planning
created_on: null
target_date: null
budget: null
tags:
  - Development-project / Research-project
---
```

### Task

```
---
id: "TASK-###"
status: to-do
created_on: null
start_date: null
end_date: null
parent_task: []
priority: 500
time_spent: 0.0
dependent_on: []
purchases: null
tags:
  - Task
---
```

### Research_note

```
---
id: "RES-###"
created_on: null
time_spent: 0.0
source: null
source_date: null
tags:
  - Research
---
```

### Purchase

```
---
id: "PUR-###"
purchase_linked_file: []
created_on: null
purchase_date: null
arrival_date: null
supplier: []
currency: EUR
amount: null
tax: null
tags:
  - Purchase
---
```

### Supplier

```
---
id: "SUP-###"
created_on: null
name: null
website: null
country: null
tags:
  - Supplier
---
```

