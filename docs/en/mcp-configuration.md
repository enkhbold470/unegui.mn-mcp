# MCP configuration

[← Back](../../README.en.md)

## Cursor / VS Code

Add to `.cursor/mcp.json` or `.vscode/mcp.json`:

```json
{
  "mcpServers": {
    "unegui-mn": {
      "command": "uv",
      "args": [
        "--directory", "/absolute/path/to/unegui.mn-mcp",
        "run", "unegui-mcp"
      ]
    }
  }
}
```

## Claude Desktop

Add the same block to `claude_desktop_config.json`.

> Replace `/absolute/path/to/unegui.mn-mcp` with your local clone path.
