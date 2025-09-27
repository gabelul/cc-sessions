# Real Situations You'll Hit

**Quick fixes for the stuff that actually happens when using cc-sessions.**

## "Claude won't edit my files"

**What's happening:** You're in discussion mode (which is the default safe state)

**The fix:** Claude should have explained what it wants to do. If you like the plan, say:
- "go ahead"
- "make it so"
- "do it"
- "sounds good"

**If Claude didn't explain anything:** Ask it to. "What do you want to change?" Then approve if you like it.

## "I want Claude to stop immediately"

**The fix:** Type `STOP` (all caps)

Claude locks down instantly. No more editing until you approve the next plan.

Works even if Claude is in the middle of implementing something.

## "Make it so" is dumb and I hate saying it

**The fix:** Add your own approval phrases

```bash
/add-trigger "yeah"
/add-trigger "do it"
/add-trigger "go for it"
/add-trigger "sounds good"
```

Now Claude responds to whatever feels natural to you.

## "I said 'go ahead' but Claude is still locked"

**Check these:**

1. **Did you say it exactly?** "Go ahead" vs "go ahead" - case doesn't matter but spelling does
2. **Did Claude actually propose something?** If Claude just analyzed without proposing changes, there's nothing to approve
3. **Are you in a subagent?** Some specialized operations run in separate contexts

**Quick fix:** Type `daic` to manually switch modes

## "Claude keeps asking for approval for tiny things"

**What's happening:** You're getting lots of small implementation steps instead of bigger chunks

**The fix:**
- Ask Claude to "plan out all the changes first"
- Approve bigger chunks: "implement all the auth changes you mentioned"
- Use phrases like "go ahead with everything we discussed"

## "I'm stuck in implementation mode"

**How to tell:** Claude is editing files without asking

**The fix:** Type `daic` to toggle back to discussion mode

**Why it happens:** Sometimes the mode doesn't auto-switch back after Claude finishes

## "Claude forgot what we were doing"

**What's happening:** This isn't a cc-sessions issue - Claude hit token limits

**The fix:**
- Check for context warnings: `[75% WARNING]` or `[90% WARNING]`
- If you see them, time to wrap up the current task
- Use the task completion protocol to preserve your work

## "Branch enforcement is annoying"

**What's happening:** CC-sessions won't let you edit files because you're on the wrong git branch

**The fix:**
```bash
# Check what branch you should be on
cat .claude/state/current_task.json

# Switch to the right branch
git checkout feature/your-task-name
```

**To disable:** Edit `sessions/sessions-config.json` and set `"branch_enforcement": {"enabled": false}`

## "The error messages are confusing"

**Common ones:**

- `[DAIC: Tool Blocked]` = You're in discussion mode, say "go ahead" to approve
- `[Branch Mismatch]` = Wrong git branch, switch to the right one
- `[Service Not in Task]` = You're editing a file not listed in your current task

**General rule:** If you're blocked, either approve the plan or type `STOP` and start over

## "I just want Claude to work normally"

**The nuclear option:**

1. Remove cc-sessions: `pipx uninstall cc-sessions`
2. But honestly? Try it for a day first

The control is actually nice once you get used to it. No more "I asked for a button and got a complete rewrite."

## "Something is broken and I don't know what"

**Emergency reset:**

1. Type `STOP`
2. Type `daic` (toggles mode manually)
3. Check what mode you're in - look for `[DAIC: Discussion Mode]` messages
4. Start with a simple request to test

**Still broken?** Check [troubleshooting.md](troubleshooting.md)

## "This is too much work"

**Hot take:** If asking for approval feels like work, maybe the changes were bigger than you thought?

CC-sessions just makes visible what Claude was always doing - it forces you both to be explicit about the scope.

**But seriously:** Once you get the rhythm, it's faster than dealing with surprise refactors.

---

*Have a scenario not covered here? That's what [troubleshooting.md](troubleshooting.md) is for.*