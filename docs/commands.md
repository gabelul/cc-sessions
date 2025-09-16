# cc-sessions Commands Reference

This document describes all slash commands and their usage in cc-sessions.

## Core Commands

### `/add-trigger`
**Description**: Add custom trigger phrases for switching to implementation mode
**Usage**: `/add-trigger "implement this"`
**Arguments**: Trigger phrase in quotes

Adds new phrases that Claude recognizes as permission to switch from discussion to implementation mode. Default triggers include "make it so", "go ahead", "run that", and "yert".

### `daic` (Global Command)
**Description**: Manual mode switching between discussion and implementation
**Usage**: `daic` (in terminal)
**Arguments**: None

Switches Claude back to discussion mode from implementation mode. Available globally after installation.

## Memory Bank MCP Commands

These commands manage persistent context storage across Claude sessions using Memory Bank MCP.

### `/sync-file`
**Description**: Add a markdown file to Memory Bank synchronization
**Usage**: `/sync-file path/to/file.md`
**Arguments**: Relative path to markdown file
**Requirements**: File must exist and have .md extension

Adds a markdown file to the sync configuration. The file will be tracked for Memory Bank storage but not uploaded until `/sync-push` is used.

**Example**:
```bash
/sync-file docs/architecture.md
/sync-file project-overview.md
```

### `/sync-push`
**Description**: Push all pending files to Memory Bank MCP
**Usage**: `/sync-push`
**Arguments**: None
**Requirements**: Memory Bank MCP enabled, files configured with `/sync-file`

Uploads all files marked as "pending" or "ready_to_sync" to Memory Bank MCP. Files are marked as "ready_to_sync" after running this command. Use Memory Bank MCP tools to complete the actual upload.

**Example Output**:
```
Found 2 files to sync with Memory Bank MCP:
  docs/architecture.md
  project-overview.md

Files marked as ready for Memory Bank sync.
```

### `/sync-pull`
**Description**: List files available in Memory Bank MCP
**Usage**: `/sync-pull`
**Arguments**: None
**Requirements**: Memory Bank MCP enabled, files synced

Shows all files currently stored in Memory Bank MCP with their last sync timestamps. Use `mcp__memory_bank__read_file` tools to read specific file contents.

**Example Output**:
```
Files available in Memory Bank MCP (2 total):
  docs/architecture.md (synced: 2025-09-14T18:30:00Z)
  project-overview.md (synced: 2025-09-14T18:45:00Z)

Use mcp__memory_bank__read_file tools in Claude to read specific file contents.
```

### `/sync-status`
**Description**: Show sync status of all configured files
**Usage**: `/sync-status`
**Arguments**: None

Displays the current sync status of all files configured for Memory Bank synchronization.

**Status Values**:
- `pending` - File added but not yet processed
- `ready_to_sync` - File prepared for upload
- `in_memory` - File successfully stored in Memory Bank
- `failed` - Sync operation failed

**Example Output**:
```
Memory Bank Sync Status:
  docs/architecture.md - in_memory (last synced: 2025-09-14T18:30:00Z)
  project-overview.md - ready_to_sync (last synced: never)
  api-design.md - pending (last synced: never)
```

### `/sync-all`
**Description**: Sync all configured files to Memory Bank MCP
**Usage**: `/sync-all`
**Arguments**: None
**Requirements**: Memory Bank MCP enabled, Claude with Memory Bank tools

Forces synchronization of all configured files regardless of current status. This command uses Memory Bank MCP tools directly and updates file statuses to "in_memory" upon success.

**Process**:
1. Lists all configured files
2. Uses `mcp__memory_bank__write_file` for each file
3. Updates sync status and timestamps
4. Provides completion summary

## Memory Bank MCP Integration

### File Status Workflow
```
1. /sync-file        → Status: pending
2. /sync-push        → Status: ready_to_sync
3. Use MCP tools     → Status: in_memory
4. Auto-load in sessions
```

### Recommended Workflow
1. **Identify Important Files**: Architecture docs, API designs, project overviews
2. **Add to Sync**: Use `/sync-file` for each important markdown file
3. **Push to Memory**: Use `/sync-push` to prepare files
4. **Complete Sync**: Use Memory Bank MCP tools to upload content
5. **Verify**: Check `/sync-status` and `/sync-pull` to confirm

### Memory Bank Tools Usage
After using sync commands, complete the upload with Memory Bank MCP tools:

```bash
# Write file to Memory Bank
mcp__memory_bank__write_file("project_name", "architecture.md", file_content)

# Read file from Memory Bank
mcp__memory_bank__read_file("project_name", "architecture.md")

# List all projects
mcp__memory_bank__list_projects()

# List files in project
mcp__memory_bank__list_files("project_name")
```

## Configuration

### Memory Bank MCP Setup
Memory Bank commands require configuration in `sessions/sessions-config.json`:

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

### Command Permissions
Memory Bank sync commands use restricted tool permissions:
- `Bash(python3:*)` - For configuration management
- `Bash(echo:*)` - For status output
- `mcp__memory_bank__*` - For Memory Bank operations (sync-all only)

## Troubleshooting

### Common Issues

**"sessions-config.json not found"**
- Ensure cc-sessions is properly installed
- Check you're in the correct project directory

**"Memory Bank MCP is not enabled"**
- Set `memory_bank_mcp.enabled: true` in sessions-config.json
- Reinstall with Memory Bank MCP option

**"No files configured for sync"**
- Use `/sync-file` to add markdown files first
- Check `/sync-status` to see current configuration

**"Failed to add file"**
- Verify file exists and has .md extension
- Check file path is relative to project root
- Ensure sessions-config.json is writable

### Memory Bank MCP Connection
Verify Memory Bank MCP is working:
```bash
# Check installed MCP servers
claude mcp list

# Test Memory Bank connection
mcp__memory_bank__list_projects()
```

### Manual Configuration
If sync commands fail, you can manually edit `sessions/sessions-config.json`:

```json
{
  "memory_bank_mcp": {
    "enabled": true,
    "sync_files": [
      {
        "path": "your-file.md",
        "status": "pending",
        "last_synced": null
      }
    ]
  }
}
```