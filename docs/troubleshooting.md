# Troubleshooting Guide

**When stuff breaks (because it will), here's how to fix it.**

## Emergency Fixes

### "Claude is editing everything and won't stop"

**Immediate fix:** Type `STOP` (all caps)

This locks Claude into discussion mode instantly.

### "I can't get Claude to edit anything"

**Check these in order:**

1. **Are you in discussion mode?** Look for `[DAIC: Discussion Mode]` in messages
2. **Did you approve?** Say "go ahead" or your custom trigger phrase
3. **Is Claude blocked?** Check for `[DAIC: Tool Blocked]` errors

**Quick fix:** Type `daic` to manually toggle modes

### "Claude forgot everything we were working on"

**This happens when:**
- Context window restarted
- You used `/clear` without a task

**Fix:**
```bash
cat .claude/state/current_task.json  # See what task you were on
cat sessions/tasks/your-task.md      # Your work is saved here
```

Tell Claude: "Let's continue working on [task-name]"

## Installation & Configuration

### Using the Installer

**The installer (`cc-sessions` command) lets you configure:**

```bash
cc-sessions  # Run the interactive installer
```

**Prompts you'll see:**
- Your name (for personalized messages)
- Enable statusline? (recommended yes)
- Trigger phrases (your approval words)
- API mode? (for token saving)
- Branch enforcement? (git integration)

**Re-run to reconfigure:**
```bash
cc-sessions --reconfigure  # Start fresh with new settings
```

### Manual Configuration

Edit `sessions/sessions-config.json` directly for fine control (see [config.md](config.md))

## Common Issues

### Trigger Phrases Not Working

**Problem:** You say "go ahead" but nothing happens

**Solutions:**

1. **Check exact spelling:**
   ```bash
   cat sessions/sessions-config.json | grep trigger_phrases
   ```

2. **Add your natural phrase:**
   ```
   /add-trigger "yeah"
   /add-trigger "do it"
   ```

3. **Re-run installer:**
   ```bash
   cc-sessions --reconfigure
   # Choose new trigger phrases when prompted
   ```

4. **Manual override:**
   ```
   daic  # Forces mode switch
   ```

### Branch Enforcement Errors

**Problem:** `[Branch Mismatch]` blocking your edits

**Solutions:**

1. **Quick disable via installer:**
   ```bash
   cc-sessions --reconfigure
   # Choose 'n' when asked about branch enforcement
   ```

2. **Manual disable:**
   Edit `sessions/sessions-config.json`:
   ```json
   "branch_enforcement": {
     "enabled": false
   }
   ```

3. **Fix the branch:**
   ```bash
   cat .claude/state/current_task.json  # See required branch
   git checkout feature/correct-branch  # Switch to it
   ```

### Context Window Issues

**Problem:** Hitting token limits repeatedly

**When you see:** `[75% WARNING]` or `[90% WARNING]`

**Solutions:**

1. **Compact current work:**
   ```
   You: Let's compact
   Claude: [Saves everything to task file]
   You: /clear
   You: Continue
   ```

2. **Enable API mode to save tokens:**
   ```bash
   cc-sessions --reconfigure
   # Choose 'y' for API mode
   ```

3. **Check what's eating tokens:**
   - Huge files in context?
   - Too many tools calls?
   - Massive conversation history?

### Installation Problems

**Problem:** Hooks not working after install

**Check:**

1. **Hooks installed?**
   ```bash
   ls .claude/hooks/
   ```

2. **Python available?**
   ```bash
   python3 --version
   pip list | grep tiktoken
   ```

3. **Reinstall with force:**
   ```bash
   pipx uninstall cc-sessions
   pipx install cc-sessions --force
   cc-sessions  # Run installer again
   ```

### Subagent Failures

**Problem:** Agents return without doing anything

**Common causes:**
- API rate limits
- Token limits in agent context
- File not found errors

**Fix:**
1. Wait a minute (rate limits)
2. Simplify the request
3. Run the agent task manually

### State File Corruption

**Problem:** Weird errors about JSON parsing

**Fix:**
```bash
# Reset state files
rm .claude/state/*.json
echo '{}' > .claude/state/current_task.json
echo '{"mode": "discussion"}' > .claude/state/daic-mode.json

# Re-run installer to reset properly
cc-sessions --reset-state
```

## Platform-Specific Issues

### Windows

**Problem:** "python3 not found"

**Fix:** Windows uses `python` not `python3`:
```bash
python --version  # Should work
```

**Problem:** Permissions errors

**Fix:** Run terminal as Administrator or use WSL

### macOS

**Problem:** "pip: command not found"

**Fix:**
```bash
python3 -m ensurepip
python3 -m pip install --upgrade pip
```

### Linux/WSL

**Problem:** Hook permissions

**Fix:**
```bash
chmod +x .claude/hooks/*.py
```

## When Nothing Works

### Nuclear Reset

**Complete removal and fresh start:**

```bash
# Uninstall
pipx uninstall cc-sessions

# Remove all files (preserves your work in sessions/tasks/)
rm -rf .claude/hooks
rm -rf .claude/state
rm -f sessions/sessions-config.json

# Reinstall fresh
pipx install cc-sessions
cc-sessions  # Run installer with fresh config
```

### Safe Uninstaller

**Use the built-in uninstaller (Booplex fork feature):**

```bash
cc-sessions-uninstall
# or
python -m cc_sessions.uninstall
```

This safely removes cc-sessions while preserving your tasks and work.

### Manual Mode

**Work without cc-sessions:**
1. Uninstall cc-sessions
2. Add to your CLAUDE.md:
   ```
   ALWAYS discuss changes before implementing
   NEVER edit without explicit approval
   ```
3. Good luck with that

### Debug Mode

**See what's actually happening:**

1. **Add logging to hooks:**
   Edit `.claude/hooks/sessions-enforce.py`:
   ```python
   import logging
   logging.basicConfig(filename='/tmp/cc-sessions.log', level=logging.DEBUG)
   logging.debug(f"Tool: {tool_name}, Mode: {discussion_mode}")
   ```

2. **Check the logs:**
   ```bash
   tail -f /tmp/cc-sessions.log
   ```

## Getting Help

### Before asking for help:

1. **Check your version:**
   ```bash
   pip show cc-sessions | grep Version
   ```

2. **Collect diagnostic info:**
   ```bash
   python3 --version
   git --version
   ls -la .claude/hooks/
   cat sessions/sessions-config.json
   cc-sessions --version  # If supported
   ```

3. **Document the issue:**
   - What you typed
   - What you expected
   - What actually happened
   - Any error messages

### Where to get help:

- **This Fork's Issues:** https://github.com/gabelul/cc-sessions/issues
- **Original Repo:** https://github.com/GWUDCAP/cc-sessions/issues
- **Quick questions:** Open an issue with "Question:" prefix

---

*Remember: The installer (`cc-sessions`) can fix most config issues. Try `cc-sessions --reconfigure` before the nuclear option.*