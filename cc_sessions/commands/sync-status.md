---
allowed-tools: Bash(python3:*)
argument-hint: ""
description: Show sync status of all configured Memory Bank files
---

!`python3 -c "import json,sys,os; project_dir=os.environ.get('CLAUDE_PROJECT_DIR','.'); config_file=os.path.join(project_dir,'sessions','sessions-config.json'); sys.exit(1) if not os.path.exists(config_file) else None; data=json.load(open(config_file)); sync_files=data.get('memory_bank_mcp',{}).get('sync_files',[]); print('Memory Bank Sync Status:') if sync_files else print('No files configured for Memory Bank sync.'); [print(f'  {f[\"path\"]} - {f[\"status\"]} (last synced: {f.get(\"last_synced\",\"never\")})') for f in sync_files]" || echo "Failed to read sync status. Check that sessions-config.json exists."`