#!/usr/bin/env node

/**
 * Claude Code Sessions Framework - Cross-Platform Node.js Installer
 * 
 * NPM wrapper installer providing identical functionality to the Python installer
 * with native Windows, macOS, and Linux support. Features interactive terminal
 * UI, platform-aware command detection, and cross-platform file operations.
 * 
 * Key Features:
 *   - Windows compatibility with .cmd and .ps1 script installation
 *   - Cross-platform command detection (where/which)
 *   - Platform-aware path handling and file permissions
 *   - Interactive menu system with keyboard navigation
 *   - Global daic command installation with PATH integration
 * 
 * Platform Support:
 *   - Windows 10/11 (Command Prompt, PowerShell, Git Bash)
 *   - macOS (Terminal, iTerm2 with Bash/Zsh)
 *   - Linux distributions (various terminals and shells)
 * 
 * Installation Methods:
 *   - npm install -g cc-sessions (global installation)
 *   - npx cc-sessions (temporary installation)
 * 
 * Windows Integration:
 *   - Creates %USERPROFILE%\AppData\Local\cc-sessions\bin directory
 *   - Installs both daic.cmd and daic.ps1 for shell compatibility
 *   - Uses Windows-style environment variables (%VAR%)
 *   - Platform-specific hook command generation
 * 
 * @module install
 * @requires fs
 * @requires path
 * @requires child_process
 * @requires readline
 */

const fs = require('fs').promises;
const path = require('path');
const { execSync } = require('child_process');
const readline = require('readline');
const { promisify } = require('util');

// Colors for terminal output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m',
  bgRed: '\x1b[41m',
  bgGreen: '\x1b[42m',
  bgYellow: '\x1b[43m',
  bgBlue: '\x1b[44m',
  bgMagenta: '\x1b[45m',
  bgCyan: '\x1b[46m'
};

// Helper to colorize output
const color = (text, colorCode) => `${colorCode}${text}${colors.reset}`;

// Icons and symbols
const icons = {
  check: '✓',
  cross: '✗',
  lock: '🔒',
  unlock: '🔓',
  info: 'ℹ',
  warning: '⚠',
  arrow: '→',
  bullet: '•',
  star: '★'
};

// Create readline interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const question = promisify(rl.question).bind(rl);

/**
 * Ask a yes/no question with a default option
 * @param {string} prompt - The question to ask
 * @param {boolean} defaultValue - True for yes default (Y/n), False for no default (y/N)
 * @returns {Promise<boolean>} - True for yes, False for no
 */
async function askYesNo(prompt, defaultValue = true) {
  const suffix = defaultValue ? ' (Y/n): ' : ' (y/N): ';

  while (true) {
    const response = (await question(color(prompt + suffix, colors.cyan))).trim().toLowerCase();

    if (response === '') {
      return defaultValue;
    } else if (['y', 'yes'].includes(response)) {
      return true;
    } else if (['n', 'no'].includes(response)) {
      return false;
    } else {
      console.log(color('  Please enter y, n, yes, no, or press Enter for default', colors.yellow));
    }
  }
}

/**
 * Interactive tool selection with arrow keys navigation
 * @param {Array} tools - Array of [name, description, isBlocked] tuples
 * @param {Array} currentBlocked - Array of currently blocked tool names
 * @returns {Promise<Array|null>} Array of tool names to block, or null if cancelled
 */
async function interactiveToolSelection(tools, currentBlocked) {
  try {
    // Check if we're in a compatible terminal
    if (!process.stdin.isTTY) {
      console.log(color('  ⚠️ Interactive mode requires a terminal (not available in pipes/scripts)', colors.yellow));
      return null;
    }

    const readline = require('readline');

    // Enable keypress events
    if (typeof process.stdin.setRawMode === 'function') {
      process.stdin.setRawMode(true);
    } else {
      console.log(color('  ⚠️ Raw mode not available in this terminal', colors.yellow));
      console.log(color('  Falling back to classic numbered input...', colors.dim));
      return null;
    }

    // Required for keypress events
    require('readline').emitKeypressEvents(process.stdin);

    // Setup readline for raw key input
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    process.stdin.resume();

    // Prepare tool list with selection state
    const toolItems = tools.map(([name, desc]) => ({
      name,
      desc,
      isSelected: currentBlocked.includes(name)
    }));

    let currentIndex = 0;

    return new Promise((resolve) => {
      const showMenu = () => {
        // Clear screen
        console.clear();

        // Show header
        console.log(color('╭───────────────────────────────────────────────────────────────╮', colors.cyan));
        console.log(color('│              Interactive Tool Selection                       │', colors.cyan));
        console.log(color('├───────────────────────────────────────────────────────────────┤', colors.cyan));
        console.log(color('│   Use ↑↓ to navigate, Space to toggle, Enter to confirm      │', colors.cyan));
        console.log(color('│   [✓] = Will be BLOCKED, [ ] = Will remain ALLOWED           │', colors.cyan));
        console.log(color('╰───────────────────────────────────────────────────────────────╯', colors.cyan));
        console.log();

        // Show tools
        toolItems.forEach((tool, i) => {
          const prefix = i === currentIndex ? '>' : ' ';
          const checkbox = tool.isSelected ? '[✓]' : '[ ]';
          const statusIcon = tool.isSelected ? '❌' : '✅';
          const statusText = tool.isSelected ? 'BLOCKED' : 'ALLOWED';
          const statusColor = tool.isSelected ? colors.red : colors.green;

          if (i === currentIndex) {
            console.log(color(`${prefix} ${checkbox} ${statusIcon} ${tool.name.padEnd(15)} - ${tool.desc}`, colors.bright + colors.white));
          } else {
            console.log(`${prefix} ${checkbox} ${statusIcon} ${color(tool.name.padEnd(15), colors.white)} - ${tool.desc}`);
          }
          console.log(`     ${color(statusText, statusColor)}`);
        });

        console.log(color('\\nPress ESC or Ctrl+C to cancel', colors.dim));
      };

      const handleKeypress = (chunk, key) => {
        if (key && key.ctrl && key.name === 'c') {
          cleanup();
          resolve(null);
          return;
        }

        if (key) {
          switch (key.name) {
            case 'up':
              if (currentIndex > 0) currentIndex--;
              showMenu();
              break;
            case 'down':
              if (currentIndex < toolItems.length - 1) currentIndex++;
              showMenu();
              break;
            case 'space':
              toolItems[currentIndex].isSelected = !toolItems[currentIndex].isSelected;
              showMenu();
              break;
            case 'return':
              cleanup();
              resolve(toolItems.filter(tool => tool.isSelected).map(tool => tool.name));
              break;
            case 'escape':
              cleanup();
              resolve(null);
              break;
          }
        }
      };

      const cleanup = () => {
        process.stdin.setRawMode(false);
        process.stdin.pause();
        process.stdin.removeListener('keypress', handleKeypress);
        rl.close();
      };

      process.stdin.on('keypress', handleKeypress);
      showMenu();
    });

  } catch (error) {
    console.log(color(`  ⚠️ Interactive mode error: ${error.message}`, colors.yellow));
    console.log(color('  Falling back to classic numbered input...', colors.dim));
    return null;
  }
}

