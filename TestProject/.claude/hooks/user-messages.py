#!/usr/bin/env python3
"""User message hook to detect DAIC trigger phrases and special patterns."""
import json
import sys
import re
import os
try:
    import tiktoken
except ImportError:
    tiktoken = None
from shared_state import check_daic_mode_bool, set_daic_mode

# Load input
input_data = json.load(sys.stdin)
prompt = input_data.get("prompt", "")
transcript_path = input_data.get("transcript_path", "")
context = ""

# Get configuration (if exists)
try:
    from pathlib import Path
    from shared_state import get_project_root
    PROJECT_ROOT = get_project_root()
    CONFIG_FILE = PROJECT_ROOT / "sessions" / "sessions-config.json"
    
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
    else:
        config = {}
except:
    config = {}

# Default trigger phrases if not configured
DEFAULT_TRIGGER_PHRASES = ["make it so", "run that", "yert"]
trigger_phrases = config.get("trigger_phrases", DEFAULT_TRIGGER_PHRASES)

# Check if this is an /add-trigger command
is_add_trigger_command = prompt.strip().startswith('/add-trigger')

# Check API mode and add ultrathink if not in API mode (skip for /add-trigger)
if not config.get("api_mode", False) and not is_add_trigger_command:
    context = "[[ ultrathink ]]\n"

# Token monitoring
def get_context_length_from_transcript(transcript_path):
    """Get current context length from the most recent main-chain message in transcript"""
    try:
        import os
        if not os.path.exists(transcript_path):
            return 0
            
        with open(transcript_path, 'r') as f:
            lines = f.readlines()
        
        most_recent_usage = None
        most_recent_timestamp = None
        
        # Parse each JSONL entry
        for line in lines:
            try:
                data = json.loads(line.strip())
                # Skip sidechain entries (subagent calls)
                if data.get('isSidechain', False):
                    continue
                    
                # Check if this entry has usage data
                if data.get('message', {}).get('usage'):
                    entry_time = data.get('timestamp')
                    # Track the most recent main-chain entry with usage
                    if entry_time and (not most_recent_timestamp or entry_time > most_recent_timestamp):
                        most_recent_timestamp = entry_time
                        most_recent_usage = data['message']['usage']
            except json.JSONDecodeError:
                continue
        
        # Calculate context length from most recent usage
        if most_recent_usage:
            context_length = (
                most_recent_usage.get('input_tokens', 0) +
                most_recent_usage.get('cache_read_input_tokens', 0) +
                most_recent_usage.get('cache_creation_input_tokens', 0)
            )
            return context_length
    except Exception:
        pass
    return 0

# Check context usage and warn if needed (only if tiktoken is available)
if transcript_path and tiktoken and os.path.exists(transcript_path):
    context_length = get_context_length_from_transcript(transcript_path)
    
    if context_length > 0:
        # Calculate percentage of usable context (160k practical limit before auto-compact)
        usable_percentage = (context_length / 160000) * 100
        
        # Check for warning flag files to avoid repeating warnings
        from pathlib import Path
        PROJECT_ROOT = get_project_root()
        warning_75_flag = PROJECT_ROOT / ".claude" / "state" / "context-warning-75.flag"
        warning_90_flag = PROJECT_ROOT / ".claude" / "state" / "context-warning-90.flag"
        
        # Token warnings (only show once per session)
        if usable_percentage >= 90 and not warning_90_flag.exists():
            context += f"\n[90% WARNING] {context_length:,}/160,000 tokens used ({usable_percentage:.1f}%). CRITICAL: Run sessions/protocols/task-completion.md to wrap up this task cleanly!\n"
            warning_90_flag.parent.mkdir(parents=True, exist_ok=True)
            warning_90_flag.touch()
        elif usable_percentage >= 75 and not warning_75_flag.exists():
            context += f"\n[75% WARNING] {context_length:,}/160,000 tokens used ({usable_percentage:.1f}%). Context is getting low. Be aware of coming context compaction trigger.\n"
            warning_75_flag.parent.mkdir(parents=True, exist_ok=True)
            warning_75_flag.touch()

# DAIC keyword detection
current_mode = check_daic_mode_bool()

# Implementation triggers (only work in discussion mode, skip for /add-trigger)
if not is_add_trigger_command and current_mode and any(phrase in prompt.lower() for phrase in trigger_phrases):
    set_daic_mode(False)  # Switch to implementation
    context += "[DAIC: Implementation Mode Activated] You may now implement ONLY the immediately discussed steps. DO NOT take **any** actions beyond what was explicitly agreed upon. If instructions were vague, consider the bounds of what was requested and *DO NOT* cross them. When you're done, run the command: daic\n"

