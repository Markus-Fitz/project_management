# Project management

This folder contains all the logic for managing the Obsidian template in the project_template repository. It will offer a command-line interface to create a project and update each of its parts and components.

The first goal is to create a working command skeleton, that is able to work with the structure of the project_template folders. First, basic operations like cloning a template and customizing it and creating and modifying Tasks, Research_notes, Purchases, Suppliers etc. will be implemented. Once that works, drawing information out of the frontmatter is the next step, so that task scheduling, cost and time accumulation and creating dashboards will be possible.

After that, the MCP server should be implemented, to provide a free-form interface to the project management software.

The end goal is a tool that takes all the creation and management of the project structure away from me, and just gives me blocks of white space I can use for notes etc.

## Setup

The project_management folder expects to be in the same folder as the project_template folder it uses to create new projects. The projects it acts on are also expected in the same parent folder as the project_management folder.

To use the project_management tool, clone this project into your projects folder containing all the projects you want to manage.

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

### Task

### Research_note

### Purchase

### Supplier