// Paths
const SCRIPT_DIR = __dirname;
let PROJECT_ROOT = process.cwd();

// Check if we're running from npx or in wrong directory
async function detectProjectDirectory() {
  // If running from node_modules or temp npx directory
  if (PROJECT_ROOT.includes('node_modules') || PROJECT_ROOT.includes('.npm')) {
    console.log(color('⚠️  Running from package directory, not project directory.', colors.yellow));
    console.log();
    const projectPath = await question('Enter the path to your project directory (or press Enter for current directory): ');
    if (projectPath) {
      PROJECT_ROOT = path.resolve(projectPath);
    } else {
      PROJECT_ROOT = process.cwd();
    }
    console.log(color(`Using project directory: ${PROJECT_ROOT}`, colors.cyan));
  }
}

// Configuration object to build
const config = {
  developer_name: "the developer",
  trigger_phrases: ["make it so", "run that", "go ahead", "yert"],
  blocked_tools: ["Edit", "Write", "MultiEdit", "NotebookEdit"],
  task_detection: { enabled: true },
  branch_enforcement: { enabled: true },
  memory_bank_mcp: { enabled: false, auto_activate: true }
};

// Global variable for existing installation detection
let existingInstallation = null;

/**
 * Detect if cc-sessions is already installed in this project
 * @returns {object|null} Installation details or null if not found
 */
function detectExistingInstallation() {
  const configFile = path.join(PROJECT_ROOT, 'sessions', 'sessions-config.json');

  if (!require('fs').existsSync(configFile)) {
    return null;
  }

  try {
    const existingConfig = JSON.parse(require('fs').readFileSync(configFile, 'utf8'));

    // Try to determine installed version
    let installedVersion = "unknown";
    if (existingConfig.version) {
      installedVersion = existingConfig.version;
    }

    // Check for statusline installation
    let hasStatusline = false;
    try {
      const settingsFile = path.join(PROJECT_ROOT, '.claude', 'settings.json');
      if (require('fs').existsSync(settingsFile)) {
        const settings = JSON.parse(require('fs').readFileSync(settingsFile, 'utf8'));
        hasStatusline = !!settings.statusLine;
      }
    } catch {
      // Ignore errors when checking statusline
    }

    return {
      configFile: configFile,
      config: existingConfig,
      version: installedVersion,
      hasHooks: require('fs').existsSync(path.join(PROJECT_ROOT, '.claude', 'hooks')),
      hasAgents: require('fs').existsSync(path.join(PROJECT_ROOT, '.claude', 'agents')),
      hasCommands: require('fs').existsSync(path.join(PROJECT_ROOT, '.claude', 'commands')),
      hasStatusline: hasStatusline,
      claudeMdExists: require('fs').existsSync(path.join(PROJECT_ROOT, 'CLAUDE.md'))
    };
  } catch (error) {
    return null;
  }
}

/**
 * Get current package version
 * @returns {string} Current version
 */
function getCurrentPackageVersion() {
  try {
    const packageJson = JSON.parse(require('fs').readFileSync(path.join(__dirname, 'package.json'), 'utf8'));
    return packageJson.version || '0.2.8';
  } catch {
    return '0.2.8'; // Fallback
  }
}

/**
 * Show installation menu for existing installations
 * @returns {Promise<string>} User's choice
 */
async function showInstallationMenu() {
  const currentVersion = getCurrentPackageVersion();
  const existingVersion = existingInstallation.version;

  console.log();
  console.log(color('╔═══════════════════════════════════════════════╗', colors.bright + colors.cyan));
  console.log(color('║          cc-sessions Already Installed        ║', colors.bright + colors.cyan));
  console.log(color('╚═══════════════════════════════════════════════╝', colors.bright + colors.cyan));
  console.log();

  console.log(color(`  Found existing installation: ${colors.bright}v${existingVersion}${colors.reset}`, colors.white));
  console.log(color(`  Current version available: ${colors.bright}v${currentVersion}${colors.reset}`, colors.white));
  console.log();

  if (existingVersion !== currentVersion) {
    console.log(color('  🆕 Update available!', colors.green));
  } else {
    console.log(color('  ✅ You have the latest version', colors.green));
  }

  console.log();
  console.log(color('  What would you like to do?', colors.cyan));
  console.log(color('  1. Update to latest version (preserve your config)', colors.white));
  console.log(color('  2. Fresh install (reset everything)', colors.yellow));
  console.log(color('  3. Repair installation (fix missing files)', colors.blue));
  console.log(color('  4. Exit (no changes)', colors.dim));
  console.log();

  while (true) {
    const choice = await question(color('  Your choice (1-4): ', colors.cyan));
    if (['1', '2', '3', '4'].includes(choice)) {
      return { '1': 'update', '2': 'fresh', '3': 'repair', '4': 'exit' }[choice];
    }
    console.log(color('  Please enter 1, 2, 3, or 4', colors.yellow));
  }
}

/**
 * Create backup of existing configuration
 * @returns {string} Backup file path
 */
async function backupExistingConfig() {
  const backupDir = path.join(PROJECT_ROOT, 'sessions', 'backups');
  await fs.mkdir(backupDir, { recursive: true });

  const timestamp = new Date().toISOString().replace(/[:.-]/g, '_').split('T')[0] + '_' +
                    new Date().toISOString().split('T')[1].split('.')[0].replace(/:/g, '');
  const backupFile = path.join(backupDir, `config_backup_${timestamp}.json`);

  await fs.copyFile(existingInstallation.configFile, backupFile);
  return backupFile;
}

/**
 * Load existing configuration to preserve user settings
 */
function loadExistingConfig() {
  const existing = existingInstallation.config;

  // Preserve user settings
  if (existing.developer_name) config.developer_name = existing.developer_name;
  if (existing.trigger_phrases) config.trigger_phrases = existing.trigger_phrases;
  if (existing.blocked_tools) config.blocked_tools = existing.blocked_tools;
  if (existing.task_detection) config.task_detection = existing.task_detection;
  if (existing.branch_enforcement) config.branch_enforcement = existing.branch_enforcement;
  if (existing.memory_bank_mcp) config.memory_bank_mcp = existing.memory_bank_mcp;

  // Preserve any custom settings not in defaults
  for (const [key, value] of Object.entries(existing)) {
    if (!(key in config)) {
      config[key] = value;
    }
  }
}

/**
 * Update existing installation preserving configuration
 */
async function runUpdate() {
  console.log();
  console.log(color('🔄 Updating cc-sessions installation...', colors.cyan));
  console.log();

  try {
    // Backup existing configuration
    const backupFile = await backupExistingConfig();
    console.log(color(`✓ Configuration backed up to ${path.basename(backupFile)}`, colors.green));

    // Load existing configuration to preserve settings
    loadExistingConfig();

    console.log(color('Updating system files...', colors.dim));

    // Update directories structure (create any missing)
    await createDirectories();

    // Install Python dependencies
    await installPythonDeps();

    // Update all code files
    await copyFiles();

    // Update daic command
    await installDaicCommand();

    // Update configuration with preserved settings + new version
    config.version = getCurrentPackageVersion();
    await saveConfig(existingInstallation.hasStatusline || false);

    // Preserve CLAUDE.md setup
    await setupClaudeMd();

    console.log();
    console.log(color('✅ Update completed successfully!', colors.green));
    console.log();
    console.log(color(`  Updated to version: ${colors.bright}v${config.version}${colors.reset}`, colors.white));
    console.log(color('  Your configuration has been preserved', colors.dim));
    console.log();
    console.log(color('  Next steps:', colors.cyan));
    console.log(color('  • Restart Claude Code to activate updated hooks', colors.dim));
    console.log(color('  • Your tasks and settings remain unchanged', colors.dim));

  } catch (error) {
    console.log();
    console.log(color('❌ Update failed!', colors.red));
    console.log(color(`  Error: ${error.message}`, colors.dim));
    console.log(color('  Your existing installation was not modified', colors.dim));
    throw error;
  }
}

