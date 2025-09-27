# CC-Sessions

```
███████╗███████╗███████╗███████╗██╗ ██████╗ ███╗   ██╗███████╗
██╔════╝██╔════╝██╔════╝██╔════╝██║██╔═══██╗████╗  ██║██╔════╝
███████╗█████╗  ███████╗███████╗██║██║   ██║██╔██╗ ██║███████╗
╚════██║██╔══╝  ╚════██║╚════██║██║██║   ██║██║╚██╗██║╚════██║
███████║███████╗███████║███████║██║╚██████╔╝██║ ╚████║███████║
╚══════╝╚══════╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
```

<sub>_Fork maintained by [Booplex](https://booplex.com) | Originally by GWUDCAP and Three AIrrows Capital_</sub>

**What it is:** Makes Claude ask permission before touching your code. Because apparently "add a button" means "refactor the entire codebase" in AI language.

## The Problem

You: *"Add error handling to this function"*
Claude: *adds error handling to every function, changes your logging format, refactors your types, questions your architectural choices*

Sound familiar?

## The Solution

With cc-sessions, Claude has to explain what it wants to do first. You approve. Then it does JUST that.

```
You: "Add a login button"
Claude: "I'll add a button component to the header with click handler..."
You: "Sounds good, go ahead"
Claude: *Actually just adds the button*
```

No more surprise refactors. No more "I was just trying to add validation and now my entire auth system is different."

## Quick Start (2 minutes)

1. **Install:** `pipx install cc-sessions`
2. **Use Claude normally** - It can now only read/analyze your code
3. **When ready:** Say "go ahead" or "make it so"
4. **Claude edits** ONLY what you discussed
5. **Emergency stop:** Say "STOP" if it's getting weird

## How It Works

- **🔒 Discussion Mode**: Claude can only read/analyze (safe)
- **✏️ Implementation Mode**: Claude can edit (after your approval)
- **🔄 Automatic**: Switches based on what you say

## Commands You'll Actually Use

- `daic` - Toggle between discussion/implementation modes
- `/add-trigger "your phrase"` - Add your own approval phrases
- Look for `[DAIC: Discussion Mode]` to know Claude is locked

## Installation Options

```bash
# Recommended (isolated install)
pipx install cc-sessions

# Via npm
npm install -g cc-sessions

# Direct pip
pip install cc-sessions
```

## Booplex Fork Enhancements

This fork includes improvements focused on making cc-sessions more practical:

- **Safe Uninstaller** - Clean removal while preserving your work
- **Enhanced cross-platform support** - Windows, Mac, Linux, WSL tested
- **Better error handling** - Real fixes for common issues

## Need More Details?

**[📖 Full Documentation →](docs/)**

- [Your first 10 minutes](docs/quickstart.md) - What's actually happening
- [Common scenarios](docs/examples.md) - Real problems, real solutions
- [All commands & config](docs/) - Everything you can do

---

*Having issues? Type "STOP" to lock Claude down, then check [troubleshooting](docs/troubleshooting.md).*

<br>
<sub>Building tools that actually solve problems (and get found by the right people).</sub>