#!/usr/bin/env python3
"""
Task Completion Workflow Hook

Detects task completion patterns in user messages and provides helpful
workflow suggestions and reminders. Enhanced with version management
reminder for cc-sessions modifications.

Hook Type: UserPromptSubmit
Trigger: User messages containing completion patterns
Actions:
- Suggest next workflow steps
- Remind about version bumping for cc-sessions changes
- Provide task management guidance
"""

import os
import sys
import json
import re
from pathlib import Path

def get_claude_project_dir():
    """Get the Claude project directory"""
    claude_project_dir = os.environ.get('CLAUDE_PROJECT_DIR')
    if not claude_project_dir:
        claude_project_dir = os.getcwd()
    return Path(claude_project_dir)

def get_current_task():
    """Get the current task from state"""
    try:
        project_dir = get_claude_project_dir()
        task_state_file = project_dir / ".claude/state/current_task.json"
        if task_state_file.exists():
            with open(task_state_file) as f:
                return json.load(f)
    except Exception:
        pass
    return None

def check_cc_sessions_modifications():
    """Check if cc-sessions files have been modified recently"""
    try:
        project_dir = get_claude_project_dir()

        # Check if this is the cc-sessions project itself
        if not (project_dir / "pyproject.toml").exists():
            return False

        # Read pyproject.toml to confirm this is cc-sessions
        pyproject_content = (project_dir / "pyproject.toml").read_text()
        if 'name = "cc-sessions"' not in pyproject_content:
            return False

        # Check for recent modifications to significant files
        import subprocess
        import time

        significant_patterns = [
            "cc_sessions/install.py",
            "install.js",
            "cc_sessions/hooks/",
            "cc_sessions/agents/",
            "cc_sessions/commands/",
            "cc_sessions/protocols/",
            "cc_sessions/templates/",
        ]

        try:
            # Get files modified in the last hour (3600 seconds)
            result = subprocess.run([
                'find', str(project_dir), '-type', 'f', '-mtime', '-1'
            ], capture_output=True, text=True, check=True)

            recent_files = result.stdout.strip().split('\n') if result.stdout.strip() else []

            for file_path in recent_files:
                rel_path = os.path.relpath(file_path, project_dir)
                for pattern in significant_patterns:
                    if pattern in rel_path:
                        return True

        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback: just check if we're in cc-sessions project
            return True

        return False

    except Exception:
        return False

def detect_completion_patterns(user_message):
    """Detect completion patterns in user message"""
    completion_patterns = [
        r'\b(?:that\'?s (?:all|done|finished|complete)|all done|finished|completed?)\b',
        r'\b(?:ready to (?:commit|push)|commit (?:this|these|that))\b',
        r'\b(?:task (?:is )?(?:done|complete|finished))\b',
        r'\b(?:we\'?re done|i\'?m done)\b',
        r'\b(?:implementation (?:is )?(?:complete|finished|done))\b',
        r'\b(?:feature (?:is )?(?:complete|finished|done|ready))\b'
    ]

    message_lower = user_message.lower()

    for pattern in completion_patterns:
        if re.search(pattern, message_lower):
            return True

    return False

def main():
    """Main hook execution"""
    try:
        # Get user message from environment or stdin
        user_message = ""
        if len(sys.argv) > 1:
            user_message = " ".join(sys.argv[1:])
        elif not sys.stdin.isatty():
            user_message = sys.stdin.read()

        if not user_message:
            return

        # Only process if completion patterns detected
        if not detect_completion_patterns(user_message):
            return

        # Get current task info
        current_task = get_current_task()

        print("\n" + "="*60)
        print("🎯 TASK COMPLETION DETECTED")
        print("="*60)

        if current_task and current_task.get('task'):
            task_name = current_task['task']
            print(f"📋 Current Task: {task_name}")

        # Check for cc-sessions modifications and remind about versioning
        if check_cc_sessions_modifications():
            print("\n🔧 CC-SESSIONS VERSION REMINDER")
            print("-" * 35)
            print("⚠️  cc-sessions files were modified!")
            print("📝 Before user reinstalls, run:")
            print("   python scripts/auto-version-bump.py")
            print("💡 This bumps the version so users get updated functionality")

        print("\n✅ SUGGESTED NEXT STEPS")
        print("-" * 25)

        if current_task:
            print("1. 📝 Update task work log with completion summary")
            print("2. 🔄 Mark task as completed in task file")
            print("3. 🧪 Run tests if applicable")
            print("4. 📋 Create follow-up tasks if needed")
        else:
            print("1. 📝 Document what was completed")
            print("2. 🧪 Test the implementation")
            print("3. 📋 Consider creating a task for tracking")

        print("\n🚀 Ready for next task!")
        print("="*60)

    except Exception as e:
        # Silent failure - don't interrupt Claude's workflow
        pass

if __name__ == "__main__":
    main()