/**
 * Repair installation by fixing missing files without changing configuration
 */
async function runRepair() {
  console.log();
  console.log(color('🔧 Repairing cc-sessions installation...', colors.cyan));
  console.log();

  try {
    // Load existing configuration
    loadExistingConfig();

    console.log(color('Checking and repairing system files...', colors.dim));

    // Recreate directories (in case any are missing)
    await createDirectories();

    // Install Python dependencies
    await installPythonDeps();

    // Restore all code files
    await copyFiles();

    // Restore daic command
    await installDaicCommand();

    // Restore CLAUDE.md setup
    await setupClaudeMd();

    console.log();
    console.log(color('✅ Repair completed successfully!', colors.green));
    console.log();
    console.log(color('  All missing files have been restored', colors.white));
    console.log(color('  Your configuration was not modified', colors.dim));
    console.log();
    console.log(color('  Next steps:', colors.cyan));
    console.log(color('  • Restart Claude Code if experiencing issues', colors.dim));
    console.log(color('  • All tasks and settings remain unchanged', colors.dim));

  } catch (error) {
    console.log();
    console.log(color('❌ Repair failed!', colors.red));
    console.log(color(`  Error: ${error.message}`, colors.dim));
    throw error;
  }
}

// Check if command exists
function commandExists(command) {
  try {
    if (process.platform === 'win32') {
      // Windows - use 'where' command
      execSync(`where ${command}`, { stdio: 'ignore' });
      return true;
    } else {
      // Unix/Mac - use 'which' command
      execSync(`which ${command}`, { stdio: 'ignore' });
      return true;
    }
  } catch {
    return false;
  }
}

// Cache for MCP servers to prevent repeated Chrome popups
let _installedMcpServers = null;

/**
 * Get list of installed MCP servers using cached results
 * @returns {string[]} Array of server names
 */
function getInstalledMcpServers() {
  if (_installedMcpServers !== null) {
    return _installedMcpServers;
  }

  try {
    const result = execSync('claude mcp list', { encoding: 'utf-8', stdio: 'pipe' });
    _installedMcpServers = result.split('\n')
      .map(line => line.trim())
      .filter(line => line && !line.startsWith('---') && !line.includes('MCP servers'))
      .map(line => line.split(/\s+/)[0])  // Extract server name (first column)
      .filter(name => name && name !== 'Name');

    return _installedMcpServers;
  } catch (error) {
    console.log(color('  Warning: Could not check MCP servers', colors.yellow));
    _installedMcpServers = [];
    return _installedMcpServers;
  }
}

/**
 * Check Memory Bank MCP requirements and installation status
 * @returns {object} Status object with availability flags
 */
function checkMemoryBankMcp() {
  const hasNpx = commandExists("npx");
  const hasClaude = commandExists("claude");
  const installedServers = getInstalledMcpServers();

  return {
    npx: hasNpx,
    claude: hasClaude,
    available: hasNpx && hasClaude,
    already_installed: installedServers.includes("memory-bank")
  };
}

/**
 * Install Memory Bank MCP server if requirements are met
 * @returns {boolean} True if installed or already present, false otherwise
 */
async function installMemoryBankMcp() {
  const memoryBankStatus = checkMemoryBankMcp();

  if (memoryBankStatus.already_installed) {
    console.log(color("✓ Memory Bank MCP already installed", colors.green));
    config.memory_bank_mcp.enabled = true;
    return true;
  }

  if (!memoryBankStatus.available) {
    const missing = [];
    if (!memoryBankStatus.npx) missing.push("npx");
    if (!memoryBankStatus.claude) missing.push("claude");

    console.log(color(`⚠️  Memory Bank MCP requirements not met. Missing: ${missing.join(", ")}`, colors.yellow));
    console.log(color("   Install Node.js for npx: https://nodejs.org", colors.dim));
    console.log(color("   Ensure Claude Code CLI is available: claude --version", colors.dim));
    return false;
  }

  console.log(color("Installing Memory Bank MCP via Smithery...", colors.cyan));

  try {
    // Use empty string to bypass API key requirement
    execSync('echo "" | npx -y @smithery/cli install @alioshr/memory-bank-mcp --client claude', {
      shell: true,
      stdio: 'pipe'
    });

    console.log(color("✓ Memory Bank MCP installed successfully", colors.green));
    config.memory_bank_mcp.enabled = true;
    return true;
  } catch (error) {
    console.log(color("⚠️ Memory Bank MCP installation failed", colors.yellow));
    console.log(color("  You can manually install later with:", colors.dim));
    console.log(color('  echo "" | npx -y @smithery/cli install @alioshr/memory-bank-mcp --client claude', colors.dim));
    return false;
  }
}

/**
 * Setup automatic file discovery and sync for Memory Bank MCP
 * @returns {boolean} True if setup completed successfully
 */
