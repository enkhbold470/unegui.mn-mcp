#!/usr/bin/env node

const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const packageJson = require('../package.json');

const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
  console.log(`
Unegui.mn MCP Server CLI (${packageJson.version})

Usage:
  npx unegui-mcp              Run the MCP server (STDIO mode)
  npx unegui-mcp install      Auto-configure Claude Desktop & Cursor
  npx unegui-mcp --version    Display version
  npx unegui-mcp --help       Show this help message

Description:
  Монголын хамгийн том зарын сайтын MCP сервер / MCP server for unegui.mn.
`);
  process.exit(0);
}

if (args.includes('--version') || args.includes('-v')) {
  console.log(`unegui-mcp v${packageJson.version}`);
  process.exit(0);
}

if (args.includes('install') || args.includes('--install') || args.includes('setup')) {
  installConfig();
} else {
  runServer();
}

function installConfig() {
  console.log('\n🚀 Configuring Unegui.mn MCP Server for Claude Desktop & Cursor...\n');

  const homeDir = os.homedir();
  const platform = os.platform();

  const configs = [];

  // Claude Desktop config path
  let claudePath;
  if (platform === 'darwin') {
    claudePath = path.join(homeDir, 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json');
  } else if (platform === 'win32') {
    claudePath = path.join(process.env.APPDATA || path.join(homeDir, 'AppData', 'Roaming'), 'Claude', 'claude_desktop_config.json');
  } else {
    claudePath = path.join(homeDir, '.config', 'Claude', 'claude_desktop_config.json');
  }

  configs.push({ name: 'Claude Desktop', path: claudePath });

  // Cursor config paths
  let cursorPathPrimary = path.join(homeDir, '.cursor', 'mcp.json');
  let cursorPathAlt;
  if (platform === 'darwin') {
    cursorPathAlt = path.join(homeDir, 'Library', 'Application Support', 'Cursor', 'User', 'globalStorage', 'cursor.mcp', 'mcp.json');
  } else if (platform === 'win32') {
    cursorPathAlt = path.join(process.env.APPDATA || path.join(homeDir, 'AppData', 'Roaming'), 'Cursor', 'User', 'globalStorage', 'cursor.mcp', 'mcp.json');
  } else {
    cursorPathAlt = path.join(homeDir, '.config', 'Cursor', 'User', 'globalStorage', 'cursor.mcp', 'mcp.json');
  }

  configs.push({ name: 'Cursor (~/.cursor/mcp.json)', path: cursorPathPrimary });
  configs.push({ name: 'Cursor Global Storage', path: cursorPathAlt });

  let updatedCount = 0;

  const serverConfig = {
    command: 'uvx',
    args: ['unegui-mcp']
  };

  for (const cfg of configs) {
    try {
      const dir = path.dirname(cfg.path);

      if (!fs.existsSync(dir)) {
        // If parent directory doesn't exist, only create for Claude or primary Cursor path if dir exists
        if (!cfg.name.includes('Global Storage')) {
          fs.mkdirSync(dir, { recursive: true });
        } else {
          continue;
        }
      }

      let jsonContent = {};
      if (fs.existsSync(cfg.path)) {
        try {
          const raw = fs.readFileSync(cfg.path, 'utf8');
          jsonContent = JSON.parse(raw);
        } catch (e) {
          jsonContent = {};
        }
      }

      if (!jsonContent.mcpServers) {
        jsonContent.mcpServers = {};
      }

      jsonContent.mcpServers['unegui-mcp'] = serverConfig;

      fs.writeFileSync(cfg.path, JSON.stringify(jsonContent, null, 2), 'utf8');
      console.log(`  ✅ Successfully updated ${cfg.name}:`);
      console.log(`     ${cfg.path}`);
      updatedCount++;
    } catch (err) {
      console.warn(`  ⚠️ Could not update ${cfg.name}: ${err.message}`);
    }
  }

  console.log(`\n🎉 Installation complete (${updatedCount} app configuration(s) updated).`);
  console.log('📌 Please restart Claude Desktop or Cursor to load unegui-mcp.\n');
}

function runServer() {
  const runner = findRunner();

  if (!runner) {
    console.error('❌ Error: Could not find "uvx", "pipx", or "unegui-mcp" in PATH.');
    console.error('Please install uv (https://astral.sh/uv) or pipx to run unegui-mcp:');
    console.error('  curl -LsSf https://astral.sh/uv/install.sh | sh');
    process.exit(1);
  }

  const child = spawn(runner.cmd, runner.args, {
    stdio: 'inherit',
    env: process.env
  });

  child.on('error', (err) => {
    console.error(`Failed to start ${runner.cmd}:`, err.message);
    process.exit(1);
  });

  child.on('exit', (code, signal) => {
    if (signal) {
      process.kill(process.pid, signal);
    } else {
      process.exit(code || 0);
    }
  });
}

function findRunner() {
  const isCmdAvailable = (cmd) => {
    try {
      execSync(process.platform === 'win32' ? `where ${cmd}` : `command -v ${cmd}`, { stdio: 'ignore' });
      return true;
    } catch (e) {
      return false;
    }
  };

  if (isCmdAvailable('uvx')) {
    return { cmd: 'uvx', args: ['--from', 'unegui-mcp', 'unegui-mcp', ...args] };
  }

  if (isCmdAvailable('pipx')) {
    return { cmd: 'pipx', args: ['run', 'unegui-mcp', ...args] };
  }

  if (isCmdAvailable('unegui-mcp')) {
    return { cmd: 'unegui-mcp', args: [...args] };
  }

  if (isCmdAvailable('python3')) {
    return { cmd: 'python3', args: ['-m', 'unegui_mcp.server', ...args] };
  }

  return null;
}
