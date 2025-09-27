# Advanced Topics

**For when you want to understand how cc-sessions actually works under the hood.**

## Hook Architecture

### How Hooks Work

CC-sessions uses Claude Code's hook system to intercept and control tool usage. Think of it as middleware for AI actions.

```
You type something
    ↓
user-messages.py (checks for triggers)
    ↓
Claude thinks about response
    ↓
sessions-enforce.py (blocks tools if needed)
    ↓
Claude executes (or gets blocked)
    ↓
post-tool-use.py (adds reminders)
```

### Key Hooks

**sessions-enforce.py**
- Runs before every tool use
- Blocks Edit/Write/MultiEdit in discussion mode
- Enforces branch requirements
- Can't be bypassed by Claude

**user-messages.py**
- Processes your messages before Claude sees them
- Detects trigger phrases ("go ahead", etc.)
- Adds context like `[[ ultrathink ]]` if not in API mode
- Monitors token usage

**session-start.py**
- Runs when you start Claude Code
- Loads current task automatically
- Restores context from previous session
- Shows Memory Bank files if available

**post-tool-use.py**
- Runs after tools execute
- Adds implementation mode reminders
- Helps maintain awareness of current mode

### Hook Communication

Hooks share state through JSON files:

```python
# .claude/state/daic-mode.json
{"mode": "discussion"}  # or "implementation"

# .claude/state/current_task.json
{
  "task": "fix-auth",
  "branch": "feature/fix-auth",
  "services": ["api", "web"]
}
```

## Custom Hooks

### Creating Your Own

1. **Create hook file:**
```python
#!/usr/bin/env python3
# .claude/hooks/my-custom-hook.py

import json
import sys

# Read input from Claude
input_data = json.load(sys.stdin)

# Your logic here
if "DELETE" in input_data.get("prompt", ""):
    print("WARNING: Delete operation detected!", file=sys.stderr)
    sys.exit(2)  # Block with feedback

# Allow to proceed
sys.exit(0)
```

2. **Register in settings:**
Edit `.claude/settings.json` to add your hook to appropriate events.

### Hook Exit Codes

- `0`: Allow operation to proceed
- `1`: Silent block (no message)
- `2`: Block with feedback (message via stderr)

## Agent Architecture

### How Agents Work

Agents are separate Claude instances that run in isolated contexts:

```
Main Thread (your conversation)
    ↓
Task Tool launches agent
    ↓
Agent gets full conversation history
    ↓
Agent works in separate context window
    ↓
Results return to main thread
```

### Why Agents Are Better

**Without agents:**
- Everything pollutes your main context
- Complex operations eat tokens
- Can't do heavy file analysis

**With agents:**
- Isolated context = no pollution
- Can read unlimited files
- Returns only essential results

### Custom Agents

Create `.claude/agents/my-agent.md`:

```markdown
You are a specialized agent for [PURPOSE].

## Your Task
[SPECIFIC INSTRUCTIONS]

## Input
You'll receive the full conversation history.
Read files from .claude/state/my-agent/ for context.

## Output
Return structured results:
- Summary of findings
- Specific recommendations
- Files modified/created
```

Then invoke:
```
Use the my-agent agent to [TASK]
```

## Branch Management

### Automatic Branch Creation

When you create a task, cc-sessions maps it to branches:

```python
task_prefixes = {
    "implement-": "feature/",
    "fix-": "fix/",
    "refactor-": "feature/",
    "migrate-": "feature/",
    "test-": "feature/",
    "docs-": "feature/"
}
```

### Multi-Service Handling

For monorepos with services:

```json
{
  "task": "fix-auth",
  "branch": "feature/fix-auth",
  "services": ["api", "web", "admin"]
}
```

Each service must be on the correct branch before editing.

## Token Optimization

### Where Tokens Go

**Big token users:**
1. File contents in context
2. Tool call results
3. Conversation history
4. Claude's thinking (if not in API mode)

### Optimization Strategies

**Automatic (built-in):**
- Context compaction at 75%/90%
- Agent isolation
- Selective file loading
- Work log compression

**Manual (you control):**
- Use `/clear` strategically
- Keep tasks focused
- Avoid huge file reads
- Enable API mode if paying per token

### API Mode Deep Dive

**Without API mode:**
```python
# Every message gets ultrathink
context = "[[ ultrathink ]]\n" + user_message
# 2-3x more tokens per message
```

**With API mode:**
```python
# Only when you explicitly ask
if "[[ultrathink]]" in user_message:
    # Deep thinking enabled
else:
    # Normal processing (saves 50-67% tokens)
```

## State Management

### State Files

```
.claude/state/
├── current_task.json      # Active task metadata
├── daic-mode.json         # Current mode (discussion/implementation)
├── context-warning-75.flag   # Shown 75% warning
├── context-warning-90.flag   # Shown 90% warning
└── in_subagent_context.flag  # Agent is running
```

### Task Files

```
sessions/tasks/
├── h-critical-bug.md      # High priority task
├── m-new-feature/         # Medium priority directory task
│   ├── README.md          # Main task description
│   ├── context.md         # Gathered context
│   └── work-log.md        # Session logs
└── l-nice-to-have.md      # Low priority task
```

## Customization Examples

### Softer Enforcement

For experienced users who want less friction:

```python
# .claude/hooks/sessions-enforce.py
# Add at line 135:
if "OVERRIDE" in prompt:
    sys.exit(0)  # Magic word bypasses everything
```

### Project-Specific Triggers

Different triggers per project:

```python
# .claude/hooks/user-messages.py
import os

project_triggers = {
    "web-app": ["ship it", "deploy"],
    "api": ["confirmed", "approved"],
    "scripts": ["run it", "execute"]
}

current_project = os.path.basename(os.getcwd())
triggers = project_triggers.get(current_project, ["go ahead"])
```

### Enhanced Logging

Track everything Claude does:

```python
# .claude/hooks/post-tool-use.py
import datetime

with open(".claude/audit.log", "a") as f:
    f.write(f"{datetime.datetime.now()}: {tool_name} on {file_path}\n")
```

## Performance Tuning

### Hook Optimization

**Slow hook?** Profile it:

```python
import time
start = time.time()
# Your hook code
print(f"Hook took {time.time() - start}s", file=sys.stderr)
```

### State Caching

Reduce file I/O:

```python
# Cache state in memory
import functools

@functools.lru_cache()
def get_cached_state():
    return json.load(open(STATE_FILE))
```

## Debugging

### Debug Output

Add to any hook:

```python
import os
if os.environ.get("CC_SESSIONS_DEBUG"):
    print(f"DEBUG: {variable}", file=sys.stderr)
```

Then run with:
```bash
CC_SESSIONS_DEBUG=1 claude
```

### Hook Testing

Test hooks without Claude:

```bash
echo '{"tool_name": "Edit", "tool_input": {}}' | python3 .claude/hooks/sessions-enforce.py
echo $?  # Check exit code
```

---

*Remember: With great power comes great opportunity to break things. Keep backups.*