async function setupMemoryBankFiles() {
  try {
    console.log(color("\n  📄 File Synchronization Setup", colors.cyan));
    console.log(color("  Discovering important project documentation for persistent context...", colors.dim));
    console.log();

    // Auto-discovery patterns
    const discoveryPatterns = {
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
    };

    const discoveredFiles = { Configuration: [], Documentation: [], Requirements: [] };

    // Scan project for files
    for (const [category, patterns] of Object.entries(discoveryPatterns)) {
      for (const pattern of patterns) {
        if (pattern.includes('*')) {
          // Use glob for wildcard patterns
          const glob = require('glob');
          const matches = glob.sync(pattern, { cwd: process.cwd(), absolute: false });

          for (const match of matches) {
            const filePath = path.join(process.cwd(), match);
            if (fs.existsSync(filePath) && path.extname(match).toLowerCase() === '.md') {
              const stats = fs.statSync(filePath);
              const isDuplicate = Object.values(discoveredFiles)
                .flat()
                .some(f => f.path === match);

              if (!isDuplicate) {
                discoveredFiles[category].push({
                  path: match,
                  exists: true,
                  size: stats.size
                });
              }
            }
          }
        } else {
          // Direct file check
          const filePath = path.join(process.cwd(), pattern);
          if (fs.existsSync(filePath)) {
            const stats = fs.statSync(filePath);
            const isDuplicate = Object.values(discoveredFiles)
              .flat()
              .some(f => f.path === pattern);

            if (!isDuplicate) {
              discoveredFiles[category].push({
                path: pattern,
                exists: true,
                size: stats.size
              });
            }
          }
        }
      }
    }

    // Display discovered files
    const totalDiscovered = Object.values(discoveredFiles)
      .reduce((sum, files) => sum + files.length, 0);

    if (totalDiscovered === 0) {
      console.log(color("  ⚠️ No documentation files auto-discovered", colors.yellow));
      console.log(color("  You can add files manually below", colors.dim));
    } else {
      console.log(color(`  ✓ Auto-discovered ${totalDiscovered} documentation files:`, colors.green));
      console.log();

      for (const [category, files] of Object.entries(discoveredFiles)) {
        if (files.length > 0) {
          console.log(color(`  ${category}:`, colors.cyan));
          for (const fileInfo of files) {
            const sizeKb = (fileInfo.size / 1024).toFixed(1);
            console.log(color(`    ✓ ${fileInfo.path} (${sizeKb}KB)`, colors.green));
          }
        }
      }

      console.log();
      if (await askYesNo("  Add all auto-discovered files to Memory Bank sync?", true)) {
        // Add all discovered files to sync configuration
        for (const [category, files] of Object.entries(discoveredFiles)) {
          for (const fileInfo of files) {
            const syncFile = {
              path: fileInfo.path,
              status: "pending",
              last_synced: null,
              category: category.toLowerCase()
            };
            config.memory_bank_mcp.sync_files.push(syncFile);
          }
        }

        console.log(color(`  ✓ Added ${totalDiscovered} files to sync configuration`, colors.green));
      } else {
        console.log(color("  Skipped auto-discovered files", colors.dim));
      }
    }

    // Manual file addition
    console.log();
    console.log(color("  Additional files:", colors.cyan));
    console.log(color('  Add specific markdown files for persistent context (e.g., "docs/api.md")', colors.dim));
    console.log();

    while (true) {
      const filePath = await question(color("  Add markdown file (Enter path relative to project root, or Enter to finish): ", colors.cyan));
      if (!filePath) {
        break;
      }

      // Skip if already added
      const isDuplicate = config.memory_bank_mcp.sync_files.some(f => f.path === filePath);
      if (isDuplicate) {
        console.log(color(`  ⚠️ File already added: ${filePath}`, colors.yellow));
        continue;
      }

      // Validate file exists and is markdown
      const fullPath = path.join(process.cwd(), filePath);
      if (!fs.existsSync(fullPath)) {
        console.log(color(`  ⚠️ File not found: ${filePath}`, colors.yellow));
        continue;
      }
      if (!filePath.toLowerCase().endsWith('.md')) {
        console.log(color("  ⚠️ Only markdown files (.md) are supported", colors.yellow));
        continue;
      }

      // Add to sync files configuration
      const syncFile = {
        path: filePath,
        status: "pending",
        last_synced: null,
        category: "manual"
      };
      config.memory_bank_mcp.sync_files.push(syncFile);
      console.log(color(`  ✓ Added: "${filePath}"`, colors.green));
    }

    // Summary
    const totalSyncFiles = config.memory_bank_mcp.sync_files.length;
    if (totalSyncFiles > 0) {
      console.log();
      console.log(color(`  📋 Total files configured for sync: ${totalSyncFiles}`, colors.cyan));
      console.log(color("  Use /sync-all to sync all files to Memory Bank", colors.dim));
      console.log(color("  Files will auto-load in future sessions for persistent context", colors.dim));
    }

    return true;

  } catch (error) {
    console.log(color("  ⚠️ Error during Memory Bank file configuration", colors.yellow));
    console.log(color(`    Error: ${error.message}`, colors.dim));
    console.log(color("    Memory Bank MCP server is still functional", colors.green));
    return false;
  }
}

// Check dependencies
async function checkDependencies() {
  console.log(color('Checking dependencies...', colors.cyan));
  
  // Check Python
  const hasPython = commandExists('python3') || commandExists('python');
  if (!hasPython) {
    console.log(color('❌ Python 3 is required but not installed.', colors.red));
    process.exit(1);
  }
  
  // Check pip
  const hasPip = commandExists('pip3') || commandExists('pip');
  if (!hasPip) {
    console.log(color('❌ pip is required but not installed.', colors.red));
    process.exit(1);
  }
  
  // Check Git (warning only)
  if (!commandExists('git')) {
    console.log(color('⚠️  Warning: Not in a git repository. Sessions works best with git.', colors.yellow));
    if (!(await askYesNo('Continue anyway?', false))) {
      process.exit(1);
    }
  }
}

// Create directory structure
async function createDirectories() {
  console.log(color('Creating directory structure...', colors.cyan));
  
  const dirs = [
    '.claude/hooks',
    '.claude/state',
    '.claude/agents',
    '.claude/commands',
    'sessions/tasks/done',
    'sessions/protocols',
    'sessions/knowledge'
  ];
  
  for (const dir of dirs) {
    await fs.mkdir(path.join(PROJECT_ROOT, dir), { recursive: true });
  }
}

// Install Python dependencies
async function installPythonDeps() {
  console.log(color('Installing Python dependencies...', colors.cyan));
  try {
    const pipCommand = commandExists('pip3') ? 'pip3' : 'pip';
    execSync(`${pipCommand} install tiktoken --quiet`, { stdio: 'ignore' });
  } catch (error) {
    console.log(color('⚠️  Could not install tiktoken. You may need to install it manually.', colors.yellow));
  }
}

// Copy files with proper permissions
async function copyFiles() {
  console.log(color('Installing hooks...', colors.cyan));
  const hookFiles = await fs.readdir(path.join(SCRIPT_DIR, 'cc_sessions/hooks'));
  for (const file of hookFiles) {
    if (file.endsWith('.py')) {
      await fs.copyFile(
        path.join(SCRIPT_DIR, 'cc_sessions/hooks', file),
        path.join(PROJECT_ROOT, '.claude/hooks', file)
      );
      if (process.platform !== 'win32') {
        await fs.chmod(path.join(PROJECT_ROOT, '.claude/hooks', file), 0o755);
      }
    }
  }
  
  console.log(color('Installing protocols...', colors.cyan));
  const protocolFiles = await fs.readdir(path.join(SCRIPT_DIR, 'cc_sessions/protocols'));
  for (const file of protocolFiles) {
    if (file.endsWith('.md')) {
      await fs.copyFile(
        path.join(SCRIPT_DIR, 'cc_sessions/protocols', file),
        path.join(PROJECT_ROOT, 'sessions/protocols', file)
      );
    }
  }
  
  console.log(color('Installing agent definitions...', colors.cyan));
  const agentFiles = await fs.readdir(path.join(SCRIPT_DIR, 'cc_sessions/agents'));
  for (const file of agentFiles) {
    if (file.endsWith('.md')) {
      await fs.copyFile(
        path.join(SCRIPT_DIR, 'cc_sessions/agents', file),
        path.join(PROJECT_ROOT, '.claude/agents', file)
      );
    }
  }
  
  console.log(color('Installing templates...', colors.cyan));
  await fs.copyFile(
    path.join(SCRIPT_DIR, 'cc_sessions/templates/TEMPLATE.md'),
    path.join(PROJECT_ROOT, 'sessions/tasks/TEMPLATE.md')
  );
  
  console.log(color('Installing commands...', colors.cyan));
  const commandFiles = await fs.readdir(path.join(SCRIPT_DIR, 'cc_sessions/commands'));
  for (const file of commandFiles) {
    if (file.endsWith('.md') || file.endsWith('.py')) {
      await fs.copyFile(
        path.join(SCRIPT_DIR, 'cc_sessions/commands', file),
        path.join(PROJECT_ROOT, '.claude/commands', file)
      );

      // Make Python commands executable on Unix
      if (file.endsWith('.py') && process.platform !== 'win32') {
        await fs.chmod(path.join(PROJECT_ROOT, '.claude/commands', file), 0o755);
      }
    }
  }
  
  // Copy knowledge files if they exist
  const knowledgePath = path.join(SCRIPT_DIR, 'cc_sessions/knowledge/claude-code');
  try {
    await fs.access(knowledgePath);
    console.log(color('Installing Claude Code knowledge base...', colors.cyan));
    await copyDir(knowledgePath, path.join(PROJECT_ROOT, 'sessions/knowledge/claude-code'));
  } catch {
    // Knowledge files don't exist, skip
  }
}

