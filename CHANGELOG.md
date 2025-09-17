# Changelog

All notable changes to this fork are documented here. Spoiler: we fixed a lot of stuff.

## [0.2.13] - 2025-09-17

### The Great Unfuckening by [gabel](https://github.com/gabelul) (with inspiration from [ddayneko](https://github.com/ddayneko)'s fork)

#### 🎯 Smart Installer System (Because Overwriting Configs Is Rude)
- **Installation Detection**: Finally checks if you already have cc-sessions installed (mindblowing, right?)
- **Update/Fresh/Repair Menu**: Like a real installer! With options! That work!
- **Configuration Preservation**: Your trigger phrases and settings survive updates (revolutionary technology)
- **Hook Deduplication**: No more duplicate hooks breeding in your settings.json

#### 🧠 [Memory Bank MCP](https://github.com/alioshr/memory-bank-mcp) Integration (Claude Gets a Brain)
- **Auto-installation**: No more "Enter your Smithery API key" nonsense
- **The Legendary `echo "" |` Hack**: Bypasses interactive prompts like a ninja
- **Actually Works**: Unlike the previous "optional" installation that wasn't optional

#### 📦 Automatic Version Management (For Goldfish Developers)
- **[auto-version-bump.py](scripts/auto-version-bump.py)**: Bumps versions when you inevitably forget
- **Task Completion Reminders**: "Hey dummy, you changed cc-sessions, bump the version"
- **Synchronized Versions**: pyproject.toml and package.json stay in sync (magic!)

#### 🪝 Enhanced Hook System (Inspired by [ddayneko's galaxy brain ideas](https://github.com/ddayneko/cc-sessions/tree/main/.claude/hooks))
- **[post-implementation-retention.py](cc_sessions/hooks/post-implementation-retention.py)**: Claude remembers what it just did (breakthrough!)
- **[document-versioning.py](cc_sessions/hooks/document-versioning.py)**: Your docs get version numbers (fancy!)
- **Git CLI Integration**: Because GitHub MCP is overkill for `git status`

#### 📝 Document Templates (Stolen Fair and Square from [ddayneko](https://github.com/ddayneko/cc-sessions))
- **[PRD_TEMPLATE.md](cc_sessions/templates/PRD_TEMPLATE.md)**: For when you need to pretend you planned this
- **[FSD_TEMPLATE.md](cc_sessions/templates/FSD_TEMPLATE.md)**: Makes your chaos look organized
- **[EPIC_TEMPLATE.md](cc_sessions/templates/EPIC_TEMPLATE.md)**: Because everything is an epic these days

### Fixed (The Bugs That Made Us Cry)
- **Colors.END AttributeError**: Python installer line 191-192 - `Colors.END` doesn't exist, who knew? Changed to `Colors.RESET` like a normal person
- **Hook Duplication Bug**: Settings.json was collecting hooks like Pokemon cards
- **document-governance.py Ghost Reference**: Removed references to a file that never existed (spooky)
- **The Config Destroyer**: Installer was overwriting existing configs like a barbarian

### Technical Shit You Probably Don't Care About (But We're Proud Of)

#### How We Detect Existing Installations
```python
# Revolutionary technology
if os.path.exists("sessions/sessions-config.json"):
    print("OMG you already have cc-sessions!")
```

#### The Smithery Bypass Hack
```bash
# This works and we're not sorry
echo "" | npx -y @smithery/cli install @alioshr/memory-bank-mcp --client claude
```

#### Hook Deduplication (Because Sets Are Cool)
```python
existing_commands = set()  # No duplicates allowed in this house
```

### Props To
- **[gabel](https://github.com/gabelul)** - Made it work, lost some sanity at [booplex.com](https://booplex.com)
- **[ddayneko](https://github.com/ddayneko)** - [Had the ideas](https://github.com/ddayneko/cc-sessions) that made us go "oh shit, that's smart"
- **[GWUDCAP](https://github.com/GWUDCAP)** - [Started this madness](https://github.com/GWUDCAP/cc-sessions)

### Links for the Curious
- [This Fork](https://github.com/gabelul/cc-sessions) - You are here
- [ddayneko's Fork](https://github.com/ddayneko/cc-sessions) - Where good ideas come from
- [Original Repo](https://github.com/GWUDCAP/cc-sessions) - Where it all began
- [Memory Bank MCP](https://github.com/alioshr/memory-bank-mcp) - Claude's new brain
- [booplex.com](https://booplex.com) - Where we build stuff with AI assistance