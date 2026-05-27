# Project management

This folder contains all the logic for managing the Obsidian template in the project_template repository. It will offer a command-line interface to create a project and update each of its parts and components.

Claude code created an interface spec document for the template, which should be followed here.

The first goal is to create a working structure, that is able to work with the commands and execute them correctly, abiding by the spec from claude code.

After that, the MCP server should be implemented, to make working with the project management software easier.

The end goal is a tool that takes all the creation and management of the project structure away from me, and just gives me blocks of white space I can use for notes etc.

## Definition of done
- [ ] implement ``vault.py`` for reads and writes of md files and frontmatter
- [ ] implement ``init_project`` for cloning a vault from a template
- [ ] implement ``add_task`` and ``update_task`` to create task from template and modify
- [ ] implement ``add_purchase`` and ``update_purchase`` to create purchase from template and modify
- [ ] implement ``add_supplier`` and ``update_supplier`` to create supplier from template and modify
- [ ] implement ``project_status``
- [ ] implement ``dashboard``
- [ ] addition of MCP server