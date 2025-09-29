# Help - Task Management Guide

**Tasks** in cc-sessions are structured work units that maintain context, enforce git workflows, and preserve progress across sessions. Think of them as your project's memory and organization system.

## Task Fundamentals

### What Tasks Provide
- **Structured context** for complex work
- **Git branch automation** and enforcement
- **Progress tracking** across sessions
- **Work log preservation** with chronological history
- **Scope boundaries** to prevent feature creep

### Task File Structure
```markdown
# Task Name

## Purpose
[Clear one-line goal]

## Context
[Current state, what exists, patterns to follow]

## Success Criteria
[Specific, measurable outcomes]

## Work Log
[Chronological progress entries]
```

## Task Types and Naming

### High Priority: `h-feature-name`
**Git branch:** `feature/feature-name`
**Use for:** Critical features, urgent fixes, core functionality
**Example:** `h-user-authentication`, `h-payment-integration`

### Medium Priority: `m-feature-name`
**Git branch:** `feature/feature-name`
**Use for:** Regular features, improvements, enhancements
**Example:** `m-dashboard-redesign`, `m-email-notifications`

### Low Priority: `l-feature-name`
**Git branch:** `feature/feature-name`
**Use for:** Nice-to-have features, cleanup, optimization
**Example:** `l-ui-polish`, `l-performance-tweaks`

### Investigations: `?-topic-name`
**Git branch:** `investigate/topic-name`
**Use for:** Research, debugging, exploration
**Example:** `?-memory-leak`, `?-framework-comparison`

### Fixes: `fix-issue-name`
**Git branch:** `fix/issue-name`
**Use for:** Bug fixes, hotfixes, error resolution
**Example:** `fix-login-timeout`, `fix-mobile-layout`

### Implementation: `implement-feature-name`
**Git branch:** `feature/feature-name`
**Use for:** Implementing designed features
**Example:** `implement-shopping-cart`, `implement-user-profiles`

## Task Lifecycle

### 1. Task Creation
**Manual creation:**
```bash
# Create task file
touch tasks/h-add-authentication.md

# Use template or create custom structure
# Include Purpose, Context, Success Criteria
```

**Guided creation:**
Use the context-gathering agent to analyze requirements and create comprehensive task context.

### 2. Task Startup
When you start working on a task:
- Git branch automatically created/switched
- Task context loaded into session
- Previous work log available
- Branch enforcement activated

### 3. Active Development
**Discussion mode:**
- Plan implementation approach
- Analyze existing code patterns
- Research integration points

**Implementation mode:**
- Write code on correct git branch
- Update work log as you progress
- Use agents for heavy analysis

### 4. Task Completion
- Verify success criteria met
- Consolidate work log (use logging agent)
- Document lessons learned
- Consider follow-up tasks

## Advanced Task Patterns

### The Epic Pattern
For large features spanning multiple sessions:
```
h-user-system/
├── README.md              # Epic overview
├── m-user-model.md        # Individual tasks
├── m-auth-middleware.md
├── m-profile-ui.md
└── l-avatar-upload.md
```

### The Investigation → Implementation Pattern
1. Start with `?-auth-research.md`
2. Research authentication options
3. Create `implement-jwt-auth.md` based on findings
4. Reference investigation in implementation task

### The Incremental Feature Pattern
```
m-dashboard-v1.md          # Basic dashboard
m-dashboard-charts.md      # Add visualizations
l-dashboard-filters.md     # Enhanced filtering
```

## Task Management Commands

### Project Management
- `/build-project` - Multi-phase structured projects
- `/project` - Flexible stepped workflows
- Use for complex features requiring multiple phases

### Context Preservation
- **Memory Bank integration** - Sync important task files
- **Agent delegation** - Use logging agent for work log maintenance
- **Session handoffs** - Task context auto-loads

### Progress Tracking
Check `.claude/state/current_task.json` for active task info:
```json
{
  "task": "h-add-authentication",
  "branch": "feature/add-authentication",
  "services": ["auth", "user"],
  "updated": "2025-01-29"
}
```

## Task Best Practices

### Scope Definition
✅ **Good task scope:**
- Clear, specific purpose
- Measurable success criteria
- Single area of responsibility
- Can be completed in reasonable time

❌ **Poor task scope:**
- Vague or multiple purposes
- Undefined success criteria
- Cross-cutting concerns without boundaries
- Open-ended exploration

### Context Quality
**Rich context includes:**
- Current system state
- Existing patterns to follow
- Integration requirements
- Dependencies and constraints
- Previous investigation results

### Work Log Discipline
- Update after each significant step
- Include both successes and failures
- Document decision rationale
- Note useful patterns discovered
- Track time estimates vs. actual

## Integration with DAIC Workflow

### Discussion Phase
- Review task context and current state
- Plan implementation approach
- Identify unknowns requiring investigation
- Clarify success criteria if needed

### Implementation Phase
- Work within task scope boundaries
- Update work log as you progress
- Stay on designated git branch
- Use agents for systematic analysis

### Check Phase
- Verify success criteria met
- Document any scope changes
- Plan follow-up tasks if needed
- Consider agent-based quality review

## Common Task Patterns

### The Research Task
**Purpose:** Investigate options for authentication framework
**Context:** Express app, need secure user login
**Success criteria:** Recommendation with pros/cons analysis
**Workflow:** Research → Document → Decide → Create implementation task

### The Feature Task
**Purpose:** Implement JWT-based authentication
**Context:** Based on research task findings, Express + bcrypt pattern
**Success criteria:** Login/logout working, tests passing, middleware complete
**Workflow:** Plan → Implement → Test → Document

### The Bug Fix Task
**Purpose:** Fix login timeout issue on mobile
**Context:** Users report 30-second timeouts, desktop works fine
**Success criteria:** Mobile login works reliably under 5 seconds
**Workflow:** Reproduce → Investigate → Fix → Verify

### The Maintenance Task
**Purpose:** Update authentication to latest security standards
**Context:** Current JWT implementation, new OWASP guidelines
**Success criteria:** Security audit passes, no breaking changes
**Workflow:** Audit → Plan → Update → Test

---

**Remember:** Tasks are your project's organizational backbone. Good task management leads to better context preservation, clearer progress tracking, and more successful AI collaboration.