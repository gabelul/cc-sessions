#!/usr/bin/env python3
"""
Claude Code Sessions Framework - Cross-Platform Python Installer

Complete installation system for the Claude Code Sessions framework with native
Windows, macOS, and Linux support. Handles platform-specific path handling,
command installation, and shell compatibility.

Key Features:
    - Windows compatibility with native .cmd and .ps1 script support
    - Cross-platform path handling using pathlib
    - Platform-aware file permission management
    - Interactive configuration with terminal UI
    - Global daic command installation with PATH integration
    
Platform Support:
    - Windows 10/11 (Command Prompt, PowerShell, Git Bash)
    - macOS (Bash, Zsh)
    - Linux distributions (Bash, other shells)

Installation Locations:
    - Windows: %USERPROFILE%\\AppData\\Local\\cc-sessions\\bin
    - Unix/Mac: /usr/local/bin

See Also:
    - install.js: Node.js installer wrapper with same functionality
    - cc_sessions.scripts.daic: Unix bash implementation
    - cc_sessions.scripts.daic.cmd: Windows Command Prompt implementation
    - cc_sessions.scripts.daic.ps1: Windows PowerShell implementation
"""

import os
import sys
import json
import shutil
import stat
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

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
    BGBLUE = '\033[44m'
    BGMAGENTA = '\033[45m'
    BGCYAN = '\033[46m'

def color(text: str, color_code: str) -> str:
    """Colorize text for terminal output"""
    return f"{color_code}{text}{Colors.RESET}"

def command_exists(command: str) -> bool:
    """Check if a command exists in the system"""
    if os.name == 'nt':
        # Windows - try with common extensions
        for ext in ['', '.exe', '.bat', '.cmd']:
            if shutil.which(command + ext):
                return True
        return False
    return shutil.which(command) is not None

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

def interactive_tool_selection(tools, current_blocked):
    """
    Interactive tool selection with arrow keys navigation

    Args:
        tools: List of (name, description, is_blocked) tuples
        current_blocked: List of currently blocked tool names

    Returns:
        List of tool names to block, or None if user cancelled
    """
    try:
        import sys
        import os

        # Check if we're in a compatible terminal
        if not sys.stdin.isatty():
            print(color("  ⚠️ Interactive mode requires a terminal (not available in pipes/scripts)", Colors.YELLOW))
            return None

        # Platform-specific key handling
        if os.name == 'nt':  # Windows
            import msvcrt

            def get_key():
                """Get a key press on Windows"""
                key = msvcrt.getch()
                if key == b'\xe0':  # Arrow key prefix
                    key = msvcrt.getch()
                    if key == b'H':  # Up arrow
                        return 'UP'
                    elif key == b'P':  # Down arrow
                        return 'DOWN'
                return key.decode('utf-8', errors='ignore')
        else:  # Unix-like systems
            try:
                import termios
                import tty
            except ImportError as e:
                print(color(f"  ⚠️ Terminal control not available: {str(e)}", Colors.YELLOW))
                print(color("  Falling back to classic numbered input...", Colors.DIM))
                return None

            def get_key():
                """Get a key press on Unix"""
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setcbreak(fd)
                    key = sys.stdin.read(1)
                    if key == '\x1b':  # ESC sequence
                        key += sys.stdin.read(2)
                        if key == '\x1b[A':  # Up arrow
                            return 'UP'
                        elif key == '\x1b[B':  # Down arrow
                            return 'DOWN'
                    return key
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        # Prepare tool list with selection state
        tool_items = []
        for name, desc, _ in tools:
            is_selected = name in current_blocked
            tool_items.append([name, desc, is_selected])

        current_index = 0

        while True:
            # Clear screen and show header
            os.system('cls' if os.name == 'nt' else 'clear')
            print(color("╭───────────────────────────────────────────────────────────────╮", Colors.CYAN))
            print(color("│              Interactive Tool Selection                       │", Colors.CYAN))
            print(color("├───────────────────────────────────────────────────────────────┤", Colors.CYAN))
            print(color("│   Use ↑↓ to navigate, Space to toggle, Enter to confirm      │", Colors.CYAN))
            print(color("│   [✓] = Will be BLOCKED, [ ] = Will remain ALLOWED           │", Colors.CYAN))
            print(color("╰───────────────────────────────────────────────────────────────╯", Colors.CYAN))
            print()

            # Show tools
            for i, (name, desc, is_selected) in enumerate(tool_items):
                prefix = ">" if i == current_index else " "
                checkbox = "[✓]" if is_selected else "[ ]"
                status_icon = "❌" if is_selected else "✅"
                status_text = "BLOCKED" if is_selected else "ALLOWED"
                status_color = Colors.RED if is_selected else Colors.GREEN

                if i == current_index:
                    print(color(f"{prefix} {checkbox} {status_icon} {name.ljust(15)} - {desc}", Colors.BRIGHT + Colors.WHITE))
                else:
                    print(f"{prefix} {checkbox} {status_icon} {color(name.ljust(15), Colors.WHITE)} - {desc}")
                print(f"     {color(status_text, status_color)}")

            print(color(f"\nPress ESC or Ctrl+C to cancel", Colors.DIM))

            # Get user input
            try:
                key = get_key()
            except KeyboardInterrupt:
                return None

            if key == 'UP' and current_index > 0:
                current_index -= 1
            elif key == 'DOWN' and current_index < len(tool_items) - 1:
                current_index += 1
            elif key == ' ':  # Space to toggle
                tool_items[current_index][2] = not tool_items[current_index][2]
            elif key == '\r' or key == '\n':  # Enter to confirm
                return [name for name, _, selected in tool_items if selected]
            elif key == '\x1b' or key == '\x03':  # ESC or Ctrl+C
                return None

    except ImportError as e:
        print(color(f"  ⚠️ Interactive mode unavailable: {str(e)}", Colors.YELLOW))
        print(color("  Falling back to classic numbered input...", Colors.DIM))
        return None
    except Exception as e:
        print(color(f"  ⚠️ Interactive mode error: {str(e)}", Colors.YELLOW))
        print(color("  Falling back to classic numbered input...", Colors.DIM))
        return None

def get_package_dir() -> Path:
    """Get the directory where the package is installed"""
    import cc_sessions
    # All data files are now inside cc_sessions/
    return Path(cc_sessions.__file__).parent

