# cc-sessions CLAUDE.md

## Purpose
Complete Claude Code Sessions framework that enforces Discussion-Alignment-Implementation-Check (DAIC) methodology for AI pair programming workflows.

## Narrative Summary

The cc-sessions package transforms Claude Code from a basic AI coding assistant into a sophisticated workflow management system. It enforces structured collaboration patterns where Claude must discuss approaches before implementing code, maintains persistent task context across sessions, and provides specialized agents for complex operations.

The core innovation is the DAIC (Discussion-Alignment-Implementation-Check) enforcement through Python hooks that cannot be bypassed. When Claude attempts to edit code without explicit user approval ("go ahead", "make it so", etc.), the hooks block the tools and require discussion first. This prevents the common AI coding problem of immediate over-implementation without alignment.

The framework includes persistent task management with git branch enforcement, context preservation through session restarts, specialized subagents for heavy operations, and automatic context compaction when approaching token limits.

## Key Files
- `cc_sessions/install.py` - Cross-platform installer with Windows compatibility and Memory Bank MCP setup
- `install.js` - Node.js installer wrapper with Memory Bank MCP integration
- `cc_sessions/hooks/sessions-enforce.py` - Core DAIC enforcement, branch protection, and enhanced mode banners
- `cc_sessions/hooks/session-start.py` - Automatic task context and Memory Bank loading
- `cc_sessions/hooks/user-messages.py` - Trigger phrase detection, mode switching, and smart workflow suggestions
- `cc_sessions/hooks/post-tool-use.py` - Implementation mode reminders
- `cc_sessions/commands/status.md` - Comprehensive session status display
- `cc_sessions/commands/daic.md` - Internal mode switching command
- `cc_sessions/hooks/document-governance.py` - PRD/FSD validation and conflict detection
- `cc_sessions/hooks/task-completion-workflow.py` - Task completion notifications
- `cc_sessions/hooks/post-implementation-retention.py` - Implementation outcome preservation with git integration
- `cc_sessions/hooks/document-versioning.py` - Automatic document version management and archiving
- `cc_sessions/scripts/daic.cmd` - Windows Command Prompt daic command
- `cc_sessions/scripts/daic.ps1` - Windows PowerShell daic command
- `cc_sessions/commands/sync-*.md` - Memory Bank MCP synchronization commands
- `cc_sessions/commands/build-project.md` - Multi-phase project management
- `cc_sessions/commands/project.py` - Flexible stepped project workflows
- `cc_sessions/agents/logging.md` - Session work log consolidation agent
- `cc_sessions/agents/build-project-parser.md` - Build project plan parsing agent
- `cc_sessions/protocols/task-creation.md` - Structured task creation workflow
- `cc_sessions/protocols/build-project-creation.md` - Build project workflow protocol
- `cc_sessions/templates/CLAUDE.sessions.md` - Behavioral guidance template
- `cc_sessions/templates/BUILD_PROJECT_TEMPLATE.md` - Build project template
- `cc_sessions/templates/PRD_TEMPLATE.md` - Product Requirements Document template
- `cc_sessions/templates/FSD_TEMPLATE.md` - Functional Specification Document template
- `cc_sessions/templates/EPIC_TEMPLATE.md` - Epic planning template
- `cc_sessions/knowledge/hooks-reference.md` - Hook system documentation
- `pyproject.toml` - Package configuration with console script entry points
- `scripts/auto-version-bump.py` - Automatic version management script

## Version Management

### Automatic Version Bumping
The project includes an automatic version bumping system to ensure releases are properly versioned:

- **Auto-bump script**: `scripts/auto-version-bump.py` automatically increments patch version when significant files are modified
- **Trigger files**: Changes to installers, hooks, agents, commands, protocols, templates, or config files trigger version bumps
- **Manual control**: For major/minor version bumps, manually edit `pyproject.toml` and `package.json`

### Version Bump Guidelines
- **Patch (0.2.7 → 0.2.8)**: Bug fixes, installer improvements, hook updates
- **Minor (0.2.8 → 0.3.0)**: New features, new agents, significant protocol changes
- **Major (0.3.0 → 1.0.0)**: Breaking changes, major workflow overhauls

### Version Management Workflow

**CRITICAL RULE**: When completing ANY changes to cc-sessions (installers, hooks, agents, commands, protocols, templates):

1. **After finishing all related changes**, run the auto-version script:
   ```bash
   python scripts/auto-version-bump.py
   ```

2. **Or manually bump** both files:
   - Edit `pyproject.toml` version field
   - Edit `package.json` version field
   - Keep them synchronized

### When to Bump Versions
- ✅ **After completing a feature/fix** (not per individual edit)
- ✅ **Before telling user to reinstall** with `pipx install -e . --force`
- ✅ **When task completion hook reminds you**
- ❌ Don't bump on every small edit (causes version inflation)

