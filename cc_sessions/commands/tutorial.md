# Tutorial Command

**Description**: Interactive cc-sessions workflow tutorial - learn DAIC in 3 minutes

## Overview

The tutorial provides a hands-on introduction to cc-sessions that actually teaches you something useful. No boring theory, just practical workflow demonstration that prevents Claude from going off-rails.

## Tutorial Flow

### 1. Welcome & Introduction (30 seconds)
- Brief explanation of what cc-sessions does
- DAIC workflow overview (Discussion-Alignment-Implementation-Check)
- Why this prevents AI disasters

### 2. Sample Task Creation (45 seconds)
- Create tutorial task: "tutorial-sample-fix"
- Show task structure and context
- Demonstrate branch enforcement

### 3. DAIC Workflow Experience (90 seconds)
- Start in Discussion mode (blocked tools)
- Explain approach and get alignment
- Use trigger phrase to enter Implementation mode
- Show how tools become available
- Complete sample implementation

### 4. Agent Demonstration (30 seconds)
- Show context-gathering agent usage
- Demonstrate how agents work in separate contexts
- Show agent results integration

### 5. Cleanup & Next Steps (15 seconds)
- Clean up tutorial files
- Show available commands
- Point to /help for more info

## Implementation

The tutorial is implemented through the Task tool, creating an interactive experience that:
- Uses separate agent context to avoid cluttering main conversation
- Creates temporary files for demonstration
- Tracks progress in `.claude/state/tutorial.json`
- Cleans up after completion
- Can be run multiple times safely

## Usage

Simply run `/tutorial` in any cc-sessions enabled project. The tutorial will:
1. Check if cc-sessions is properly installed
2. Create a safe learning environment
3. Guide you through the complete workflow
4. Clean up when finished

## Tutorial State

Progress is tracked in `.claude/state/tutorial.json`:
```json
{
  "started": "2025-01-29T12:00:00Z",
  "completed": null,
  "current_step": 1,
  "total_steps": 5,
  "sample_task_created": false,
  "cleanup_needed": false
}
```

## Reset Tutorial

If the tutorial gets stuck or needs to be reset:
1. Delete `.claude/state/tutorial.json`
2. Delete `sessions/tasks/tutorial-sample-fix.md` if it exists
3. Run `/tutorial` again

## Requirements

- cc-sessions properly installed
- Git repository (for branch demonstration)
- Claude Code Sessions framework active

## Pro Tips

- The tutorial takes exactly 3 minutes - perfect for coffee break learning
- You can interrupt and resume at any step
- Run it again anytime to refresh your memory
- Share with team members for consistent workflow adoption

## Behind the Scenes

The tutorial demonstrates real cc-sessions features:
- ✅ Actual DAIC enforcement (not simulation)
- ✅ Real branch creation and switching
- ✅ Genuine tool blocking/unblocking
- ✅ Working agent delegation
- ✅ Live Memory Bank integration (if available)

Because learning should use the actual system, not fake demos.