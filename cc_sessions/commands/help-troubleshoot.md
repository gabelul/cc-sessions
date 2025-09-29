# Help - Troubleshooting Guide

Common issues with cc-sessions and their solutions - because sometimes even the best systems have their quirks.

## DAIC Workflow Issues

### "Stuck in discussion mode"
**Symptoms:** Can't edit files, tools blocked, trigger phrases not working

**Solutions:**
1. **Check your trigger phrases:**
   ```
   /status
   ```
   Look for "Trigger phrases" section

2. **Try explicit mode switch:**
   ```
   /daic implementation
   ```

3. **Verify trigger phrase syntax:**
   - Must be exact match (case-sensitive)
   - Default: "make it so", "go ahead", "ship it", "run that"
   - Add custom phrases: `/add-trigger "let's do this"`

4. **Reset if all else fails:**
   ```
   /daic discussion
   /daic implementation
   ```

### "Surprise code changes"
**Symptoms:** Code written without explicit approval

**Likely causes:**
- Accidentally used trigger phrase in normal conversation
- Hook configuration issue
- Mixed mode state

**Solutions:**
1. **Review trigger phrases:**
   ```
   /status
   ```
   Consider removing common phrases that might trigger accidentally

2. **Add more specific triggers:**
   ```
   /add-trigger "implement the plan"
   /add-trigger "execute this approach"
   ```

3. **Use explicit mode control:**
   ```
   /daic discussion  # Force discussion when planning
   /daic implementation  # Only when ready for code
   ```

### "Mode not switching"
**Symptoms:** Trigger phrases ignored, mode stays the same

**Diagnosis steps:**
1. Check current mode: `/status`
2. Verify hook installation: Look for mode banners (🔴/🟢)
3. Check configuration: `sessions/sessions-config.json`

**Solutions:**
- Reinstall cc-sessions: `pipx install cc-sessions --force`
- Manual mode switch: `/daic implementation`
- Check for conflicting hooks in `.claude/settings.json`

## Git and Branch Issues

### "Wrong branch" error
**Symptoms:** Hook blocks edits, says "wrong branch for task type"

**Understanding:** Task types map to branch prefixes:
- `h-*/m-*/l-*` → `feature/`
- `fix-*` → `fix/`
- `?-*` → `investigate/`
- `implement-*` → `feature/`

**Solutions:**
1. **Switch to correct branch:**
   ```bash
   git checkout feature/task-name
   ```

2. **Create missing branch:**
   ```bash
   git checkout -b feature/task-name
   ```

3. **Update task file if needed:**
   Check `.claude/state/current_task.json`

### "No current task" error
**Symptoms:** Branch enforcement blocks edits, no active task

**Solutions:**
1. **Check task state:**
   ```bash
   cat .claude/state/current_task.json
   ```

2. **Set current task:**
   Create or update the file with correct format:
   ```json
   {
     "task": "task-name",
     "branch": "feature/task-name",
     "services": ["auth"],
     "updated": "2025-01-29"
   }
   ```

3. **Disable branch enforcement temporarily:**
   Edit `sessions/sessions-config.json`:
   ```json
   {
     "branch_enforcement": {"enabled": false}
   }
   ```

### "Branch missing" error
**Symptoms:** Task expects branch that doesn't exist

**Solution:**
```bash
# Create the expected branch
git checkout -b feature/task-name

# Or switch to existing similar branch
git checkout feature/existing-branch

# Update current_task.json to match
```

## Memory Bank Issues

### "Memory Bank not available"
**Symptoms:** Sync commands fail, no persistent context

**Diagnosis:**
1. Check Memory Bank installation:
   ```bash
   which memory-bank-mcp
   npm list -g memory-bank-mcp
   ```

2. Check cc-sessions configuration:
   ```
   /sync-status
   ```

**Solutions:**
1. **Install Memory Bank MCP:**
   ```bash
   npm install -g memory-bank-mcp
   ```

2. **Reconfigure cc-sessions:**
   ```bash
   pipx install cc-sessions --force
   ```

