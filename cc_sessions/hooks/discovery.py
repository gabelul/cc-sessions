#!/usr/bin/env python3
"""
Discovery hook for contextual feature suggestions and progressive disclosure.
Tracks usage patterns and provides smart recommendations for cc-sessions features.
"""
import json
import sys
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from shared_state import get_project_root, ensure_state_dir, check_daic_mode_bool

def load_usage_stats():
    """Load user engagement and feature usage statistics."""
    try:
        project_root = get_project_root()
        ensure_state_dir()
        stats_file = project_root / ".claude" / "state" / "usage_stats.json"

        if stats_file.exists():
            with open(stats_file, 'r') as f:
                return json.load(f)
        else:
            # Initialize default stats structure
            return {
                "session_count": 0,
                "task_count": 0,
                "commands_used": {},
                "agents_used": {},
                "daic_switches": 0,
                "last_session": None,
                "feature_discoveries": {},
                "user_level": "novice",  # novice, comfortable, advanced
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat()
            }
    except Exception:
        return {}

def save_usage_stats(stats):
    """Save updated usage statistics."""
    try:
        project_root = get_project_root()
        ensure_state_dir()
        stats_file = project_root / ".claude" / "state" / "usage_stats.json"

        stats["last_updated"] = datetime.now().isoformat()

        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
    except Exception:
        pass  # Graceful failure - don't break workflow

def update_session_stats(stats):
    """Update session-level statistics."""
    stats["session_count"] = stats.get("session_count", 0) + 1
    stats["last_session"] = datetime.now().isoformat()

    # Update user level based on experience
    if stats["session_count"] < 4:
        stats["user_level"] = "novice"
    elif stats["session_count"] < 15:
        stats["user_level"] = "comfortable"
    else:
        stats["user_level"] = "advanced"

def get_contextual_suggestions(stats, prompt=""):
    """Generate contextual feature suggestions based on user patterns and input."""
    suggestions = []
    user_level = stats.get("user_level", "novice")
    commands_used = stats.get("commands_used", {})
    agents_used = stats.get("agents_used", {})

    # Analyze user input patterns
    prompt_lower = prompt.lower()

    # New user guidance
    if user_level == "novice":
        if stats.get("session_count", 0) == 1:
            suggestions.append({
                "type": "tutorial",
                "message": "🌱 New to cc-sessions? Try `/tutorial` for a 3-minute hands-on walkthrough of the DAIC workflow.",
                "urgency": "high"
            })

        if "/status" not in commands_used and stats.get("session_count", 0) > 1:
            suggestions.append({
                "type": "status_awareness",
                "message": "💡 Lost? Use `/status` anytime to see what's happening and get your bearings.",
                "urgency": "medium"
            })

    # Feature discovery based on patterns
    if user_level in ["comfortable", "advanced"]:
        # Agent suggestions
        if len(agents_used) == 0 and stats.get("task_count", 0) > 3:
            suggestions.append({
                "type": "agents_introduction",
                "message": "🤖 Ready for specialized help? Try `/help agents` to learn about AI assistants for heavy analysis.",
                "urgency": "medium"
            })

        # Memory Bank suggestions
        if "sync-file" not in commands_used and stats.get("session_count", 0) > 5:
            suggestions.append({
                "type": "memory_bank",
                "message": "🧠 Working on complex projects? Memory Bank preserves context across sessions. See `/help memory`.",
                "urgency": "low"
            })

    # Context-specific suggestions based on user input
    if any(word in prompt_lower for word in ["stuck", "confused", "not working", "help", "how"]):
        if "troubleshoot" not in commands_used:
            suggestions.append({
                "type": "troubleshoot",
                "message": "🔧 Having issues? Check `/help troubleshoot` for common problems and solutions.",
                "urgency": "high"
            })

    if any(word in prompt_lower for word in ["agent", "analyze", "review", "heavy", "complex"]):
        if len(agents_used) < 2:
            suggestions.append({
                "type": "agents_specific",
                "message": "⚡ For heavy analysis work, try specialized agents: `/help agents` shows what's available.",
                "urgency": "medium"
            })

    if any(word in prompt_lower for word in ["project", "multiple", "phases", "steps", "build"]):
        if "build-project" not in commands_used:
            suggestions.append({
                "type": "build_project",
                "message": "🏗️ Multi-step project? Try `/build-project` for structured phase management.",
                "urgency": "medium"
            })

    # Advanced workflow suggestions
    if user_level == "advanced":
        if stats.get("daic_switches", 0) > 10 and "add-trigger" not in commands_used:
            suggestions.append({
                "type": "custom_triggers",
                "message": "⚡ Power user tip: Create custom trigger phrases with `/add-trigger` for personalized workflow.",
                "urgency": "low"
            })

    return suggestions

