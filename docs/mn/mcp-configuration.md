# MCP тохиргоо

[← Буцах](../../README.md)

## ⚡ Автомат тохиргоо (Хамгийн хялбар)

Терминал дээр дараах тушаалыг ажиллуулбал Claude Desktop болон Cursor-ийн тохиргоог автоматаар хийнэ:

```bash
npx @enkhbold470/unegui-mcp install
```

## 🛠️ Гар тохиргоо

### NPX ашиглах:

```json
{
  "mcpServers": {
    "unegui-mcp": {
      "command": "npx",
      "args": ["-y", "@enkhbold470/unegui-mcp"]
    }
  }
}
```

### UVX ашиглах:

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

### Эх кодоор локал ажиллуулах (Cursor / Claude Desktop):

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