// Recursive directory copy
async function copyDir(src, dest) {
  await fs.mkdir(dest, { recursive: true });
  const entries = await fs.readdir(src, { withFileTypes: true });
  
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    
    if (entry.isDirectory()) {
      await copyDir(srcPath, destPath);
    } else {
      await fs.copyFile(srcPath, destPath);
    }
  }
}

// Install daic command
async function installDaicCommand() {
  console.log(color('Installing daic command...', colors.cyan));
  
  if (process.platform === 'win32') {
    // Windows installation
    const daicCmdSource = path.join(SCRIPT_DIR, 'cc_sessions/scripts/daic.cmd');
    const daicPs1Source = path.join(SCRIPT_DIR, 'cc_sessions/scripts/daic.ps1');
    
    // Install to user's local directory
    const localBin = path.join(process.env.USERPROFILE || process.env.HOME, 'AppData', 'Local', 'cc-sessions', 'bin');
    await fs.mkdir(localBin, { recursive: true });
    
    try {
      // Copy .cmd script
      await fs.access(daicCmdSource);
      const daicCmdDest = path.join(localBin, 'daic.cmd');
      await fs.copyFile(daicCmdSource, daicCmdDest);
      console.log(color(`  ✓ Installed daic.cmd to ${localBin}`, colors.green));
    } catch {
      console.log(color('  ⚠️ daic.cmd script not found', colors.yellow));
    }
    
    try {
      // Copy .ps1 script
      await fs.access(daicPs1Source);
      const daicPs1Dest = path.join(localBin, 'daic.ps1');
      await fs.copyFile(daicPs1Source, daicPs1Dest);
      console.log(color(`  ✓ Installed daic.ps1 to ${localBin}`, colors.green));
    } catch {
      console.log(color('  ⚠️ daic.ps1 script not found', colors.yellow));
    }
    
    console.log(color(`  ℹ Add ${localBin} to your PATH to use 'daic' command`, colors.yellow));
  } else {
    // Unix/Mac installation
    const daicSource = path.join(SCRIPT_DIR, 'cc_sessions/scripts/daic');
    const daicDest = '/usr/local/bin/daic';
    
    try {
      await fs.copyFile(daicSource, daicDest);
      await fs.chmod(daicDest, 0o755);
    } catch (error) {
      if (error.code === 'EACCES') {
        console.log(color('⚠️  Cannot write to /usr/local/bin. Trying with sudo...', colors.yellow));
        try {
          execSync(`sudo cp ${daicSource} ${daicDest}`, { stdio: 'inherit' });
          execSync(`sudo chmod +x ${daicDest}`, { stdio: 'inherit' });
        } catch {
          console.log(color('⚠️  Could not install daic command globally. You can run it locally from .claude/scripts/', colors.yellow));
        }
      }
    }
  }
}

// Interactive menu with keyboard navigation
async function interactiveMenu(items, options = {}) {
  const {
    title = 'Select an option',
    multiSelect = false,
    selectedItems = new Set(),
    formatItem = (item, selected) => item
  } = options;
  
  let currentIndex = 0;
  let selected = new Set(selectedItems);
  let done = false;
  
  // Hide cursor
  process.stdout.write('\x1B[?25l');
  
  const renderMenu = () => {
    // Clear previous menu
    console.clear();
    
    // Render title
    if (title) {
      console.log(title);
    }
    
    // Render items
    items.forEach((item, index) => {
      const isSelected = selected.has(item);
      const isCurrent = index === currentIndex;
      
      let prefix = '  ';
      if (isCurrent) {
        prefix = color('▶ ', colors.cyan);
      }
      
      console.log(prefix + formatItem(item, isSelected, isCurrent));
    });
  };
  
  return new Promise((resolve) => {
    renderMenu();
    
    // Set raw mode for key input
    readline.emitKeypressEvents(process.stdin);
    if (process.stdin.setRawMode) {
      process.stdin.setRawMode(true);
    }
    process.stdin.resume();
    
    const keyHandler = (str, key) => {
      if (key) {
        if (key.name === 'up') {
          currentIndex = (currentIndex - 1 + items.length) % items.length;
          renderMenu();
        } else if (key.name === 'down') {
          currentIndex = (currentIndex + 1) % items.length;
          renderMenu();
        } else if (key.name === 'space' && multiSelect) {
          const item = items[currentIndex];
          if (selected.has(item)) {
            selected.delete(item);
          } else {
            selected.add(item);
          }
          renderMenu();
        } else if (key.name === 'return') {
          done = true;
          // Restore terminal
          if (process.stdin.setRawMode) {
            process.stdin.setRawMode(false);
          }
          process.stdin.removeListener('keypress', keyHandler);
          process.stdout.write('\x1B[?25h'); // Show cursor
          console.clear();
          
          // Resume stdin for subsequent prompts (don't pause!)
          process.stdin.resume();
          
          if (multiSelect) {
            resolve(selected);
          } else {
            resolve(items[currentIndex]);
          }
        } else if (key.ctrl && key.name === 'c') {
          // Handle Ctrl+C
          if (process.stdin.setRawMode) {
            process.stdin.setRawMode(false);
          }
          process.stdin.pause();
          process.stdout.write('\x1B[?25h'); // Show cursor
          process.exit(0);
        }
      }
    };
    
    process.stdin.on('keypress', keyHandler);
  });
}

