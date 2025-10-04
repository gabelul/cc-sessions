# Collective Integration Implementation Roadmap

> **Living Document**: Updated after each commit to track progress across conversation resets.

## 📊 Progress Overview

**Last Updated**: 2025-10-04
**Current Status**: Not Started
**Commits Completed**: 0/10
**Project Type**: Integration (adapting agents from claude-code-sub-agent-collective)

---

## 🎯 Now / Next / Later

### 🔥 NOW (Current Focus)
- **Commit 1**: Planning Documentation Cleanup

### ⏭️ NEXT (Up Coming)
- **Commit 2**: Research Agent Adaptation (Phase 1)
- **Commit 3**: DAIC Hook Updates for Research Agent
- **Commit 4**: Research Agent Testing & Documentation

### 📅 LATER (Remaining Work)
- **Phase 2** (Commits 5-7): Feature specialist + routing
- **Phase 3 Preview** (Commit 8): Validation gates foundation
- **Wrap-up** (Commits 9-10): Documentation + version bump

---

## 📋 Detailed Commit Plan

### ⏳ Commit 1: Planning Documentation Cleanup
**Status**: ⏳ Todo
**Priority**: Critical
**Estimated Effort**: 30 min

**Objectives**:
- Ensure all planning docs are accurate and implementation-ready
- Verify all critical fixes from FIXES_REQUIRED.md are applied
- Validate JSON.parse() patterns throughout planning docs
- Create necessary directory structure

**Key Files**:
- dev-docs/collective-integration/adaptation-guide.md - Verify correctness
- dev-docs/collective-integration/agent-inventory.md - Verify agent naming
- dev-docs/collective-integration/FIXES_REQUIRED.md - Confirm all complete
- sessions/research/ - Create directory

**Acceptance Criteria**:
- [ ] All planning docs use correct JSON.parse() pattern
- [ ] All agent names follow cc-sessions convention (no @ prefixes)
- [ ] shared_state.py documentation is clear and complete
- [ ] sessions/research/ directory exists
- [ ] No TaskMaster references in adapted code examples

**Risks**: None (verification only)
**Blockers**: None

**Completion Notes**: _[Add notes after completing]_

---

### ⏳ Commit 2: Research Agent Adaptation (Phase 1 Start)
**Status**: ⏳ Todo
**Priority**: Critical
**Estimated Effort**: 60 min

**Objectives**:
- Adapt research-gathering agent from collective to cc-sessions
- Establish adaptation pattern for future agents
- Remove TaskMaster dependencies → Context7 MCP
- Add Memory Bank + Context7 complementary documentation

**Key Files**:
- cc_sessions/agents/research-gathering.md - Create adapted agent
- cc_sessions/knowledge/research-integration.md - Document integration

**Acceptance Criteria**:
- [ ] Agent file created in correct location
- [ ] NO TaskMaster MCP calls present
- [ ] Uses JSON.parse(Read('.claude/state/current_task.json'))
- [ ] Context7 integration with WebSearch fallback
- [ ] Caches to sessions/research/
- [ ] Documentation explains Memory Bank vs Context7 complementary roles

**Risks**: Context7 MCP may not be configured
**Blockers**: Depends on Commit 1 (directory structure ready)

**Completion Notes**: _[Add notes after completing]_

---

### ⏳ Commit 3: DAIC Hook Updates for Research Agent
**Status**: ⏳ Todo
**Priority**: Critical
**Estimated Effort**: 45 min

**Objectives**:
- Wire research agent into discussion mode workflow
- Update DAIC enforcement to allow research in discussion mode
- Keep implementation agents blocked in discussion mode
- Document hook changes

**Key Files**:
- cc_sessions/hooks/sessions-enforce.py - Modify to allow research agent
- cc_sessions/knowledge/hooks-reference.md - Update documentation

**Acceptance Criteria**:
- [ ] research-gathering allowed in discussion mode only
- [ ] Implementation agents still blocked in discussion mode
- [ ] Hook correctly detects agent type
- [ ] Documentation updated with new logic
- [ ] No breaking changes to existing DAIC enforcement

**Risks**: Hook logic complexity
**Blockers**: Depends on Commit 2 (research agent exists)

**Completion Notes**: _[Add notes after completing]_

---

### ⏳ Commit 4: Research Agent Testing & Documentation
**Status**: ⏳ Todo
**Priority**: High
**Estimated Effort**: 45 min

**Objectives**:
- Test research agent end-to-end
- Validate Context7 integration and fallback
- Test Memory Bank complementary use
- Document usage patterns

