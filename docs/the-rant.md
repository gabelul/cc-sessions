# The Original Rant

_This is the original README that started it all - preserved for its entertainment value and raw honesty about the AI coding experience._

---

```
███████╗███████╗███████╗███████╗██╗ ██████╗ ███╗   ██╗███████╗
██╔════╝██╔════╝██╔════╝██╔════╝██║██╔═══██╗████╗  ██║██╔════╝
███████╗█████╗  ███████╗███████╗██║██║   ██║██╔██╗ ██║███████╗
╚════██║██╔══╝  ╚════██║╚════██║██║██║   ██║██║╚██╗██║╚════██║
███████║███████╗███████║███████║██║╚██████╔╝██║ ╚████║███████║
╚══════╝╚══════╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
```

<sub>_A public good brought to you by GWUDCAP and Three AIrrows Capital_</sub>

---

<br>
<div align="center">

##### ⚡ SHOCKING REPORT REVEALS ⚡

# **Vibe coding is shitty and confusing and produces garbage software that sucks to work on.**<br>

### _Claude Code makes it less shitty, but not by enough._

---
</div>

## 🔥 The Problem

### How you got here

I'm going to guess how you got here and you can tell me if I get it right:

- 💭 The LLM programmer hype gave you a nerd chub
- 😬 The people hyping LLM programming made your nerd chub crawl back into your body <br> <sup>_(are you ready to 'scale your impact', dog?)_</sup>
- 🤮 You held your nose and downloaded Cursor/added Cline or Roo Code/npm installed Claude Code

At first this was obviously novel and interesting. Some things were shitty but mostly you were enjoying not having to write a context manager or even recognize that you needed one for your dumb client wrapper.

**You were _scaling_ your _impact_** _(whew)_.

But then Claude started doing some concerning things.

You asked it to add error handling to **one** function. It added error handling to **_every function in the file_**. And changed your error types. And your logging format. And somehow your indentation is different now?

The context window thing started getting annoying. You're explaining the same architecture for the fifth time today. Claude's like _'let me look for the database'_ **Brother. We've been using Postgres for six hours. You were just in there.**

Your CLAUDE.md is now longer than your actual code.
- `'NEVER use class components.'`
- `'ALWAYS use the existing auth middleware.'`
- `'DO NOT refactor unrelated code.'`
- `'REMEMBER we use PostgreSQL.'`

Claude reads the first line and then macrodoses window pane LSD for the rest.

You tried the subagents, but quickly realized that **you can't even talk to these things.** 10 minutes into a "code review" and the agent hits some kind of API error and returns to your main thread with no explanation of what it did or what it discovered.

Run it again, I guess?

_This fucking sucks_.

Now you're here. Your codebase is 'done' but you couldn't, in a million years, explain what that means or how it satisfies the definition.

There's three different global clients for the same database connection and two of them use hallucinated environment variables (the other just yeets your client secret into the service code).

You've got utility functions that are duplicated in four files because Claude kept forgetting they exist.

20% of your code lines are comments explaining why something *isn't* there and *is* somewhere else.

You don't even know exactly what's wrong and fixing it means understanding code you didn't write in patterns you don't recognize using approaches you wouldn't choose.

### **Are you scaling your impact yet?**

---

_[The rest of the original README continues with the solution sections, but you get the idea. This was the hilarious but confusing part that made people struggle to understand what cc-sessions actually does.]_

---

**Note:** For the actual documentation that explains what cc-sessions does in plain language, see [the main docs](index.md).