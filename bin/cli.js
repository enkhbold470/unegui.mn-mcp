#!/usr/bin/env node

const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const packageJson = require('../package.json');
const packageRoot = path.resolve(__dirname, '..');

const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
  console.log(`
Unegui.mn MCP Server CLI (${packageJson.version})

Usage:
  npx -y unegui.mn-mcp          Run the MCP server (STDIO mode)
  npx -y unegui.mn-mcp install  Auto-configure Claude Desktop & Cursor
  bunx unegui.mn-mcp            Run using BunX
  npx -y unegui.mn-mcp --help   Show this help message

Description:
  Монголын хамгийн том зарын сайтын MCP сервер / MCP server for unegui.mn.

Requires: Node.js 18+ and uv (https://astral.sh/uv)
`);
  process.exit(0);
}

if (args.includes('--version') || args.includes('-v')) {
  console.log(`unegui.mn-mcp v${packageJson.version}`);
  process.exit(0);
}

if (args.includes('install') || args.includes('--install') || args.includes('setup')) {
  installConfig();
} else {
  runServer();
}

function enrichedEnv() {
  const home = os.homedir();
  const extra = [
    path.join(home, '.local', 'bin'),
    path.join(home, '.cargo', 'bin'),
    '/opt/homebrew/bin',
    '/usr/local/bin',
    '/home/linuxbrew/.linuxbrew/bin',
  ];
  const pathKey = process.platform === 'win32' ? 'Path' : 'PATH';
  const current = process.env[pathKey] || process.env.PATH || '';
  return {
    ...process.env,
    [pathKey]: [...extra, current].filter(Boolean).join(path.delimiter),
  };
}

function isCmdAvailable(cmd, env) {
  try {
    execSync(process.platform === 'win32' ? `where ${cmd}` : `command -v ${cmd}`, {
      stdio: 'ignore',
      env,
    });
    return true;
  } catch {
    return false;
  }
}

function installConfig() {
  console.log('\n🚀 Configuring Unegui.mn MCP Server for Claude Desktop & Cursor...\n');

  const homeDir = os.homedir();
  const platform = os.platform();
  const configs = [];

  let claudePath;
  if (platform === 'darwin') {
    claudePath = path.join(homeDir, 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json');
  } else if (platform === 'win32') {
    claudePath = path.join(process.env.APPDATA || path.join(homeDir, 'AppData', 'Roaming'), 'Claude', 'claude_desktop_config.json');
  } else {
    claudePath = path.join(homeDir, '.config', 'Claude', 'claude_desktop_config.json');
  }
  configs.push({ name: 'Claude Desktop', path: claudePath });

  const cursorPathPrimary = path.join(homeDir, '.cursor', 'mcp.json');
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

  const serverConfig = {
    command: 'npx',
    args: ['-y', 'unegui.mn-mcp'],
  };

  let updatedCount = 0;
  for (const cfg of configs) {
    try {
      const dir = path.dirname(cfg.path);
      if (!fs.existsSync(dir)) {
        if (cfg.name.includes('Global Storage')) continue;
        fs.mkdirSync(dir, { recursive: true });
      }

      let jsonContent = {};
      if (fs.existsSync(cfg.path)) {
        try {
          jsonContent = JSON.parse(fs.readFileSync(cfg.path, 'utf8'));
        } catch {
          jsonContent = {};
        }
      }
      if (!jsonContent.mcpServers) jsonContent.mcpServers = {};
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
  console.log('📌 Restart Claude Desktop or Cursor to load unegui-mcp.');
  console.log('📌 Requires uv: https://astral.sh/uv\n');
}

function runServer() {
  const env = enrichedEnv();
  const runner = findRunner(env);

  if (!runner) {
    console.error('❌ Could not start unegui.mn-mcp.');
    console.error('Install uv (required to run the Python MCP server):');
    console.error('  curl -LsSf https://astral.sh/uv/install.sh | sh');
    process.exit(1);
  }

  const child = spawn(runner.cmd, runner.args, {
    stdio: 'inherit',
    env,
  });

  child.on('error', (err) => {
    console.error(`Failed to start ${runner.cmd}:`, err.message);
    process.exit(1);
  });

  child.on('exit', (code, signal) => {
    if (signal) process.kill(process.pid, signal);
    else process.exit(code || 0);
  });
}

function hasPythonProject(root) {
  return (
    fs.existsSync(path.join(root, 'pyproject.toml')) &&
    fs.existsSync(path.join(root, 'src', 'unegui_mcp'))
  );
}

function findRunner(env) {
  // Prefer local package root (bundled in npm tarball or git checkout)
  if (hasPythonProject(packageRoot)) {
    if (isCmdAvailable('uvx', env)) {
      return { cmd: 'uvx', args: ['--from', packageRoot, 'unegui-mcp', ...args] };
    }
    if (isCmdAvailable('uv', env)) {
      return {
        cmd: 'uv',
        args: ['run', '--directory', packageRoot, 'unegui-mcp', ...args],
      };
    }
  }

  // Fallback: PyPI (if published later)
  if (isCmdAvailable('uvx', env)) {
    return { cmd: 'uvx', args: ['--from', 'unegui-mcp', 'unegui-mcp', ...args] };
  }

  if (isCmdAvailable('pipx', env)) {
    return { cmd: 'pipx', args: ['run', 'unegui-mcp', ...args] };
  }

  if (isCmdAvailable('unegui-mcp', env)) {
    return { cmd: 'unegui-mcp', args: [...args] };
  }

  return null;
}