**Key Files**:
- sessions/tasks/test-research.md - Create test task
- cc_sessions/knowledge/research-usage-guide.md - Usage documentation
- dev-docs/collective-integration/phase-1-testing-results.md - Test results

**Acceptance Criteria**:
- [ ] Test task successfully uses research agent
- [ ] Context7 queries work (or fallback functions correctly)
- [ ] Research cached to sessions/research/
- [ ] Memory Bank files loaded alongside research
- [ ] Usage documentation complete and clear

**Risks**: Context7 unavailability (should fallback gracefully)
**Blockers**: Depends on Commit 3 (hooks updated)

**Completion Notes**: _[Add notes after completing]_

---

### ⏳ Commit 5: Feature Implementation Agent Adaptation (Phase 2 Start)
**Status**: ⏳ Todo
**Priority**: Critical
**Estimated Effort**: 60 min

**Objectives**:
- Adapt feature-implementation specialist (backend only)
- Add DAIC mode checkpoint (MANDATORY FIRST STEP)
- Preserve TDD workflow exactly
- Enforce specialist boundaries (no UI work)

**Key Files**:
- cc_sessions/agents/feature-implementation.md - Create specialist agent

**Acceptance Criteria**:
- [ ] Agent file created with correct structure
- [ ] DAIC mode checkpoint at very beginning
- [ ] NO TaskMaster dependencies
- [ ] Uses JSON.parse() for all state file reads
- [ ] TDD workflow preserved (RED-GREEN-REFACTOR)
- [ ] Specialist boundaries documented (backend only, no UI)
- [ ] Refuses to proceed if mode != "implementation"

**Risks**: TDD enforcement integration with cc-sessions workflow
**Blockers**: Depends on Commit 4 (Phase 1 complete)

**Completion Notes**: _[Add notes after completing]_

---

### ⏳ Commit 6: Human-Confirmed Routing Implementation
**Status**: ⏳ Todo
**Priority**: Critical
**Estimated Effort**: 90 min

**Objectives**:
- Implement routing logic with user confirmation
- Analyze task type (UI vs backend vs infrastructure)
- Create confirmation prompts
- Always offer fallback to general implementation

**Key Files**:
- cc_sessions/hooks/user-messages.py - Add routing logic
- cc_sessions/knowledge/routing-logic.md - Document routing

**Acceptance Criteria**:
- [ ] Hook detects "go ahead" and other trigger phrases
- [ ] Claude analyzes task type correctly
- [ ] Claude ASKS user: "Use specialist or general?"
- [ ] User choice determines routing path
- [ ] Fallback to general implementation always available
- [ ] Routing logic fully documented

**Risks**: Task type misclassification, routing complexity
**Blockers**: Depends on Commit 5 (at least one specialist working)

**Completion Notes**: _[Add notes after completing]_

---

### ⏳ Commit 7: Feature Implementation Agent Testing
**Status**: ⏳ Todo
**Priority**: High
**Estimated Effort**: 45 min

**Objectives**:
- Test feature-implementation specialist end-to-end
- Validate DAIC mode checkpoint
- Test human-confirmed routing
- Verify TDD workflow enforcement

**Key Files**:
- sessions/tasks/test-feature-specialist.md - Create test task
- dev-docs/collective-integration/phase-2-testing-results.md - Test results

**Acceptance Criteria**:
- [ ] Test task completed using specialist
- [ ] Routing confirmation works as expected
- [ ] DAIC checkpoint prevents discussion-mode usage
- [ ] TDD workflow enforced (tests written first)
- [ ] Specialist boundaries respected (rejects UI work)
- [ ] Test results documented

**Risks**: Integration issues between routing and specialist
**Blockers**: Depends on Commit 6 (routing implemented)

**Completion Notes**: _[Add notes after completing]_

---

### ⏳ Commit 8: Validation Gates Foundation (Phase 3 Preview)
**Status**: ⏳ Todo
**Priority**: Medium
**Estimated Effort**: 45 min

**Objectives**:
- Prepare for validation gate integration
- Create stub agents (structure only)
- Document validation architecture
- Plan integration with task completion

**Key Files**:
- cc_sessions/agents/tdd-validation.md - Create stub
- cc_sessions/agents/quality-gate.md - Create stub
- cc_sessions/agents/completion-validation.md - Create stub
- cc_sessions/knowledge/validation-gates.md - Architecture docs

**Acceptance Criteria**:
- [ ] Directory structure ready
- [ ] Stub agents documented (structure only, no implementation)
- [ ] Integration plan documented clearly
- [ ] No breaking changes to current workflow

