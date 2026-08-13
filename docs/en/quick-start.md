# Quick start

[← Back](README.md)

## Prerequisites

- Node.js 18+ (for `npx`)
- [uv](https://docs.astral.sh/uv/) (used under the hood to run the Python MCP server)

## NPX (simplest)

```bash
# Auto-configure Claude Desktop & Cursor
npx -y unegui.mn-mcp install

# Run the MCP server (STDIO)
npx -y unegui.mn-mcp
```

## Run from source

```bash
git clone https://github.com/enkhbold470/unegui.mn-mcp.git
cd unegui.mn-mcp
uv sync
uv run unegui-mcp
```