def track_feature_discovery(stats, feature_type):
    """Track when user discovers and starts using features."""
    discoveries = stats.get("feature_discoveries", {})
    if feature_type not in discoveries:
        discoveries[feature_type] = {
            "discovered": datetime.now().isoformat(),
            "usage_count": 1
        }
    else:
        discoveries[feature_type]["usage_count"] += 1

    stats["feature_discoveries"] = discoveries

def detect_frustration_indicators(prompt):
    """Detect potential user frustration and provide helpful guidance."""
    frustration_words = [
        "stuck", "confused", "not working", "broken", "error", "failed",
        "doesn't work", "won't work", "can't", "unable", "problem"
    ]

    prompt_lower = prompt.lower()
    return any(word in prompt_lower for word in frustration_words)

def detect_capability_questions(prompt):
    """Detect questions about what cc-sessions can do."""
    capability_patterns = [
        "can you", "can claude", "can this", "does this", "can cc-sessions",
        "how do i", "how to", "what can", "is it possible"
    ]

    prompt_lower = prompt.lower()
    return any(pattern in prompt_lower for pattern in capability_patterns)

def main():
    """Main discovery hook execution."""
    try:
        # Load input
        input_data = json.load(sys.stdin)
        prompt = input_data.get("prompt", "")

        # Load current usage stats
        stats = load_usage_stats()

        # Update session stats (only once per session)
        current_time = datetime.now().isoformat()
        last_session = stats.get("last_session")

        # Consider it a new session if last session was more than 30 minutes ago
        if not last_session or (
            datetime.fromisoformat(current_time) -
            datetime.fromisoformat(last_session) > timedelta(minutes=30)
        ):
            update_session_stats(stats)

        # Generate contextual suggestions
        suggestions = get_contextual_suggestions(stats, prompt)

        # Build response context
        context = ""

        # Add suggestions if any (limit to most important ones)
        if suggestions:
            # Sort by urgency and limit to 2 suggestions max
            suggestions.sort(key=lambda x: {"high": 3, "medium": 2, "low": 1}[x["urgency"]], reverse=True)
            limited_suggestions = suggestions[:2]

            if limited_suggestions:
                context += "\n" + "="*50 + "\n"
                context += "FEATURE DISCOVERY SUGGESTIONS\n"
                context += "="*50 + "\n"

                for suggestion in limited_suggestions:
                    context += f"{suggestion['message']}\n"

                context += "="*50 + "\n"

        # Special handling for frustration or capability questions
        if detect_frustration_indicators(prompt):
            track_feature_discovery(stats, "troubleshooting_help")
            if not any(s["type"] == "troubleshoot" for s in suggestions):
                context += "\n🆘 **Having trouble?** Check `/help troubleshoot` or `/status` for guidance.\n"

        if detect_capability_questions(prompt):
            track_feature_discovery(stats, "capability_inquiry")
            context += "\n💡 **Exploring capabilities?** Use `/help` for feature overview or `/help commands` for complete reference.\n"

        # Save updated stats
        save_usage_stats(stats)

        # Output context for Claude
        print(context)

    except Exception as e:
        # Graceful failure - don't break the workflow
        print("")  # Empty output if discovery fails

if __name__ == "__main__":
    main()