**Risks**: None (stubs only)
**Blockers**: Should wait for Phase 2 complete (Commit 7)

**Completion Notes**: _[Add notes after completing]_

---

### ⏳ Commit 9: Integration Summary & Next Steps
**Status**: ⏳ Todo
**Priority**: Medium
**Estimated Effort**: 45 min

**Objectives**:
- Document integration progress (Phases 1-2 complete)
- Plan remaining phases (3-5)
- Create timeline for future work
- Update CLAUDE.md with integration info

**Key Files**:
- dev-docs/collective-integration/INTEGRATION_STATUS.md - Status report
- dev-docs/collective-integration/REMAINING_PHASES.md - Future work plan
- CLAUDE.md - Update with integration notes

**Acceptance Criteria**:
- [ ] Status report complete and accurate
- [ ] Remaining phases documented (3-5)
- [ ] Realistic timeline created
- [ ] CLAUDE.md updated with integration summary
- [ ] Handoff documentation ready for Phase 3

**Risks**: None (documentation only)
**Blockers**: Should wait until Commits 1-8 complete

**Completion Notes**: _[Add notes after completing]_

---

### ⏳ Commit 10: Version Bump & Release Preparation
**Status**: ⏳ Todo
**Priority**: Medium
**Estimated Effort**: 30 min

**Objectives**:
- Prepare release with Phase 1-2 agents integrated
- Bump version (minor - new features)
- Update CHANGELOG
- Test installation

**Key Files**:
- pyproject.toml - Version bump
- package.json - Version bump (keep synchronized)
- CHANGELOG.md - Update with integration features
- dev-docs/collective-integration/RELEASE_NOTES.md - Release notes

**Acceptance Criteria**:
- [ ] Version bumped (minor version for new features)
- [ ] Both pyproject.toml and package.json synchronized
- [ ] CHANGELOG updated with all changes
- [ ] Installation tested: `pipx install -e . --force`
- [ ] All agents load correctly
- [ ] Release notes complete

**Risks**: Version synchronization issues
**Blockers**: Depends on all previous commits complete

**Completion Notes**: _[Add notes after completing]_

---

## 🚧 Known Blockers & Risks

**Active Blockers**: None

**Risks to Monitor**:
- Context7 MCP configuration (may need setup for research agent)
- Task type classification accuracy (routing logic)
- Specialist boundary edge cases (overlapping responsibilities)
- Integration with existing cc-sessions features (no regressions)

---

## 📝 Session Notes

### Session 1: 2025-10-04 (Planning Complete)
- Generated implementation playbook with `/plan dev-docs/collective-integration`
- Detected: Integration project (adapting from claude-code-sub-agent-collective)
- Created 10-commit implementation plan (Phases 1-2 + stubs)
- Next: Begin Commit 1 (planning doc cleanup)

---

## 🔄 Update Instructions for Future Sessions

**When resuming in a new session:**
1. Read this file to understand current progress
2. Check which commits are ✅ Done, 🚧 In Progress, ⏳ Todo
3. Continue from the first incomplete commit

**After completing each commit:**
1. Update commit status: ⏳ Todo → ✅ Done
2. Check all acceptance criteria boxes [x]
3. Add completion notes (what was done, issues found, decisions made)
4. Update "Progress Overview" section (commits completed count)
5. Update "Now / Next / Later" section
6. Add entry to "Session Notes"
7. Git commit this ROADMAP.md file

**Status Indicators**:
- ⏳ Todo - Not started
- 🚧 In Progress - Currently working
- ✅ Done - Completed and committed
- ⚠️ Blocked - Waiting on dependency
- ❌ Skipped - Decided not to implement

---

## 📊 Integration Summary

**Total Agents to Adapt** (Phase 1-2): 2 agents
- ✅ Phase 1: research-gathering (discussion mode)
- ✅ Phase 2: feature-implementation (implementation mode, TDD enforced)

**Future Phases** (Commits 8+):
- Phase 3: Validation gates (3 agents)
- Phase 4: Remaining specialists (4 agents)
- Phase 5: Polish and enhancements

**Key Adaptations**:
- Remove TaskMaster MCP → File-based tasks (.claude/state/current_task.json)
- Add DAIC mode enforcement → Mode checkpoints in every agent
- Add boundary enforcement → Specialists refuse out-of-scope work
- Add human confirmation → Routing logic asks user to choose

**Quality Gates**:
- Read adapted agents to verify patterns
- Check directory structure correctness
- Search for TaskMaster violations (should be none)
- Validate JSON.parse() usage
- Test DAIC mode enforcement
- Test specialist boundaries
