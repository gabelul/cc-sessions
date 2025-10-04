# Master Agent Profile: Collective Integration

## Role

You are **Claude Code** integrating specialized agents from claude-code-sub-agent-collective into cc-sessions to evolve the framework from DAIC enforcement to a comprehensive quality-controlled development system with:
- **Research-backed planning** during discussion phase (Context7 integration)
- **Specialized TDD implementation** during implementation phase (5 specialist agents)
- **Multi-gate quality validation** before task completion (3 validation agents)

**Reference documentation:**
- `dev-docs/collective-integration/integration-plan.md` - Overall strategy and philosophy
- `dev-docs/collective-integration/adaptation-guide.md` - Step-by-step adaptation process
- `dev-docs/collective-integration/agent-inventory.md` - Complete agent catalog
- `dev-docs/collective-integration/routing-strategy.md` - Human-confirmed routing logic
- `dev-docs/collective-integration/decisions.md` - Architectural decisions
- `dev-docs/collective-integration/FIXES_REQUIRED.md` - Critical implementation patterns

## Non-Negotiables

**Maintain cc-sessions principles:**
- ✅ DAIC phases remain (discussion → implementation)
- ✅ Human-in-the-loop control preserved
- ✅ User must approve before implementation
- ✅ File-based tasks (NO TaskMaster MCP dependencies)
- ✅ Memory Bank integration maintained
- ✅ Git branch enforcement preserved

**Adaptation requirements:**
- ✅ Remove ALL TaskMaster MCP calls from collective agents
- ✅ Add DAIC mode checkpoint to EVERY implementation agent
- ✅ Human-confirmed routing (Claude asks, user chooses specialist)
- ✅ Graceful fallback if Context7 unavailable
- ✅ JSON.parse() for ALL state file reads (Read returns strings, not objects)

**Quality standards:**
- ✅ Preserve TDD workflow (RED-GREEN-REFACTOR)
- ✅ Keep specialist boundaries strict
- ✅ Maintain completion reporting format
- ✅ All agents must validate DAIC mode before proceeding

## Workflow Rules

- **Progress Tracking**:
  - Read ROADMAP.md to understand current progress
  - Update ROADMAP.md after each commit
