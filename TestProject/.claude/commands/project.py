#!/usr/bin/env python3
"""
Project management command for flexible stepped workflows.
Provides a simpler alternative to /build-project for manual project planning and execution.
"""
import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

# Parse arguments
args = sys.argv[1:]  # Skip script name
if not args:
    print('Usage: /project <command> [args...]')
    print('Commands:')
    print('  create [name]           - Initialize new project')
    print('  list [name?]            - Show all projects or steps for specific project')
    print('  work [name] [step]      - Start working on specific step')
    print('  complete [name] [step]  - Mark step as completed')
    print('  status [name]           - Show project progress')
    print('  parse [name]            - Re-parse plan files for changes')
    sys.exit(0)

command = args[0]
project_dir = Path(os.environ.get('CLAUDE_PROJECT_DIR', '.')).resolve()
projects_dir = project_dir / 'sessions' / 'projects'

def ensure_projects_dir():
    """Ensure projects directory exists."""
    projects_dir.mkdir(parents=True, exist_ok=True)

def get_project_path(name):
    """Get path to project directory."""
    return projects_dir / name

def get_project_state_path(name):
    """Get path to project state file."""
    return get_project_path(name) / 'state.json'

def load_project_state(name):
    """Load project state from JSON file."""
    state_file = get_project_state_path(name)
    if state_file.exists():
        with open(state_file) as f:
            return json.load(f)
    return None

def save_project_state(name, state):
    """Save project state to JSON file."""
    state_file = get_project_state_path(name)
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

def update_current_task(task_data):
    """Update current task state for integration with cc-sessions."""
    task_file = project_dir / '.claude' / 'state' / 'current_task.json'
    task_file.parent.mkdir(parents=True, exist_ok=True)
    with open(task_file, 'w') as f:
        json.dump(task_data, f, indent=2)

