#!/bin/bash

# Claude Code StatusLine Script
# Provides comprehensive session information in a clean format
# System-agnostic version using Python instead of jq

# Read JSON input from stdin
input=$(cat)

# Extract basic info using Python (works on all systems)
cwd=$(echo "$input" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('workspace', {}).get('current_dir') or data.get('cwd', ''))")
model_name=$(echo "$input" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('model', {}).get('display_name', 'Claude'))")
session_id=$(echo "$input" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('session_id', ''))")

# Function to calculate context breakdown and progress
calculate_context() {
    # Get transcript if available
    transcript_path=$(echo "$input" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('transcript_path', ''))")
    
    # Context Limit Detection
    # ========================
    # Claude Code auto-compacts context at 75-90% usage, so we show 80% of the
    # theoretical limit as "usable context". This prevents users from being surprised
    # when they hit auto-compaction before reaching the displayed limit.
    #
    # Model Context Windows (theoretical):
    # - All current Claude models: 200K tokens
    # - Sonnet 4 with 1M beta: 1,000,000 tokens (requires special API header)
    #
    # Usable Context (80% rule):
    # - Standard models: 160K tokens (80% of 200K)
    # - Sonnet 4 with 1M beta: 800K tokens (80% of 1M)

    # Default: 160K for all models (80% of standard 200K context)
    context_limit=160000

    # Special case: Sonnet 4 might have 1M beta access
    # Users must explicitly enable this since we can't auto-detect beta access
    if [[ "$model_name" == *"Sonnet 4"* ]] || [[ "$model_name" == *"sonnet-4"* ]]; then
        if [[ "$CLAUDE_SONNET4_1M" == "true" ]] || [[ "$CLAUDE_SONNET4_1M" == "1" ]]; then
            context_limit=800000  # 80% of 1M for confirmed beta users
        fi
        # Otherwise stays at default 160K (80% of 200K)
    fi

    # Allow complete override for special cases or future models
    if [[ -n "$CLAUDE_CONTEXT_LIMIT" ]]; then
        context_limit=$CLAUDE_CONTEXT_LIMIT
        # Optional: Validate the override is reasonable
        if [[ $context_limit -lt 1000 ]] || [[ $context_limit -gt 1000000 ]]; then
            echo "Warning: CLAUDE_CONTEXT_LIMIT seems unusual: $context_limit" >&2
        fi
    fi

    # Debug logging to understand what models Claude Code reports
    if [[ "$DEBUG_STATUSLINE" == "true" ]]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') Model='$model_name' Context=$context_limit" >> ~/.claude-statusline-debug.log
    fi
    
    if [[ -n "$transcript_path" && -f "$transcript_path" ]]; then
        # Parse transcript to get real token usage from most recent main-chain message
        total_tokens=$(python3 -c "
import sys, json

try:
    with open('$transcript_path', 'r') as f:
        lines = f.readlines()
    
    most_recent_usage = None
    most_recent_timestamp = None
    
    for line in lines:
        try:
            data = json.loads(line.strip())
            # Skip sidechain entries (subagent calls)
            if data.get('isSidechain', False):
                continue
            
            # Check for usage data in main-chain messages
            if data.get('message', {}).get('usage'):
                timestamp = data.get('timestamp')
                if timestamp and (not most_recent_timestamp or timestamp > most_recent_timestamp):
                    most_recent_timestamp = timestamp
                    most_recent_usage = data['message']['usage']
        except:
            continue
    
    # Calculate context length (input + cache tokens only, NOT output)
    if most_recent_usage:
        context_length = (
            most_recent_usage.get('input_tokens', 0) +
            most_recent_usage.get('cache_read_input_tokens', 0) +
            most_recent_usage.get('cache_creation_input_tokens', 0)
        )
        print(context_length)
    else:
        print(0)
except:
    print(0)
" 2>/dev/null)
        
        # Calculate actual context usage percentage
        if [[ $total_tokens -gt 0 ]]; then
            # Use Python for floating point math (bc not available on all systems)
            progress_pct=$(python3 -c "print(f'{$total_tokens * 100 / $context_limit:.1f}')")
            progress_pct_int=$(python3 -c "print(int($total_tokens * 100 / $context_limit))")
            if [[ $progress_pct_int -gt 100 ]]; then
                progress_pct="100.0"
                progress_pct_int=100
            fi
        else
            progress_pct="0.0"
            progress_pct_int=0
        fi
    else
        # Default values when no transcript available - still add default context
        total_tokens=17900
        progress_pct=$(python3 -c "print(f'{$total_tokens * 100 / $context_limit:.1f}')")
        progress_pct_int=$(python3 -c "print(int($total_tokens * 100 / $context_limit))")
    fi
    
    # Format token count in 'k' format
    formatted_tokens=$(python3 -c "print(f'{$total_tokens // 1000}k')")
    formatted_limit=$(python3 -c "print(f'{$context_limit // 1000}k')")
    
    # Create progress bar (capped at 100%) with Ayu Dark colors
    filled_blocks=$((progress_pct_int / 10))
    if [[ $filled_blocks -gt 10 ]]; then filled_blocks=10; fi
    empty_blocks=$((10 - filled_blocks))
    
    # Ayu Dark colors (converted to closest ANSI 256)
    if [[ $progress_pct_int -lt 50 ]]; then
        bar_color="\033[38;5;114m"  # AAD94C green
    elif [[ $progress_pct_int -lt 80 ]]; then
        bar_color="\033[38;5;215m"  # FFB454 orange
    else
        bar_color="\033[38;5;203m"  # F26D78 red
    fi
    gray_color="\033[38;5;242m"     # Dim for empty blocks
    text_color="\033[38;5;250m"     # BFBDB6 light gray
    reset="\033[0m"
    
    progress_bar="${bar_color}"
    for ((i=0; i<filled_blocks; i++)); do progress_bar+="█"; done
    progress_bar+="${gray_color}"
    for ((i=0; i<empty_blocks; i++)); do progress_bar+="░"; done
    progress_bar+="${reset} ${text_color}${progress_pct}% (${formatted_tokens}/${formatted_limit})${reset}"
    
    echo -e "$progress_bar"
}

# Get current task with color
get_current_task() {
    cyan="\033[38;5;111m"    # 59C2FF entity blue
    reset="\033[0m"
    if [[ -f "$cwd/.claude/state/current_task.json" ]]; then
        task_name=$(python3 -c "
import sys, json
try:
    with open('$cwd/.claude/state/current_task.json', 'r') as f:
        data = json.load(f)
        print(data.get('task', 'None'))
except:
    print('None')
" 2>/dev/null)
        echo -e "${cyan}Task: $task_name${reset}"
    else
        echo -e "${cyan}Task: None${reset}"
    fi
}

# Get DAIC mode with color
get_daic_mode() {
    if [[ -f "$cwd/.claude/state/daic-mode.json" ]]; then
        mode=$(python3 -c "
import sys, json
try:
    with open('$cwd/.claude/state/daic-mode.json', 'r') as f:
        data = json.load(f)
        print(data.get('mode', 'discussion'))
except:
    print('discussion')
" 2>/dev/null)
        if [[ "$mode" == "discussion" ]]; then
            purple="\033[38;5;183m"  # D2A6FF constant purple
            reset="\033[0m"
            echo -e "${purple}DAIC: Discussion${reset}"
        else
            green="\033[38;5;114m"   # AAD94C string green
            reset="\033[0m"
            echo -e "${green}DAIC: Implementation${reset}"
        fi
    else
        purple="\033[38;5;183m"      # D2A6FF constant purple
        reset="\033[0m"
        echo -e "${purple}DAIC: Discussion${reset}"
    fi
}

# Count edited files with color
count_edited_files() {
    yellow="\033[38;5;215m"  # FFB454 func orange
    reset="\033[0m"
    if [[ -d "$cwd/.git" ]]; then
        cd "$cwd"
        # Count modified and staged files
        modified_count=$(git status --porcelain 2>/dev/null | grep -E '^[AM]|^.[AM]' | wc -l || echo "0")
        echo -e "${yellow}✎ $modified_count files${reset}"
    else
        echo -e "${yellow}✎ 0 files${reset}"
    fi
}

# Count open tasks with color
count_open_tasks() {
    blue="\033[38;5;111m"    # 73B8FF modified blue
    reset="\033[0m"
    tasks_dir="$cwd/sessions/tasks"
    if [[ -d "$tasks_dir" ]]; then
        # Count .md files that don't contain "Status: done" or "Status: completed"
        open_count=0
        for task_file in "$tasks_dir"/*.md; do
            if [[ -f "$task_file" ]]; then
                if ! grep -q -E "Status:\s*(done|completed)" "$task_file" 2>/dev/null; then
                    ((open_count++))
                fi
            fi
        done
        echo -e "${blue}[$open_count open]${reset}"
    else
        echo -e "${blue}[0 open]${reset}"
    fi
}

# Build the complete statusline
progress_info=$(calculate_context)
task_info=$(get_current_task)
daic_info=$(get_daic_mode)
files_info=$(count_edited_files)
tasks_info=$(count_open_tasks)

# Output the complete statusline in two lines with color support
# Line 1: Progress bar | Current task
# Line 2: DAIC mode | Files edited | Open tasks
echo -e "$progress_info | $task_info"
echo -e "$daic_info | $files_info | $tasks_info"
