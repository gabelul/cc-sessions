# Memory MCP Options and Upgrade Path

This document outlines the memory MCP server options for cc-sessions and provides a roadmap for potential upgrades.

## Current Implementation

**Using:** `@alioshr/memory-bank-mcp`
**Status:** Implemented via ddayneko fork integration
**Installation:** `claude mcp add memory-bank npx -y @alioshr/memory-bank-mcp`

### Features:
- ✅ Simple file-based storage
- ✅ Project isolation
- ✅ Basic CRUD operations (read, write, update, list)
- ✅ Proven integration with cc-sessions
- ✅ Minimal dependencies (just Node.js)

### API:
- `mcp__memory_bank__read_file`
- `mcp__memory_bank__write_file`
- `mcp__memory_bank__update_file`
- `mcp__memory_bank__list_projects`
- `mcp__memory_bank__list_files`

## Future Upgrade Options

### Option A: Basic Memory (basicmachines-co)
**Repository:** https://github.com/basicmachines-co/basic-memory
**Documentation:** https://docs.basicmemory.com/integrations/claude-code/
**Best for:** Users who want Obsidian integration and visual knowledge graphs

#### Advantages:
- ✅ **Obsidian integration** - Visual knowledge graph and editing
- ✅ **Markdown format** - Human-readable, editable files
- ✅ **SQLite indexing** - Fast search without heavy database
- ✅ **Import ChatGPT history** - Migrate existing conversations
- ✅ **Active development** - Updated August 2025
- ✅ **Local-first** - Privacy-focused, no cloud dependencies

#### Requirements:
- Python with UV package manager
- Optional: Obsidian for visualization
- ~100MB storage for knowledge base

#### Installation:
```bash
uv tool install basic-memory
# OR
npx -y @Claude's native MCP management/cli install @basicmachines-co/basic-memory --client claude
```

### Option B: WhenMoon Claude Memory MCP
**Repository:** https://github.com/WhenMoon-afk/claude-memory-mcp
**Best for:** Users who want intelligent, automatic memory management

#### Advantages:
- ✅ **Tiered memory** - Short-term, long-term, and archival
- ✅ **Automatic consolidation** - No manual memory management
- ✅ **Semantic search** - Find memories by meaning, not just keywords
- ✅ **Multiple memory types** - Conversations, knowledge, entities, reflections
- ✅ **Importance-based retention** - Automatically prioritizes valuable information
- ✅ **Research-based** - Built on optimal LLM memory techniques

#### Requirements:
- Python environment
- Optional: Docker for easier deployment
- JSON-based storage

#### Installation:
```bash
# Manual
git clone https://github.com/WhenMoon-afk/claude-memory-mcp.git
cd claude-memory-mcp
pip install -r requirements.txt
./setup.sh

# Docker
docker-compose up -d
```

### Option C: ViralV00d00 Claude Code Memory
**Repository:** https://github.com/ViralV00d00/claude-code-memory
**Best for:** Users who need sophisticated relationship tracking and pattern analysis

#### Advantages:
- ✅ **Neo4j graph database** - Complex relationship mapping
- ✅ **Code pattern analysis** - Learns successful development patterns
- ✅ **Relationship tracking** - Understands how concepts connect
- ✅ **Context-aware retrieval** - Project and technology-specific memory
- ✅ **Task execution tracking** - Monitors Claude's activities

#### Requirements:
- Neo4j database
- More complex infrastructure
- Higher resource usage

#### Note:
Most complex option - only consider if you need advanced relationship analysis.

## Migration Strategy

### Phase 1: Current (@alioshr/memory-bank-mcp) ✅
- Simple file storage
- Get memory persistence working immediately
- Learn usage patterns and requirements

### Phase 2: Evaluate Upgrade (Future)
Based on experience with basic memory, consider:

**If you use Obsidian:** → Basic Memory
- Visual knowledge graphs
- Manual editing capabilities
- Integration with existing Obsidian workflows

**If you want automation:** → WhenMoon Memory
- Automatic memory management
- Intelligent consolidation
- Semantic search capabilities

**If you need advanced analysis:** → ViralV00d00
- Complex relationship tracking
- Code pattern analysis
- Research-grade features

### Migration Process

1. **Export existing memories** from current MCP
2. **Install new MCP** alongside current one
3. **Import/migrate data** using conversion scripts
4. **Update cc-sessions configuration** to use new MCP
5. **Test sync commands** with new system
6. **Remove old MCP** after verification

## Implementation Details

### Current Integration Points:
- `cc_sessions/install.py` - Setup and configuration
- `cc_sessions/commands/sync-*.md` - File synchronization commands
- `cc_sessions/hooks/session-start.py` - Auto-load context
- `cc_sessions/agents/context-gathering.md` - Enhanced with memory tools

### API Compatibility:
When upgrading, these functions need to be updated:
- Memory storage/retrieval calls
- File synchronization logic
- Context loading mechanisms
- Search and query interfaces

## Recommendation Timeline

**Month 1-2:** Use current @alioshr/memory-bank-mcp implementation
**Month 3:** Evaluate actual usage patterns and needs
**Month 4+:** Consider upgrade based on findings:
- Heavy Obsidian user → Basic Memory
- Want set-and-forget → WhenMoon Memory
- Need advanced analysis → ViralV00d00

## Notes

- All options support the Model Context Protocol (MCP)
- Migration between options is possible but requires adaptation
- Start simple, upgrade based on real needs rather than theoretical benefits
- Consider maintenance overhead when choosing complex options

---

**Last Updated:** September 2025
**Current Choice:** @alioshr/memory-bank-mcp (Phase 1 implementation)
**Next Review:** After 1-2 months of usage