### Auto-Detection
The task completion system will remind you if you've modified cc-sessions files and haven't bumped the version yet.

**IMPORTANT**: Version bumping ensures users get updated functionality when reinstalling cc-sessions.

## Installation Methods
- `pipx install cc-sessions` - Isolated Python install (recommended)
- `npm install -g cc-sessions` - Global npm install
- `pip install cc-sessions` - Direct pip install
- Direct bash: `./install.sh` from repository

## Core Features

### DAIC Enforcement
- Blocks Edit/Write/MultiEdit tools in discussion mode
- Requires explicit trigger phrases to enter implementation mode
- Configurable trigger phrases via `/add-trigger` command
- Read-only Bash commands allowed in discussion mode

### Task Management
- Priority-prefixed tasks: h- (high), m- (medium), l- (low), ?- (investigate)
- Automatic git branch creation and enforcement
- Persistent context across session restarts
- Work log consolidation and cleanup

### Branch Enforcement
- Task-to-branch mapping: implement- → feature/, fix- → fix/, etc.
- Blocks code edits if current branch doesn't match task requirements
- Four failure modes: wrong branch, no branch, task missing, branch missing

### Context Preservation
- Automatic context compaction at 75%/90% token usage
- Session restart with full task context loading
- Specialized agents operate in separate contexts

### Memory Persistence
- **Memory Bank MCP Integration** - Persistent context storage across sessions
- **Cross-session knowledge** - Architectural insights and project understanding survive restarts
- **Sync commands** - `/sync-file`, `/sync-push`, `/sync-pull`, `/sync-status`, `/sync-all`
- **Auto-loading** - Memory Bank files automatically presented during session startup
- **Graceful fallback** - Full functionality with or without Memory Bank available

### Build Project Management
- **Multi-phase projects** - Structured project workflow with numbered implementation steps (1.1, 1.2, etc.)
- **Step tracking** - Automatic validation and completion percentage monitoring
- **State preservation** - Project state survives session restarts
- **Template-driven** - Consistent project structure via BUILD_PROJECT_TEMPLATE.md

### Document Governance
- **PRD/FSD validation** - Validates code changes against project requirements documents
- **Conflict detection** - Identifies potential violations of documented restrictions
- **Template system** - Standardized templates for PRD, FSD, and EPIC documents
- **Automated enforcement** - Hooks automatically check changes during development

### Task Completion Workflow
- **Enhanced completion tracking** - Structured task completion with workflow suggestions
- **Integration ready** - Designed to work with GitHub MCP when available
- **Notification system** - Simple completion notifications and next-step guidance

### Implementation Context Retention
- **Automatic outcome capture** - Preserves implementation details after code edits using git CLI
- **Git context integration** - Captures git status, diffs, and branch information
- **Memory Bank storage** - Persistent storage of implementation outcomes across sessions
- **Local fallback** - Graceful degradation when Memory Bank MCP unavailable
- **AI memory compensation** - Helps Claude remember what was implemented between sessions

### Document Versioning
- **Automatic version management** - Increments document version numbers after changes
- **Archive system** - Preserves previous versions with configurable history limits
- **Git complement** - Provides backup versioning independent of git commits
- **Change logging** - Maintains document change logs with timestamps and descriptions
- **Recovery support** - Enables restoration of previous document versions

### Flexible Project Management
- **Manual step planning** - Alternative to /build-project for custom workflows
- **Git branch integration** - Automatic branch creation and switching using git CLI
- **Step tracking** - Monitors progress through numbered implementation steps
- **State persistence** - Project state survives session restarts
- **Progress visualization** - Completion percentages and step status indicators

### Specialized Agents
- **context-gathering**: Creates comprehensive task context manifests with Memory Bank integration
- **logging**: Consolidates work logs with cleanup and chronological ordering
- **code-review**: Reviews implementations for quality and patterns
- **context-refinement**: Updates context with session discoveries
- **service-documentation**: Maintains CLAUDE.md files for services
- **build-project-parser**: Parses implementation plans and tracks step completion

## Integration Points

### Consumes
- Claude Code hooks system for behavioral enforcement
- Git for branch management and enforcement
- Python 3.8+ with tiktoken for token counting
- Shell environment for command execution (Bash/PowerShell/Command Prompt)

### Provides
- `/add-trigger` - Dynamic trigger phrase configuration
- `daic` - Manual mode switching command
- `/sync-file`, `/sync-push`, `/sync-pull`, `/sync-status`, `/sync-all` - Memory Bank MCP commands
- `/build-project` - Multi-phase project management commands
- `/project` - Flexible stepped project workflows
- Hook-based tool blocking and behavioral enforcement
- Task file templates and management protocols
- Document governance with PRD/FSD/EPIC templates
- Agent-based specialized operations