def get_current_git_branch():
    """Get current git branch using CLI."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            cwd=project_dir
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except subprocess.CalledProcessError:
        pass
    return 'main'

def create_git_branch(branch_name):
    """Create and checkout git branch using CLI."""
    try:
        # Check if branch already exists
        result = subprocess.run(
            ['git', 'rev-parse', '--verify', branch_name],
            capture_output=True,
            text=True,
            cwd=project_dir
        )

        if result.returncode == 0:
            # Branch exists, just checkout
            subprocess.run(
                ['git', 'checkout', branch_name],
                capture_output=True,
                text=True,
                cwd=project_dir
            )
        else:
            # Create new branch
            subprocess.run(
                ['git', 'checkout', '-b', branch_name],
                capture_output=True,
                text=True,
                cwd=project_dir
            )
        return True
    except subprocess.CalledProcessError:
        return False

if command == 'create':
    if len(args) < 2:
        print('Error: Project name required for create command')
        sys.exit(1)

    name = args[1]
    ensure_projects_dir()
    project_path = get_project_path(name)

    if project_path.exists():
        print(f'Error: Project {name} already exists')
        sys.exit(1)

    # Create project structure
    project_path.mkdir()
    (project_path / 'plan').mkdir()

    # Copy template if available
    template_source = project_dir / 'sessions' / 'BUILD_PROJECT_TEMPLATE.md'
    if template_source.exists():
        import shutil
        shutil.copy2(template_source, project_path / 'README.md')

    # Initialize state
    current_branch = get_current_git_branch()
    state = {
        'project': name,
        'status': 'pending',
        'created': datetime.now().strftime('%Y-%m-%d'),
        'updated': datetime.now().strftime('%Y-%m-%d'),
        'current_step': None,
        'completed_steps': [],
        'active_branch': current_branch,
        'plan_files': [],
        'total_steps': 0,
        'completion_percentage': 0.0,
        'step_details': {}
    }
    save_project_state(name, state)

    print(f'✅ Project {name} created successfully!')
    print(f'Next steps:')
    print(f'1. Add implementation plan files to: sessions/projects/{name}/plan/')
    print(f'2. Run: /project parse {name}')
    print(f'3. Start work: /project work {name} [step-number]')

elif command == 'list':
    ensure_projects_dir()

    if len(args) > 1:
        # List steps for specific project
        name = args[1]
        state = load_project_state(name)
        if not state:
            print(f'Error: Project {name} not found')
            sys.exit(1)

        print(f'🔨 Project: {name}')
        print(f'Status: {state["status"]}')
        print(f'Progress: {state["completion_percentage"]:.1f}% ({len(state["completed_steps"])}/{state["total_steps"]} steps)')
        print()

        if state['step_details']:
            for step_num in sorted(state['step_details'].keys(), key=lambda x: tuple(map(int, x.split('.')))):
                step = state['step_details'][step_num]
                status_icon = '✅' if step.get('status') == 'completed' else ('🔄' if step.get('status') == 'in-progress' else '⏸️')
                print(f'{status_icon} {step_num}: {step["title"]} ({step["file"]})')
        else:
            print('No steps found. Run /project parse {name} to scan plan files.')

    else:
        # List all projects
        if not projects_dir.exists():
            print('No projects found.')
            print('Create one with: /project create [name]')
            sys.exit(0)

        projects = [d for d in projects_dir.iterdir() if d.is_dir()]
        if not projects:
            print('No projects found.')
            print('Create one with: /project create [name]')
            sys.exit(0)

        print('🔨 Projects:')
        print()
        for project_path in sorted(projects):
            name = project_path.name
            state = load_project_state(name)
            if state:
                status_icon = '✅' if state['status'] == 'completed' else ('🔄' if state['status'] == 'active' else '⏸️')
                print(f'{status_icon} {name} - {state["completion_percentage"]:.1f}% complete ({state["status"]})')
            else:
                print(f'❓ {name} - No state file')

elif command == 'work':
    if len(args) < 3:
        print('Error: Project name and step number required')
        print('Usage: /project work [name] [step]')
        sys.exit(1)

    name, step = args[1], args[2]
    state = load_project_state(name)
    if not state:
        print(f'Error: Project {name} not found')
        sys.exit(1)

    if step not in state['step_details']:
        print(f'Error: Step {step} not found in project {name}')
        print('Available steps:')
        for s in sorted(state['step_details'].keys()):
            print(f'  {s}: {state["step_details"][s]["title"]}')
        sys.exit(1)

    step_info = state['step_details'][step]
    branch_name = f'project/{name}/step-{step.replace(".", "-")}'

    # Create git branch using CLI
    if create_git_branch(branch_name):
        print(f'🌿 Created/switched to branch: {branch_name}')
    else:
        print(f'⚠️  Warning: Could not create/switch to branch {branch_name}')

    # Update project state
    state['current_step'] = step
    state['status'] = 'active'
    state['active_branch'] = branch_name
    if step_info.get('status') != 'completed':
        step_info['status'] = 'in-progress'
        step_info['started_date'] = datetime.now().strftime('%Y-%m-%d')
    state['updated'] = datetime.now().strftime('%Y-%m-%d')
    save_project_state(name, state)

    # Update current task for cc-sessions integration
    task_data = {
        'task': f'project:{name}:{step}',
        'branch': branch_name,
        'services': [],
        'updated': datetime.now().strftime('%Y-%m-%d'),
        'project': {
            'project': name,
            'step': step,
            'step_title': step_info['title']
        }
    }
    update_current_task(task_data)

    print(f'🔨 Starting work on step {step}: {step_info["title"]}')
    print(f'📁 File: {step_info["file"]}')
    print(f'🌿 Branch: {branch_name}')
    print()
    print('Implementation:')
    print(step_info.get('implementation', 'No implementation details available'))
    print()
    if step_info.get('validation'):
        print('Validation Criteria:')
        for criterion in step_info['validation']:
            print(f'- [ ] {criterion}')
    print()
    print(f'When complete, run: /project complete {name} {step}')

elif command == 'complete':
    if len(args) < 3:
        print('Error: Project name and step number required')
        print('Usage: /project complete [name] [step]')
        sys.exit(1)

    name, step = args[1], args[2]
    state = load_project_state(name)
    if not state:
        print(f'Error: Project {name} not found')
        sys.exit(1)

    if step not in state['step_details']:
        print(f'Error: Step {step} not found in project {name}')
        sys.exit(1)

    step_info = state['step_details'][step]

    # Mark step as completed
    step_info['status'] = 'completed'
    step_info['completed_date'] = datetime.now().strftime('%Y-%m-%d')

    if step not in state['completed_steps']:
        state['completed_steps'].append(step)

    # Update completion percentage
    state['completion_percentage'] = (len(state['completed_steps']) / state['total_steps']) * 100 if state['total_steps'] > 0 else 0

    # Update project status
    if len(state['completed_steps']) == state['total_steps']:
        state['status'] = 'completed'

    state['updated'] = datetime.now().strftime('%Y-%m-%d')
    save_project_state(name, state)

    print(f'✅ Step {step} completed: {step_info["title"]}')
    print(f'📊 Project progress: {state["completion_percentage"]:.1f}% ({len(state["completed_steps"])}/{state["total_steps"]} steps)')

    if state['status'] == 'completed':
        print('🎉 Project completed!')
    else:
        # Suggest next steps
        remaining = [s for s in state['step_details'] if state['step_details'][s].get('status') != 'completed']
        if remaining:
            next_step = sorted(remaining, key=lambda x: tuple(map(int, x.split('.'))))[0]
            print(f'💡 Next suggested step: /project work {name} {next_step}')

elif command == 'status':
    if len(args) < 2:
        print('Error: Project name required')
        sys.exit(1)

    name = args[1]
    state = load_project_state(name)
    if not state:
        print(f'Error: Project {name} not found')
        sys.exit(1)

    print(f'🔨 Project Status: {name}')
    print(f'📊 Progress: {state["completion_percentage"]:.1f}% ({len(state["completed_steps"])}/{state["total_steps"]} steps)')
    print(f'🏷️ Status: {state["status"]}')
    print(f'📅 Created: {state["created"]}')
    print(f'📅 Updated: {state["updated"]}')

    if state.get('current_step'):
        current_step_info = state['step_details'][state['current_step']]
        print(f'🔄 Current Step: {state["current_step"]} - {current_step_info["title"]}')

    if state.get('active_branch'):
        print(f'🌿 Active Branch: {state["active_branch"]}')

    print()

    # Show step breakdown
    completed = [s for s in state['step_details'] if state['step_details'][s].get('status') == 'completed']
    in_progress = [s for s in state['step_details'] if state['step_details'][s].get('status') == 'in-progress']
    pending = [s for s in state['step_details'] if state['step_details'][s].get('status') not in ['completed', 'in-progress']]

    if completed:
        print(f'✅ Completed Steps ({len(completed)}):')
        for step in sorted(completed, key=lambda x: tuple(map(int, x.split('.')))):
            step_info = state['step_details'][step]
            print(f'  {step}: {step_info["title"]}')

    if in_progress:
        print(f'🔄 In Progress ({len(in_progress)}):')
        for step in sorted(in_progress, key=lambda x: tuple(map(int, x.split('.')))):
            step_info = state['step_details'][step]
            print(f'  {step}: {step_info["title"]}')

    if pending:
        print(f'⏸️ Pending Steps ({len(pending)}):')
        for step in sorted(pending, key=lambda x: tuple(map(int, x.split('.'))))[0:5]:
            step_info = state['step_details'][step]
            print(f'  {step}: {step_info["title"]}')
        if len(pending) > 5:
            print(f'  ... and {len(pending) - 5} more')

elif command == 'parse':
    if len(args) < 2:
        print('Error: Project name required')
        sys.exit(1)

    name = args[1]
    project_path = get_project_path(name)
    if not project_path.exists():
        print(f'Error: Project {name} not found')
        sys.exit(1)

    print(f'🔍 Parsing project: {name}')
    print('Using build-project-parser agent for detailed parsing...')

    # This will be handled by the build-project-parser agent
    # For now, just indicate that parsing is needed
    print('Call the build-project-parser agent with the project path to complete parsing.')

else:
    print(f'Error: Unknown command {command}')
    print('Available commands: create, list, work, complete, status, parse')
    sys.exit(1)