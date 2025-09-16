---
allowed-tools: Bash(python:*), Bash(python3:*)
argument-hint: "command [args...]"
description: Flexible stepped project workflows - create, manage, and track project steps
---

Project management command for flexible stepped workflows.

**Usage:**
- `/project create <name>` - Initialize new project
- `/project list [name]` - Show all projects or steps for specific project
- `/project work <name> <step>` - Start working on specific step
- `/project complete <name> <step>` - Mark step as completed
- `/project status <name>` - Show project progress
- `/project parse <name>` - Re-parse plan files for changes

!`python3 "$CLAUDE_PROJECT_DIR/.claude/commands/project.py" $ARGUMENTS`