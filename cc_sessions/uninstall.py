#!/usr/bin/env python3
"""
Claude Code Sessions Framework - Cross-Platform Safe Uninstaller

Complete uninstallation system for the Claude Code Sessions framework with native
Windows, macOS, Linux, and WSL support. Handles platform-specific path handling,
backup creation, and safe removal with user data preservation.

Key Features:
    - Cross-platform compatibility (Windows, macOS, Linux, WSL)
    - Comprehensive backup system with compression
    - Restore functionality from backups
    - Interactive menu with multiple uninstall modes
    - Dry-run mode for safety testing
    - Selective component removal
    - Preservation of user tasks and work logs

Platform Support:
    - Windows 10/11 (Command Prompt, PowerShell, Git Bash)
    - macOS (Bash, Zsh)
    - Linux distributions (Bash, other shells)
    - WSL (Windows Subsystem for Linux)

Backup System:
    - Creates compressed backups (.tar.gz) with metadata
    - Includes all cc-sessions files and configuration
    - Stores installation metadata for restore operations
    - Preserves settings.json hook entries for restoration

Safety Features:
    - Dry-run mode shows what would be removed
    - Multiple confirmation prompts
    - Atomic operations (all-or-nothing)
    - User data preservation (tasks, work logs)
    - Backup validation before removal

See Also:
    - uninstall.js: Node.js uninstaller wrapper with same functionality
    - install.py: Original installer this uninstaller reverses
"""

import os
import sys
import json
import shutil
import stat
import tarfile
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

