# Help - Complete Command Reference

All the slash commands available in cc-sessions, organized by category.

## Core Workflow Commands

### `/status`
**What:** Complete overview of current session state
**Shows:** Current mode, active task, trigger phrases, context usage, Memory Bank status, next steps
**Use when:** You're lost, starting a session, or need to see what's happening

### `/daic`
**What:** Internal mode switching
**Options:**
- `/daic` - Toggle current mode
- `/daic discussion` - Force discussion mode
- `/daic implementation` - Force implementation mode
**Use when:** Need explicit mode control without trigger phrases

### `/tutorial`
**What:** Interactive 3-minute walkthrough of DAIC workflow
**Includes:** Sample task creation, mode switching practice, agent demonstration
**Use when:** First time using cc-sessions or teaching someone else

## Configuration Commands

### `/add-trigger`
**What:** Add custom trigger phrases for implementation mode
**Example:** `/add-trigger "let's do this"`
**Default phrases:** "make it so", "go ahead", "ship it", "run that"
**Use when:** Want personalized workflow triggers

### `/api-mode`
**What:** Toggle between ultrathink mode and API mode
**Ultrathink mode:** Enhanced reasoning for complex problems (default)
**API mode:** Faster responses for simple tasks
**Use when:** Want to optimize for speed vs. depth

## Project Management Commands

### `/build-project`
**What:** Multi-phase project management with numbered steps
**Features:** Step tracking, state preservation, completion percentages
**Use when:** Complex features requiring multiple implementation phases

### `/project`
**What:** Flexible stepped project workflows (alternative to build-project)
**Features:** Manual step planning, git branch integration, progress visualization
**Use when:** Want custom project structure without template constraints

## Memory Bank Integration Commands
*Available when Memory Bank MCP is installed*

### `/sync-file <path>`
**What:** Sync specific file to Memory Bank for persistent storage
**Example:** `/sync-file CLAUDE.md`
**Use when:** Want specific files to persist across sessions

### `/sync-push`
**What:** Push all local changes to Memory Bank
**Use when:** Ending session and want to preserve context

### `/sync-pull`
**What:** Pull latest context from Memory Bank
**Use when:** Starting session and want fresh persistent context

### `/sync-status`
**What:** Show Memory Bank sync status for all tracked files
**Use when:** Want to see what's synced vs. local-only

### `/sync-all`
**What:** Complete Memory Bank synchronization (bidirectional)
**Use when:** Want full context sync before important work

### `/update-unsynced`
**What:** Discover and optionally sync important untracked files
**Use when:** Want to find valuable files not yet in Memory Bank

## Help Commands

### `/help`
**What:** Main help overview with feature discovery path
**Use when:** Need general guidance or starting out

### `/help workflow`
**What:** Deep dive into DAIC methodology
**Use when:** Want to understand the philosophy and best practices

### `/help agents`
**What:** Guide to specialized AI assistants
**Use when:** Need heavy analysis or systematic work

### `/help commands`
**What:** This complete command reference
**Use when:** Looking for specific command details

### `/help memory`
**What:** Memory Bank integration guide
**Use when:** Want persistent context across sessions

### `/help tasks`
**What:** Task management and organization guide
**Use when:** Working on complex multi-step work

### `/help troubleshoot`
**What:** Common issues and solutions
**Use when:** Something's not working as expected

## Command Usage Patterns

### Daily Workflow
1. Start session: Check `/status`
2. Plan work: Discuss in discussion mode
3. Implement: Use trigger phrases
4. Review: Check `/status` again
5. End session: Consider `/sync-push` if using Memory Bank

### Complex Projects
1. Initialize: `/build-project` or `/project`
2. Context: Use context-gathering agent
3. Implement: Work through numbered steps
4. Maintain: Use logging agent for cleanup
5. Document: Use service-documentation agent

### Learning and Discovery
1. Start: `/tutorial` for hands-on experience
2. Explore: `/help` topics as needed
3. Customize: `/add-trigger` for personal workflow
4. Advanced: `/help agents` for specialized capabilities

## Pro Tips

### Command Combinations
- `/status` + `/help troubleshoot` when stuck
- `/sync-status` + `/update-unsynced` for Memory Bank health check
- `/tutorial` + `/help workflow` for complete understanding

### Context Optimization
- Use `/sync-push` before context limits
- Combine agents with `/help agents` guidance
- Check `/status` regularly to monitor context usage

### Productivity Shortcuts
- Create custom trigger phrases with `/add-trigger`
- Use `/build-project` for systematic feature development
- Set up Memory Bank with `/sync-file` for key documents

---

**Remember:** Commands are tools to enhance your workflow, not replace your thinking. Use them to stay organized and productive while maintaining control over the AI collaboration.