## Configuration

Primary configuration in `sessions/sessions-config.json`:
- `developer_name` - How Claude addresses the user
- `trigger_phrases` - Phrases that switch to implementation mode
- `blocked_tools` - Tools blocked in discussion mode
- `branch_enforcement.enabled` - Enable/disable git branch checking
- `task_detection.enabled` - Enable/disable task-based workflows
- `memory_bank_mcp` - Memory Bank MCP configuration and sync files

State files in `.claude/state/`:
- `current_task.json` - Active task metadata
- `daic-mode.json` - Current discussion/implementation mode

Windows-specific configuration in `.claude/settings.json`:
- Hook commands use Windows-style paths with `%CLAUDE_PROJECT_DIR%`
- Python interpreter explicitly specified for `.py` hook execution
- Native `.cmd` and `.ps1` script support for daic command

## Git Commit Guidelines

### Commit Voice and Attribution
- **NEVER add Claude/AI names** to commits - these are Gabi's commits using Gabi's persona
- **Use Gabi's authentic voice**: playfully sarcastic, helpful, technically competent
- **Commit style**: Happy, funny, self-aware about tech pain points
- **Tone example**: "because doing X manually 47 times was driving me nuts"
- **NO corporate speak** - write like talking to a smart friend who gets the references
- **Attribution**: These are Gabi's innovations and improvements, not AI-generated work

### Commit Message Structure
```
feat: short description - because [relatable tech frustration]

[Observational humor about the problem being solved]

New features:
• Feature 1 - practical benefit
• Feature 2 - practical benefit

[Brief explanation of value with personality]

[Backwards compatibility note if relevant]
```

## Key Patterns

### Hook Architecture
- Pre-tool-use hooks for enforcement (sessions-enforce.py)
- Post-tool-use hooks for reminders (post-tool-use.py) 
- User message hooks for trigger detection (user-messages.py)
- Session start hooks for context loading (session-start.py)
- Shared state management across all hooks (shared_state.py)
- Cross-platform path handling using pathlib.Path throughout
- Windows-specific command prefixing with explicit python interpreter

### Agent Delegation
- Heavy file operations delegated to specialized agents
- Agents receive full conversation transcript for context
- Agent results returned to main conversation thread
- Agent state isolated in separate context windows

### Task Structure
- Markdown files with standardized sections (Purpose, Context, Success Criteria, Work Log)
- Directory-based tasks for complex multi-phase work
- File-based tasks for focused single objectives
- Automatic branch mapping from task naming conventions

### Subagent Protection
- Detection mechanism prevents DAIC reminders in subagent contexts
- Subagents blocked from editing .claude/state files
- Strict separation between main thread and agent operations

### Windows Compatibility
- Platform detection using `os.name == 'nt'` (Python) and `process.platform === 'win32'` (Node.js)
- File operations skip Unix permissions on Windows (no chmod calls)
- Command detection handles Windows executable extensions (.exe, .bat, .cmd)
- Global command installation to `%USERPROFILE%\AppData\Local\cc-sessions\bin`
- Hook commands use explicit `python` prefix and Windows environment variable format
- Native Windows scripts: daic.cmd (Command Prompt) and daic.ps1 (PowerShell)

## Package Structure

### Installation Variants
- Python package with pip/pipx/uv support
- NPM package wrapper for JavaScript environments
- Direct bash script for build-from-source installations
- Cross-platform compatibility (macOS, Linux, Windows 10/11)

### Template System
- Task templates for consistent structure
- CLAUDE.sessions.md behavioral template
- Protocol markdown files for complex workflows
- Agent prompt templates for specialized operations

## Quality Assurance Features

### Context Management
- Token counting and usage warnings at 75%/90% thresholds
- Automatic context compaction protocols
- State preservation across session boundaries
- Clean task file maintenance through logging agent

### Work Quality
- Mandatory discussion before implementation
- Code review agent for quality checks
- Pattern consistency through context gathering
- Branch enforcement prevents wrong-branch commits

### Process Integrity
- Hook-based enforcement cannot be bypassed
- State file protection from unauthorized changes
- Chronological work log maintenance
- Task scope enforcement through structured protocols

## Related Documentation

- docs/INSTALL.md - Detailed installation guide
- docs/USAGE_GUIDE.md - Workflow and feature documentation
- cc_sessions/knowledge/ - Internal architecture documentation
- README.md - Marketing-focused feature overview
- sessions/protocols/ - Workflow protocol specifications (in installed projects)

## Sessions System Behaviors

@CLAUDE.sessions.md