class SessionsInstaller:
    def __init__(self):
        self.package_dir = get_package_dir()
        self.project_root = self.detect_project_directory()
        self._installed_mcp_servers = None  # Cache for MCP servers list
        self.existing_installation = self.detect_existing_installation()
        self.config = {
            "developer_name": "the developer",
            "trigger_phrases": ["make it so", "run that", "go ahead", "yert"],
            "blocked_tools": ["Edit", "Write", "MultiEdit", "NotebookEdit"],
            "task_detection": {"enabled": True},
            "branch_enforcement": {"enabled": True},
            "document_governance": {
                "enabled": False,
                "auto_context_retention": True,
                "document_validation": True,
                "conflict_detection": True,
                "auto_versioning": True,
                "documents_path": "sessions/documents",
                "version_history_limit": 10,
                "require_user_confirmation": True,
                "prd_file": None,
                "fsd_file": None
            },
            "memory_bank_mcp": {
                "enabled": False,
                "auto_activate": True,
                "memory_bank_root": "",
                "sync_files": []
            }
        }
    
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
                # Default to user's current working directory before pip ran
                return Path.cwd()
        
        return current_dir

    def detect_existing_installation(self) -> Optional[Dict[str, Any]]:
        """Detect if cc-sessions is already installed in this project"""
        config_file = self.project_root / "sessions/sessions-config.json"
        if not config_file.exists():
            return None

        try:
            with open(config_file) as f:
                existing_config = json.load(f)

            # Try to determine installed version from various sources
            installed_version = "unknown"

            # Check if there's a version in the config (future enhancement)
            if "version" in existing_config:
                installed_version = existing_config["version"]

            return {
                "config_file": config_file,
                "config": existing_config,
                "version": installed_version,
                "has_hooks": (self.project_root / ".claude/hooks").exists(),
                "has_agents": (self.project_root / ".claude/agents").exists(),
                "has_commands": (self.project_root / ".claude/commands").exists(),
                "claude_md_exists": (self.project_root / "CLAUDE.md").exists()
            }
        except Exception:
            return None

    def get_current_package_version(self) -> str:
        """Get the current package version from pyproject.toml"""
        try:
            # Try to get version from package metadata
            import cc_sessions
            if hasattr(cc_sessions, '__version__'):
                return cc_sessions.__version__

            # Fallback: read from pyproject.toml in package dir
            pyproject_file = self.package_dir.parent / "pyproject.toml"
            if pyproject_file.exists():
                content = pyproject_file.read_text()
                import re
                version_match = re.search(r'version = "([^"]*)"', content)
                if version_match:
                    return version_match.group(1)
        except Exception:
            pass

        return "0.2.8"  # Current version as fallback

    def show_installation_menu(self) -> str:
        """Show menu for existing installations"""
        current_version = self.get_current_package_version()
        existing_version = self.existing_installation["version"]

        print()
        print(color("╔═══════════════════════════════════════════════╗", Colors.BRIGHT + Colors.CYAN))
        print(color("║          cc-sessions Already Installed        ║", Colors.BRIGHT + Colors.CYAN))
        print(color("╚═══════════════════════════════════════════════╝", Colors.BRIGHT + Colors.CYAN))
        print()

        print(color(f"  Found existing installation: {Colors.BRIGHT}v{existing_version}{Colors.RESET}", Colors.WHITE))
        print(color(f"  Current version available: {Colors.BRIGHT}v{current_version}{Colors.RESET}", Colors.WHITE))
        print()

        if existing_version != current_version:
            print(color("  🆕 Update available!", Colors.GREEN))
        else:
            print(color("  ✅ You have the latest version", Colors.GREEN))

        print()
        print(color("  What would you like to do?", Colors.CYAN))
        print(color("  1. Update to latest version (preserve your config)", Colors.WHITE))
        print(color("  2. Fresh install (reset everything)", Colors.YELLOW))
        print(color("  3. Repair installation (fix missing files)", Colors.BLUE))
        print(color("  4. Exit (no changes)", Colors.DIM))
        print()

        while True:
            choice = input(color("  Your choice (1-4): ", Colors.CYAN))
            if choice in ['1', '2', '3', '4']:
                return {'1': 'update', '2': 'fresh', '3': 'repair', '4': 'exit'}[choice]
            print(color("  Please enter 1, 2, 3, or 4", Colors.YELLOW))

    def backup_existing_config(self) -> Path:
        """Create backup of existing configuration"""
        backup_dir = self.project_root / "sessions" / "backups"
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"config_backup_{timestamp}.json"

        shutil.copy2(self.existing_installation["config_file"], backup_file)
        return backup_file

    def load_existing_config(self):
        """Load existing configuration to preserve user settings"""
        existing_config = self.existing_installation["config"]

        # Preserve user settings
        if "developer_name" in existing_config:
            self.config["developer_name"] = existing_config["developer_name"]
        if "trigger_phrases" in existing_config:
            self.config["trigger_phrases"] = existing_config["trigger_phrases"]
        if "blocked_tools" in existing_config:
            self.config["blocked_tools"] = existing_config["blocked_tools"]
        if "task_detection" in existing_config:
            self.config["task_detection"] = existing_config["task_detection"]
        if "branch_enforcement" in existing_config:
            self.config["branch_enforcement"] = existing_config["branch_enforcement"]
        if "memory_bank_mcp" in existing_config:
            self.config["memory_bank_mcp"] = existing_config["memory_bank_mcp"]

        # Preserve any custom settings not in our defaults
        for key, value in existing_config.items():
            if key not in self.config:
                self.config[key] = value

    def check_dependencies(self) -> None:
        """Check for required dependencies"""
        print(color("Checking dependencies...", Colors.CYAN))
        
        # Check Python version
        if sys.version_info < (3, 8):
            print(color("❌ Python 3.8+ is required.", Colors.RED))
            sys.exit(1)
        
        # Check pip
        if not command_exists("pip3") and not command_exists("pip"):
            print(color("❌ pip is required but not installed.", Colors.RED))
            sys.exit(1)
        
        # Check Git (warning only)
        if not command_exists("git"):
            print(color("⚠️  Warning: Git not found. Sessions works best with git.", Colors.YELLOW))
            if not ask_yes_no("Continue anyway?", default=False):
                sys.exit(1)

    def get_installed_mcp_servers(self) -> set:
        """Get list of already installed MCP servers (cached to prevent repeated chrome launches)"""
        if self._installed_mcp_servers is not None:
            return self._installed_mcp_servers

        if not command_exists("claude"):
            self._installed_mcp_servers = set()
            return self._installed_mcp_servers

        try:
            result = subprocess.run(["claude", "mcp", "list"],
                                  capture_output=True, text=True, check=True)
            installed = set()
            for line in result.stdout.split('\n'):
                if 'memory-bank' in line.lower() or 'memorybank' in line.lower():
                    installed.add('memory-bank')
                elif 'github-mcp' in line.lower() or 'github_mcp' in line.lower():
                    installed.add('github')
                elif 'storybook-mcp' in line.lower() or 'storybook' in line.lower():
                    installed.add('storybook')
                elif 'playwright-mcp' in line.lower() or 'playwright' in line.lower():
                    installed.add('playwright')
            self._installed_mcp_servers = installed
            return installed
        except (subprocess.CalledProcessError, FileNotFoundError):
            self._installed_mcp_servers = set()
            return set()

    def check_memory_bank_mcp(self) -> dict:
        """Check for Memory Bank MCP availability"""
        has_npx = command_exists("npx")
        has_claude = command_exists("claude")
        installed_servers = self.get_installed_mcp_servers()

        return {
            "npx": has_npx,
            "claude": has_claude,
            "available": has_npx and has_claude,
            "already_installed": "memory-bank" in installed_servers
        }

    def install_memory_bank_mcp(self) -> bool:
        """Install Memory Bank MCP server"""
        memory_bank_status = self.check_memory_bank_mcp()

        if memory_bank_status["already_installed"]:
            print(color("✓ Memory Bank MCP already installed", Colors.GREEN))
            self.config["memory_bank_mcp"]["enabled"] = True
            return True

        if not memory_bank_status["available"]:
            missing = []
            if not memory_bank_status["npx"]:
                missing.append("npx (Node.js package runner)")
            if not memory_bank_status["claude"]:
                missing.append("claude (Claude Code CLI)")

            print(color(f"⚠️  Memory Bank MCP requirements not met. Missing: {', '.join(missing)}", Colors.YELLOW))
            print(color("   Install Node.js to get npx: https://nodejs.org/", Colors.DIM))
            print(color("   Memory Bank MCP features will be disabled but workflow continues normally.", Colors.DIM))
            return False

        print(color("✓ Memory Bank MCP requirements detected", Colors.GREEN))

        print(color("Installing Memory Bank MCP via Smithery...", Colors.CYAN))
        # Use empty string to bypass API key requirement
        result = subprocess.run(
            'echo "" | npx -y @smithery/cli install @alioshr/memory-bank-mcp --client claude',
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(color("✓ Memory Bank MCP installed successfully", Colors.GREEN))
            self.config["memory_bank_mcp"]["enabled"] = True
            return True
        else:
            print(color("⚠️ Memory Bank MCP installation failed", Colors.YELLOW))
            print(color("  You can manually install later with:", Colors.DIM))
            print(color('  echo "" | npx -y @smithery/cli install @alioshr/memory-bank-mcp --client claude', Colors.DIM))
            return False

    def setup_memory_bank_files(self) -> bool:
        """Setup automatic file discovery and sync for Memory Bank MCP"""
        try:
            print(color("\n  📄 File Synchronization Setup", Colors.CYAN))
            print(color("  Discovering important project documentation for persistent context...", Colors.DIM))
            print()

            # Auto-discovery patterns
            discovery_patterns = {
                "Configuration": [
                    "CLAUDE.md", "CLAUDE.sessions.md", ".claude/CLAUDE*.md"
                ],
                "Documentation": [
                    "README.md", "ARCHITECTURE.md", "DESIGN.md",
                    "docs/*.md", "documentation/*.md"
                ],
                "Requirements": [
                    "PRD.md", "FSD.md", "*requirements*.md",
                    "*product*.md", "*spec*.md"
                ]
            }

            discovered_files = {"Configuration": [], "Documentation": [], "Requirements": []}

            # Scan project for files
            for category, patterns in discovery_patterns.items():
                for pattern in patterns:
                    if '*' in pattern:
                        # Use glob for wildcard patterns
                        matches = list(self.project_root.glob(pattern))
                        for match in matches:
                            if match.is_file() and match.suffix.lower() == '.md':
                                rel_path = str(match.relative_to(self.project_root))
                                if rel_path not in [f["path"] for files in discovered_files.values() for f in files]:
                                    discovered_files[category].append({
                                        "path": rel_path,
                                        "exists": True,
                                        "size": match.stat().st_size
                                    })
                    else:
                        # Direct file check
                        file_path = self.project_root / pattern
                        if file_path.exists() and file_path.is_file():
                            rel_path = str(file_path.relative_to(self.project_root))
                            if rel_path not in [f["path"] for files in discovered_files.values() for f in files]:
                                discovered_files[category].append({
                                    "path": rel_path,
                                    "exists": True,
                                    "size": file_path.stat().st_size
                                })

            # Display discovered files
            total_discovered = sum(len(files) for files in discovered_files.values())

            if total_discovered == 0:
                print(color("  ⚠️ No documentation files auto-discovered", Colors.YELLOW))
                print(color("  You can add files manually below", Colors.DIM))
            else:
                print(color(f"  ✓ Auto-discovered {total_discovered} documentation files:", Colors.GREEN))
                print()

                for category, files in discovered_files.items():
                    if files:
                        print(color(f"  {category}:", Colors.CYAN))
                        for file_info in files:
                            size_kb = file_info["size"] / 1024
                            print(color(f'    ✓ {file_info["path"]} ({size_kb:.1f}KB)', Colors.GREEN))

                print()
                if ask_yes_no("  Add all auto-discovered files to Memory Bank sync?", default=True):
                    # Add all discovered files to sync configuration
                    for category, files in discovered_files.items():
                        for file_info in files:
                            sync_file = {
                                "path": file_info["path"],
                                "status": "pending",
                                "last_synced": None,
                                "category": category.lower()
                            }
                            self.config["memory_bank_mcp"]["sync_files"].append(sync_file)

                    print(color(f"  ✓ Added {total_discovered} files to sync configuration", Colors.GREEN))
                else:
                    print(color("  Skipped auto-discovered files", Colors.DIM))

            # Manual file addition
            print()
            print(color("  Additional files:", Colors.CYAN))
            print(color('  Add specific markdown files for persistent context (e.g., "docs/api.md")', Colors.DIM))
            print()

            while True:
                file_path = input(color("  Add markdown file (Enter path relative to project root, or Enter to finish): ", Colors.CYAN))
                if not file_path:
                    break

                # Skip if already added
                if any(f["path"] == file_path for f in self.config["memory_bank_mcp"]["sync_files"]):
                    print(color(f"  ⚠️ File already added: {file_path}", Colors.YELLOW))
                    continue

                # Validate file exists and is markdown
                full_path = self.project_root / file_path
                if not full_path.exists():
                    print(color(f"  ⚠️ File not found: {file_path}", Colors.YELLOW))
                    continue
                if not file_path.lower().endswith('.md'):
                    print(color("  ⚠️ Only markdown files (.md) are supported", Colors.YELLOW))
                    continue

                # Add to sync files configuration
                sync_file = {
                    "path": file_path,
                    "status": "pending",
                    "last_synced": None,
                    "category": "manual"
                }
                self.config["memory_bank_mcp"]["sync_files"].append(sync_file)
                print(color(f'  ✓ Added: "{file_path}"', Colors.GREEN))

            # Summary
            total_sync_files = len(self.config["memory_bank_mcp"]["sync_files"])
            if total_sync_files > 0:
                print()
                print(color(f"  📋 Total files configured for sync: {total_sync_files}", Colors.CYAN))
                print(color("  Use /sync-all to sync all files to Memory Bank", Colors.DIM))
                print(color("  Files will auto-load in future sessions for persistent context", Colors.DIM))

            return True

        except Exception as e:
            print(color("  ⚠️ Error during Memory Bank file configuration", Colors.YELLOW))
            print(color(f"    Error: {str(e)}", Colors.DIM))
            print(color("    Memory Bank MCP server is still functional", Colors.GREEN))
            return False

    def create_directories(self) -> None:
        """Create necessary directory structure"""
        print(color("Creating directory structure...", Colors.CYAN))
        
        dirs = [
            ".claude/hooks",
            ".claude/state", 
            ".claude/agents",
            ".claude/commands",
            "sessions/tasks",
            "sessions/tasks/done",
            "sessions/protocols",
            "sessions/knowledge"
        ]
        
        for dir_path in dirs:
            (self.project_root / dir_path).mkdir(parents=True, exist_ok=True)
    
    def install_python_deps(self) -> None:
        """Install Python dependencies"""
        print(color("Installing Python dependencies...", Colors.CYAN))
        try:
            pip_cmd = "pip3" if command_exists("pip3") else "pip"
            subprocess.run([pip_cmd, "install", "tiktoken", "--quiet"], 
                         capture_output=True, check=True)
        except subprocess.CalledProcessError:
            print(color("⚠️  Could not install tiktoken. You may need to install it manually.", Colors.YELLOW))
    
    def copy_files(self) -> None:
        """Copy all necessary files to the project"""
        # Copy hooks
        print(color("Installing hooks...", Colors.CYAN))
        hooks_dir = self.package_dir / "hooks"
        if hooks_dir.exists():
            for hook_file in hooks_dir.glob("*.py"):
                dest = self.project_root / ".claude/hooks" / hook_file.name
                shutil.copy2(hook_file, dest)
                if os.name != 'nt':
                    dest.chmod(0o755)
        
        # Copy protocols
        print(color("Installing protocols...", Colors.CYAN))
        protocols_dir = self.package_dir / "protocols"
        if protocols_dir.exists():
            for protocol_file in protocols_dir.glob("*.md"):
                dest = self.project_root / "sessions/protocols" / protocol_file.name
                shutil.copy2(protocol_file, dest)
        
        # Copy agents
        print(color("Installing agent definitions...", Colors.CYAN))
        agents_dir = self.package_dir / "agents"
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.md"):
                dest = self.project_root / ".claude/agents" / agent_file.name
                shutil.copy2(agent_file, dest)
        
        # Copy templates
        print(color("Installing templates...", Colors.CYAN))
        template_file = self.package_dir / "templates/TEMPLATE.md"
        if template_file.exists():
            dest = self.project_root / "sessions/tasks/TEMPLATE.md"
            shutil.copy2(template_file, dest)
        
        # Copy commands
        print(color("Installing commands...", Colors.CYAN))
        commands_dir = self.package_dir / "commands"
        if commands_dir.exists():
            for command_file in commands_dir.glob("*.md"):
                dest = self.project_root / ".claude/commands" / command_file.name
                shutil.copy2(command_file, dest)
            for command_file in commands_dir.glob("*.py"):
                dest = self.project_root / ".claude/commands" / command_file.name
                shutil.copy2(command_file, dest)
                # Make Python commands executable on Unix
                if os.name != 'nt':
                    dest.chmod(dest.stat().st_mode | stat.S_IEXEC)
        
        # Copy knowledge files
        knowledge_dir = self.package_dir / "knowledge/claude-code"
        if knowledge_dir.exists():
            print(color("Installing Claude Code knowledge base...", Colors.CYAN))
            dest_dir = self.project_root / "sessions/knowledge/claude-code"
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            shutil.copytree(knowledge_dir, dest_dir)
    
    def install_daic_command(self) -> None:
        """Install the daic command globally"""
        print(color("Installing daic command...", Colors.CYAN))
        
        if os.name == 'nt':  # Windows
            # Install Windows scripts (.cmd and .ps1)
            daic_cmd_source = self.package_dir / "scripts/daic.cmd"
            daic_ps1_source = self.package_dir / "scripts/daic.ps1"
            
            # Try to install to user's local directory
            local_bin = Path.home() / "AppData" / "Local" / "cc-sessions" / "bin"
            local_bin.mkdir(parents=True, exist_ok=True)
            
            if daic_cmd_source.exists():
                daic_cmd_dest = local_bin / "daic.cmd"
                shutil.copy2(daic_cmd_source, daic_cmd_dest)
                print(color(f"  ✓ Installed daic.cmd to {local_bin}", Colors.GREEN))
            
            if daic_ps1_source.exists():
                daic_ps1_dest = local_bin / "daic.ps1"
                shutil.copy2(daic_ps1_source, daic_ps1_dest)
                print(color(f"  ✓ Installed daic.ps1 to {local_bin}", Colors.GREEN))
            
            print(color(f"  ℹ Add {local_bin} to your PATH to use 'daic' command", Colors.YELLOW))
        else:
            # Unix/Mac installation
            daic_source = self.package_dir / "scripts/daic"
            if not daic_source.exists():
                print(color("⚠️  daic script not found in package.", Colors.YELLOW))
                return
            
            daic_dest = Path("/usr/local/bin/daic")
            
            try:
                shutil.copy2(daic_source, daic_dest)
                daic_dest.chmod(0o755)
            except PermissionError:
                print(color("⚠️  Cannot write to /usr/local/bin. Trying with sudo...", Colors.YELLOW))
                try:
                    subprocess.run(["sudo", "cp", str(daic_source), str(daic_dest)], check=True)
                    subprocess.run(["sudo", "chmod", "+x", str(daic_dest)], check=True)
                except subprocess.CalledProcessError:
                    print(color("⚠️  Could not install daic command globally.", Colors.YELLOW))
    
    def configure(self) -> None:
        """Interactive configuration"""
        print()
        print(color("╔═══════════════════════════════════════════════════════════════╗", Colors.BRIGHT + Colors.CYAN))
        print(color("║                    CONFIGURATION SETUP                        ║", Colors.BRIGHT + Colors.CYAN))
        print(color("╚═══════════════════════════════════════════════════════════════╝", Colors.BRIGHT + Colors.CYAN))
        print()
        
        self.statusline_installed = False
        
        # Developer name section
        print(color(f"\n★ DEVELOPER IDENTITY", Colors.BRIGHT + Colors.MAGENTA))
        print(color("─" * 60, Colors.DIM))
        print(color("  Claude will use this name when addressing you in sessions", Colors.DIM))
        print()
        
        name = input(color("  Your name: ", Colors.CYAN))
        if name:
            self.config["developer_name"] = name
            print(color(f"  ✓ Hello, {name}!", Colors.GREEN))
        
        # Statusline installation section
        print(color(f"\n\n★ STATUSLINE INSTALLATION", Colors.BRIGHT + Colors.MAGENTA))
        print(color("─" * 60, Colors.DIM))
        print(color("  Real-time status display in Claude Code showing:", Colors.WHITE))
        print(color("    • Current task and DAIC mode", Colors.CYAN))
        print(color("    • Token usage with visual progress bar", Colors.CYAN))
        print(color("    • Modified file counts", Colors.CYAN))
        print(color("    • Open task count", Colors.CYAN))
        print()

        if ask_yes_no("  Install statusline?", default=False):
            statusline_source = self.package_dir / "scripts/statusline-script.sh"
            if statusline_source.exists():
                print(color("  Installing statusline script...", Colors.DIM))
                statusline_dest = self.project_root / ".claude/statusline-script.sh"
                shutil.copy2(statusline_source, statusline_dest)
                statusline_dest.chmod(0o755)
                self.statusline_installed = True
                print(color("  ✓ Statusline installed successfully", Colors.GREEN))
            else:
                print(color("  ⚠ Statusline script not found in package", Colors.YELLOW))
        
        # DAIC trigger phrases section
        print(color(f"\n\n★ DAIC WORKFLOW CONFIGURATION", Colors.BRIGHT + Colors.MAGENTA))
        print(color("─" * 60, Colors.DIM))
        print(color("  The DAIC system enforces discussion before implementation.", Colors.WHITE))
        print(color("  Trigger phrases tell Claude when you're ready to proceed.", Colors.WHITE))
        print()
        print(color("  Default triggers:", Colors.CYAN))
        for phrase in self.config['trigger_phrases']:
            print(color(f'    → "{phrase}"', Colors.GREEN))
        print()
        print(color('  Hint: Common additions: "implement it", "do it", "proceed"', Colors.DIM))
        print()
        
        # Allow adding multiple custom trigger phrases
        while True:
            custom_trigger = input(color("  Add custom trigger phrase (Enter to skip): ", Colors.CYAN))
            if not custom_trigger:
                break
            self.config["trigger_phrases"].append(custom_trigger)
            print(color(f'  ✓ Added: "{custom_trigger}"', Colors.GREEN))
        
        # API Mode configuration
        print(color(f"\n\n★ THINKING BUDGET CONFIGURATION", Colors.BRIGHT + Colors.MAGENTA))
        print(color("─" * 60, Colors.DIM))
        print(color("  Token usage is not much of a concern with Claude Code Max", Colors.WHITE))
        print(color("  plans, especially the $200 tier. But API users are often", Colors.WHITE))
        print(color("  budget-conscious and want manual control.", Colors.WHITE))
        print()
        print(color("  Sessions was built to preserve tokens across context windows", Colors.CYAN))
        print(color("  but uses saved tokens to enable 'ultrathink' - Claude's", Colors.CYAN))
        print(color("  maximum thinking budget - on every interaction for best results.", Colors.CYAN))
        print()
        print(color("  • Max users (recommended): Automatic ultrathink every message", Colors.DIM))
        print(color("  • API users: Manual control with [[ ultrathink ]] when needed", Colors.DIM))
        print()
        print(color("  You can toggle this anytime with: /api-mode", Colors.DIM))
        print()

        if ask_yes_no("  Enable automatic ultrathink for best performance?", default=False):
            self.config["api_mode"] = False
            print(color("  ✓ Max mode - ultrathink enabled for best performance", Colors.GREEN))
        else:
            self.config["api_mode"] = True
            print(color("  ✓ API mode - manual ultrathink control (use [[ ultrathink ]])", Colors.GREEN))
        
        # Advanced configuration
        print(color(f"\n\n★ ADVANCED OPTIONS", Colors.BRIGHT + Colors.MAGENTA))
        print(color("─" * 60, Colors.DIM))
        print(color("  Configure tool blocking, task prefixes, and more", Colors.WHITE))
        print()

        if ask_yes_no("  Configure advanced options?", default=False):
            # Tool blocking
            print()
            print(color("╭───────────────────────────────────────────────────────────────╮", Colors.CYAN))
            print(color("│              Tool Blocking Configuration                      │", Colors.CYAN))
            print(color("├───────────────────────────────────────────────────────────────┤", Colors.CYAN))
            print(color("│   Tools can be blocked in discussion mode to enforce DAIC     │", Colors.DIM))
            print(color("│   Default: Edit, Write, MultiEdit, NotebookEdit are blocked   │", Colors.DIM))
            print(color("╰───────────────────────────────────────────────────────────────╯", Colors.CYAN))
            print()
            
            tools = [
                ("Edit", "Edit existing files", True),
                ("Write", "Create new files", True),
                ("MultiEdit", "Multiple edits in one operation", True),
                ("NotebookEdit", "Edit Jupyter notebooks", True),
                ("Bash", "Run shell commands", False),
                ("Read", "Read file contents", False),
                ("Grep", "Search file contents", False),
                ("Glob", "Find files by pattern", False),
                ("LS", "List directory contents", False),
                ("WebSearch", "Search the web", False),
                ("WebFetch", "Fetch web content", False),
                ("Task", "Launch specialized agents", False)
            ]
            
            print(color("  Available tools:", Colors.WHITE))
            for i, (name, desc, blocked) in enumerate(tools, 1):
                icon = "❌" if blocked else "✅"
                status_text = "BLOCKED" if blocked else "ALLOWED"
                status_color = Colors.RED if blocked else Colors.GREEN
                print(f"    {i:2}. {icon} {color(name.ljust(15), Colors.WHITE)} - {desc}")
                print(f"         {color(status_text, status_color)}")
            print()
            print(color("  Select tools to BLOCK in discussion mode (blocked tools enforce DAIC workflow)", Colors.DIM))
            print()

            if ask_yes_no("  🎮 Try interactive tool selector (arrow keys + space to toggle)?", default=True):
                print(color("  Starting interactive tool selection...", Colors.DIM))
                blocked_tools = interactive_tool_selection(tools, self.config.get("blocked_tools", []))

                if blocked_tools is not None:
                    self.config["blocked_tools"] = blocked_tools
                    print(color(f"  ✓ Tool blocking configuration saved ({len(blocked_tools)} tools blocked)", Colors.GREEN))
                else:
                    print(color("  Interactive mode cancelled or failed, trying classic mode...", Colors.YELLOW))
                    # Automatically fall back to classic mode
                    if ask_yes_no("  Modify blocked tools list (numbered input)?", default=True):
                        tool_numbers = input(color("  Enter comma-separated tool numbers to block: ", Colors.CYAN))
                        if tool_numbers:
                            tool_names = [t[0] for t in tools]
                            blocked_list = []
                            for num_str in tool_numbers.split(','):
                                try:
                                    num = int(num_str.strip())
                                    if 1 <= num <= len(tools):
                                        blocked_list.append(tool_names[num - 1])
                                except ValueError:
                                    pass
                            if blocked_list:
                                self.config["blocked_tools"] = blocked_list
                                print(color("  ✓ Tool blocking configuration saved", Colors.GREEN))
            elif ask_yes_no("  Modify blocked tools list (numbered input)?", default=False):
                tool_numbers = input(color("  Enter comma-separated tool numbers to block: ", Colors.CYAN))
                if tool_numbers:
                    tool_names = [t[0] for t in tools]
                    blocked_list = []
                    for num_str in tool_numbers.split(','):
                        try:
                            num = int(num_str.strip())
                            if 1 <= num <= len(tools):
                                blocked_list.append(tool_names[num - 1])
                        except ValueError:
                            pass
                    if blocked_list:
                        self.config["blocked_tools"] = blocked_list
                        print(color("  ✓ Tool blocking configuration saved", Colors.GREEN))
            
            # Task prefix configuration
            print(color(f"\n\n★ TASK PREFIX CONFIGURATION", Colors.BRIGHT + Colors.MAGENTA))
            print(color("─" * 60, Colors.DIM))
            print(color("  Task prefixes organize work by priority and type", Colors.WHITE))
            print()
            print(color("  Current prefixes:", Colors.CYAN))
            print(color("    → h- (high priority)", Colors.WHITE))
            print(color("    → m- (medium priority)", Colors.WHITE))
            print(color("    → l- (low priority)", Colors.WHITE))
            print(color("    → ?- (investigate/research)", Colors.WHITE))
            print()

            if ask_yes_no("  Customize task prefixes?", default=False):
                high = input(color("  High priority prefix [h-]: ", Colors.CYAN)) or 'h-'
                med = input(color("  Medium priority prefix [m-]: ", Colors.CYAN)) or 'm-'
                low = input(color("  Low priority prefix [l-]: ", Colors.CYAN)) or 'l-'
                inv = input(color("  Investigate prefix [?-]: ", Colors.CYAN)) or '?-'
                
                self.config["task_prefixes"] = {
                    "priority": [high, med, low, inv]
                }
                
                print(color("  ✓ Task prefixes updated", Colors.GREEN))
    
    def save_config(self) -> None:
        """Save configuration files"""
        print(color("Creating configuration...", Colors.CYAN))

        # Add version to config before saving
        self.config["version"] = self.get_current_package_version()

        # Save sessions config
        config_file = self.project_root / "sessions/sessions-config.json"
        config_file.write_text(json.dumps(self.config, indent=2))
        
        # Create or update .claude/settings.json with all hooks
        print(color("Configuring hooks in settings.json...", Colors.CYAN))
        settings_file = self.project_root / ".claude/settings.json"
        
        settings = {}
        if settings_file.exists():
            print(color("Found existing settings.json, merging sessions hooks...", Colors.CYAN))
            try:
                settings = json.loads(settings_file.read_text())
            except:
                settings = {}
        else:
            print(color("Creating new settings.json with sessions hooks...", Colors.CYAN))
        
        # Define the sessions hooks
        sessions_hooks = {
            "UserPromptSubmit": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/user-messages.py" if os.name != 'nt' else "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\user-messages.py\""
                        },
                        {
                            "type": "command",
                            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/task-completion-workflow.py" if os.name != 'nt' else "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\task-completion-workflow.py\""
                        }
                    ]
                }
            ],
            "PreToolUse": [
                {
                    "matcher": "Write|Edit|MultiEdit|Task|Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/sessions-enforce.py" if os.name != 'nt' else "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\sessions-enforce.py\""
                        }
                    ]
                },
                {
                    "matcher": "Task",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/task-transcript-link.py" if os.name != 'nt' else "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\task-transcript-link.py\""
                        }
                    ]
                }
            ],
            "PostToolUse": [
                {
                    "matcher": "Edit|Write|MultiEdit|NotebookEdit",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-implementation-retention.py" if os.name != 'nt' else "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\post-implementation-retention.py\""
                        }
                    ]
                },
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-use.py" if os.name != 'nt' else "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\post-tool-use.py\""
                        }
                    ]
                }
            ],
            "SessionStart": [
                {
                    "matcher": "startup|clear",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.py" if os.name != 'nt' else "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\session-start.py\""
                        }
                    ]
                }
            ]
        }
        
        # Merge hooks (sessions hooks take precedence)
        if "hooks" not in settings:
            settings["hooks"] = {}
        
        # Merge each hook type (avoid duplicates)
        for hook_type, hook_config in sessions_hooks.items():
            if hook_type not in settings["hooks"]:
                settings["hooks"][hook_type] = hook_config
            else:
                # Merge without duplicates by checking command strings
                existing_commands = set()
                for hook_entry in settings["hooks"][hook_type]:
                    if "hooks" in hook_entry:
                        for hook in hook_entry["hooks"]:
                            existing_commands.add(hook.get("command", ""))

                # Only add new hook configurations that don't exist
                for new_hook_entry in hook_config:
                    entry_commands = set()
                    if "hooks" in new_hook_entry:
                        for hook in new_hook_entry["hooks"]:
                            entry_commands.add(hook.get("command", ""))

                    # If none of the commands in this entry already exist, add the whole entry
                    if not entry_commands.intersection(existing_commands):
                        settings["hooks"][hook_type].append(new_hook_entry)
                        existing_commands.update(entry_commands)
        
        # Add statusline if requested
        if hasattr(self, 'statusline_installed') and self.statusline_installed:
            settings["statusLine"] = {
                "type": "command",
                "command": "$CLAUDE_PROJECT_DIR/.claude/statusline-script.sh" if os.name != 'nt' else "%CLAUDE_PROJECT_DIR%\\.claude\\statusline-script.sh",
                "padding": 0
            }
        
        # Save the updated settings
        settings_file.write_text(json.dumps(settings, indent=2))
        print(color("✓ Sessions hooks configured in settings.json", Colors.GREEN))
        
        # Initialize DAIC state
        daic_state = self.project_root / ".claude/state/daic-mode.json"
        daic_state.write_text(json.dumps({"mode": "discussion"}, indent=2))
        
        # Create initial task state
        current_date = datetime.now().strftime("%Y-%m-%d")
        task_state = self.project_root / ".claude/state/current_task.json"
        task_state.write_text(json.dumps({
            "task": None,
            "branch": None,
            "services": [],
            "updated": current_date
        }, indent=2))
    
    def setup_claude_md(self) -> None:
        """Set up CLAUDE.md integration"""
        print()
        print(color("═══════════════════════════════════════════", Colors.BRIGHT))
        print(color("         CLAUDE.md Integration", Colors.BRIGHT))
        print(color("═══════════════════════════════════════════", Colors.BRIGHT))
        print()
        
        # Check for existing CLAUDE.md
        sessions_md = self.package_dir / "templates/CLAUDE.sessions.md"
        claude_md = self.project_root / "CLAUDE.md"
        
        if claude_md.exists():
            # File exists, preserve it and add sessions as separate file
            print(color("CLAUDE.md already exists, preserving your project-specific rules...", Colors.CYAN))
            
            # Copy CLAUDE.sessions.md as separate file
            if sessions_md.exists():
                dest = self.project_root / "CLAUDE.sessions.md"
                shutil.copy2(sessions_md, dest)
            
            # Check if it already includes sessions
            content = claude_md.read_text()
            if "@CLAUDE.sessions.md" not in content:
                print(color("Adding sessions include to existing CLAUDE.md...", Colors.CYAN))
                
                addition = "\n## Sessions System Behaviors\n\n@CLAUDE.sessions.md\n"
                with claude_md.open("a") as f:
                    f.write(addition)
                
                print(color("✅ Added @CLAUDE.sessions.md include to your CLAUDE.md", Colors.GREEN))
            else:
                print(color("✅ CLAUDE.md already includes sessions behaviors", Colors.GREEN))
        else:
            # File doesn't exist, use sessions as CLAUDE.md
            print(color("No existing CLAUDE.md found, installing sessions as your CLAUDE.md...", Colors.CYAN))
            if sessions_md.exists():
                shutil.copy2(sessions_md, claude_md)
                print(color("✅ CLAUDE.md created with complete sessions behaviors", Colors.GREEN))

    def run_update(self) -> None:
        """Update existing installation preserving configuration"""
        print()
        print(color("🔄 UPDATING CC-SESSIONS", Colors.BRIGHT + Colors.CYAN))
        print(color("─────────────────────────", Colors.DIM))

        try:
            # Backup existing config
            backup_file = self.backup_existing_config()
            print(color(f"📋 Configuration backed up to: {backup_file.name}", Colors.GREEN))

            # Load existing configuration
            self.load_existing_config()

            # Update code files only
            print(color("📦 Updating hooks, agents, commands, and protocols...", Colors.CYAN))
            self.copy_files()

            # Update version in config
            self.config["version"] = self.get_current_package_version()

            # Save config with preserved settings
            self.save_config()

            # Update CLAUDE.md if needed
            self.setup_claude_md()

            print()
            print(color("╔═══════════════════════════════════════════════╗", Colors.BRIGHT + Colors.GREEN))
            print(color("║              🎉 UPDATE COMPLETE! 🎉           ║", Colors.BRIGHT + Colors.GREEN))
            print(color("╚═══════════════════════════════════════════════╝", Colors.BRIGHT + Colors.GREEN))
            print()

            print(color("  ✓ Code files updated to latest version", Colors.GREEN))
            print(color("  ✓ Your configuration preserved", Colors.GREEN))
            print(color("  ✓ Configuration backup created", Colors.GREEN))
            print()
            print(color("  💡 Restart Claude Code to use updated hooks", Colors.CYAN))

        except Exception as e:
            print(color(f"❌ Update failed: {e}", Colors.RED))

    def run_repair(self) -> None:
        """Repair missing files without changing configuration"""
        print()
        print(color("🔧 REPAIRING CC-SESSIONS", Colors.BRIGHT + Colors.BLUE))
        print(color("─────────────────────────", Colors.DIM))

        try:
            # Load existing configuration
            self.load_existing_config()

            # Check what's missing and fix it
            missing_items = []

            if not self.existing_installation["has_hooks"]:
                missing_items.append("hooks")
            if not self.existing_installation["has_agents"]:
                missing_items.append("agents")
            if not self.existing_installation["has_commands"]:
                missing_items.append("commands")

            if missing_items:
                print(color(f"🔍 Missing components detected: {', '.join(missing_items)}", Colors.YELLOW))
                print(color("📦 Restoring missing files...", Colors.CYAN))

                # Ensure directories exist
                self.create_directories()

                # Restore files
                self.copy_files()

                print(color("✅ Missing files restored", Colors.GREEN))
            else:
                print(color("✅ All components present - running full file refresh", Colors.GREEN))
                self.copy_files()

            # Update CLAUDE.md if missing
            if not self.existing_installation["claude_md_exists"]:
                self.setup_claude_md()

            print()
            print(color("╔═══════════════════════════════════════════════╗", Colors.BRIGHT + Colors.GREEN))
            print(color("║             🎉 REPAIR COMPLETE! 🎉            ║", Colors.BRIGHT + Colors.GREEN))
            print(color("╚═══════════════════════════════════════════════╝", Colors.BRIGHT + Colors.GREEN))
            print()

            print(color("  ✓ Missing files restored", Colors.GREEN))
            print(color("  ✓ Configuration unchanged", Colors.GREEN))
            print()
            print(color("  💡 Restart Claude Code to ensure all hooks are loaded", Colors.CYAN))

        except Exception as e:
            print(color(f"❌ Repair failed: {e}", Colors.RED))

    def run(self) -> None:
        """Run the full installation process"""
        print(color("╔════════════════════════════════════════════╗", Colors.BRIGHT))
        print(color("║            cc-sessions Installer           ║", Colors.BRIGHT))
        print(color("╚════════════════════════════════════════════╝", Colors.BRIGHT))
        print()

        # Handle existing installations
        if self.existing_installation:
            installation_mode = self.show_installation_menu()

            if installation_mode == 'exit':
                print(color("\n  👋 No changes made. Exiting...", Colors.CYAN))
                return

            if installation_mode == 'update':
                return self.run_update()
            elif installation_mode == 'repair':
                return self.run_repair()
            # 'fresh' continues with full installation below

        # Check CLAUDE_PROJECT_DIR
        if not os.environ.get("CLAUDE_PROJECT_DIR"):
            print(color(f"⚠️  CLAUDE_PROJECT_DIR not set. Setting it to {self.project_root}", Colors.YELLOW))
            print("   To make this permanent, add to your shell profile:")
            print(f'   export CLAUDE_PROJECT_DIR="{self.project_root}"')
            print()

        try:
            self.check_dependencies()
            self.create_directories()
            self.install_python_deps()
            self.copy_files()
            self.install_daic_command()

            # Optional MCP integrations
            print()
            print(color("🔌 Optional MCP Integrations", Colors.BRIGHT + Colors.CYAN))
            print(color("─────────────────────────────", Colors.DIM))
            memory_bank_installed = self.install_memory_bank_mcp()

            # Setup Memory Bank file sync if installation successful
            if memory_bank_installed:
                self.setup_memory_bank_files()

            self.configure()
            self.save_config()
            self.setup_claude_md()
            
            # Success message
            print()
            print()
            print(color("╔═══════════════════════════════════════════════════════════════╗", Colors.BRIGHT + Colors.GREEN))
            print(color("║                 🎉 INSTALLATION COMPLETE! 🎉                  ║", Colors.BRIGHT + Colors.GREEN))
            print(color("╚═══════════════════════════════════════════════════════════════╝", Colors.BRIGHT + Colors.GREEN))
            print()
            
            print(color("  Installation Summary:", Colors.BRIGHT + Colors.CYAN))
            print(color("  ─────────────────────", Colors.DIM))
            print(color("  ✓ Directory structure created", Colors.GREEN))
            print(color("  ✓ Hooks installed and configured", Colors.GREEN))
            print(color("  ✓ Protocols and agents deployed", Colors.GREEN))
            print(color("  ✓ daic command available globally", Colors.GREEN))
            print(color("  ✓ Configuration saved", Colors.GREEN))
            print(color("  ✓ DAIC state initialized (Discussion mode)", Colors.GREEN))
            
            if hasattr(self, 'statusline_installed') and self.statusline_installed:
                print(color("  ✓ Statusline configured", Colors.GREEN))
            
            print()
            
            # Test daic command
            if command_exists("daic"):
                print(color("  ✓ daic command verified and working", Colors.GREEN))
            else:
                print(color("  ⚠ daic command not in PATH", Colors.YELLOW))
                print(color("       Add /usr/local/bin to your PATH", Colors.DIM))
            
            print()
            print(color("  ★ NEXT STEPS", Colors.BRIGHT + Colors.MAGENTA))
            print(color("  ─────────────", Colors.DIM))
            print()
            print(color("  1. Restart Claude Code to activate the sessions hooks", Colors.WHITE))
            print(color("     → Close and reopen Claude Code", Colors.DIM))
            print()
            print(color("  2. Create your first task:", Colors.WHITE))
            print(color('     → Tell Claude: "Create a new task"', Colors.CYAN))
            print(color('     → Or: "Create a task for implementing feature X"', Colors.CYAN))
            print()
            print(color("  3. Start working with the DAIC workflow:", Colors.WHITE))
            print(color("     → Discuss approach first", Colors.DIM))
            print(color('     → Say "make it so" to implement', Colors.DIM))
            print(color('     → Run "daic" to return to discussion', Colors.DIM))
            print()
            print(color("  ──────────────────────────────────────────────────────", Colors.DIM))
            print()
            print(color(f"  Welcome aboard, {self.config['developer_name']}! 🚀", Colors.BRIGHT + Colors.CYAN))
            
        except Exception as e:
            print(color(f"❌ Installation failed: {e}", Colors.RED))
            sys.exit(1)

def main():
    """Main entry point for the installer"""
    installer = SessionsInstaller()
    installer.run()

def install():
    """Alias for main() for compatibility"""
    main()

if __name__ == "__main__":
    main()
