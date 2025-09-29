# Help - DAIC Workflow Deep Dive

**DAIC** = Discussion-Alignment-Implementation-Check

## The Problem DAIC Solves

Ever had Claude just... start coding when you wanted to brainstorm? Or had it make assumptions about what you actually wanted? DAIC prevents the classic AI coding pitfalls:

- **Assumption overload** - AI guessing what you meant
- **Surprise implementations** - Code appearing without your explicit approval
- **Context loss** - Forgetting what was discussed when sessions restart
- **Scope creep** - Simple requests becoming complex refactors

## How DAIC Works

### 1. Discussion Mode (🔴 Default)
**What happens:**
- You can ask questions, brainstorm, explain problems
- Claude can read files, search code, analyze patterns
- **No code gets written** (Edit/Write tools are blocked)
- Perfect for: planning, understanding, debugging, exploring

**Example conversation:**
```
You: I need to add user authentication to my app
Claude: Let me examine your current setup... [reads files]
I see you're using Express. For auth, we could use:
1. JWT with bcrypt for local auth
2. OAuth with Passport.js for social login
3. Auth0 for managed service

Which direction fits your needs?
```

### 2. Implementation Mode (🟢 After Trigger)
**What happens:**
- Code editing tools are enabled
- Claude implements what was discussed
- You maintain explicit control over when coding starts

**Trigger phrases** (customizable with `/add-trigger`):
- "make it so"
- "go ahead"
- "ship it"
- "run that"

**Example:**
```
You: Let's go with JWT. Make it so.
Claude: [switches to implementation mode]
I'll implement JWT authentication...
[creates middleware, routes, etc.]
```

### 3. Check Phase (Automatic)
**What happens:**
- Review implemented code
- Test the solution
- Switch back to discussion for iterations

## Advanced DAIC Features

### Internal Mode Switching
- `/daic` - Toggle current mode
- `/daic discussion` - Force discussion mode
- `/daic implementation` - Force implementation mode

### Context Preservation
- Session state survives restarts
- Task context automatically reloaded
- Work logs maintained chronologically

### Branch Enforcement
- Automatically creates git branches for tasks
- Prevents wrong-branch commits
- Maps task types to branch prefixes (implement- → feature/)

## DAIC Best Practices

### For Discussion Mode
- Ask "what if" questions freely
- Request code analysis and explanations
- Explore multiple approaches before deciding
- Use `/status` to see current state

### For Implementation Mode
- Be specific about what to implement
- Review changes before switching back
- Use trigger phrases when you're ready for action
- Remember: you can always go back to discussion

### For Complex Work
- Break large features into smaller tasks
- Use specialized agents for heavy analysis
- Set up Memory Bank for context persistence
- Consider `/build-project` for multi-phase work

## Common DAIC Patterns

### The Planning Session
1. Start with problem description
2. Examine existing code structure
3. Discuss multiple solution approaches
4. Align on specific implementation plan
5. Use trigger phrase to begin coding

### The Debug Hunt
1. Describe the issue you're seeing
2. Let Claude analyze logs, code paths
3. Discuss potential root causes
4. Agree on debugging approach
5. "make it so" to implement fixes

### The Feature Build
1. Define feature requirements
2. Review existing patterns in codebase
3. Plan implementation steps
4. Get explicit approval
5. Use agents for heavy lifting if needed

## Troubleshooting DAIC

**Stuck in discussion mode?**
- Use trigger phrases: "make it so", "go ahead"
- Check `/status` for current state
- Try `/daic implementation` to force switch

**Unexpected implementations?**
- Check your trigger phrases with `/status`
- Add custom phrases with `/add-trigger`
- Remember: hooks enforce the workflow

**Lost context after restart?**
- Task context auto-loads from git branch
- Use Memory Bank for persistent knowledge
- Check `.claude/state/current_task.json`

---

**The goal**: You think and decide, AI implements reliably. DAIC makes this happen consistently.