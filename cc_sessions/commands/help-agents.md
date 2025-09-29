# Help - Specialized Agents Guide

**Agents** are specialized AI assistants that handle heavy-duty operations in separate context windows. Think of them as your AI team members, each with specific expertise.

## Available Agents

### 🔍 context-gathering
**What it does:** Creates comprehensive task context manifests by analyzing your codebase

**When to use:**
- Starting a new task and need to understand the current state
- Working on unfamiliar code areas
- Need a complete picture before making changes

**Example invocation:**
```
Use the context-gathering agent on tasks/h-add-auth.md
```

**What you get:**
- File analysis and pattern detection
- Architectural insights
- Dependency mapping
- Integration points
- Ready-to-use context manifest

### 📝 logging
**What it does:** Consolidates and cleans up work logs chronologically

**When to use:**
- End of complex tasks to clean up notes
- Context window getting full and need to preserve history
- Want chronological summary of work completed

**Example invocation:**
```
Use the logging agent to consolidate the work log for this task
```

**What you get:**
- Chronologically ordered events
- Cleaned up duplicate entries
- Proper markdown formatting
- Preserved important decisions and outcomes

### 🔎 code-review
**What it does:** Reviews implemented code for quality, security, and patterns

**When to use:**
- After implementing significant features
- Before committing major changes
- When you want a second opinion on code quality
- Security-sensitive implementations

**Example invocation:**
```
Use the code-review agent on src/auth/ - focus on security patterns
```

**What you get:**
- Security vulnerability detection
- Code quality assessment
- Pattern consistency review
- Performance considerations
- Recommendations for improvements

### 🧩 context-refinement
**What it does:** Updates task context with discoveries from your work session

**When to use:**
- Approaching context window limits but task continues
- Made significant discoveries during implementation
- Need to preserve learnings for next session

**Example invocation:**
```
Use the context-refinement agent to update the task context
```

**What you get:**
- Updated context with new discoveries
- Refined understanding of the problem space
- Preserved architectural insights
- Ready for session handoff

### 📚 service-documentation
**What it does:** Maintains CLAUDE.md files for individual services/modules

**When to use:**
- After making changes to service architecture
- Adding new services or major features
- Need to document service-specific patterns

**Example invocation:**
```
Use the service-documentation agent for the auth service
```

**What you get:**
- Updated service CLAUDE.md files
- Consistent documentation format
- Integration guidance
- Behavioral expectations

## Agent Best Practices

### Delegation Strategy
- **Heavy file operations** → Delegate to agents
- **Analysis tasks** → Perfect for agents
- **Maintenance work** → Let agents handle it
- **Creative decisions** → Keep in main conversation

### Prompting Agents
- **Be specific** about the task scope
- **Provide context** if deviating from normal use
- **Trust their expertise** - they have full conversation history
- **Keep prompts focused** - avoid over-explaining

### Integration with DAIC
- **Discussion mode**: Plan which agents to use
- **Implementation mode**: Call agents for heavy lifting
- **Check phase**: Use code-review agent for validation

## Advanced Agent Patterns

### The Context-First Pattern
1. Start task with context-gathering agent
2. Use insights to plan implementation
3. Build feature based on context
4. End with code-review agent

### The Handoff Pattern
1. Work on complex task until context full
2. Use logging agent to consolidate history
3. Use context-refinement to preserve discoveries
4. Restart session with preserved context

### The Quality Assurance Pattern
1. Implement feature in discussion/implementation cycles
2. Use code-review agent for security/quality check
3. Address any findings
4. Use service-documentation agent for final docs

## Agent Troubleshooting

**When to use agents vs. main conversation:**
- **File-heavy analysis** → Agents
- **Quick questions** → Main conversation
- **Creative brainstorming** → Main conversation
- **Systematic review** → Agents

**Agent not giving expected results:**
- Check if you provided the right context (file paths, scope)
- Agents see full conversation history, but specific guidance helps
- Try rephrasing the request with clearer objectives

**Agents vs. Tools:**
- **Agents** operate in separate contexts, return structured results
- **Tools** are direct file/system operations in current context
- **Agents** are better for analysis, tools for direct manipulation

## Memory Bank Integration

When Memory Bank MCP is available, agents gain enhanced capabilities:
- **Persistent knowledge** across sessions
- **Architectural insights** that survive restarts
- **Cross-project learning** from similar codebases

Without Memory Bank, agents still provide full functionality using standard tools.

---

**Remember:** Agents are your AI specialists. Use them for the heavy lifting while you focus on thinking, planning, and decision-making.