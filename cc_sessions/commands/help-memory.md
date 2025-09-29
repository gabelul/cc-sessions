# Help - Memory Bank Integration Guide

**Memory Bank MCP** provides persistent context storage that survives session restarts, crashes, and even complete Claude Code reinstalls. Think of it as your AI's long-term memory.

## What Memory Bank Solves

### The Context Loss Problem
- **Session restarts** wipe out conversation history
- **Complex projects** lose architectural understanding
- **Bug fixes** forget previous investigation context
- **Team handoffs** lose project knowledge

### Memory Bank Solution
- **Persistent files** sync bidirectionally across sessions
- **Architectural insights** preserved automatically
- **Cross-session learning** maintains project understanding
- **Graceful fallback** when Memory Bank unavailable

## Setup and Installation

### Prerequisites
```bash
# Install Memory Bank MCP (separate from cc-sessions)
npm install -g memory-bank-mcp
# or
pipx install memory-bank-mcp
```

### Configuration
Memory Bank configuration happens during cc-sessions installation:
```bash
pipx install cc-sessions  # Auto-detects and configures Memory Bank
```

**Manual configuration** (if needed):
```json
// sessions/sessions-config.json
{
  "memory_bank_mcp": {
    "enabled": true,
    "sync_files": [
      {
        "path": "CLAUDE.md",
        "category": "configuration",
        "status": "in_memory"
      }
    ]
  }
}
```

## Core Memory Bank Commands

### `/sync-file <path>`
**Purpose:** Add specific file to persistent storage
**Example:**
```
/sync-file ARCHITECTURE.md
/sync-file src/components/README.md
```
**Best for:** Important docs, configuration files, architectural guides

### `/sync-push`
**Purpose:** Save all local changes to Memory Bank
**When to use:**
- End of productive session
- Before major refactoring
- After solving complex bugs
- Preserving investigation results

### `/sync-pull`
**Purpose:** Get latest context from Memory Bank
**When to use:**
- Starting new session
- After team member updates
- Recovering from crashed session
- Fresh perspective on existing problem

### `/sync-status`
**Purpose:** See sync state of all tracked files
**Shows:**
- Files in Memory Bank vs. local versions
- Last sync timestamps
- Conflict indicators
- Sync health status

### `/sync-all`
**Purpose:** Complete bidirectional synchronization
**What happens:**
1. Push local changes to Memory Bank
2. Pull remote updates from Memory Bank
3. Resolve any conflicts intelligently
4. Update sync status

### `/update-unsynced`
**Purpose:** Discover valuable files not yet tracked
**Finds:**
- CLAUDE.md, README.md files
- Architecture and design documents
- PRD/FSD specification files
- Other important project docs

## Memory Bank Workflow Patterns

### The Persistent Project Pattern
1. **Setup:** `/sync-file CLAUDE.md` and key docs
2. **Work:** Normal DAIC workflow
3. **Preserve:** `/sync-push` at session end
4. **Resume:** `/sync-pull` at session start
5. **Maintain:** `/sync-status` periodically

### The Team Collaboration Pattern
1. **Sync before work:** `/sync-pull`
2. **Document discoveries:** Update tracked files
3. **Share insights:** `/sync-push`
4. **Conflict resolution:** Use `/sync-all` when needed

### The Investigation Pattern
1. **Start:** `/sync-pull` for historical context
2. **Investigate:** Normal debugging workflow
3. **Document findings:** Update relevant files
4. **Preserve:** `/sync-push` with investigation results

## Files Worth Syncing

### Essential for Every Project
- `CLAUDE.md` - Project instructions and context
- `ARCHITECTURE.md` - System design and patterns
- `README.md` - Project overview and setup

### For Complex Projects
- `PRD.md` - Product requirements
- `FSD.md` - Functional specifications
- Service-specific `CLAUDE.md` files
- Investigation notes and bug reports

### Development Workflow Files
- `.claude/sessions-config.json` - cc-sessions configuration
- Task files for ongoing work
- Build and deployment documentation

## Advanced Memory Bank Features

### Automatic Context Loading
When Memory Bank files are synced, cc-sessions automatically:
- Loads file list at session start
- Shows sync status in session banner
- Provides quick access to synced content

### Intelligent Conflict Resolution
When local and Memory Bank versions differ:
- Timestamps determine most recent
- Content comparison shows differences
- Manual resolution options available
- Backup versions preserved

### Cross-Session Architecture Preservation
Memory Bank helps maintain:
- **Design decisions** and their rationale
- **Integration patterns** used in the project
- **Bug investigation** context and findings
- **Performance optimization** insights

## Memory Bank Best Practices

### What to Sync
✅ **Do sync:**
- High-level architecture docs
- Project configuration files
- Investigation findings
- Design decision records

❌ **Don't sync:**
- Generated files (builds, dependencies)
- Temporary investigation files
- Personal notes not relevant to project
- Files that change frequently without meaning

### Sync Timing
- **Start of session:** `/sync-pull` for latest context
- **Major discoveries:** Update files immediately
- **End of session:** `/sync-push` to preserve work
- **Before complex work:** `/sync-all` for clean state

### File Organization
```
project/
├── CLAUDE.md              # Sync this
├── ARCHITECTURE.md        # Sync this
├── sessions/
│   ├── sessions-config.json   # Sync this
│   └── tasks/
│       └── h-auth-task.md     # Maybe sync if complex
└── src/                   # Don't sync source code directly
```

## Troubleshooting Memory Bank

### "Memory Bank not available"
- Check Memory Bank MCP installation
- Verify cc-sessions configuration
- Try `/sync-status` to test connection

### Sync conflicts
- Use `/sync-all` for intelligent resolution
- Check file timestamps with `/sync-status`
- Manual resolution: edit files and `/sync-push`

### Missing context after restart
- Check `/sync-status` for file sync state
- Use `/sync-pull` to get latest Memory Bank state
- Verify important files are tracked with `/update-unsynced`

### Performance issues
- Memory Bank operations are designed to be fast
- Large files may take longer to sync
- Consider splitting large docs into smaller files

---

**Bottom line:** Memory Bank turns cc-sessions from session-based tool into a persistent AI collaborator that remembers your project context across time.