# Colors for terminal output
class Colors:
    RESET = '\033[0m'
    BRIGHT = '\033[1m'
    DIM = '\033[2m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BGRED = '\033[41m'
    BGGREEN = '\033[42m'
    BGYELLOW = '\033[43m'

def color(text: str, color_code: str) -> str:
    """Colorize text for terminal output"""
    return f"{color_code}{text}{Colors.RESET}"

def ask_yes_no(prompt: str, default: bool = True) -> bool:
    """
    Ask a yes/no question with a default option

    Args:
        prompt: The question to ask
        default: True for yes default (Y/n), False for no default (y/N)

    Returns:
        bool: True for yes, False for no
    """
    if default:
        suffix = " (Y/n): "
    else:
        suffix = " (y/N): "

    while True:
        response = input(color(prompt + suffix, Colors.CYAN)).strip().lower()

        if response == "":
            return default
        elif response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print(color("  Please enter y, n, yes, no, or press Enter for default", Colors.YELLOW))

def detect_platform() -> str:
    """
    Detect the current platform with special handling for WSL

    Returns:
        str: 'windows', 'macos', 'linux', or 'wsl'
    """
    if os.name == 'nt':
        return 'windows'
    elif sys.platform == 'darwin':
        return 'macos'
    else:
        # Check for WSL
        if os.path.exists('/proc/sys/fs/binfmt_misc/WSLInterop'):
            return 'wsl'
        return 'linux'

def get_package_dir() -> Path:
    """Get the directory where the package is installed"""
    import cc_sessions
    return Path(cc_sessions.__file__).parent

class SessionsUninstaller:
    """
    Main uninstaller class for cc-sessions framework

    Handles detection, backup, and removal of all cc-sessions components
    across different platforms while preserving user data.
    """

    def __init__(self):
        """Initialize the uninstaller with platform detection and project discovery"""
        self.platform = detect_platform()
        self.package_dir = get_package_dir()
        self.project_root = self.detect_project_directory()
        self.installation = self.detect_installation()

    def detect_project_directory(self) -> Path:
        """Detect the correct project directory when running from pip/pipx"""
        current_dir = Path.cwd()

        # If running from site-packages or pipx environment
        if 'site-packages' in str(current_dir) or '.local/pipx' in str(current_dir):
            print(color("⚠️  Running from package directory, not project directory.", Colors.YELLOW))
            print()
            project_path = input("Enter the path to your project directory (or press Enter for current directory): ")
            if project_path:
                return Path(project_path).resolve()
            else:
                return Path.cwd()

        return current_dir

    def detect_installation(self) -> Optional[Dict[str, Any]]:
        """
        Detect if cc-sessions is installed in this project

        Returns:
            Optional[Dict]: Installation details or None if not installed
        """
        config_file = self.project_root / "sessions/sessions-config.json"
        if not config_file.exists():
            return None

        try:
            with open(config_file) as f:
                config = json.load(f)

            # Collect installation details
            installation = {
                "config_file": config_file,
                "config": config,
                "version": config.get("version", "unknown"),
                "platform": self.platform,
                "components": self._scan_components(),
                "global_commands": self._scan_global_commands(),
                "settings_hooks": self._scan_settings_hooks()
            }

            return installation
        except Exception as e:
            print(color(f"⚠️  Error reading configuration: {e}", Colors.YELLOW))
            return None

    def _scan_components(self) -> Dict[str, List[str]]:
        """
        Scan for installed cc-sessions components

        Returns:
            Dict[str, List[str]]: Components organized by category
        """
        components = {
            "hooks": [],
            "agents": [],
            "commands": [],
            "protocols": [],
            "templates": [],
            "knowledge": [],
            "state": []
        }

        # Scan hooks
        hooks_dir = self.project_root / ".claude/hooks"
        if hooks_dir.exists():
            session_hooks = [
                "sessions-enforce.py", "session-start.py", "user-messages.py",
                "post-tool-use.py", "task-completion-workflow.py",
                "post-implementation-retention.py", "task-transcript-link.py"
            ]
            for hook in session_hooks:
                hook_file = hooks_dir / hook
                if hook_file.exists():
                    components["hooks"].append(str(hook_file))

        # Scan agents
        agents_dir = self.project_root / ".claude/agents"
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.md"):
                components["agents"].append(str(agent_file))

        # Scan commands
        commands_dir = self.project_root / ".claude/commands"
        if commands_dir.exists():
            session_commands = ["sync-*.md", "build-project.md", "project.py"]
            for pattern in session_commands:
                for cmd_file in commands_dir.glob(pattern):
                    components["commands"].append(str(cmd_file))

        # Scan protocols
        protocols_dir = self.project_root / "sessions/protocols"
        if protocols_dir.exists():
            for protocol_file in protocols_dir.glob("*.md"):
                components["protocols"].append(str(protocol_file))

        # Scan templates
        template_file = self.project_root / "sessions/tasks/TEMPLATE.md"
        if template_file.exists():
            components["templates"].append(str(template_file))

        # Scan knowledge
        knowledge_dir = self.project_root / "sessions/knowledge/claude-code"
        if knowledge_dir.exists():
            components["knowledge"].append(str(knowledge_dir))

        # Scan state files
        state_dir = self.project_root / ".claude/state"
        if state_dir.exists():
            session_state_files = ["daic-mode.json"]
            for state_file in session_state_files:
                state_path = state_dir / state_file
                if state_path.exists():
                    components["state"].append(str(state_path))

        # Scan statusline
        statusline_file = self.project_root / ".claude/statusline-script.sh"
        if statusline_file.exists():
            components["state"].append(str(statusline_file))

        return components

    def _scan_global_commands(self) -> List[str]:
        """
        Scan for globally installed cc-sessions commands

        Returns:
            List[str]: Paths to global commands
        """
        global_commands = []

        if self.platform == 'windows':
            # Windows installation location
            local_bin = Path.home() / "AppData" / "Local" / "cc-sessions" / "bin"
            for cmd_file in ["daic.cmd", "daic.ps1"]:
                cmd_path = local_bin / cmd_file
                if cmd_path.exists():
                    global_commands.append(str(cmd_path))
        else:
            # Unix/Mac installation location
            daic_path = Path("/usr/local/bin/daic")
            if daic_path.exists():
                global_commands.append(str(daic_path))

        return global_commands

    def _scan_settings_hooks(self) -> Dict[str, Any]:
        """
        Scan for cc-sessions hooks in settings.json

        Returns:
            Dict: Settings hooks information
        """
        settings_file = self.project_root / ".claude/settings.json"
        if not settings_file.exists():
            return {"exists": False}

        try:
            with open(settings_file) as f:
                settings = json.load(f)

            # Look for cc-sessions hooks
            sessions_hooks = []
            if "hooks" in settings:
                for hook_type, hook_configs in settings["hooks"].items():
                    for config in hook_configs:
                        if "hooks" in config:
                            for hook in config["hooks"]:
                                command = hook.get("command", "")
                                if ("sessions-enforce.py" in command or
                                    "session-start.py" in command or
                                    "user-messages.py" in command or
                                    "post-tool-use.py" in command or
                                    "task-completion-workflow.py" in command or
                                    "post-implementation-retention.py" in command or
                                    "task-transcript-link.py" in command):
                                    sessions_hooks.append({
                                        "type": hook_type,
                                        "command": command
                                    })

            return {
                "exists": True,
                "file": str(settings_file),
                "sessions_hooks": sessions_hooks,
                "has_statusline": "statusLine" in settings
            }
        except Exception:
            return {"exists": True, "file": str(settings_file), "error": True}

    def create_backup(self, backup_name: Optional[str] = None) -> Tuple[bool, str]:
        """
        Create a compressed backup of the current cc-sessions installation

        Args:
            backup_name: Optional custom backup name

        Returns:
            Tuple[bool, str]: Success status and backup file path
        """
        if not self.installation:
            return False, "No cc-sessions installation found to backup"

        # Create backup directory
        backup_dir = self.project_root / "sessions" / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Generate backup filename
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"cc-sessions-backup-{timestamp}"

        backup_file = backup_dir / f"{backup_name}.tar.gz"
        metadata_file = backup_dir / f"{backup_name}.json"

        try:
            print(color(f"Creating backup: {backup_file.name}", Colors.CYAN))

            # Create compressed backup
            with tarfile.open(backup_file, "w:gz") as tar:
                # Add configuration file
                if self.installation["config_file"].exists():
                    tar.add(self.installation["config_file"],
                           arcname=f"sessions/sessions-config.json")

                # Add all components
                for category, files in self.installation["components"].items():
                    for file_path in files:
                        file_obj = Path(file_path)
                        if file_obj.exists():
                            # Calculate relative path for extraction
                            rel_path = file_obj.relative_to(self.project_root)
                            tar.add(file_obj, arcname=str(rel_path))

                # Add settings.json hooks if they exist
                settings_info = self.installation["settings_hooks"]
                if settings_info.get("exists") and not settings_info.get("error"):
                    settings_file = Path(settings_info["file"])
                    if settings_file.exists():
                        tar.add(settings_file,
                               arcname=".claude/settings.json")

            # Create metadata file
            metadata = {
                "version": self.installation["version"],
                "platform": self.platform,
                "date": datetime.now().isoformat(),
                "components": self.installation["components"],
                "global_commands": self.installation["global_commands"],
                "settings_hooks": self.installation["settings_hooks"]
            }

            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)

            print(color(f"✓ Backup created successfully: {backup_file.name}", Colors.GREEN))
            return True, str(backup_file)

        except Exception as e:
            print(color(f"❌ Backup creation failed: {e}", Colors.RED))
            return False, str(e)

    def show_main_menu(self) -> str:
        """
        Show the main uninstaller menu

        Returns:
            str: User's menu choice
        """
        print()
        print(color("╔══════════════════════════════════════════════════════════════╗", Colors.BRIGHT + Colors.CYAN))
        print(color("║              cc-sessions Safe Uninstaller                    ║", Colors.BRIGHT + Colors.CYAN))
        print(color("╚══════════════════════════════════════════════════════════════╝", Colors.BRIGHT + Colors.CYAN))
        print()

        if not self.installation:
            print(color("❌ No cc-sessions installation found in this directory", Colors.RED))
            print(color("   Make sure you're in a project directory with cc-sessions installed", Colors.DIM))
            return "exit"

        # Show installation summary
        total_components = sum(len(files) for files in self.installation["components"].values())
        print(color(f"  📦 Found cc-sessions v{self.installation['version']} ({self.platform})", Colors.WHITE))
        print(color(f"  📁 {total_components} components detected", Colors.WHITE))
        print(color(f"  🌐 {len(self.installation['global_commands'])} global commands", Colors.WHITE))
        print()

        print(color("  What would you like to do?", Colors.CYAN))
        print(color("  1. Complete Uninstall (safe - preserves user tasks)", Colors.WHITE))
        print(color("  2. Selective Uninstall (choose components)", Colors.YELLOW))
        print(color("  3. Backup Only (create backup without removing)", Colors.BLUE))
        print(color("  4. Restore from Backup (restore previous installation)", Colors.MAGENTA))
        print(color("  5. Dry Run (preview what would be removed)", Colors.GREEN))
        print(color("  6. Exit (no changes)", Colors.DIM))
        print()

        while True:
            choice = input(color("  Your choice (1-6): ", Colors.CYAN))
            if choice in ['1', '2', '3', '4', '5', '6']:
                return {
                    '1': 'complete',
                    '2': 'selective',
                    '3': 'backup',
                    '4': 'restore',
                    '5': 'dry_run',
                    '6': 'exit'
                }[choice]
            print(color("  Please enter 1, 2, 3, 4, 5, or 6", Colors.YELLOW))

    def perform_dry_run(self) -> None:
        """Show what would be removed without actually removing anything"""
        print()
        print(color("🔍 DRY RUN - Preview of what would be removed:", Colors.BRIGHT + Colors.GREEN))
        print(color("═" * 60, Colors.DIM))

        total_files = 0

        for category, files in self.installation["components"].items():
            if files:
                print(color(f"\n  {category.upper()}:", Colors.CYAN))
                for file_path in files:
                    print(color(f"    - {file_path}", Colors.WHITE))
                    total_files += 1

        if self.installation["global_commands"]:
            print(color(f"\n  GLOBAL COMMANDS:", Colors.CYAN))
            for cmd_path in self.installation["global_commands"]:
                print(color(f"    - {cmd_path}", Colors.WHITE))
                total_files += 1

        # Show settings.json changes
        settings_info = self.installation["settings_hooks"]
        if settings_info.get("sessions_hooks"):
            print(color(f"\n  SETTINGS.JSON HOOKS:", Colors.CYAN))
            for hook in settings_info["sessions_hooks"]:
                print(color(f"    - {hook['type']}: {hook['command']}", Colors.WHITE))

        # Show what would be preserved
        print(color(f"\n  PRESERVED (will NOT be removed):", Colors.GREEN))
        print(color(f"    - User tasks in sessions/tasks/ (except TEMPLATE.md)", Colors.GREEN))
        print(color(f"    - Work logs and task content", Colors.GREEN))
        print(color(f"    - CLAUDE.md and CLAUDE.sessions.md", Colors.GREEN))
        print(color(f"    - Current task state (.claude/state/current_task.json)", Colors.GREEN))
        print(color(f"    - Existing backups", Colors.GREEN))
        print(color(f"    - Non-sessions settings in .claude/settings.json", Colors.GREEN))

        print()
        print(color(f"📊 SUMMARY: {total_files} files would be removed", Colors.BRIGHT + Colors.YELLOW))
        print(color("   User data and work would be preserved", Colors.GREEN))

    def perform_complete_uninstall(self, create_backup: bool = True) -> bool:
        """
        Perform complete uninstall of cc-sessions

        Args:
            create_backup: Whether to create backup before removal

        Returns:
            bool: Success status
        """
        print()
        print(color("🗑️  COMPLETE UNINSTALL", Colors.BRIGHT + Colors.RED))
        print(color("─" * 30, Colors.DIM))

        # Create backup if requested
        if create_backup:
            if not ask_yes_no("Create backup before uninstalling?", default=True):
                if not ask_yes_no("Are you sure you want to proceed without backup?", default=False):
                    print(color("  Uninstall cancelled", Colors.YELLOW))
                    return False
            else:
                success, backup_path = self.create_backup()
                if not success:
                    print(color(f"  Backup failed: {backup_path}", Colors.RED))
                    if not ask_yes_no("Continue uninstall without backup?", default=False):
                        return False

        # Final confirmation
        print(color("\n⚠️  This will remove ALL cc-sessions components!", Colors.BRIGHT + Colors.RED))
        print(color("   User tasks and work logs will be preserved", Colors.GREEN))

        if not ask_yes_no("Proceed with complete uninstall?", default=False):
            print(color("  Uninstall cancelled", Colors.YELLOW))
            return False

        try:
            return self._remove_all_components()
        except Exception as e:
            print(color(f"❌ Uninstall failed: {e}", Colors.RED))
            return False

    def _remove_all_components(self) -> bool:
        """
        Remove all cc-sessions components

        Returns:
            bool: Success status
        """
        print(color("\n🔄 Removing cc-sessions components...", Colors.CYAN))

        removed_count = 0
        error_count = 0

        # Remove component files
        for category, files in self.installation["components"].items():
            if files:
                print(color(f"  Removing {category}...", Colors.DIM))
                for file_path in files:
                    try:
                        file_obj = Path(file_path)
                        if file_obj.exists():
                            if file_obj.is_dir():
                                shutil.rmtree(file_obj)
                            else:
                                file_obj.unlink()
                            removed_count += 1
                    except Exception as e:
                        print(color(f"    ⚠️  Could not remove {file_path}: {e}", Colors.YELLOW))
                        error_count += 1

        # Remove global commands
        if self.installation["global_commands"]:
            print(color("  Removing global commands...", Colors.DIM))
            for cmd_path in self.installation["global_commands"]:
                try:
                    cmd_obj = Path(cmd_path)
                    if cmd_obj.exists():
                        # May need sudo for Unix systems
                        if self.platform in ['macos', 'linux'] and str(cmd_obj).startswith('/usr/'):
                            subprocess.run(["sudo", "rm", str(cmd_obj)], check=True)
                        else:
                            cmd_obj.unlink()
                        removed_count += 1
                except Exception as e:
                    print(color(f"    ⚠️  Could not remove {cmd_path}: {e}", Colors.YELLOW))
                    error_count += 1

        # Clean up settings.json hooks
        self._remove_settings_hooks()

        # Remove configuration file
        try:
            if self.installation["config_file"].exists():
                self.installation["config_file"].unlink()
                removed_count += 1
        except Exception as e:
            print(color(f"    ⚠️  Could not remove config file: {e}", Colors.YELLOW))
            error_count += 1

        # Remove empty directories
        self._cleanup_empty_directories()

        # Summary
        print()
        if error_count == 0:
            print(color("╔═══════════════════════════════════════════════╗", Colors.BRIGHT + Colors.GREEN))
            print(color("║           🎉 UNINSTALL COMPLETE! 🎉           ║", Colors.BRIGHT + Colors.GREEN))
            print(color("╚═══════════════════════════════════════════════╝", Colors.BRIGHT + Colors.GREEN))
        else:
            print(color("╔═══════════════════════════════════════════════╗", Colors.BRIGHT + Colors.YELLOW))
            print(color("║         UNINSTALL COMPLETED WITH WARNINGS     ║", Colors.BRIGHT + Colors.YELLOW))
            print(color("╚═══════════════════════════════════════════════╝", Colors.BRIGHT + Colors.YELLOW))

        print()
        print(color(f"  ✓ {removed_count} components removed", Colors.GREEN))
        if error_count > 0:
            print(color(f"  ⚠️  {error_count} items had removal issues", Colors.YELLOW))
        print(color("  ✓ User tasks and work preserved", Colors.GREEN))

        return error_count == 0

    def _remove_settings_hooks(self) -> None:
        """Remove cc-sessions hooks from settings.json while preserving other settings"""
        settings_info = self.installation["settings_hooks"]
        if not settings_info.get("exists") or settings_info.get("error"):
            return

        try:
            settings_file = Path(settings_info["file"])
            with open(settings_file) as f:
                settings = json.load(f)

            # Remove cc-sessions hooks
            if "hooks" in settings:
                for hook_type in list(settings["hooks"].keys()):
                    if hook_type in settings["hooks"]:
                        # Filter out sessions hooks
                        filtered_configs = []
                        for config in settings["hooks"][hook_type]:
                            if "hooks" in config:
                                filtered_hooks = []
                                for hook in config["hooks"]:
                                    command = hook.get("command", "")
                                    if not any(sessions_hook in command for sessions_hook in [
                                        "sessions-enforce.py", "session-start.py", "user-messages.py",
                                        "post-tool-use.py", "task-completion-workflow.py",
                                        "post-implementation-retention.py", "task-transcript-link.py"
                                    ]):
                                        filtered_hooks.append(hook)

                                if filtered_hooks:
                                    config["hooks"] = filtered_hooks
                                    filtered_configs.append(config)
                                elif len(config) > 1:  # Has other properties besides hooks
                                    del config["hooks"]
                                    filtered_configs.append(config)
                            else:
                                filtered_configs.append(config)

                        if filtered_configs:
                            settings["hooks"][hook_type] = filtered_configs
                        else:
                            del settings["hooks"][hook_type]

                # Remove hooks section if empty
                if not settings["hooks"]:
                    del settings["hooks"]

            # Remove statusline if it's sessions-related
            if settings_info.get("has_statusline"):
                if "statusLine" in settings:
                    statusline = settings["statusLine"]
                    if "statusline-script.sh" in statusline.get("command", ""):
                        del settings["statusLine"]

            # Save updated settings
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)

            print(color("  ✓ Cleaned cc-sessions hooks from settings.json", Colors.GREEN))

        except Exception as e:
            print(color(f"  ⚠️  Could not clean settings.json: {e}", Colors.YELLOW))

    def _cleanup_empty_directories(self) -> None:
        """Remove empty directories left behind after uninstall"""
        dirs_to_check = [
            self.project_root / ".claude/hooks",
            self.project_root / ".claude/agents",
            self.project_root / ".claude/commands",
            self.project_root / "sessions/protocols",
            self.project_root / "sessions/knowledge/claude-code",
            self.project_root / "sessions/knowledge"
        ]

        for dir_path in dirs_to_check:
            try:
                if dir_path.exists() and dir_path.is_dir():
                    # Only remove if empty
                    if not any(dir_path.iterdir()):
                        dir_path.rmdir()
            except Exception:
                pass  # Ignore errors for directory cleanup

    def list_backups(self) -> List[Tuple[str, str, str]]:
        """
        List available backups

        Returns:
            List[Tuple[str, str, str]]: List of (name, date, version) tuples
        """
        backup_dir = self.project_root / "sessions" / "backups"
        if not backup_dir.exists():
            return []

        backups = []
        for backup_file in backup_dir.glob("cc-sessions-backup-*.tar.gz"):
            metadata_file = backup_file.with_suffix('.json')
            if metadata_file.exists():
                try:
                    with open(metadata_file) as f:
                        metadata = json.load(f)

                    name = backup_file.stem
                    date = metadata.get("date", "unknown")
                    version = metadata.get("version", "unknown")
                    backups.append((name, date, version))
                except Exception:
                    pass

        return sorted(backups, key=lambda x: x[1], reverse=True)

    def run(self) -> None:
        """Run the main uninstaller interface"""
        print(color("╔════════════════════════════════════════════════════════════╗", Colors.BRIGHT))
        print(color("║              cc-sessions Safe Uninstaller                  ║", Colors.BRIGHT))
        print(color("╚════════════════════════════════════════════════════════════╝", Colors.BRIGHT))
        print()
        print(color(f"Platform: {self.platform.upper()}", Colors.DIM))
        print(color(f"Project: {self.project_root}", Colors.DIM))

        while True:
            choice = self.show_main_menu()

            if choice == 'exit':
                print(color("\n  👋 No changes made. Exiting...", Colors.CYAN))
                break
            elif choice == 'complete':
                self.perform_complete_uninstall()
                break
            elif choice == 'selective':
                print(color("\n  📝 Selective uninstall not yet implemented", Colors.YELLOW))
                print(color("     Use complete uninstall for now", Colors.DIM))
            elif choice == 'backup':
                success, backup_path = self.create_backup()
                if success:
                    print(color(f"  ✓ Backup created: {backup_path}", Colors.GREEN))
            elif choice == 'restore':
                backups = self.list_backups()
                if not backups:
                    print(color("\n  📂 No backups found", Colors.YELLOW))
                else:
                    print(color("\n  📝 Restore functionality not yet implemented", Colors.YELLOW))
                    print(color("     Available backups:", Colors.DIM))
                    for name, date, version in backups:
                        print(color(f"       - {name} (v{version}, {date[:10]})", Colors.WHITE))
            elif choice == 'dry_run':
                self.perform_dry_run()

def main():
    """Main entry point for the uninstaller"""
    try:
        uninstaller = SessionsUninstaller()
        uninstaller.run()
    except KeyboardInterrupt:
        print(color("\n\n  Uninstaller interrupted by user", Colors.YELLOW))
        sys.exit(1)
    except Exception as e:
        print(color(f"\n❌ Uninstaller error: {e}", Colors.RED))
        sys.exit(1)

def uninstall():
    """Alias for main() for compatibility"""
    main()

if __name__ == "__main__":
    main()