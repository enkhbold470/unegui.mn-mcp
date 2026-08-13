# MCP configuration

[← Back](README.md)

## Auto-configure (simplest)

```bash
npx -y unegui.mn-mcp install
```

Writes `unegui-mcp` into Claude Desktop and Cursor `mcp.json` configs.

## Manual configuration

### NPX (recommended)

```json
{
  "mcpServers": {
    "unegui-mcp": {
      "command": "npx",
      "args": ["-y", "unegui.mn-mcp"]
    }
  }
}
```

### UVX

```json
{
  "mcpServers": {
    "unegui-mcp": {
      "command": "uvx",
      "args": ["unegui-mcp"]
    }
  }
}
```

### Local clone (Cursor / Claude Desktop)

```json
{
  "mcpServers": {
    "unegui-mcp": {
      "command": "uv",
      "args": [
        "--directory", "/absolute/path/to/unegui.mn-mcp",
        "run", "unegui-mcp"
      ]
    }
  }
}
```

> Replace `/absolute/path/to/unegui.mn-mcp` with your local clone path.
