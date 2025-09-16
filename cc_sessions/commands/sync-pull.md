---
allowed-tools: Bash(python3:*)
argument-hint: ""
description: Read synchronized files from Memory Bank MCP for verification
---

!`python3 -c "
import json,sys,os
project_dir=os.environ.get('CLAUDE_PROJECT_DIR','.')
config_file=os.path.join(project_dir,'sessions','sessions-config.json')

if not os.path.exists(config_file):
    print('Error: sessions-config.json not found')
    sys.exit(1)

data=json.load(open(config_file))
memory_bank_config=data.get('memory_bank_mcp',{})

if not memory_bank_config.get('enabled',False):
    print('Memory Bank MCP is not enabled')
    sys.exit(1)

sync_files=memory_bank_config.get('sync_files',[])
if not sync_files:
    print('No files configured for sync')
    sys.exit(0)

synced_files=[f for f in sync_files if f.get('status')=='in_memory']
if not synced_files:
    print('No files are currently synced with Memory Bank')
    sys.exit(0)

print(f'Files available in Memory Bank MCP ({len(synced_files)} total):')
for f in synced_files:
    last_synced=f.get('last_synced','unknown')
    print(f'  {f[\"path\"]} (synced: {last_synced})')

print('\\nUse mcp__memory_bank__read_file tools in Claude to read specific file contents.')
print('Example: mcp__memory_bank__read_file(project_name, \"filename\")')
" || echo "Failed to list Memory Bank files."`