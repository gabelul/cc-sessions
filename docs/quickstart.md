# Your First 10 Minutes with CC-Sessions

**TL;DR: You installed cc-sessions. Now Claude can't edit files without permission. That's literally it.**

## What Just Happened to Claude?

Before cc-sessions: Claude reads your request, immediately starts editing files
After cc-sessions: Claude reads your request, analyzes code, explains what it wants to do, then waits for you to say "go ahead"

## Minute 1: Understanding the Lock

Try this right now:

1. Type something like "fix the auth bug" or "add a search bar"
2. Watch Claude read files and analyze your code
3. Notice it's **NOT editing anything yet**
4. Claude will explain what it wants to do instead

You should see something like:
```
[DAIC: Discussion Mode] I can see the auth issue. I need to...
```

## Minute 3: Your First Approval

Claude just explained its plan. You like it?

**Say one of these:**
- "go ahead"
- "make it so"
- "do it"
- "sounds good"
- "yep"

Claude will respond with:
```
[DAIC: Implementation Mode Activated] I'll implement the discussed changes...
```

Now Claude can edit files. It will do ONLY what you just agreed to.

## Minute 5: The Safety Net

Claude starts doing too much? Getting carried away?

**Type "STOP" (all caps)**

Boom. Claude is locked again. No more editing until you approve the next plan.

## Minute 7: Adding Your Phrases

Hate saying "make it so" like you're Captain Picard?

**Add your own approval phrases:**
```
/add-trigger "yeah"
/add-trigger "do it"
/add-trigger "go for it"
```

Now Claude will respond to whatever feels natural to you.

## Minute 10: You Get It

The workflow is:
1. **Claude discusses** → explains what it wants to do
2. **You approve** → say "go ahead" (or your custom phrase)
3. **Claude implements** → edits ONLY what was discussed
4. **Repeat** → back to discussion mode for next change

## What Changed?

**Before cc-sessions:**
- You: "Add a button"
- Claude: *adds button, refactors entire component, changes your styling system, questions your life choices*

**With cc-sessions:**
- You: "Add a button"
- Claude: "I'll add a button component to the header with onClick handler..."
- You: "go ahead"
- Claude: *Actually just adds the button*

## Common First Questions

**"Claude won't edit my files"**
You're in discussion mode. That's the point. Say "go ahead" after Claude explains what it wants to do.

**"How do I know what mode I'm in?"**
Look for these messages:
- `[DAIC: Discussion Mode]` = Claude is locked
- `[DAIC: Implementation Mode Activated]` = Claude can edit

**"This feels weird"**
Yeah, it does at first. You're used to Claude just doing whatever it wants. Give it a few interactions. The control is actually nice.

**"Can I turn this off?"**
You can run `daic` to manually toggle modes, but honestly? Try it for a day. You'll appreciate not having surprise refactors.

## Next Steps

- **[Real scenarios you'll hit](examples.md)** - Common situations and how to handle them
- **[All commands](commands.md)** - Everything you can do beyond the basics
- **[Configuration](config.md)** - Make it work your way

---

*Still confused? That's normal. Try one more interaction and it'll click.*