// Tool blocking menu
async function configureToolBlocking() {
  const allTools = [
    ['Edit', 'Edit existing files'],
    ['Write', 'Create new files'],
    ['MultiEdit', 'Multiple edits in one operation'],
    ['NotebookEdit', 'Edit Jupyter notebooks'],
    ['Bash', 'Run shell commands'],
    ['Read', 'Read file contents'],
    ['Grep', 'Search file contents'],
    ['Glob', 'Find files by pattern'],
    ['LS', 'List directory contents'],
    ['WebSearch', 'Search the web'],
    ['WebFetch', 'Fetch web content'],
    ['Task', 'Launch specialized agents']
  ];

  // Show current status first
  console.log(color('  Available tools:', colors.white));
  for (let i = 0; i < allTools.length; i++) {
    const [name, desc] = allTools[i];
    const isBlocked = config.blocked_tools.includes(name);
    const icon = isBlocked ? '❌' : '✅';
    const statusText = isBlocked ? 'BLOCKED' : 'ALLOWED';
    const statusColor = isBlocked ? colors.red : colors.green;

    console.log(`    ${i + 1:2}. ${icon} ${color(name.padEnd(15), colors.white)} - ${desc}`);
    console.log(`         ${color(statusText, statusColor)}`);
  }
  console.log();
  console.log(color('  Select tools to BLOCK in discussion mode (blocked tools enforce DAIC workflow)', colors.dim));
  console.log();

  // Offer interactive mode
  if (await askYesNo('  🎮 Try interactive tool selector (arrow keys + space to toggle)?', true)) {
    console.log(color('  Starting interactive tool selection...', colors.dim));
    const blockedTools = await interactiveToolSelection(allTools, config.blocked_tools);

    if (blockedTools !== null) {
      config.blocked_tools = blockedTools;
      console.log(color(`  ✓ Tool blocking configuration saved (${blockedTools.length} tools blocked)`, colors.green));
    } else {
      console.log(color('  Interactive mode cancelled or failed, trying classic mode...', colors.yellow));
      // Automatically fall back to classic mode
      if (await askYesNo('  Modify blocked tools list (numbered input)?', true)) {
        const numbers = await question(color('  Enter comma-separated tool numbers to block: ', colors.cyan));
        if (numbers.trim()) {
          const blockedList = [];
          numbers.split(',').forEach(numStr => {
            const num = parseInt(numStr.trim());
            if (num >= 1 && num <= allTools.length) {
              blockedList.push(allTools[num - 1][0]);
            }
          });
          if (blockedList.length > 0) {
            config.blocked_tools = blockedList;
            console.log(color('  ✓ Tool blocking configuration saved', colors.green));
          }
        }
      }
    }
  } else {
    // Fallback to classic numbered input
    const numbers = await question(color('  Enter comma-separated tool numbers to block: ', colors.cyan));
    if (numbers.trim()) {
      const blockedList = [];
      numbers.split(',').forEach(numStr => {
        const num = parseInt(numStr.trim());
        if (num >= 1 && num <= allTools.length) {
          blockedList.push(allTools[num - 1][0]);
        }
      });
      if (blockedList.length > 0) {
        config.blocked_tools = blockedList;
        console.log(color('  ✓ Tool blocking configuration saved', colors.green));
      }
    }
  }
}

// Interactive configuration
async function configure() {
  console.log();
  console.log(color('╔═══════════════════════════════════════════════════════════════╗', colors.bright + colors.cyan));
  console.log(color('║                    CONFIGURATION SETUP                        ║', colors.bright + colors.cyan));
  console.log(color('╚═══════════════════════════════════════════════════════════════╝', colors.bright + colors.cyan));
  console.log();
  
  let statuslineInstalled = false;
  
  // Developer name section
  console.log(color(`\n${icons.star} DEVELOPER IDENTITY`, colors.bright + colors.magenta));
  console.log(color('─'.repeat(60), colors.dim));
  console.log(color('  Claude will use this name when addressing you in sessions', colors.dim));
  console.log();
  
  const name = await question(color('  Your name: ', colors.cyan));
  if (name) {
    config.developer_name = name;
    console.log(color(`  ${icons.check} Hello, ${name}!`, colors.green));
  }
  
  // Statusline installation section
  console.log(color(`\n\n${icons.star} STATUSLINE INSTALLATION`, colors.bright + colors.magenta));
  console.log(color('─'.repeat(60), colors.dim));
  console.log(color('  Real-time status display in Claude Code showing:', colors.white));
  console.log(color(`    ${icons.bullet} Current task and DAIC mode`, colors.cyan));
  console.log(color(`    ${icons.bullet} Token usage with visual progress bar`, colors.cyan));
  console.log(color(`    ${icons.bullet} Modified file counts`, colors.cyan));
  console.log(color(`    ${icons.bullet} Open task count`, colors.cyan));
  console.log();

  if (await askYesNo('  Install statusline?', false)) {
    const statuslineSource = path.join(SCRIPT_DIR, 'cc_sessions/scripts/statusline-script.sh');
    try {
      await fs.access(statuslineSource);
      console.log(color('  Installing statusline script...', colors.dim));
      await fs.copyFile(statuslineSource, path.join(PROJECT_ROOT, '.claude/statusline-script.sh'));
      await fs.chmod(path.join(PROJECT_ROOT, '.claude/statusline-script.sh'), 0o755);
      statuslineInstalled = true;
      console.log(color(`  ${icons.check} Statusline installed successfully`, colors.green));
    } catch {
      console.log(color(`  ${icons.warning} Statusline script not found in package`, colors.yellow));
    }
  }
  
  // DAIC trigger phrases section
  console.log(color(`\n\n${icons.star} DAIC WORKFLOW CONFIGURATION`, colors.bright + colors.magenta));
  console.log(color('─'.repeat(60), colors.dim));
  console.log(color('  The DAIC system enforces discussion before implementation.', colors.white));
  console.log(color('  Trigger phrases tell Claude when you\'re ready to proceed.', colors.white));
  console.log();
  console.log(color('  Default triggers:', colors.cyan));
  config.trigger_phrases.forEach(phrase => {
    console.log(color(`    ${icons.arrow} "${phrase}"`, colors.green));
  });
  console.log();
  console.log(color('  Hint: Common additions: "implement it", "do it", "proceed"', colors.dim));
  console.log();
  
  // Allow adding multiple custom trigger phrases
  let addingTriggers = true;
  while (addingTriggers) {
    const customTrigger = await question(color('  Add custom trigger phrase (Enter to skip): ', colors.cyan));
    if (customTrigger) {
      config.trigger_phrases.push(customTrigger);
      console.log(color(`  ${icons.check} Added: "${customTrigger}"`, colors.green));
    } else {
      addingTriggers = false;
    }
  }
  
  // API Mode configuration
  console.log(color(`\n\n${icons.star} THINKING BUDGET CONFIGURATION`, colors.bright + colors.magenta));
  console.log(color('─'.repeat(60), colors.dim));
  console.log(color('  Token usage is not much of a concern with Claude Code Max', colors.white));
  console.log(color('  plans, especially the $200 tier. But API users are often', colors.white));
  console.log(color('  budget-conscious and want manual control.', colors.white));
  console.log();
  console.log(color('  Sessions was built to preserve tokens across context windows', colors.cyan));
  console.log(color('  but uses saved tokens to enable \'ultrathink\' - Claude\'s', colors.cyan));
  console.log(color('  maximum thinking budget - on every interaction for best results.', colors.cyan));
  console.log();
  console.log(color('  • Max users (recommended): Automatic ultrathink every message', colors.dim));
  console.log(color('  • API users: Manual control with [[ ultrathink ]] when needed', colors.dim));
  console.log();
  console.log(color('  You can toggle this anytime with: /api-mode', colors.dim));
  console.log();

  if (await askYesNo('  Enable automatic ultrathink for best performance?', false)) {
    config.api_mode = false;
    console.log(color(`  ${icons.check} Max mode - ultrathink enabled for best performance`, colors.green));
  } else {
    config.api_mode = true;
    console.log(color(`  ${icons.check} API mode - manual ultrathink control (use [[ ultrathink ]])`, colors.green));
  }
  
  // Advanced configuration
  console.log(color(`\n\n${icons.star} ADVANCED OPTIONS`, colors.bright + colors.magenta));
  console.log(color('─'.repeat(60), colors.dim));
  console.log(color('  Configure tool blocking, task prefixes, and more', colors.white));
  console.log();

  if (await askYesNo('  Configure advanced options?', false)) {
    await configureToolBlocking();
    
    // Task prefix configuration
    console.log(color(`\n\n${icons.star} TASK PREFIX CONFIGURATION`, colors.bright + colors.magenta));
    console.log(color('─'.repeat(60), colors.dim));
    console.log(color('  Task prefixes organize work by priority and type', colors.white));
    console.log();
    console.log(color('  Current prefixes:', colors.cyan));
    console.log(color(`    ${icons.arrow} h- (high priority)`, colors.white));
    console.log(color(`    ${icons.arrow} m- (medium priority)`, colors.white));
    console.log(color(`    ${icons.arrow} l- (low priority)`, colors.white));
    console.log(color(`    ${icons.arrow} ?- (investigate/research)`, colors.white));
    console.log();

    if (await askYesNo('  Customize task prefixes?', false)) {
      const high = await question(color('  High priority prefix [h-]: ', colors.cyan)) || 'h-';
      const med = await question(color('  Medium priority prefix [m-]: ', colors.cyan)) || 'm-';
      const low = await question(color('  Low priority prefix [l-]: ', colors.cyan)) || 'l-';
      const inv = await question(color('  Investigate prefix [?-]: ', colors.cyan)) || '?-';
      
      config.task_prefixes = {
        priority: [high, med, low, inv]
      };
      
      console.log(color(`  ${icons.check} Task prefixes updated`, colors.green));
    }
  }
  
  return { statuslineInstalled };
}

