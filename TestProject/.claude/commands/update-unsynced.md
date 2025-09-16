---
allowed-tools: mcp__memory_bank__write_file, Bash(python3:*)
argument-hint: ""
description: Sync only files that are not already in Memory Bank MCP (not marked as in_memory)
---

I'll sync only the files that aren't already in Memory Bank MCP.

First, let me identify which files need syncing:

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
    print('Error: Memory Bank MCP is not enabled')
    sys.exit(1)

sync_files=memory_bank_config.get('sync_files',[])
if not sync_files:
    print('No files configured for sync')
    sys.exit(0)

# Find files that are NOT already in memory
unsynced_files=[f for f in sync_files if f.get('status') != 'in_memory']
already_synced=[f for f in sync_files if f.get('status') == 'in_memory']

print(f'Total files configured: {len(sync_files)}')
print(f'Already synced to Memory Bank: {len(already_synced)}')
print(f'Need to sync: {len(unsynced_files)}')

if already_synced:
    print('\\nAlready in Memory Bank:')
    for f in already_synced:
        last_synced = f.get('last_synced', 'unknown')
        print(f'  {f[\"path\"]} (synced: {last_synced})')

if unsynced_files:
    print('\\nFiles to sync:')
    for f in unsynced_files:
        status = f.get('status', 'pending')
        print(f'  {f[\"path\"]} ({status})')
        
        # Check if file exists
        file_path = os.path.join(project_dir, f['path'])
        if not os.path.exists(file_path):
            print(f'    WARNING: File {f[\"path\"]} not found on disk')
else:
    print('\\nAll files are already synced to Memory Bank!')
    sys.exit(0)

print('\\nReady to sync unsynced files to Memory Bank MCP...')
"`

Now I'll sync only the unsynced files to Memory Bank MCP:

!`python3 -c "
import json,sys,os,datetime
project_dir=os.environ.get('CLAUDE_PROJECT_DIR','.')
config_file=os.path.join(project_dir,'sessions','sessions-config.json')

# Load config
data=json.load(open(config_file))
sync_files=data['memory_bank_mcp']['sync_files']

# Get project name for Memory Bank
project_name = os.path.basename(project_dir)

# Process only unsynced files
unsynced_count = 0
for i, file_info in enumerate(sync_files):
    if file_info.get('status') == 'in_memory':
        continue  # Skip already synced files
        
    file_path = file_info['path'] 
    full_path = os.path.join(project_dir, file_path)
    
    if os.path.exists(full_path):
        print(f'Processing: {file_path}')
        # File will be synced via Memory Bank MCP tools in the next step
        
        # Update status to indicate sync in progress
        sync_files[i]['status'] = 'syncing'
        sync_files[i]['last_synced'] = datetime.datetime.now().isoformat()[:10]
        unsynced_count += 1
    else:
        print(f'SKIP: {file_path} (file not found)')
        sync_files[i]['status'] = 'error'

# Save updated config
json.dump(data,open(config_file,'w'),indent=2)
print(f'\\nProcessed {unsynced_count} unsynced files. Configuration updated.')
print('Files marked for Memory Bank MCP sync.')
"`

The unsynced files are now ready for Memory Bank MCP sync. I'll need to use the Memory Bank MCP tools to actually upload each file that wasn't already in memory. The configuration has been updated to track which files are being synced.