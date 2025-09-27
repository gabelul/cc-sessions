# Agents Guide

**How to use specialized agents to do the heavy lifting without destroying your context window.**

## What Are Agents?

Agents are specialized Claude instances that:
- Run in separate context windows
- Handle specific tasks really well
- Don't pollute your main conversation
- Return structured results

Think of them as expert contractors you bring in for specific jobs.

## Available Agents

### context-gathering

**What it does:** Analyzes your entire codebase to understand patterns, architecture, and conventions

**When to use:**
- Starting a new task
- Need comprehensive understanding
- Want to document existing patterns

**How to use:**
```
Use the context-gathering agent to analyze our authentication system
```

**Returns:**
- Architecture overview
- Key patterns found
- File locations
- Implementation guidelines

### logging

**What it does:** Consolidates and cleans work logs from your session

**When to use:**
- End of session
- Before context compaction
- Task completion

**How to use:**
```
Use the logging agent to update the work log
```

**Returns:**
- Chronological work log
- Cleaned up duplicates
- Organized by timestamp

### code-review

**What it does:** Reviews code changes for quality, security, and patterns

**When to use:**
- After implementing features
- Before commits
- When unsure about approach

**How to use:**
```
Use the code-review agent to review the changes in src/auth/
```

**Returns:**
- Quality assessment
- Security concerns
- Pattern violations
- Improvement suggestions

### context-refinement

**What it does:** Updates task context with discoveries from current session

**When to use:**
- Found new information
- Pattern changes
- Architecture updates

**How to use:**
```
Use the context-refinement agent to update our task context
```

**Returns:**
- Updated context manifest
- New discoveries added
- Obsolete info removed

### service-documentation

**What it does:** Creates/updates CLAUDE.md files for services

**When to use:**
- After service changes
- New service creation
- Documentation updates

**How to use:**
```
Use the service-documentation agent for the api service
```

**Returns:**
- Updated CLAUDE.md
- Service-specific patterns
- Configuration documented

## How Agents Work

### The Flow

```
You: "Use the context-gathering agent"
    ↓
Claude: Launches agent with Task tool
    ↓
Agent: Gets full conversation history
    ↓
Agent: Works in isolated context
    ↓
Agent: Returns results to main thread
    ↓
Claude: Continues with results
```

### Why This Matters

**Without agents:**
```
You: Analyze all authentication files
Claude: [Reads 50 files into YOUR context]
Context: 80% full, everything is slow now
```

**With agents:**
```
You: Use context-gathering agent for auth
Agent: [Reads 50 files in SEPARATE context]
Claude: Here's the summary [adds 500 tokens, not 50,000]
Context: Still fresh and fast
```

## Creating Custom Agents

### Basic Structure

Create `.claude/agents/my-custom-agent.md`:

```markdown
You are a specialized agent for [SPECIFIC PURPOSE].

## Your Role
[What you're expert at]

## Your Task
1. [First thing to do]
2. [Second thing to do]
3. [Return structured results]

## Input Context
- Full conversation history available
- Current task in .claude/state/current_task.json
- Your previous work in .claude/state/my-custom-agent/

## Expected Output
Provide results in this format:
- **Summary**: Brief overview
- **Findings**: Detailed discoveries
- **Recommendations**: Next steps
- **Files Modified**: What you changed
```

### Advanced Agent

```markdown
You are the database-migration agent.

## Capabilities
- Analyze schema changes
- Generate migration scripts
- Verify data integrity
- Plan rollback strategies

## Process
1. Read current schema from db/schema.sql
2. Read proposed changes from task file
3. Generate migration with up/down methods
4. Create verification queries
5. Document risks and mitigation

## Safety Rules
- NEVER drop columns without backup plan
- ALWAYS include rollback migrations
- TEST migrations on sample data first
- FLAG any data loss risks

## Output Format
```sql
-- Migration: [description]
-- Risk Level: [low/medium/high]
-- Rollback: [possible/complex/impossible]

-- UP Migration
[SQL HERE]

-- DOWN Migration
[SQL HERE]

-- Verification
[QUERIES HERE]
```
```

## Agent Best Practices

### Do's

✅ **Give agents specific, focused tasks**
```
Good: "Use context-gathering agent for the payment module"
Bad: "Use context-gathering agent for everything"
```

✅ **Let agents read many files**
```
They have fresh context - use it
```

✅ **Chain agents for complex work**
```
1. Context-gathering → understand system
2. Implementation → make changes
3. Code-review → verify quality
4. Logging → document work
```

✅ **Trust agent results**
```
They see everything in detail, you see the summary
```

### Don'ts

❌ **Don't call agents in tight loops**
```
Bad: Calling logging agent after every small edit
Good: Call once at session end
```

❌ **Don't pass huge prompts to agents**
```
Bad: 10,000 word instruction essay
Good: "Review auth changes for security issues"
```

❌ **Don't expect agents to maintain state**
```
Each agent call is independent - they don't remember previous runs
```

## Real-World Examples

### Starting a New Feature

```
You: Create a task for adding user notifications

Claude: Creating task file...
        Using context-gathering agent...

Agent: Found existing patterns:
       - Email service at /services/email
       - Queue system using Bull
       - Notification preferences in user_settings table

You: Perfect, let's implement email notifications

Claude: Based on the context, I'll follow your Bull queue pattern...
```

### Debugging Complex Issue

```
You: Something is wrong with our caching

Claude: I'll use context-gathering agent on the cache system

Agent: Cache implementation found:
       - Redis at /lib/cache/redis.js
       - 30 minute TTL default
       - Key pattern: service:entity:id
       - Invalidation in /lib/cache/invalidator.js
       Problem: Invalidation not called in PUT endpoints

You: That's it! Fix the PUT endpoints

Claude: I'll add invalidation calls to all PUT endpoints...
```

### End of Session

```
Claude: [90% context warning shown]

You: Let's wrap up

Claude: I'll use the logging agent to consolidate our work

Agent: Session work log updated:
       - Fixed cache invalidation (3 files)
       - Added tests (2 files)
       - Updated documentation (1 file)

Claude: Ready for context compaction. Run /clear when ready.
```

## Advanced Agent Patterns

### Multi-Agent Workflows

```python
# In your task file, document the workflow:

## Implementation Plan
1. context-gathering → Understand current system
2. Implementation → Make changes
3. code-review → Verify quality
4. service-documentation → Update docs
5. logging → Record work
```

### Agent Specialization

Create agents for your specific needs:
- `security-audit` - Checks for vulnerabilities
- `performance-analyzer` - Finds bottlenecks
- `test-generator` - Creates test cases
- `api-documentor` - Generates OpenAPI specs
- `dependency-updater` - Manages package updates

### Agent Communication

Agents can build on each other's work:

```
context-gathering writes to: context-manifest.md
code-review reads from: context-manifest.md
```

## Troubleshooting Agents

### Agent Returns Nothing

**Causes:**
- API rate limit hit
- Token limit in agent context
- File not found errors

**Fix:**
- Wait and retry
- Simplify the request
- Check file paths exist

### Agent Takes Forever

**Causes:**
- Reading too many files
- Complex analysis requested
- API slowdown

**Fix:**
- Be more specific about scope
- Break into smaller requests
- Check API status

### Agent Results Don't Make Sense

**Causes:**
- Unclear instructions
- Conflicting context
- Agent hallucination

**Fix:**
- Provide clearer task description
- Verify source files exist
- Cross-check results manually

---

*Pro tip: Agents are like contractors - give them clear, specific jobs and let them work in their own space. Your context stays clean, work gets done efficiently.*