// Save configuration
async function saveConfig(installStatusline = false) {
  console.log(color('Creating configuration...', colors.cyan));

  // Add version to config before saving
  config.version = getCurrentPackageVersion();

  await fs.writeFile(
    path.join(PROJECT_ROOT, 'sessions/sessions-config.json'),
    JSON.stringify(config, null, 2)
  );
  
  // Create or update .claude/settings.json with hooks configuration
  const settingsPath = path.join(PROJECT_ROOT, '.claude/settings.json');
  let settings = {};
  
  // Check if settings.json already exists
  try {
    const existingSettings = await fs.readFile(settingsPath, 'utf-8');
    settings = JSON.parse(existingSettings);
    console.log(color('Found existing settings.json, merging sessions hooks...', colors.cyan));
  } catch {
    console.log(color('Creating new settings.json with sessions hooks...', colors.cyan));
  }
  
  // Define the sessions hooks
  const sessionsHooks = {
    UserPromptSubmit: [
      {
        hooks: [
          {
            type: "command",
            command: process.platform === 'win32' ? "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\user-messages.py\"" : "$CLAUDE_PROJECT_DIR/.claude/hooks/user-messages.py"
          },
          {
            type: "command",
            command: process.platform === 'win32' ? "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\task-completion-workflow.py\"" : "$CLAUDE_PROJECT_DIR/.claude/hooks/task-completion-workflow.py"
          }
        ]
      }
    ],
    PreToolUse: [
      {
        matcher: "Write|Edit|MultiEdit|Task|Bash",
        hooks: [
          {
            type: "command",
            command: process.platform === 'win32' ? "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\sessions-enforce.py\"" : "$CLAUDE_PROJECT_DIR/.claude/hooks/sessions-enforce.py"
          }
        ]
      },
      {
        matcher: "Task",
        hooks: [
          {
            type: "command",
            command: process.platform === 'win32' ? "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\task-transcript-link.py\"" : "$CLAUDE_PROJECT_DIR/.claude/hooks/task-transcript-link.py"
          }
        ]
      }
    ],
    PostToolUse: [
      {
        matcher: "Edit|Write|MultiEdit|NotebookEdit",
        hooks: [
          {
            type: "command",
            command: process.platform === 'win32' ? "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\post-implementation-retention.py\"" : "$CLAUDE_PROJECT_DIR/.claude/hooks/post-implementation-retention.py"
          }
        ]
      },
      {
        hooks: [
          {
            type: "command",
            command: process.platform === 'win32' ? "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\post-tool-use.py\"" : "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-use.py"
          }
        ]
      }
    ],
    SessionStart: [
      {
        matcher: "startup|clear",
        hooks: [
          {
            type: "command",
            command: process.platform === 'win32' ? "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\session-start.py\"" : "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.py"
          }
        ]
      }
    ]
  };
  
  // Merge hooks (sessions hooks take precedence)
  if (!settings.hooks) {
    settings.hooks = {};
  }
  
  // Merge each hook type (avoid duplicates)
  for (const [hookType, hookConfig] of Object.entries(sessionsHooks)) {
    if (!settings.hooks[hookType]) {
      settings.hooks[hookType] = hookConfig;
    } else {
      // Merge without duplicates by checking command strings
      const existingCommands = new Set();
      for (const hookEntry of settings.hooks[hookType]) {
        if (hookEntry.hooks) {
          for (const hook of hookEntry.hooks) {
            existingCommands.add(hook.command || '');
          }
        }
      }

      // Only add new hook configurations that don't exist
      for (const newHookEntry of hookConfig) {
        const entryCommands = new Set();
        if (newHookEntry.hooks) {
          for (const hook of newHookEntry.hooks) {
            entryCommands.add(hook.command || '');
          }
        }

        // If none of the commands in this entry already exist, add the whole entry
        const hasIntersection = [...entryCommands].some(cmd => existingCommands.has(cmd));
        if (!hasIntersection) {
          settings.hooks[hookType].push(newHookEntry);
          for (const cmd of entryCommands) {
            existingCommands.add(cmd);
          }
        }
      }
    }
  }
  
  // Add statusline if requested
  if (installStatusline) {
    settings.statusLine = {
      type: "command",
      command: process.platform === 'win32' ? "%CLAUDE_PROJECT_DIR%\\.claude\\statusline-script.sh" : "$CLAUDE_PROJECT_DIR/.claude/statusline-script.sh",
      padding: 0
    };
  }
  
  // Save the updated settings
  await fs.writeFile(settingsPath, JSON.stringify(settings, null, 2));
  console.log(color('✅ Sessions hooks configured in settings.json', colors.green));
  
  // Initialize DAIC state
  await fs.writeFile(
    path.join(PROJECT_ROOT, '.claude/state/daic-mode.json'),
    JSON.stringify({ mode: "discussion" }, null, 2)
  );
  
  // Create initial task state
  const currentDate = new Date().toISOString().split('T')[0];
  await fs.writeFile(
    path.join(PROJECT_ROOT, '.claude/state/current_task.json'),
    JSON.stringify({
      task: null,
      branch: null,
      services: [],
      updated: currentDate
    }, null, 2)
  );
}

