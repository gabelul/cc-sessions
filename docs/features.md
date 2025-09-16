# cc-sessions Features

This document describes the current features available in cc-sessions.

## Core Features

### DAIC Workflow Enforcement
- **Discussion-Alignment-Implementation-Check** methodology enforcement
- Blocks code editing tools until explicit user approval
- Configurable trigger phrases to switch to implementation mode
- Prevents over-implementation without alignment

### Task Management
- **Priority-based task organization**: h- (high), m- (medium), l- (low), ?- (investigate)
- **Git branch enforcement**: Automatic branch creation and validation
- **Persistent task context**: Tasks survive session restarts
- **Work log consolidation**: Automatic logging and cleanup

### Memory Bank MCP Integration

#### Persistent Context Across Sessions
cc-sessions integrates with [Memory Bank MCP](https://github.com/alioshr/memory-bank-mcp) to solve the context loss problem when Claude sessions restart. This enables long-term project memory and architectural knowledge preservation.

**Key Benefits:**
- **Context Preservation**: Important project insights survive session restarts
- **Knowledge Building**: Cumulative understanding grows over time
- **Efficiency**: Avoid re-explaining architecture repeatedly
- **Consistency**: Maintain implementation patterns across sessions

#### How Memory Bank Works
1. **File Synchronization**: Mark important markdown files for sync with `/sync-file`
2. **Push to Memory**: Use `/sync-push` to store files in Memory Bank
3. **Auto-Loading**: Session startup automatically shows available memory files
4. **Access**: Use `mcp__memory_bank__read_file` tools to retrieve specific content

#### Available Sync Commands
- `/sync-file [path]` - Add markdown file to sync configuration
- `/sync-push` - Push pending files to Memory Bank MCP
- `/sync-pull` - Read synchronized files from Memory Bank
- `/sync-status` - Show sync status of all configured files
- `/sync-all` - Sync all configured files regardless of status

#### Configuration
Memory Bank MCP is configured in `sessions/sessions-config.json`:
```json
{
  "memory_bank_mcp": {
    "enabled": true,
    "auto_activate": true,
    "sync_files": [
      {
        "path": "docs/architecture.md",
        "status": "in_memory",
        "last_synced": "2025-09-14T18:30:00Z"
      }
    ]
  }
}
```

### Build Project Management
- **Multi-phase project creation**: Structured project workflow with numbered steps
- **Step tracking**: Automatic validation and completion tracking
- **State management**: Project state preservation across sessions
- **Template-driven**: Consistent project structure and documentation

#### Build Project Commands
- **Create project**: Initialize new build project with structured plan directory
- **Step management**: Track completion of implementation steps (1.1, 1.2, etc.)
- **Status monitoring**: View project progress and completion percentage
- **Integration**: Works with git branches and task management

### Document Governance
- **PRD/FSD validation**: Validates code changes against project requirements
- **Conflict detection**: Identifies potential violations of documented restrictions
- **Template system**: Standardized templates for PRD, FSD, and EPIC documents
- **Governance hooks**: Automatic validation during development workflow

#### Available Document Templates
- **PRD_TEMPLATE.md**: Product Requirements Document with sections for executive summary, functional requirements, and success metrics
- **FSD_TEMPLATE.md**: Functional Specification Document with API specs, data models, and technical architecture
- **EPIC_TEMPLATE.md**: Epic planning template with user stories, acceptance criteria, and timeline management

### Task Completion Workflow
- **Completion tracking**: Enhanced task completion with workflow suggestions
- **Integration ready**: Designed to work with GitHub MCP when available
- **Notification system**: Simple completion notifications and next-step guidance

### Implementation Context Retention
- **Automatic capture**: Preserves implementation outcomes after code edits
- **Git integration**: Uses git CLI to capture status, diffs, and branch information
- **Memory persistence**: Stores outcomes in Memory Bank MCP for cross-session continuity
- **AI assistance**: Helps Claude remember what was implemented between sessions
- **Local fallback**: Works with or without Memory Bank MCP available

#### Implementation Context Features
- Captures modified files and implementation types (code_modification, file_creation, etc.)
- Records git branch, status, and diff information automatically
- Creates timestamped implementation outcome documents
- Provides git command suggestions for review and commit workflows

### Document Versioning
- **Automatic versioning**: Increments document version numbers after changes
- **Version archiving**: Preserves previous versions with configurable history limits
- **Git independence**: Backup versioning system independent of git commits
- **Change logging**: Maintains document change logs with timestamps
- **Version recovery**: Supports restoration of previous document versions

#### Document Versioning Commands
- **Version creation**: `python document-versioning.py version <file> [description]`
- **Version history**: `python document-versioning.py history <file>`
- **Version restore**: `python document-versioning.py restore <file> <version>`

### Flexible Project Management
- **Manual workflows**: Alternative to /build-project for custom project structures
- **Git branch automation**: Automatic branch creation and switching using git CLI
- **Step-by-step tracking**: Progress monitoring through numbered implementation steps
- **State persistence**: Project state survives session restarts and context limits
- **Visual progress**: Completion percentages and step status indicators

#### Project Management Commands
- **Create project**: `/project create <name>` - Initialize new project structure
- **List projects**: `/project list` - Show all projects or specific project steps
- **Start work**: `/project work <name> <step>` - Begin working on specific step
- **Complete step**: `/project complete <name> <step>` - Mark step as completed
- **Check status**: `/project status <name>` - View project progress and details
- **Parse plans**: `/project parse <name>` - Re-parse plan files for changes

### Specialized Agents
- **context-gathering**: Creates comprehensive task context manifests with Memory Bank integration
- **logging**: Consolidates work logs with cleanup and chronological ordering
- **code-review**: Reviews implementations for quality and patterns
- **context-refinement**: Updates context with session discoveries
- **service-documentation**: Maintains CLAUDE.md files for services

### Cross-Platform Support
- **Windows**: Native PowerShell and Command Prompt support
- **macOS/Linux**: Full Unix shell integration
- **Installation**: Python (pipx/pip) or Node.js (npm) installers
- **Commands**: Global `daic` command for manual mode switching

### Context Management
- **Token tracking**: Automatic warnings at 75%/90% usage thresholds
- **Context compaction**: Automated context compression protocols
- **State preservation**: Maintains session state across boundaries
- **Subagent isolation**: Specialized operations in separate contexts

### Branch Enforcement
- **Task-to-branch mapping**: Automatic branch creation based on task naming
- **Protection**: Blocks code edits on wrong branches
- **Validation**: Ensures task requirements match current branch
- **Flexibility**: Override branch enforcement when needed

## Installation Options

1. **Python (Recommended)**: `pipx install cc-sessions`
2. **Node.js**: `npm install -g cc-sessions`
3. **Direct**: Clone repository and run installer

## Configuration Files

- `sessions/sessions-config.json` - Main configuration
- `.claude/state/current_task.json` - Active task metadata
- `.claude/state/daic-mode.json` - Current discussion/implementation mode
- `.claude/settings.json` - Hook configuration for Claude Code

## Integration Requirements

- **Claude Code**: Uses hooks system for tool blocking
- **Git**: Branch management and enforcement
- **Python 3.8+**: With tiktoken for token counting
- **Optional**: Memory Bank MCP for persistent context