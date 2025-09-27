# Configuration Guide

**How to make cc-sessions work exactly the way you want it.**

## Quick Start

Your main config file: `sessions/sessions-config.json`

If it doesn't exist, cc-sessions creates it with sensible defaults.

## Core Settings

### Trigger Phrases

**What it does:** Words that switch Claude from discussion to implementation mode

**Default:**
```json
"trigger_phrases": ["make it so", "run that", "yert"]
```

**Your style:**
```json
"trigger_phrases": ["go ahead", "do it", "yeah", "sounds good", "lgtm"]
```

**Add phrases without editing:**
```
/add-trigger "ship it"
/add-trigger "let's go"
```

### Developer Name

**What it does:** How Claude addresses you in messages

```json
"developer_name": "Gabi"
```

Claude will say things like "Got it, Gabi" instead of generic responses.

### Blocked Tools

**What it does:** Tools Claude can't use in discussion mode

**Default:**
```json
"blocked_tools": ["Edit", "Write", "MultiEdit", "NotebookEdit"]
```

**Less restrictive:**
```json
"blocked_tools": ["Edit", "Write"]  // Allows MultiEdit
```

### Branch Enforcement

**What it does:** Makes sure you're on the right git branch for your task

```json
"branch_enforcement": {
  "enabled": true,
  "task_prefixes": ["implement-", "fix-", "refactor-", "migrate-", "test-", "docs-"],
  "branch_prefixes": {
    "implement-": "feature/",
    "fix-": "fix/",
    "refactor-": "feature/",
    "migrate-": "feature/",
    "test-": "feature/",
    "docs-": "feature/"
  }
}
```

**To disable:** Set `"enabled": false`

**Why you might disable:** Working in a monorepo, not using git, or find it annoying

### Read-Only Bash Commands

**What it does:** Commands allowed in discussion mode (no filesystem changes)

```json
"read_only_bash_commands": [
  "ls", "pwd", "cat", "grep", "find",
  "git status", "git log", "git diff",
  "npm list", "pip list",
  // ... many more
]
```

**Add your own:**
```json
"read_only_bash_commands": [
  // ... existing commands ...
  "docker ps",
  "kubectl get pods",
  "terraform plan"
]
```

### API Mode

**What it does:** Disables ultrathink to save tokens (for API users)

```json
"api_mode": false  // true if paying per token
```

**Effect:**
- `false`: Ultrathink on every message (better reasoning, more tokens)
- `true`: No ultrathink unless you add `[[ ultrathink ]]` to your message

### Task Detection

**What it does:** Automatically suggests creating tasks when you mention work

```json
"task_detection": {
  "enabled": true
}
```

**Disable if:** You find the suggestions annoying

### Memory Bank MCP

**What it does:** Configures persistent memory storage

```json
"memory_bank_mcp": {
  "enabled": true,
  "sync_files": [
    "sessions/tasks/*.md",
    ".claude/state/current_task.json"
  ]
}
```

## Example Configurations

### Minimal Enforcement

For experienced users who want less friction:

```json
{
  "developer_name": "Gabi",
  "trigger_phrases": ["yeah", "do it", "go"],
  "blocked_tools": ["Edit", "Write"],
  "branch_enforcement": {
    "enabled": false
  },
  "task_detection": {
    "enabled": false
  }
}
```

### Maximum Safety

For complex projects where mistakes are expensive:

```json
{
  "developer_name": "Gabi",
  "trigger_phrases": ["approved", "confirmed", "execute"],
  "blocked_tools": ["Edit", "Write", "MultiEdit", "NotebookEdit", "Bash"],
  "branch_enforcement": {
    "enabled": true
  },
  "task_detection": {
    "enabled": true
  }
}
```

### API User Optimized

For users paying per token:

```json
{
  "developer_name": "Gabi",
  "trigger_phrases": ["go ahead", "do it"],
  "blocked_tools": ["Edit", "Write", "MultiEdit", "NotebookEdit"],
  "api_mode": true,
  "memory_bank_mcp": {
    "enabled": true
  }
}
```

## Advanced Configuration

### Custom Task Prefixes

Add your own task types:

```json
"task_prefixes": ["implement-", "fix-", "research-", "design-"],
"branch_prefixes": {
  "research-": "research/",
  "design-": "design/"
}
```

### Service-Specific Settings

For monorepos with multiple services, create service-specific configs:

```
services/api/sessions-config.json
services/web/sessions-config.json
```

### Hook Customization

Beyond JSON config, you can modify the Python hooks directly:

```
.claude/hooks/sessions-enforce.py  # Tool blocking logic
.claude/hooks/user-messages.py     # Trigger phrase detection
.claude/hooks/session-start.py     # Startup behavior
```

## Troubleshooting Config Issues

**Config not loading?**
- Check file exists: `sessions/sessions-config.json`
- Validate JSON: No trailing commas, proper quotes

**Trigger phrases not working?**
- Case doesn't matter but spelling does
- Check they're in the array correctly
- Try `/add-trigger` command instead

**Branch enforcement too strict?**
- Temporarily disable: `"enabled": false`
- Or just work on the main branch

**Tools still blocked after approval?**
- Check you're in implementation mode
- Try manual toggle: `daic`

---

*Remember: Start with defaults, then adjust based on what annoys you.*