// CLAUDE.md integration
async function setupClaudeMd() {
  console.log();
  console.log(color('═══════════════════════════════════════════', colors.bright));
  console.log(color('         CLAUDE.md Integration', colors.bright));
  console.log(color('═══════════════════════════════════════════', colors.bright));
  console.log();
  
  // Check for existing CLAUDE.md
  try {
    await fs.access(path.join(PROJECT_ROOT, 'CLAUDE.md'));
    
    // File exists, preserve it and add sessions as separate file
    console.log(color('CLAUDE.md already exists, preserving your project-specific rules...', colors.cyan));
    
    // Copy CLAUDE.sessions.md as separate file
    await fs.copyFile(
      path.join(SCRIPT_DIR, 'cc_sessions/templates/CLAUDE.sessions.md'),
      path.join(PROJECT_ROOT, 'CLAUDE.sessions.md')
    );
    
    // Check if it already includes sessions
    const content = await fs.readFile(path.join(PROJECT_ROOT, 'CLAUDE.md'), 'utf-8');
    if (!content.includes('@CLAUDE.sessions.md')) {
      console.log(color('Adding sessions include to existing CLAUDE.md...', colors.cyan));
      
      const addition = '\n## Sessions System Behaviors\n\n@CLAUDE.sessions.md\n';
      await fs.appendFile(path.join(PROJECT_ROOT, 'CLAUDE.md'), addition);
      
      console.log(color('✅ Added @CLAUDE.sessions.md include to your CLAUDE.md', colors.green));
    } else {
      console.log(color('✅ CLAUDE.md already includes sessions behaviors', colors.green));
    }
  } catch {
    // File doesn't exist, use sessions as CLAUDE.md
    console.log(color('No existing CLAUDE.md found, installing sessions as your CLAUDE.md...', colors.cyan));
    await fs.copyFile(
      path.join(SCRIPT_DIR, 'cc_sessions/templates/CLAUDE.sessions.md'),
      path.join(PROJECT_ROOT, 'CLAUDE.md')
    );
    console.log(color('✅ CLAUDE.md created with complete sessions behaviors', colors.green));
  }
}

// Main installation function
async function install() {
  console.log(color('╔════════════════════════════════════════════╗', colors.bright));
  console.log(color('║            cc-sessions Installer           ║', colors.bright));
  console.log(color('╚════════════════════════════════════════════╝', colors.bright));
  console.log();

  // Detect correct project directory
  await detectProjectDirectory();

  // Check for existing installation
  existingInstallation = detectExistingInstallation();

  if (existingInstallation) {
    console.log(color('Existing installation detected!', colors.yellow));
    console.log();

    const choice = await showInstallationMenu();

    switch (choice) {
      case 'update':
        await runUpdate();
        return;

      case 'fresh':
        console.log(color('\n🔄 Performing fresh installation...', colors.cyan));
        console.log(color('This will reset your configuration to defaults', colors.yellow));
        console.log();
        if (!(await askYesNo('Are you sure?', false))) {
          console.log(color('Installation cancelled', colors.dim));
          return;
        }
        // Continue with fresh installation below
        break;

      case 'repair':
        await runRepair();
        return;

      case 'exit':
        console.log(color('No changes made', colors.dim));
        return;
    }
  }

  // Check CLAUDE_PROJECT_DIR
  if (!process.env.CLAUDE_PROJECT_DIR) {
    console.log(color(`⚠️  CLAUDE_PROJECT_DIR not set. Setting it to ${PROJECT_ROOT}`, colors.yellow));
    console.log('   To make this permanent, add to your shell profile:');
    console.log(`   export CLAUDE_PROJECT_DIR="${PROJECT_ROOT}"`);
    console.log();
  }

  try {
    await checkDependencies();
    await createDirectories();
    await installPythonDeps();
    await copyFiles();
    await installDaicCommand();

    // Optional MCP integrations
    console.log();
    console.log(color('🔌 Optional MCP Integrations', colors.bright + colors.cyan));
    console.log(color('─────────────────────────────', colors.dim));
    const memoryBankInstalled = await installMemoryBankMcp();

    // Setup Memory Bank file sync if installation successful
    if (memoryBankInstalled) {
      await setupMemoryBankFiles();
    }

    const { statuslineInstalled } = await configure();

    // Set version for fresh installation
    config.version = getCurrentPackageVersion();

    await saveConfig(statuslineInstalled);
    await setupClaudeMd();
    
    // Success message
    console.log();
    console.log();
    console.log(color('╔═══════════════════════════════════════════════════════════════╗', colors.bright + colors.green));
    console.log(color('║                 🎉 INSTALLATION COMPLETE! 🎉                  ║', colors.bright + colors.green));
    console.log(color('╚═══════════════════════════════════════════════════════════════╝', colors.bright + colors.green));
    console.log();
    
    console.log(color('  Installation Summary:', colors.bright + colors.cyan));
    console.log(color('  ─────────────────────', colors.dim));
    console.log(color(`  ${icons.check} Directory structure created`, colors.green));
    console.log(color(`  ${icons.check} Hooks installed and configured`, colors.green));
    console.log(color(`  ${icons.check} Protocols and agents deployed`, colors.green));
    console.log(color(`  ${icons.check} daic command available globally`, colors.green));
    console.log(color(`  ${icons.check} Configuration saved`, colors.green));
    console.log(color(`  ${icons.check} DAIC state initialized (Discussion mode)`, colors.green));
    
    if (statuslineInstalled) {
      console.log(color(`  ${icons.check} Statusline configured`, colors.green));
    }

    if (memoryBankInstalled) {
      console.log(color(`  ${icons.check} Memory Bank MCP installed for persistent context`, colors.green));
    }
    
    console.log();
    
    // Test daic command
    if (commandExists('daic')) {
      console.log(color(`  ${icons.check} daic command verified and working`, colors.green));
    } else {
      console.log(color(`  ${icons.warning} daic command not in PATH`, colors.yellow));
      console.log(color('       Add /usr/local/bin to your PATH', colors.dim));
    }
    
    console.log();
    console.log(color(`  ${icons.star} NEXT STEPS`, colors.bright + colors.magenta));
    console.log(color('  ─────────────', colors.dim));
    console.log();
    console.log(color('  1. Restart Claude Code to activate the sessions hooks', colors.white));
    console.log(color('     ' + icons.arrow + ' Close and reopen Claude Code', colors.dim));
    console.log();
    console.log(color('  2. Create your first task:', colors.white));
    console.log(color('     ' + icons.arrow + ' Tell Claude: "Create a new task"', colors.cyan));
    console.log(color('     ' + icons.arrow + ' Or: "Create a task for implementing feature X"', colors.cyan));
    console.log();
    console.log(color('  3. Start working with the DAIC workflow:', colors.white));
    console.log(color('     ' + icons.arrow + ' Discuss approach first', colors.dim));
    console.log(color('     ' + icons.arrow + ' Say "make it so" to implement', colors.dim));
    console.log(color('     ' + icons.arrow + ' Run "daic" to return to discussion', colors.dim));
    console.log();
    console.log(color('  ──────────────────────────────────────────────────────', colors.dim));
    console.log();
    console.log(color(`  Welcome aboard, ${config.developer_name}! 🚀`, colors.bright + colors.cyan));
    
  } catch (error) {
    console.error(color(`❌ Installation failed: ${error.message}`, colors.red));
    process.exit(1);
  } finally {
    rl.close();
  }
}

// Run installation
if (require.main === module) {
  install().catch(error => {
    console.error(color(`❌ Fatal error: ${error}`, colors.red));
    process.exit(1);
  });
}

module.exports = { install };
