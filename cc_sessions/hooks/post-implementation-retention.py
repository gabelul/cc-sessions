#!/usr/bin/env python3
"""Post-implementation context retention hook for preserving implementation outcomes with git CLI integration."""
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from shared_state import get_project_root, get_task_state, check_daic_mode_bool

def load_config():
    """Load document governance configuration."""
    project_root = get_project_root()
    config_file = project_root / "sessions" / "sessions-config.json"

    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get("document_governance", {})
        except (json.JSONDecodeError, FileNotFoundError):
            pass

    return {"enabled": False, "auto_context_retention": True}

def check_memory_bank_available():
    """Check if Memory Bank MCP is available."""
    try:
        result = subprocess.run(
            ["claude", "mcp", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "memory-bank" in result.stdout.lower()
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_git_context():
    """Get current git context using CLI commands."""
    project_root = get_project_root()
    git_context = {
        "status": "unknown",
        "diff": "",
        "branch": "unknown",
        "changes": []
    }

    try:
        # Get current branch
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        if branch_result.returncode == 0:
            git_context["branch"] = branch_result.stdout.strip()

        # Get git status
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        if status_result.returncode == 0:
            git_context["status"] = status_result.stdout.strip()
            if git_context["status"]:
                git_context["changes"] = git_context["status"].split('\n')

        # Get diff of changes
        diff_result = subprocess.run(
            ["git", "diff", "HEAD"],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        if diff_result.returncode == 0:
            git_context["diff"] = diff_result.stdout.strip()

    except subprocess.CalledProcessError:
        pass

    return git_context

def analyze_implementation_outcome(tool_name, tool_input):
    """Analyze what was implemented and gather outcome data with git context."""
    outcome_data = {
        "tool_used": tool_name,
        "timestamp": datetime.now().isoformat(),
        "files_modified": [],
        "implementation_type": "unknown",
        "git_context": get_git_context()
    }

    # Extract file information from tool input
    if tool_name in ["Edit", "MultiEdit"]:
        file_path = tool_input.get("file_path", "")
        if file_path:
            outcome_data["files_modified"].append(file_path)
            outcome_data["implementation_type"] = "code_modification"
    elif tool_name == "Write":
        file_path = tool_input.get("file_path", "")
        if file_path:
            outcome_data["files_modified"].append(file_path)
            outcome_data["implementation_type"] = "file_creation"
    elif tool_name == "NotebookEdit":
        notebook_path = tool_input.get("notebook_path", "")
        if notebook_path:
            outcome_data["files_modified"].append(notebook_path)
            outcome_data["implementation_type"] = "notebook_modification"

    # Determine if this is a significant implementation step
    if outcome_data["files_modified"] or outcome_data["git_context"]["changes"]:
        outcome_data["significant"] = True
    else:
        outcome_data["significant"] = False

    return outcome_data

def preserve_implementation_context(outcome_data):
    """Preserve implementation outcome to Memory Bank with git context."""
    if not check_memory_bank_available():
        # Fallback: save to local sessions directory
        return preserve_to_local(outcome_data)

    try:
        project_root = get_project_root()
        project_name = project_root.name
        task_state = get_task_state()

        # Create implementation outcome file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_name = task_state.get("task", "unknown")
        outcome_filename = f"implementation_{task_name}_{timestamp}.md"

        # Format git changes
        git_changes_text = "No git changes detected"
        if outcome_data["git_context"]["changes"]:
            git_changes_text = "\\n".join(f"- {change}" for change in outcome_data["git_context"]["changes"])

        # Format git diff (truncated for readability)
        git_diff_text = outcome_data["git_context"]["diff"][:1000] if outcome_data["git_context"]["diff"] else "No diff available"
        if len(outcome_data["git_context"]["diff"]) > 1000:
            git_diff_text += "\\n\\n[Truncated - full diff available in git log]"

        # Format outcome data
        outcome_content = f"""# Implementation Outcome - {task_name}

**Generated:** {outcome_data['timestamp']}
**Task:** {task_name}
**Git Branch:** {outcome_data["git_context"]["branch"]}
**Tool Used:** {outcome_data['tool_used']}
**Implementation Type:** {outcome_data['implementation_type']}

## Files Modified
{chr(10).join(f"- {file}" for file in outcome_data['files_modified']) if outcome_data['files_modified'] else "No files specified in tool input"}

## Git Status
{git_changes_text}

## Git Diff Preview
```diff
{git_diff_text}
```

## Implementation Details
This implementation step was completed as part of task {task_name}.

### Changes Made
- Tool: {outcome_data['tool_used']}
- Timestamp: {outcome_data['timestamp']}
- Significance: {'High' if outcome_data['significant'] else 'Low'}
- Git Branch: {outcome_data["git_context"]["branch"]}

## Next Steps
Implementation outcome preserved for future reference and context continuity.

### Git Commands for Review
```bash
git status
git diff HEAD
git log --oneline -5
```

## Context Preservation
This document captures the implementation outcome with git context for future sessions.
"""

        # Write outcome to Memory Bank context
        outcome_file = project_root / "sessions" / "memory_bank" / project_name / "implementations" / outcome_filename
        outcome_file.parent.mkdir(parents=True, exist_ok=True)
        outcome_file.write_text(outcome_content)

        return True
    except Exception as e:
        print(f"Warning: Could not preserve implementation context: {e}", file=sys.stderr)
        return False

def preserve_to_local(outcome_data):
    """Fallback: preserve to local sessions directory when Memory Bank unavailable."""
    try:
        project_root = get_project_root()
        task_state = get_task_state()

        # Create implementation outcome file locally
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_name = task_state.get("task", "unknown")
        outcome_filename = f"implementation_{task_name}_{timestamp}.md"

        outcome_content = f"""# Implementation Outcome - {task_name}

**Generated:** {outcome_data['timestamp']}
**Tool Used:** {outcome_data['tool_used']}
**Git Branch:** {outcome_data["git_context"]["branch"]}

## Files Modified
{chr(10).join(f"- {file}" for file in outcome_data['files_modified'])}

## Git Context
- Branch: {outcome_data["git_context"]["branch"]}
- Changes: {len(outcome_data["git_context"]["changes"])} files modified

## Note
Memory Bank MCP not available - saved locally.
Use `/sync-file` to add this to Memory Bank later.
"""

        # Write to local sessions directory
        outcome_file = project_root / "sessions" / "implementations" / outcome_filename
        outcome_file.parent.mkdir(parents=True, exist_ok=True)
        outcome_file.write_text(outcome_content)

        return True
    except Exception as e:
        print(f"Warning: Could not preserve implementation context locally: {e}", file=sys.stderr)
        return False

def check_task_completion():
    """Check if the current task appears to be completed."""
    try:
        # Check if we're switching back to discussion mode
        discussion_mode = check_daic_mode_bool()
        if discussion_mode:
            return True

        # Additional completion indicators could be added here
        return False
    except:
        return False

def preserve_final_task_context():
    """Preserve comprehensive task completion context with git status."""
    if not check_memory_bank_available():
        return preserve_final_to_local()

    try:
        project_root = get_project_root()
        project_name = project_root.name
        task_state = get_task_state()
        git_context = get_git_context()

        # Create final task context file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_name = task_state.get("task", "unknown")
        final_filename = f"task_completion_{task_name}_{timestamp}.md"

        # Format final context
        final_content = f"""# Task Completion Context - {task_name}

**Completed:** {datetime.now().isoformat()}
**Task:** {task_name}
**Git Branch:** {git_context["branch"]}

## Task Summary
Task {task_name} has been completed.

## Final Git Status
{chr(10).join(f"- {change}" for change in git_context["changes"]) if git_context["changes"] else "No pending changes"}

## Services Modified
{chr(10).join(f"- {service}" for service in task_state.get("services", [])) if task_state.get("services") else "No services specified"}

## Git Context at Completion
- Current Branch: {git_context["branch"]}
- Pending Changes: {len(git_context["changes"])} files
- Status: {git_context["status"] or "Clean working directory"}

## Recommended Next Steps
```bash
# Review changes
git status
git diff HEAD

# If satisfied, commit changes
git add .
git commit -m "Complete task: {task_name}"

# Consider pushing to remote
git push origin {git_context["branch"]}
```

## Context Preservation
This document marks the completion of task {task_name} with full git context.
Generated: {datetime.now().isoformat()}
"""

        # Write final context to Memory Bank
        final_file = project_root / "sessions" / "memory_bank" / project_name / "completions" / final_filename
        final_file.parent.mkdir(parents=True, exist_ok=True)
        final_file.write_text(final_content)

        return True
    except Exception as e:
        print(f"Warning: Could not preserve final task context: {e}", file=sys.stderr)
        return False

def preserve_final_to_local():
    """Fallback: preserve final task context locally."""
    try:
        project_root = get_project_root()
        task_state = get_task_state()
        git_context = get_git_context()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_name = task_state.get("task", "unknown")
        final_filename = f"completion_{task_name}_{timestamp}.md"

        final_content = f"""# Task Completion - {task_name}

**Completed:** {datetime.now().isoformat()}
**Git Branch:** {git_context["branch"]}

## Final Status
Task completed with {len(git_context["changes"])} pending changes.

## Git Commands
```bash
git status
git commit -am "Complete {task_name}"
```
"""

        final_file = project_root / "sessions" / "completions" / final_filename
        final_file.parent.mkdir(parents=True, exist_ok=True)
        final_file.write_text(final_content)

        return True
    except Exception:
        return False

def main():
    """Main post-implementation hook function."""
    try:
        # Load input from stdin
        input_data = json.load(sys.stdin)

        # Get configuration
        config = load_config()

        if not config.get("enabled", False) or not config.get("auto_context_retention", True):
            return

        # Extract tool information
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # Check if this is an implementation tool
        implementation_tools = ["Edit", "Write", "MultiEdit", "NotebookEdit"]

        if tool_name in implementation_tools:
            # Analyze and preserve implementation outcome
            outcome_data = analyze_implementation_outcome(tool_name, tool_input)

            if outcome_data["significant"]:
                preserve_implementation_context(outcome_data)

        # Check for task completion indicators
        if tool_name == "Bash" and "daic" in str(tool_input):
            # Task likely completing, preserve final context
            preserve_final_task_context()

        # Check for other completion indicators
        elif check_task_completion():
            preserve_final_task_context()

    except json.JSONDecodeError:
        pass
    except Exception as e:
        print(f"Post-implementation retention hook error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()