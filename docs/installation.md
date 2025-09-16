# cc-sessions Installation Guide

This guide walks through installing cc-sessions and its optional Memory Bank MCP integration.

## Quick Installation

### Option 1: Python (Recommended)
```bash
# Install in isolated environment
pipx install cc-sessions

# Or use regular pip
pip install cc-sessions
```

### Option 2: Node.js
```bash
# Global installation
npm install -g cc-sessions

# Or run without installing
npx cc-sessions
```

### Option 3: Direct Installation
```bash
# Clone and run installer
git clone <repository>
cd cc-sessions
python cc_sessions/install.py
# OR
node install.js
```

## Step-by-Step Installation

### 1. Prerequisites
- **Python 3.8+** (for hooks and token counting)
- **pip** or **pipx** (Python package management)
- **Git** (recommended for branch enforcement)
- **Claude Code** (for hook system integration)

Optional for Memory Bank MCP:
- **Node.js** (for npx command)
- **Claude Code CLI** (for MCP server management)

### 2. Run the Installer

The installer will:
1. Check dependencies
2. Create directory structure
3. Install Python dependencies (tiktoken)
4. Copy hooks, agents, and protocols
5. Install daic command globally
6. **Optional**: Install Memory Bank MCP
7. Configure settings and create initial state

#### Interactive Configuration

**Developer Name**: How Claude addresses you in sessions
```
Your name: John Developer
```

**DAIC Trigger Phrases**: Phrases that switch to implementation mode
```
Default triggers: "make it so", "run that", "go ahead", "yert"
Add custom trigger phrase (Enter to skip): implement it
```

**Memory Bank MCP** (Optional):
```
🧠 Memory Bank MCP - Persistent context across sessions
   Stores task context, architectural insights, and project knowledge
   Enables seamless context restoration when sessions restart

   Install Memory Bank MCP? (y/n): y
```

**Tool Blocking Configuration**: Choose which tools are blocked in discussion mode
- Edit, Write, MultiEdit, NotebookEdit (blocked by default)
- Bash, Read, Grep, Glob (allowed by default)

### 3. Memory Bank MCP Setup

If you choose to install Memory Bank MCP, the installer will:

1. **Check Requirements**:
   - Verify `npx` command is available (Node.js)
   - Verify `claude` command is available (Claude Code CLI)

2. **Install via Smithery**:
   ```bash
   claude mcp add memory-bank npx -y @alioshr/memory-bank-mcp
   ```

3. **Configure Integration**:
   - Enable Memory Bank in `sessions-config.json`
   - Initialize empty sync files list
   - Set up auto-activation

### 4. Post-Installation

#### Restart Claude Code
Close and reopen Claude Code to activate the sessions hooks.

#### Verify Installation
```bash
# Check daic command
daic

# Verify hooks are loaded (should show sessions hooks)
# Check .claude/settings.json exists with hook configuration
```

#### Create Your First Task
```bash
# Tell Claude to create a task
"Create a new task for implementing user authentication"

# Or manually follow the protocol
# Copy template and fill in details
cp sessions/tasks/TEMPLATE.md sessions/tasks/h-implement-auth.md
```

## Directory Structure Created

```
project/
├── .claude/
│   ├── hooks/                  # Python hooks for DAIC enforcement
│   │   ├── sessions-enforce.py
│   │   ├── session-start.py
│   │   ├── user-messages.py
│   │   └── post-tool-use.py
│   ├── agents/                 # Specialized agent definitions
│   ├── state/                  # Session state files
│   │   ├── current_task.json
│   │   └── daic-mode.json
│   └── settings.json          # Hook configuration
├── sessions/
│   ├── tasks/                 # Task files and templates
│   │   └── TEMPLATE.md
│   ├── protocols/             # Workflow protocols
│   ├── knowledge/             # Project knowledge base
│   └── sessions-config.json   # Main configuration
└── CLAUDE.sessions.md          # Behavioral guidance
```

## Configuration Files

### sessions-config.json
```json
{
  "developer_name": "the developer",
  "trigger_phrases": ["make it so", "run that", "go ahead", "yert"],
  "blocked_tools": ["Edit", "Write", "MultiEdit", "NotebookEdit"],
  "task_detection": { "enabled": true },
  "branch_enforcement": { "enabled": true },
  "memory_bank_mcp": {
    "enabled": true,
    "auto_activate": true,
    "sync_files": []
  }
}
```

### .claude/settings.json (Generated)
Contains hook configuration for Claude Code integration.

## Memory Bank MCP Workflow

### 1. Mark Files for Sync
```bash
# Add important project files to Memory Bank
/sync-file docs/architecture.md
/sync-file docs/api-design.md
```

### 2. Push to Memory Bank
```bash
# Upload files to Memory Bank MCP
/sync-push
```

### 3. Automatic Loading
When you start a new Claude session, any files marked as "in_memory" will be automatically listed, allowing you to use Memory Bank MCP tools to retrieve specific content.

### 4. Access Stored Knowledge
```bash
# Use Memory Bank MCP tools in Claude
mcp__memory_bank__read_file("project_name", "architecture.md")
```

## Troubleshooting

### Memory Bank MCP Issues
- **"Requirements not met"**: Install Node.js and ensure `claude --version` works
- **Installation fails**: Try manual installation with `claude mcp add memory-bank npx -y @alioshr/memory-bank-mcp`
- **Files not syncing**: Check `/sync-status` and ensure files are marked as "in_memory"

### DAIC Hook Issues
- **Tools not blocked**: Restart Claude Code and check `.claude/settings.json` exists
- **daic command not found**: Add installation directory to your PATH
- **Windows issues**: Ensure both `.cmd` and `.ps1` scripts are installed

### General Issues
- **Python errors**: Ensure `pip install tiktoken` succeeds
- **Permission errors**: Use `pipx` instead of `pip`, or run with appropriate permissions
- **Git branch errors**: Ensure you're in a git repository, or disable branch enforcement

## Manual Memory Bank MCP Installation

If automatic installation fails:

```bash
# Install Claude's native MCP management CLI and Memory Bank MCP
claude mcp add memory-bank npx -y @alioshr/memory-bank-mcp

# Add to Claude Code MCP servers
claude mcp add memory-bank npx -y @alioshr/memory-bank-mcp

# Enable in sessions configuration
# Edit sessions/sessions-config.json and set memory_bank_mcp.enabled: true
```