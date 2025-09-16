#!/usr/bin/env python3
"""Session start hook to initialize Claude Code Sessions context."""
import json
import os
import sys
import subprocess
from pathlib import Path
from shared_state import get_project_root, ensure_state_dir, get_task_state

# Get project root
PROJECT_ROOT = get_project_root()

def load_memory_bank_files(project_root):
    """Load synchronized files from Memory Bank MCP if available."""
    try:
        config_file = project_root / 'sessions' / 'sessions-config.json'
        if not config_file.exists():
            return None

        with open(config_file, 'r') as f:
            config = json.load(f)

        memory_bank_config = config.get('memory_bank_mcp', {})
        if not memory_bank_config.get('enabled', False):
            return None

        sync_files = memory_bank_config.get('sync_files', [])
        if not sync_files:
            return None

        # Check for files marked as "in_memory"
        in_memory_files = [f for f in sync_files if f.get('status') == 'in_memory']
        if not in_memory_files:
            return None

        context = "\n\n" + "="*60 + "\n"
        context += "PERSISTENT MEMORY BANK CONTEXT\n"
        context += "="*60 + "\n\n"
        context += f"The following {len(in_memory_files)} files are synchronized with Memory Bank MCP:\n\n"

        for file_info in in_memory_files:
            file_path = file_info['path']
            last_synced = file_info.get('last_synced', 'unknown')
            context += f"• {file_path} (last synced: {last_synced})\n"

        context += "\nThese files contain persistent project context and architectural knowledge.\n"
        context += "Use Memory Bank MCP tools to read specific file contents as needed.\n"
        context += "="*60 + "\n"

        return context

    except Exception as e:
        # Graceful fallback - don't break session startup
        return None

def discover_unsynced_files(project_root):
    """Discover important files that aren't yet synced to Memory Bank."""
    try:
        config_file = project_root / 'sessions' / 'sessions-config.json'
        if not config_file.exists():
            return None

        with open(config_file, 'r') as f:
            config = json.load(f)

        memory_bank_config = config.get('memory_bank_mcp', {})
        if not memory_bank_config.get('enabled', False):
            return None

        # Get currently synced files
        sync_files = memory_bank_config.get('sync_files', [])
        synced_paths = {f['path'] for f in sync_files}

        # Auto-discovery patterns (same as installer)
        discovery_patterns = {
            "Configuration": [
                "CLAUDE.md", "CLAUDE.sessions.md"
            ],
            "Documentation": [
                "README.md", "ARCHITECTURE.md", "DESIGN.md"
            ],
            "Requirements": [
                "PRD.md", "FSD.md"
            ]
        }

        unsynced_files = []
        for category, patterns in discovery_patterns.items():
            for pattern in patterns:
                if '*' in pattern:
                    # Use glob for wildcard patterns
                    matches = list(project_root.glob(pattern))
                    for match in matches:
                        if match.is_file() and match.suffix.lower() == '.md':
                            rel_path = str(match.relative_to(project_root))
                            if rel_path not in synced_paths:
                                unsynced_files.append({
                                    "path": rel_path,
                                    "category": category.lower(),
                                    "size": match.stat().st_size
                                })
                else:
                    # Direct file check
                    file_path = project_root / pattern
                    if file_path.exists() and file_path.is_file():
                        rel_path = str(file_path.relative_to(project_root))
                        if rel_path not in synced_paths:
                            unsynced_files.append({
                                "path": rel_path,
                                "category": category.lower(),
                                "size": file_path.stat().st_size
                            })

        # Check docs/ folder for additional documentation
        docs_folder = project_root / 'docs'
        if docs_folder.exists() and docs_folder.is_dir():
            for md_file in docs_folder.glob('*.md'):
                rel_path = str(md_file.relative_to(project_root))
                if rel_path not in synced_paths:
                    unsynced_files.append({
                        "path": rel_path,
                        "category": "documentation",
                        "size": md_file.stat().st_size
                    })

        return unsynced_files if unsynced_files else None

    except Exception as e:
        return None

# Get developer name from config
try:
    CONFIG_FILE = PROJECT_ROOT / 'sessions' / 'sessions-config.json'
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            developer_name = config.get('developer_name', 'the developer')
    else:
        developer_name = 'the developer'
except:
    developer_name = 'the developer'

# Initialize context
context = f"""You are beginning a new context window with {developer_name}.

"""

# Quick configuration checks
needs_setup = False
quick_checks = []

# 1. Check if daic command exists
try:
    import shutil
    import os
    # Cross-platform command detection
    if os.name == 'nt':
        # Windows - check for .cmd or .ps1 versions
        if not (shutil.which('daic.cmd') or shutil.which('daic.ps1') or shutil.which('daic')):
            needs_setup = True
            quick_checks.append("daic command")
    else:
        # Unix/Mac - use which command
        if not shutil.which('daic'):
            needs_setup = True
            quick_checks.append("daic command")
except:
    needs_setup = True
    quick_checks.append("daic command")

# 2. Check if tiktoken is installed (required for subagent transcript chunking)
try:
    import tiktoken
except ImportError:
    needs_setup = True
    quick_checks.append("tiktoken (pip install tiktoken)")

