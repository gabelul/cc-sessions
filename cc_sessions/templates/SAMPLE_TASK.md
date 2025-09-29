# Tutorial Sample Task

**Priority**: High
**Task**: tutorial-sample-fix
**Created**: Auto-generated for tutorial
**Branch**: feature/tutorial-sample

## Purpose

This is a sample task created specifically for the cc-sessions tutorial. It demonstrates:
- Task structure and organization
- DAIC workflow enforcement
- Branch management integration
- Context preservation across sessions

**Note**: This task is automatically created and cleaned up by the tutorial system.

## Context

### What We're "Fixing"
Imagine we need to fix a common AI coding problem: Claude going off-rails and implementing before discussing the approach.

### The Scenario
- **Problem**: AI assistants often start coding immediately without alignment
- **Solution**: Implement DAIC workflow to enforce discussion first
- **Goal**: Show how cc-sessions prevents over-implementation

### Technical Background
- **DAIC**: Discussion-Alignment-Implementation-Check methodology
- **Tool Blocking**: Edit/Write tools blocked until trigger phrase used
- **Branch Enforcement**: Ensures code changes happen on correct branch

## Success Criteria

✅ **Primary Goals**:
- Understand DAIC workflow phases
- Experience tool blocking in Discussion mode
- Use trigger phrase to enter Implementation mode
- See how agents work in separate contexts

✅ **Learning Outcomes**:
- Know when to use trigger phrases
- Understand branch enforcement
- Recognize Discussion vs Implementation modes
- Learn basic cc-sessions commands

✅ **Tutorial Completion**:
- Complete all 5 tutorial steps
- Experience real workflow (not simulation)
- Clean up tutorial files
- Ready to start real work

## Implementation Strategy

### Phase 1: Discussion (Tutorial Step 3)
1. **Analyze the "problem"** (AI going off-rails)
2. **Discuss approach** (DAIC workflow enforcement)
3. **Get alignment** on solution strategy
4. **Show tool blocking** in action

### Phase 2: Implementation (Tutorial Step 3 continued)
1. **Use trigger phrase** ("make it so")
2. **Enter Implementation mode** (tools unblocked)
3. **Make sample changes** (demonstrate edit capability)
4. **Show mode switching** back to Discussion

### Phase 3: Agent Demonstration (Tutorial Step 4)
1. **Invoke context-gathering agent** on this task
2. **Show separate agent context** operation
3. **Demonstrate result integration** back to main thread

## Work Log

### Tutorial Session
**Date**: Auto-generated
**Objective**: Complete interactive cc-sessions walkthrough

**What we learned**:
- DAIC workflow prevents AI disasters
- Tool blocking enforces discussion first
- Trigger phrases control implementation timing
- Agents handle heavy operations separately
- Branch enforcement prevents wrong-branch commits

**Next Steps**:
- Start working on real tasks
- Use `/help` to explore all commands
- Set up Memory Bank integration if desired
- Customize trigger phrases with `/add-trigger`

---

## Notes for Tutorial System

### Auto-Creation Logic
```python
# Tutorial creates this task with:
task_name = "tutorial-sample-fix"
branch_name = "feature/tutorial-sample"
priority = "h-"  # High priority prefix
```

### Cleanup Requirements
- Delete this file after tutorial completion
- Remove created git branch if it exists
- Clear tutorial state from `.claude/state/tutorial.json`
- Restore original working branch

### Integration Points
- **Branch Management**: Demonstrates git integration
- **DAIC Enforcement**: Shows real tool blocking
- **Agent System**: Uses actual context-gathering agent
- **Memory Bank**: Integrates if MCP available

This task exists purely for education and is designed to be temporary. It teaches the workflow without affecting real work.

**Remember**: This is a learning exercise. Real tasks will have genuine implementation requirements and permanent outcomes.

*Happy learning! 🚀*