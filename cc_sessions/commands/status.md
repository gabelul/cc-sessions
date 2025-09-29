---
allowed-tools: Bash(python3:*)
argument-hint: ""
description: Show comprehensive cc-sessions status and current state
---

!`python3 -c "
import json
import sys
import os
from pathlib import Path

def get_status():
    try:
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
        project_root = Path(project_dir)

        # Load configuration
        config_file = project_root / 'sessions' / 'sessions-config.json'
        if not config_file.exists():
            print('⚠️  cc-sessions not properly configured (sessions-config.json missing)')
            return

        with open(config_file, 'r') as f:
            config = json.load(f)

        # Get current DAIC mode
        daic_mode_file = project_root / '.claude' / 'state' / 'daic-mode.json'
        if daic_mode_file.exists():
            with open(daic_mode_file, 'r') as f:
                daic_data = json.load(f)
                current_mode = 'Implementation' if daic_data.get('implementation_mode', False) else 'Discussion'
                mode_emoji = '🟢' if daic_data.get('implementation_mode', False) else '🔴'
        else:
            current_mode = 'Discussion'
            mode_emoji = '🔴'

        # Get current task
        current_task_file = project_root / '.claude' / 'state' / 'current_task.json'
        if current_task_file.exists():
            with open(current_task_file, 'r') as f:
                task_data = json.load(f)
                task_name = task_data.get('task', 'None')
                task_branch = task_data.get('branch', 'None')
        else:
            task_name = 'None'
            task_branch = 'None'

        # Get current git branch
        try:
            import subprocess
            result = subprocess.run(['git', 'branch', '--show-current'],
                                  capture_output=True, text=True, cwd=project_dir)
            git_branch = result.stdout.strip() if result.returncode == 0 else 'Not in git repo'
        except:
            git_branch = 'Unknown'

        # Get trigger phrases
        trigger_phrases = config.get('trigger_phrases', ['make it so', 'run that'])
        trigger_list = ', '.join([f'\\\"{phrase}\\\"' for phrase in trigger_phrases])

        # Check Memory Bank MCP status
        memory_bank_config = config.get('memory_bank_mcp', {})
        memory_bank_enabled = memory_bank_config.get('enabled', False)
        sync_files_count = len(memory_bank_config.get('sync_files', []))

        if memory_bank_enabled and sync_files_count > 0:
            memory_status = f'✅ Connected ({sync_files_count} files synced)'
        elif memory_bank_enabled:
            memory_status = '⚠️  Enabled but no files configured'
        else:
            memory_status = '❌ Disabled'

        # Get API mode status
        api_mode = config.get('api_mode', False)
        ultrathink_status = '❌ API Mode' if api_mode else '✅ Ultrathink Mode'

        print(f'''╔══════════════════════════════════════╗
║           CC-SESSIONS STATUS         ║
╚══════════════════════════════════════╝

{mode_emoji} Mode: {current_mode}
📋 Task: {task_name}
🌳 Current Branch: {git_branch}
🔀 Task Branch: {task_branch}
🔧 Triggers: {trigger_list}
🧠 Memory Bank: {memory_status}
⚡ Claude Mode: {ultrathink_status}

Commands Available:
• /daic        - Switch to {'Discussion' if current_mode == 'Implementation' else 'Implementation'} mode
• /tutorial    - Interactive workflow guide
• /add-trigger - Add new trigger phrases
• /sync-status - Memory Bank sync details

Next: {'Say a trigger phrase to start implementing' if current_mode == 'Discussion' else 'Describe your approach, then implement'}''')

    except Exception as e:
        print(f'Error getting status: {str(e)}')
        print('Check that cc-sessions is properly installed and configured.')

get_status()
" || echo "Failed to get cc-sessions status. Check that sessions-config.json exists."`