# 3. Check if DAIC state file exists (create if not)
ensure_state_dir()
daic_state_file = PROJECT_ROOT / '.claude' / 'state' / 'daic-mode.json'
if not daic_state_file.exists():
    # Create default state
    with open(daic_state_file, 'w') as f:
        json.dump({"mode": "discussion"}, f, indent=2)

# 4. Clear context warning flags for new session
warning_75_flag = PROJECT_ROOT / '.claude' / 'state' / 'context-warning-75.flag'
warning_90_flag = PROJECT_ROOT / '.claude' / 'state' / 'context-warning-90.flag'
if warning_75_flag.exists():
    warning_75_flag.unlink()
if warning_90_flag.exists():
    warning_90_flag.unlink()

# 5. Check if sessions directory exists
sessions_dir = PROJECT_ROOT / 'sessions'
if sessions_dir.exists():
    # Check for active task
    task_state = get_task_state()
    if task_state.get("task"):
        task_file = sessions_dir / 'tasks' / f"{task_state['task']}.md"
        if task_file.exists():
            # Check if task status is pending and update to in-progress
            task_content = task_file.read_text()
            task_updated = False
            
            # Parse task frontmatter to check status
            if task_content.startswith('---'):
                lines = task_content.split('\n')
                for i, line in enumerate(lines[1:], 1):
                    if line.startswith('---'):
                        break
                    if line.startswith('status: pending'):
                        lines[i] = 'status: in-progress'
                        task_updated = True
                        # Write back the updated content
                        task_file.write_text('\n'.join(lines))
                        task_content = '\n'.join(lines)
                        break
            
            # Output the full task state
            context += f"""Current task state:
```json
{json.dumps(task_state, indent=2)}
```

Loading task file: {task_state['task']}.md
{"=" * 60}
{task_content}
{"=" * 60}
"""
            
            if task_updated:
                context += """
[Note: Task status updated from 'pending' to 'in-progress']
Follow the task-startup protocol to create branches and set up the work environment.
"""
            else:
                context += """
Review the Work Log at the end of the task file above.
Continue from where you left off, updating the work log as you progress.
"""

        # Load synchronized files from Memory Bank MCP if available
        memory_bank_context = load_memory_bank_files(PROJECT_ROOT)
        if memory_bank_context:
            context += memory_bank_context

        # Check for unsynced important files
        unsynced_files = discover_unsynced_files(PROJECT_ROOT)
        if unsynced_files:
            context += "\n\n" + "="*60 + "\n"
            context += "UNSYNCED DOCUMENTATION DETECTED\n"
            context += "="*60 + "\n\n"
            context += f"Found {len(unsynced_files)} important files not yet synced to Memory Bank:\n\n"

            # Group by category
            by_category = {}
            for file_info in unsynced_files:
                category = file_info['category'].title()
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append(file_info)

            for category, files in by_category.items():
                context += f"{category}:\n"
                for file_info in files:
                    size_kb = file_info['size'] / 1024
                    context += f"  • {file_info['path']} ({size_kb:.1f}KB)\n"
                context += "\n"

            context += "Consider syncing these files for persistent context:\n"
            context += "• Use /sync-file [path] to sync individual files\n"
            context += "• Use /sync-all to sync all configured files\n"
            context += "="*60 + "\n"
    else:
        # No active task - list available tasks
        tasks_dir = sessions_dir / 'tasks'
        task_files = []
        if tasks_dir.exists():
            task_files = sorted([f for f in tasks_dir.glob('*.md') if f.name != 'TEMPLATE.md'])
        
        if task_files:
            context += """No active task set. Available tasks:

"""
            for task_file in task_files:
                # Read first few lines to get task info
                with open(task_file, 'r') as f:
                    lines = f.readlines()[:10]
                    task_name = task_file.stem
                    status = 'unknown'
                    for line in lines:
                        if line.startswith('status:'):
                            status = line.split(':')[1].strip()
                            break
                    context += f"  • {task_name} ({status})\n"
            
            context += """
To select a task:
1. Update .claude/state/current_task.json with the task name
2. Or create a new task following sessions/protocols/task-creation.md
"""
        else:
            context += """No tasks found. 

To create your first task:
1. Copy the template: cp sessions/tasks/TEMPLATE.md sessions/tasks/[priority]-[task-name].md
   Priority prefixes: h- (high), m- (medium), l- (low), ?- (investigate)
2. Fill in the task details
3. Update .claude/state/current_task.json
4. Follow sessions/protocols/task-startup.md
"""
else:
    # Sessions directory doesn't exist - likely first run
    context += """Sessions system is not yet initialized.

Run the install script to set up the sessions framework:
.claude/sessions-setup.sh

Or follow the manual setup in the documentation.
"""

# If setup is needed, provide guidance
if needs_setup:
    context += f"""
[Setup Required]
Missing components: {', '.join(quick_checks)}

To complete setup:
1. Run the cc-sessions installer
2. Ensure the daic command is in your PATH

The sessions system helps manage tasks and maintain discussion/implementation workflow discipline.
"""

output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context
    }
}
print(json.dumps(output))