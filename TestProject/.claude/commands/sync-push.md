---
allowed-tools: Bash(python3:*), Bash(echo:*)
argument-hint: ""
description: Push configured files to Memory Bank MCP and mark as synced
---

!`python3 -c "
import json,sys,os,datetime
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

pending_files=[f for f in sync_files if f.get('status')=='pending']
if not pending_files:
    print('All files are already synced')
    sys.exit(0)

print(f'Found {len(pending_files)} files to sync with Memory Bank MCP:')
for f in pending_files:
    print(f'  {f[\"path\"]}')

print('\\nNote: Actual Memory Bank MCP sync requires mcp__memory_bank__write_file tools.')
print('Files have been marked as ready for sync. Use Memory Bank MCP tools in Claude to complete the sync.')

# Mark files as ready for sync
for f in sync_files:
    if f.get('status') == 'pending':
        f['status'] = 'ready_to_sync'

json.dump(data,open(config_file,'w'),indent=2)
print('\\nFiles marked as ready for Memory Bank sync.')
" || echo "Failed to prepare files for Memory Bank sync."`