# Emergency stop (works in any mode)
if any(word in prompt for word in ["SILENCE", "STOP"]):  # Case sensitive
    set_daic_mode(True)  # Force discussion mode
    context += "[DAIC: EMERGENCY STOP] All tools locked. You are now in discussion mode. Re-align with your pair programmer.\n"

# Iterloop detection
if "iterloop" in prompt.lower():
    context += "You have been instructed to iteratively loop over a list. Identify what list the user is referring to, then follow this loop: present one item, wait for the user to respond with questions and discussion points, only continue to the next item when the user explicitly says 'continue' or something similar\n"

# Protocol detection - explicit phrases that trigger protocol reading
prompt_lower = prompt.lower()

# Context compaction detection
if any(phrase in prompt_lower for phrase in ["compact", "restart session", "context compaction"]):
    context += "If the user is asking to compact context, read and follow sessions/protocols/context-compaction.md protocol.\n"

# Task completion detection
if any(phrase in prompt_lower for phrase in ["complete the task", "finish the task", "task is done", 
                                               "mark as complete", "close the task", "wrap up the task"]):
    context += "If the user is asking to complete the task, read and follow sessions/protocols/task-completion.md protocol.\n"

# Task creation detection
if any(phrase in prompt_lower for phrase in ["create a new task", "create a task", "make a task",
                                               "new task for", "add a task"]):
    context += "If the user is asking to create a task, read and follow sessions/protocols/task-creation.md protocol.\n"

# Task switching detection
if any(phrase in prompt_lower for phrase in ["switch to task", "work on task", "change to task"]):
    context += "If the user is asking to switch tasks, read and follow sessions/protocols/task-startup.md protocol.\n"

# Task detection patterns (optional feature)
if config.get("task_detection", {}).get("enabled", True):
    task_patterns = [
        r"(?i)we (should|need to|have to) (implement|fix|refactor|migrate|test|research)",
        r"(?i)create a task for",
        r"(?i)add this to the (task list|todo|backlog)",
        r"(?i)we'll (need to|have to) (do|handle|address) (this|that) later",
        r"(?i)that's a separate (task|issue|problem)",
        r"(?i)file this as a (bug|task|issue)"
    ]
    
    task_mentioned = any(re.search(pattern, prompt) for pattern in task_patterns)
    
    if task_mentioned:
        # Add task detection note
        context += """
[Task Detection Notice]
The message may reference something that could be a task.

IF you or the user have discovered a potential task that is sufficiently unrelated to the current task, ask if they'd like to create a task file.

Tasks are:
• More than a couple commands to complete
• Semantically distinct units of work
• Work that takes meaningful context
• Single focused goals (not bundled multiple goals)
• Things that would take multiple days should be broken down
• NOT subtasks of current work (those go in the current task file/directory)

If they want to create a task, follow the task creation protocol.
"""

# Smart feature discovery integration
def update_usage_stats_for_user_input(prompt):
    """Update usage statistics based on user input patterns."""
    try:
        from pathlib import Path
        PROJECT_ROOT = get_project_root()
        stats_file = PROJECT_ROOT / ".claude" / "state" / "usage_stats.json"

        # Load existing stats
        if stats_file.exists():
            with open(stats_file, 'r') as f:
                stats = json.load(f)
        else:
            return  # Discovery hook will initialize on first run

        # Track command usage
        if prompt.strip().startswith('/'):
            command = prompt.strip().split()[0]
            commands_used = stats.get("commands_used", {})
            commands_used[command] = commands_used.get(command, 0) + 1
            stats["commands_used"] = commands_used

        # Track agent mentions
        if "agent" in prompt.lower():
            agent_keywords = ["context-gathering", "logging", "code-review", "context-refinement", "service-documentation"]
            for keyword in agent_keywords:
                if keyword in prompt.lower():
                    agents_used = stats.get("agents_used", {})
                    agents_used[keyword] = agents_used.get(keyword, 0) + 1
                    stats["agents_used"] = agents_used

        # Track DAIC switches
        if any(phrase in prompt.lower() for phrase in trigger_phrases):
            stats["daic_switches"] = stats.get("daic_switches", 0) + 1

        # Track task-related activity
        if any(word in prompt.lower() for word in ["task", "create", "implement", "fix"]):
            stats["task_count"] = stats.get("task_count", 0) + 1

        # Save updated stats
        stats["last_updated"] = json.dumps(os.times().elapsed).strip('"')
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)

    except Exception:
        pass  # Graceful failure