3. **Manual configuration:**
   Edit `sessions/sessions-config.json` to enable Memory Bank

### "Sync conflicts"
**Symptoms:** `/sync-pull` reports conflicts, outdated local files

**Solutions:**
1. **Check sync status:**
   ```
   /sync-status
   ```

2. **Force bidirectional sync:**
   ```
   /sync-all
   ```

3. **Manual resolution:**
   - Edit conflicting files locally
   - Use `/sync-push` to overwrite Memory Bank version

### "Files not syncing"
**Symptoms:** Changes not preserved across sessions

**Solutions:**
1. **Add files to sync:**
   ```
   /sync-file CLAUDE.md
   /sync-file ARCHITECTURE.md
   ```

2. **Push changes explicitly:**
   ```
   /sync-push
   ```

3. **Discover unsynced files:**
   ```
   /update-unsynced
   ```

## Context and Performance Issues

### "Context too full"
**Symptoms:** Warnings about token usage, slow responses

**Solutions:**
1. **Check context usage:**
   ```
   /status
   ```

2. **Use logging agent to clean up:**
   ```
   Use the logging agent to consolidate the work log
   ```

3. **Delegate heavy work to agents:**
   - Context-gathering for analysis
   - Code-review for quality checks
   - Context-refinement for session handoffs

### "Session restart loses context"
**Symptoms:** Claude doesn't remember previous work

**Solutions:**
1. **Set up Memory Bank:** (best solution)
   ```
   /sync-file important-files.md
   /sync-push
   ```

2. **Use task files for context:**
   Create comprehensive task documentation

3. **Use context-gathering agent:**
   ```
   Use the context-gathering agent on this project
   ```

## Installation and Configuration Issues

### "Commands not working"
**Symptoms:** `/status`, `/help` etc. not recognized

**Solutions:**
1. **Verify installation:**
   ```bash
   pipx list | grep cc-sessions
   ```

2. **Reinstall with force:**
   ```bash
   pipx install cc-sessions --force
   ```

3. **Check Claude Code settings:**
   Look for cc-sessions hooks in `.claude/settings.json`

### "Hooks not running"
**Symptoms:** No mode banners, no trigger phrase detection

**Diagnosis:**
1. Check hook files exist in `cc_sessions/hooks/`
2. Verify `.claude/settings.json` has correct hook paths
3. Look for Python interpreter issues

**Solutions:**
1. **Reinstall cc-sessions:**
   ```bash
   pipx uninstall cc-sessions
   pipx install cc-sessions
   ```

2. **Check Python path:**
   Hooks need Python 3.8+ with tiktoken library

3. **Manual hook verification:**
   ```bash
   python cc_sessions/hooks/session-start.py
   ```

## Agent Issues

### "Agent not responding properly"
**Symptoms:** Agent returns minimal or incorrect results

**Solutions:**
1. **Be more specific in prompting:**
   ```
   Use the context-gathering agent on tasks/h-auth.md - focus on security patterns
   ```

2. **Check agent file exists:**
   ```bash
   ls cc_sessions/agents/
   ```

3. **Try different agent:**
   Maybe the task needs a different specialist

### "Agent context too large"
**Symptoms:** Agent operations slow or fail

**Solutions:**
1. **Scope agent work more narrowly:**
   Specify exact files or components

2. **Use multiple focused agent calls:**
   Instead of one large analysis, break into parts

3. **Clean up context first:**
   Use logging agent to consolidate before other agents

## Getting Help

### When troubleshooting doesn't work:
1. **Check cc-sessions documentation:** README.md and docs/
2. **Review working examples:** Look at successful task files
3. **Reset to clean state:** Reinstall and reconfigure
4. **Report issues:** GitHub issues with specific error details

### Information to include when asking for help:
- Operating system and Python version
- cc-sessions version: `pipx list | grep cc-sessions`
- Error messages and when they occur
- Current configuration files
- Steps to reproduce the issue

---

**Remember:** Most issues are configuration-related. When in doubt, reinstall cc-sessions and reconfigure from scratch - it's usually faster than debugging complex state issues.