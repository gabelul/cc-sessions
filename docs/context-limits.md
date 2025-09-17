# Context Limit Configuration

## Understanding the 80% Rule

The statusline shows **80% of your model's theoretical context limit** as the usable context. This is because Claude Code automatically triggers context compaction when you reach 75-90% of the theoretical limit.

**Why do we do this?**
- Prevents surprise compaction when you think you have space left
- Shows realistic, actually-usable context
- Aligns with Claude Code's internal behavior

## Default Context Limits

| Model | Theoretical Limit | Displayed (80%) | Notes |
|-------|------------------|-----------------|-------|
| Opus 4/4.1 | 200K tokens | 160K tokens | Standard for all Opus models |
| Sonnet 4 | 200K tokens | 160K tokens | Default without 1M beta |
| Sonnet 4 (1M beta) | 1M tokens | 800K tokens | Requires configuration |
| Sonnet 3.5/3.7 | 200K tokens | 160K tokens | Standard context |
| Haiku 3.5 | 200K tokens | 160K tokens | Standard context |

## Configuration Options

### For Sonnet 4 Users with 1M Beta Access

If you have access to Sonnet 4's 1M context window (beta), enable it:

```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export CLAUDE_SONNET4_1M=true
```

### Custom Context Override

For special cases or future models:

```bash
# Set a custom limit (in tokens)
export CLAUDE_CONTEXT_LIMIT=500000  # Custom 500K limit
```

### Debug Mode

To see what model Claude Code reports:

```bash
export DEBUG_STATUSLINE=true
# Check logs at ~/.claude-statusline-debug.log
```

## Troubleshooting

**Q: Why does my progress bar show 160K when docs say 200K?**
A: The 160K is 80% of 200K - the usable amount before auto-compaction.

**Q: I have Sonnet 4 but only see 160K**
A: Sonnet 4 defaults to 200K context. The 1M context is beta and must be explicitly enabled with `CLAUDE_SONNET4_1M=true`.

**Q: How do I know if I have 1M beta access?**
A: Check your Claude Code settings or API configuration. If you've enabled the 1M context window beta feature, set the environment variable.

**Q: Can I see what model name Claude Code reports?**
A: Yes! Enable debug mode with `DEBUG_STATUSLINE=true` and check `~/.claude-statusline-debug.log`.

## Technical Details

### Auto-Compaction Behavior

Claude Code automatically compacts context when usage approaches the theoretical limit:
- First warning at ~75%
- Auto-compaction typically triggers at 75-90%
- The 80% rule provides a safety buffer

### Model Detection Logic

The statusline script checks the model display name:
1. If contains "Sonnet 4" or "sonnet-4" AND `CLAUDE_SONNET4_1M=true` → 800K (80% of 1M)
2. Otherwise → 160K (80% of 200K)

### Environment Variables

- `CLAUDE_SONNET4_1M`: Set to "true" or "1" to enable 1M context for Sonnet 4
- `CLAUDE_CONTEXT_LIMIT`: Override with custom token limit (use carefully)
- `DEBUG_STATUSLINE`: Set to "true" to enable debug logging

## Examples

### Basic Usage (Most Users)
No configuration needed. All models show 160K usable context.

### Sonnet 4 with 1M Beta
```bash
# In your shell profile
export CLAUDE_SONNET4_1M=true
# Restart shell or source profile, then use Claude Code
```

### Debugging Model Detection
```bash
export DEBUG_STATUSLINE=true
# Use Claude Code, then check:
cat ~/.claude-statusline-debug.log
```

### Custom Limit Override
```bash
# For special cases (rarely needed)
export CLAUDE_CONTEXT_LIMIT=320000  # 320K custom limit
```