# Smart pattern detection and contextual suggestions (combines Phase 2 & 3 features)
def add_smart_suggestions(prompt):
    """Add contextual suggestions based on user input patterns."""
    suggestions = ""

    try:
        # Get current task state (Phase 2 functionality)
        from shared_state import get_task_state
        task_state = get_task_state()

        # Check for first-time user patterns (Phase 2)
        if any(phrase in prompt.lower() for phrase in ["how do i", "what should i", "what's next", "help me"]):
            if not task_state.get("task"):
                suggestions += "\n💡 Tip: Start by creating a task with 'create a new task' or try '/tutorial' for a guided walkthrough.\n"
            elif current_mode:  # Discussion mode
                suggestions += f"\n💡 Tip: You're in discussion mode. Describe your approach, then say a trigger phrase like '{trigger_phrases[0]}' to implement.\n"

        # Help-seeking patterns (Phase 3)
        help_patterns = [
            ("can you", "🔍 Exploring capabilities? Try `/help` to see what's available."),
            ("stuck", "🆘 Need help? Use `/status` to see current state or `/help troubleshoot` for common issues."),
            ("confused", "🧭 Lost? Use `/status` for your bearings and `/help workflow` to understand DAIC."),
            ("not working", "🔧 Something broken? Check `/help troubleshoot` for solutions."),
        ]

        for pattern, suggestion in help_patterns:
            if pattern in prompt.lower():
                suggestions += f"\n{suggestion}\n"
                break  # Only one help suggestion at a time

        # Suggest agents for complex analysis (Phase 2 enhanced with Phase 3)
        if any(phrase in prompt.lower() for phrase in ["analyze", "review", "understand", "examine", "investigate"]):
            if "context-gathering" not in prompt.lower():
                suggestions += "\n💡 Tip: For deep code analysis, try 'Use the context-gathering agent on [file/task]'.\n"

        # Feature opportunity detection (Phase 3)
        feature_opportunities = [
            (["multiple files", "many files", "several files"], "📁 Working with many files? Try the context-gathering agent for comprehensive analysis."),
            (["complex project", "big project", "large project"], "🧠 Complex project? Consider Memory Bank (`/help memory`) for persistent context."),
            (["step by step", "phases", "multiple steps"], "🏗️ Multi-step work? Try `/build-project` for structured project management."),
            (["review", "check", "quality"], "🔍 Need code review? Try the code-review agent for quality analysis."),
            (["document", "docs", "documentation"], "📚 Need docs? Try the service-documentation agent for structured documentation."),
        ]

        for patterns, suggestion in feature_opportunities:
            if any(pattern in prompt.lower() for pattern in patterns):
                suggestions += f"\n{suggestion}\n"
                break  # Only one feature suggestion at a time

        # Suggest Memory Bank for returning users (Phase 2)
        if any(phrase in prompt.lower() for phrase in ["remember", "previous", "last time", "before"]):
            if not config.get("memory_bank_mcp", {}).get("enabled"):
                suggestions += "\n💡 Tip: Enable Memory Bank to preserve insights across sessions. Run '/sync-status' to check setup.\n"

        # Suggest status command when user seems confused about state (Phase 2)
        if any(phrase in prompt.lower() for phrase in ["what mode", "current state", "where am i"]):
            suggestions += "\n💡 Tip: Run '/status' to see your current mode, task, and available commands.\n"

        # Suggest build-project for complex multi-step work (Phase 2)
        if any(phrase in prompt.lower() for phrase in ["big task", "multiple steps", "complex project", "roadmap"]):
            suggestions += "\n💡 Tip: For multi-phase projects, try '/build-project' for structured planning.\n"

        # Suggest code review after significant changes (Phase 2)
        if task_state.get("task") and any(phrase in prompt.lower() for phrase in ["done", "finished", "completed", "commit"]):
            suggestions += "\n💡 Tip: Before committing, consider using the code-review agent to check your work.\n"

    except Exception:
        # Fail silently - suggestions are optional
        pass

    return suggestions

# Update usage stats from this input (Phase 3)
update_usage_stats_for_user_input(prompt)

# Add smart suggestions based on input patterns (Combined Phase 2 & 3)
smart_suggestions = add_smart_suggestions(prompt)
if smart_suggestions:
    context += smart_suggestions

# Output the context additions
if context:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context
        }
    }
    print(json.dumps(output))

sys.exit(0)
