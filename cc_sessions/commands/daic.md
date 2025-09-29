---
allowed-tools: Bash(python3:*)
argument-hint: "[discussion|implementation]"
description: Switch between Discussion and Implementation modes
---

!`python3 -c "
import json
import sys
import os
from pathlib import Path

def toggle_daic_mode(target_mode=None):
    try:
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
        project_root = Path(project_dir)

        # Get current mode
        daic_mode_file = project_root / '.claude' / 'state' / 'daic-mode.json'
        current_implementation_mode = False

        if daic_mode_file.exists():
            try:
                with open(daic_mode_file, 'r') as f:
                    daic_data = json.load(f)
                    current_implementation_mode = daic_data.get('implementation_mode', False)
            except:
                pass

        # Determine new mode
        if target_mode == 'discussion':
            new_implementation_mode = False
        elif target_mode == 'implementation':
            new_implementation_mode = True
        else:
            # Toggle mode
            new_implementation_mode = not current_implementation_mode

        # Update the mode file
        daic_mode_file.parent.mkdir(parents=True, exist_ok=True)
        with open(daic_mode_file, 'w') as f:
            json.dump({
                'implementation_mode': new_implementation_mode,
                'last_updated': '2025-01-29'
            }, f, indent=2)

        # Show status
        if new_implementation_mode:
            print('''╔══════════════════════════════════════════╗
║ 🟢 IMPLEMENTATION MODE - Ready to code ║
╚══════════════════════════════════════════╝

Mode switched to Implementation.
You can now use Edit, Write, and MultiEdit tools.
''')
        else:
            print('''╔════════════════════════════════════════╗
║ 🔴 DISCUSSION MODE - Let's plan first ║
╚════════════════════════════════════════╝

Mode switched to Discussion.
Edit tools are blocked until you get alignment.
''')

            # Show trigger phrases
            config_file = project_root / 'sessions' / 'sessions-config.json'
            if config_file.exists():
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                        trigger_phrases = config.get('trigger_phrases', ['make it so', 'run that'])
                        if trigger_phrases:
                            print('💡 To switch back to implementation mode, say:')
                            for phrase in trigger_phrases[:3]:
                                print(f'   • \\\"{phrase}\\\"')
                except:
                    pass

    except Exception as e:
        print(f'Error switching DAIC mode: {str(e)}')
        sys.exit(1)

# Parse argument
arg = '$ARGUMENTS'.strip().lower()
if arg in ['discussion', 'd']:
    toggle_daic_mode('discussion')
elif arg in ['implementation', 'impl', 'i']:
    toggle_daic_mode('implementation')
elif arg == '' or arg == 'toggle':
    toggle_daic_mode()
else:
    print('Usage: /daic [discussion|implementation]')
    print('')
    print('  /daic                    - Toggle mode')
    print('  /daic discussion         - Switch to discussion mode')
    print('  /daic implementation     - Switch to implementation mode')
    print('')
    print('Aliases: d, impl, i')
" || echo "Failed to switch DAIC mode. Check that .claude/state directory exists."`