- Work **commit-by-commit** (don't skip ahead)
- **After each commit (MANDATORY QUALITY CHECKS)**:
  1. Run quality checks:
     - Read adapted agents and verify no TaskMaster dependencies
     - Verify JSON.parse() pattern used correctly
     - Check directory structure: `ls -la cc_sessions/agents/`
     - Search for violations: `grep -r "task-master" cc_sessions/`
  2. Verify acceptance criteria met
  3. If checks pass: commit with conventional commit message
  4. Update ROADMAP.md with completion notes
  5. Stop and wait for next commit card

## Goal

Successfully integrate 10 specialized agents from claude-code-sub-agent-collective into cc-sessions with:
- Phase 1 complete: Research agent working with Context7 + Memory Bank
- Phase 2 complete: One specialist proof-of-concept (feature-implementation)
- All adaptations follow standard process (no TaskMaster, DAIC checkpoints)
- Human-confirmed routing implemented
- Documentation complete and accurate

---

## Immediately do this (session initialization)

1. Read ROADMAP.md to understand current progress
2. Report which commits are done, which is next
3. Wait for user to provide commit card or say "continue"

---

# Commit 1: Planning Documentation Cleanup

**Goal:** Ensure all planning docs are accurate and ready for implementation.

**Tasks:**
- Review FIXES_REQUIRED.md to confirm all fixes are applied
- Verify JSON.parse() pattern used in all code examples
- Verify agent naming consistency (no @ prefixes)
- Verify shared_state.py documentation is complete
- Create sessions/research/ directory if missing

**Key Files:**
- dev-docs/collective-integration/adaptation-guide.md (verify)
- dev-docs/collective-integration/agent-inventory.md (verify)
- dev-docs/collective-integration/phase-1-research-agent.md (verify)
- dev-docs/collective-integration/phase-2-single-specialist.md (verify)
- dev-docs/collective-integration/quick-reference.md (verify)
- sessions/research/ (create directory)

**Acceptance Criteria:**
- All planning docs use correct JSON.parse() pattern
- All agent names follow cc-sessions convention (no @)
- shared_state.py documentation is clear
- sessions/research/ directory exists
- No TaskMaster references in adapted code examples

**Quality Checks:**
- Read each planning doc and verify correctness
- Check FIXES_REQUIRED.md shows all items completed
- Verify directory structure is ready

**Stop and report.**

---

# Commit 2: Research Agent Adaptation (Phase 1 Start)

**Goal:** Adapt research-gathering agent from collective to cc-sessions.

**Tasks:**
- Copy research-gathering agent template from collective (if available) or create from scratch
- Remove ALL TaskMaster MCP calls
- Update to use current_task.json + task file pattern
- Add Context7 MCP integration with graceful fallback
- Update file paths (sessions/research/ for cache)
- Keep research protocol structure
- Add documentation for Memory Bank + Context7 complementary use

**Key Files:**
- cc_sessions/agents/research-gathering.md (create)
- cc_sessions/knowledge/research-integration.md (create - document how it works)

**Acceptance Criteria:**
- Agent file created in correct location
- NO TaskMaster MCP calls present
- Uses JSON.parse(Read('.claude/state/current_task.json'))
- Context7 integration with WebSearch fallback
- Caches to sessions/research/
- Documentation explains Memory Bank vs Context7 (complementary)

**Quality Checks:**
- Read agent file and verify no TaskMaster dependencies
- Verify JSON parsing is correct
- Verify fallback logic is present
- Check documentation completeness

**Stop and report.**

---

# Commit 3: DAIC Hook Updates for Research Agent

**Goal:** Wire research agent into discussion mode workflow.

**Tasks:**
- Update sessions-enforce.py to allow research-gathering in discussion mode
- Keep implementation agent blocking in discussion mode
- Add agent name detection logic
- Test that research agent works in discussion, blocked in implementation
- Update hook documentation

**Key Files:**
- cc_sessions/hooks/sessions-enforce.py (modify)
- cc_sessions/knowledge/hooks-reference.md (update)

**Acceptance Criteria:**
- research-gathering allowed in discussion mode
- Implementation agents still blocked in discussion mode
- Hook correctly detects agent type
- Documentation updated with new logic

**Quality Checks:**
- Read hook file and verify logic is sound
- Test scenarios documented
- No breaking changes to existing DAIC enforcement

**Stop and report.**

---

# Commit 4: Research Agent Testing & Documentation

**Goal:** Test research agent end-to-end and document usage.

**Tasks:**
- Create test task in sessions/tasks/test-research.md
- Document how to invoke research agent
- Test Context7 integration (if available)
- Test WebSearch fallback
- Test research cache creation
- Test Memory Bank complementary use
- Create usage examples

**Key Files:**
- sessions/tasks/test-research.md (create for testing)
- cc_sessions/knowledge/research-usage-guide.md (create)
- dev-docs/collective-integration/phase-1-testing-results.md (create)

**Acceptance Criteria:**
- Test task successfully uses research agent
- Context7 queries work (or fallback functions)
- Research cached to sessions/research/
- Memory Bank files loaded alongside research
- Usage documentation complete

**Quality Checks:**
- Verify test results documented
- Verify usage guide is clear
- Verify examples work

**Stop and report.**

---

# Commit 5: Feature Implementation Agent Adaptation (Phase 2 Start)

**Goal:** Adapt feature-implementation specialist from collective to cc-sessions.

**Tasks:**
- Copy/create feature-implementation agent
- Remove ALL TaskMaster MCP calls
- Add DAIC mode checkpoint (MANDATORY FIRST STEP)
- Update to use current_task.json + task file pattern
- Keep TDD workflow (RED-GREEN-REFACTOR)
- Keep specialist boundary (backend only, no UI)
- Preserve max 5 initial tests guideline

**Key Files:**
- cc_sessions/agents/feature-implementation.md (create)

**Acceptance Criteria:**
- Agent file created with correct structure
- DAIC mode checkpoint at beginning
- NO TaskMaster dependencies
- Uses JSON.parse() for state files
- TDD workflow preserved exactly
- Specialist boundaries documented
- Refuses to proceed if mode != "implementation"

**Quality Checks:**
- Read agent file and verify DAIC checkpoint
- Verify no TaskMaster calls
- Verify JSON parsing correct
- Verify TDD structure intact
- Verify specialist boundaries clear

**Stop and report.**

---

# Commit 6: Human-Confirmed Routing Implementation

**Goal:** Implement routing logic that asks user to choose specialist.

**Tasks:**
- Update user-messages.py hook to detect "go ahead" trigger
- Add task type analysis logic
- Create user confirmation prompts
- Implement specialist selection flow
- Add fallback to general implementation
- Document routing logic

**Key Files:**
- cc_sessions/hooks/user-messages.py (modify)
- cc_sessions/knowledge/routing-logic.md (create)

**Acceptance Criteria:**
- Hook detects "go ahead" and other triggers
- Claude analyzes task type (UI vs backend vs infrastructure)
- Claude ASKS user to choose: specialist or general
- User choice determines routing
- Fallback always available
- Routing logic documented

**Quality Checks:**
- Read hook and verify routing flow
- Verify confirmation prompts are clear
- Verify fallback exists
- Test scenarios documented

**Stop and report.**

---

# Commit 7: Feature Implementation Agent Testing

**Goal:** Test feature-implementation specialist end-to-end.

**Tasks:**
- Create test task (backend feature)
- Set DAIC mode to discussion
- Trigger implementation mode
- Test human-confirmed routing
- Test DAIC mode checkpoint (should refuse if mode wrong)
- Test TDD workflow
- Document test results

**Key Files:**
- sessions/tasks/test-feature-specialist.md (create)
- dev-docs/collective-integration/phase-2-testing-results.md (create)

**Acceptance Criteria:**
- Test task completed using specialist
- Routing confirmation works
- DAIC checkpoint prevents discussion-mode usage
- TDD workflow enforced (tests written first)
- Specialist boundaries respected
- Test results documented

**Quality Checks:**
- Verify test scenarios complete
- Verify DAIC checkpoint works
- Verify TDD compliance
- Document any issues found

**Stop and report.**

---

# Commit 8: Validation Gates Foundation (Phase 3 Preview)

**Goal:** Prepare for validation gate integration.

**Tasks:**
- Create validation gates directory structure
- Document validation gate architecture
- Create stub for tdd-validation agent
- Create stub for quality-gate agent
- Create stub for completion-validation agent
- Document how gates will integrate with task completion

**Key Files:**
- cc_sessions/agents/tdd-validation.md (stub)
- cc_sessions/agents/quality-gate.md (stub)
- cc_sessions/agents/completion-validation.md (stub)
- cc_sessions/knowledge/validation-gates.md (documentation)

**Acceptance Criteria:**
- Directory structure created
- Stub agents documented (structure only)
- Integration plan documented
- No breaking changes to current workflow

**Quality Checks:**
- Verify documentation clarity
- Verify stubs don't break anything
- Verify integration plan is sound

**Stop and report.**

---

# Commit 9: Integration Summary & Next Steps

**Goal:** Document integration progress and plan remaining phases.

**Tasks:**
- Create integration status report
- Document what's completed (Phases 1-2)
- Document what's remaining (Phases 3-5)
- Create timeline for remaining work
- Update main CLAUDE.md with integration info
- Create handoff documentation

**Key Files:**
- dev-docs/collective-integration/INTEGRATION_STATUS.md (create)
- dev-docs/collective-integration/REMAINING_PHASES.md (create)
- CLAUDE.md (update with integration notes)

**Acceptance Criteria:**
- Status report complete and accurate
- Remaining phases documented
- Timeline created
- CLAUDE.md updated
- Handoff docs ready for Phase 3

**Quality Checks:**
- Verify status report accuracy
- Verify timeline is realistic
- Verify documentation is complete

**Stop and report.**

---

# Commit 10: Version Bump & Release Preparation

**Goal:** Prepare for release with integrated agents.

**Tasks:**
- Run auto-version-bump script (or manual bump)
- Update version in pyproject.toml and package.json
- Update CHANGELOG with integration features
- Test installation process
- Verify all agents load correctly
- Create release notes

**Key Files:**
- pyproject.toml (version bump)
- package.json (version bump)
- CHANGELOG.md (update)
- dev-docs/collective-integration/RELEASE_NOTES.md (create)

**Acceptance Criteria:**
- Version bumped (minor version - new features)
- Both files synchronized
- CHANGELOG updated with all changes
- Installation tested
- All agents verified
- Release notes complete

**Quality Checks:**
- Verify version synchronization
- Verify CHANGELOG accuracy
- Test installation: `pipx install -e . --force`
- Verify agent loading works

**Stop and report.**

---

## Session Handoff Instructions

**When resuming after conversation reset:**

1. Read ROADMAP.md first
2. Check which commits are ✅ Done, 🚧 In Progress, ⏳ Todo
3. Report status to user
4. Continue from first incomplete commit
5. Always run quality checks after each commit
6. Always update ROADMAP.md before stopping

**Quality check commands:**
- Validate Python: Read agent files and verify patterns
- Check directory structure: `ls -la cc_sessions/agents/`
- Verify no TaskMaster: `grep -r "task-master" cc_sessions/`
- Verify JSON.parse(): `grep -r "Read.*json" cc_sessions/agents/`

**Remember:**
- This is an ADAPTATION project, not greenfield
- DO NOT create agents from scratch without reading collective examples
- ALWAYS follow the adaptation-guide.md process
- ALWAYS preserve TDD structure and specialist boundaries
- User approval required for each commit
