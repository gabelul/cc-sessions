---
name: plan
description: Generate implementation playbook from planning docs
---

# Playbook Generator Command

You are generating a structured implementation playbook from planning documentation.

## Arguments
- `{{args}}` - Path to planning documentation directory (relative to project root)

---

## Phase 1: Project Context Analysis (MANDATORY FIRST)

Before generating anything, you MUST analyze the target project to understand context:

### 1. Technology Stack Detection

Read these files to detect project type:
- `package.json` → Node.js/TypeScript project
  - Check `scripts` section for: `test`, `lint`, `typecheck`, `build`
  - Check `dependencies` for framework (React, Vue, etc.)
- `requirements.txt` or `pyproject.toml` → Python project
  - Look for test framework: pytest, unittest
  - Look for linting: ruff, flake8, pylint
  - Look for type checking: mypy
- `go.mod` → Go project
  - Default commands: `go test ./...`, `go build ./...`, `golangci-lint run`
- `Cargo.toml` → Rust project
  - Default commands: `cargo test`, `cargo build`, `cargo clippy`
- `README.md` → Check for custom commands, setup instructions

### 2. Existing Project Structure

Check if these exist to determine project type:
- `.claude/agents/` → Existing agent system (likely integration/adaptation project)
- `.claude/commands/` → Existing command structure
- `CLAUDE.md` or `.claude/CLAUDE.md` → Read for project-specific rules/context
- `docs/` or `DevDocs/` → Read for architecture context

### 3. Planning Docs Analysis

Read ALL files in `{{args}}` and detect project intent:

**Integration/Adaptation signals** (DON'T create new agents):
- Keywords: "adapt", "integrate", "migrate", "refactor", "copy from", "wire into"
- Files named: `adaptation-guide.md`, `integration-plan.md`, `migration-*.md`
- References to external repos or existing codebases
- Tasks focused on modifying existing code

**Greenfield signals** (DO create new agents):
- Keywords: "create", "build", "implement new", "add feature"
- No references to existing implementations
- Starting from scratch
- New feature development

### 4. Quality Check Commands

Based on detected stack, determine appropriate commands:

**Node.js/TypeScript:**
```bash
# Check package.json scripts first, fallback to these:
npm test  # or bun run test, pnpm test
npm run lint  # or bun run lint
npm run typecheck  # or tsc --noEmit
npm run build  # if exists
```

**Python:**
```bash
pytest  # or python -m pytest
mypy .  # if type hints used
ruff check .  # or flake8
```

**Go:**
```bash
go test ./...
go build ./...
golangci-lint run
```

**Rust:**
```bash
cargo test
cargo build
cargo clippy
```

---

## Phase 2: Generate Playbook

Now generate based on detected context:

### Load Reference Examples

Read these reference files for structure:
- `.claude/commands/examples/playbook-ref.md` → Playbook structure
- `.claude/commands/examples/roadmap-ref.md` → Roadmap structure

### Generate Files

Create these files in the project root (or in specified output location):

**1. IMPLEMENTATION-PLAYBOOK.md**

Structure:
```markdown
# Master Agent Profile: [Project Name]

## Role
[Describe what Claude will implement based on planning docs]

## Non-Negotiables
[Extract key rules/constraints from planning docs]

## Workflow Rules
- Read ROADMAP.md for progress tracking
- Work commit-by-commit
- After each commit:
  1. [Quality check commands from Phase 1]
  2. Verify acceptance criteria
  3. Update ROADMAP.md
  4. Stop and wait

## Goal
[Success criteria from planning docs]

---

## Commit 1: [Title]
[Break planning docs into 6-12 logical commits]
[Each commit: tasks, files, acceptance criteria, quality checks]
[Stop and report instruction]

## Commit 2: [Title]
...
```

**2. ROADMAP.md**

Structure:
```markdown
# [Project Name] Implementation Roadmap

## Progress Overview
**Last Updated**: [Current date]
**Current Status**: Not Started
**Commits Completed**: 0/[N]

## Now / Next / Later
[Organize commits by priority]

## Detailed Commit Plan
[One section per commit with status ⏳ Todo]

## Session Notes
[Empty - will be filled during implementation]
```

**3. .claude/agents/*.md (ONLY if greenfield project)**

If Phase 1 detected **greenfield project**, generate agent files:
- Extract agent roles from planning docs
- Create one .md file per agent
- Follow .claude/agents/ file format

If Phase 1 detected **integration project**, SKIP agent generation and note in playbook:
```markdown
# Note: Agent Integration
This project adapts existing agents from [source].
Agent files should be copied from source repo, not generated.
See planning docs for adaptation instructions.
```

---

## Phase 3: Project-Type-Specific Adaptations

### For Integration Projects:

Focus playbook on:
- Commit 1: Copy agents from source
- Commit 2: Remove/adapt dependencies
- Commit 3: Wire into existing system
- Commit 4: Test integration
- NO agent file generation

### For Greenfield Projects:

Focus playbook on:
- Commit 1: Foundation (types, configs)
- Commits 2-N: Feature implementation
- Quality gates after each commit
- Generate agent files in .claude/agents/

### For Refactoring Projects:

Focus playbook on:
- Commit 1: Add tests for existing behavior
- Commits 2-N: Incremental refactoring
- Quality gates ensure no regressions
- NO new agent files (use existing)

---

## Output Format

After generating, present to user:

```
✅ Generated Implementation Playbook

Files created:
- IMPLEMENTATION-PLAYBOOK.md (X commits, Y lines)
- ROADMAP.md (tracking structure)
- .claude/agents/*.md (N agents) [only if greenfield]

Detected context:
- Technology: [Node.js/Python/Go/Rust]
- Project type: [Greenfield/Integration/Refactoring]
- Quality checks: [list commands]
- Existing structure: [what was found]

Next steps:
1. Review IMPLEMENTATION-PLAYBOOK.md
2. Adjust if needed
3. Start with: "Begin with Commit 1"
```

---

## Example Invocations

```bash
# User in project root:
/plan dev-docs/collective-integration

# Claude does:
# 1. Detects Node.js project (package.json)
# 2. Reads .claude/agents/ → Existing agents found
# 3. Reads dev-docs/collective-integration/* → "adapt agent" found
# 4. Determines: Integration project
# 5. Generates playbook focused on adaptation (NO agent files)
# 6. Uses detected npm scripts for quality checks
```

```bash
# User in project root:
/plan planning/new-auth-feature

# Claude does:
# 1. Detects Python project (requirements.txt)
# 2. No .claude/agents/ found
# 3. Reads planning/new-auth-feature/* → "implement new" found
# 4. Determines: Greenfield project
# 5. Generates playbook + agent files
# 6. Uses pytest/mypy/ruff for quality checks
```

---

## Error Handling

If planning docs not found:
```
❌ Error: Planning docs not found at {{args}}

Please provide a valid path to planning documentation.
Example: /plan dev-docs/feature-planning
```

If cannot detect project type:
```
⚠️ Warning: Could not detect project type

Defaulting to generic playbook structure.
Please review and adjust quality check commands.
```

---

## Important Notes

- ALWAYS run Phase 1 analysis before generating
- NEVER assume project type without checking
- Quality check commands MUST match detected stack
- Integration projects should NOT generate agent files
- Reference the planning docs extensively in playbook
- Break work into 6-12 logical, sequential commits
- Each commit should take 15-45 minutes to implement
