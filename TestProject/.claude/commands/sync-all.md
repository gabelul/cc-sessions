---
allowed-tools: mcp__memory_bank__write_file, Bash(python3:*)
argument-hint: ""
description: Sync all configured files to Memory Bank MCP regardless of current status
---

I'll sync all configured files to Memory Bank MCP.

First, let me check what files are configured for sync:

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

print(f'Found {len(sync_files)} files to sync:')
for f in sync_files:
    status = f.get('status', 'pending')
    print(f'  {f[\"path\"]} ({status})')
    
    # Check if file exists
    file_path = os.path.join(project_dir, f['path'])
    if not os.path.exists(file_path):
        print(f'    WARNING: File {f[\"path\"]} not found on disk')

print('\\nReady to sync all files to Memory Bank MCP...')
"`

Now I'll sync each file to Memory Bank MCP. For each file, I'll:
1. Read the file contents from disk
2. Use Memory Bank MCP to write the file 
3. Update the configuration with sync status

Let me process each file:

!`python3 -c "
import json,sys,os,datetime
project_dir=os.environ.get('CLAUDE_PROJECT_DIR','.')
config_file=os.path.join(project_dir,'sessions','sessions-config.json')

# Load config
data=json.load(open(config_file))
sync_files=data['memory_bank_mcp']['sync_files']

# Get project name for Memory Bank
project_name = os.path.basename(project_dir)

for i, file_info in enumerate(sync_files):
    file_path = file_info['path'] 
    full_path = os.path.join(project_dir, file_path)
    
    if os.path.exists(full_path):
        print(f'Processing: {file_path}')
        # File will be synced via Memory Bank MCP tools in the next step
        
        # Update status to indicate sync in progress
        sync_files[i]['status'] = 'syncing'
        sync_files[i]['last_synced'] = datetime.datetime.now().isoformat()[:10]
    else:
        print(f'SKIP: {file_path} (file not found)')
        sync_files[i]['status'] = 'error'

# Save updated config
json.dump(data,open(config_file,'w'),indent=2)
print('\\nConfiguration updated. Files marked for Memory Bank MCP sync.')
"`

The files are now ready for Memory Bank MCP sync. I'll need to use the Memory Bank MCP tools to actually upload each file. The configuration has been updated to track the sync progress.