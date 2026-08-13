# CLAUDE.md

Guidance for AI assistants working in this repository.

## What this is

MCP (Model Context Protocol) server for [unegui.mn](https://www.unegui.mn) — Mongolia's largest classifieds marketplace. Users search/browse listings from Claude Desktop, Cursor, or any MCP client.

- **Default language:** Mongolian (`message` + `message_en` in API responses)
- **Author:** Enkhbold Ganbold ([@enkhbold470](https://github.com/enkhbold470))
- **License:** MIT

## Packages (two registries)

| Registry | Package name | Role |
|----------|--------------|------|
| **npm** (public) | `unegui.mn-mcp` | Thin Node CLI (`bin/cli.js`) — user-facing install/run |
| **PyPI** / uv | `unegui-mcp` | Actual Python MCP server (`src/unegui_mcp/`) |

Keep the npm package **unscoped** on the default registry (`https://registry.npmjs.org`). Do not republish as `@scope/...` unless explicitly requested.

### User-facing commands (canonical)

```bash
npx -y unegui.mn-mcp install   # write MCP config for Claude Desktop + Cursor
npx -y unegui.mn-mcp           # run server (stdio)
```

MCP client config written by `install` (and shown in docs):

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

Under the hood, `bin/cli.js` runs the **bundled** Python project with `uvx --from <npm-package-root> unegui-mcp` (falls back to `uv run --directory`). It also prepends common `uv` paths so Cursor/Claude's minimal `PATH` still finds `uv`/`uvx`.

PyPI package `unegui-mcp` is optional; the npm tarball ships `src/` + `pyproject.toml` so `npx` works without a PyPI publish.

## Layout

```
unegui.mn-mcp/
├── bin/cli.js                 # npm entry: install | run | --help
├── package.json               # npm name: unegui.mn-mcp
├── pyproject.toml             # Python name: unegui-mcp, script: unegui-mcp
├── src/unegui_mcp/
│   ├── server.py              # MCP tools (stdio)
│   ├── scraper.py             # HTTP (curl_cffi) + BeautifulSoup/lxml
│   ├── categories.py          # Category keys + MN/EN labels
│   ├── i18n.py                # Bilingual strings / server instructions
│   └── __init__.py
├── tests/                     # pytest (+ fixtures)
├── docs/
│   ├── mn/                    # Mongolian guides
│   ├── en/                    # English guides
│   └── CHANGELOG.md, CONTRIBUTING.md, ...
├── README.md                  # Mongolian landing (primary)
└── CLAUDE.md                  # This file
```

## MCP tools (`server.py`)

| Tool | Purpose |
|------|---------|
| `search_listings` | Keyword search (`query`, optional `category`, `page`) |
| `browse_category` | Category / subcategory browse |
| `get_listing_details` | Full listing from URL |
| `list_categories` | All categories (MN/EN) |
| `get_recent_listings` | Homepage recent ads (`limit` 1–50) |

Server name: `unegui-mn`. Entry: `unegui_mcp.server:main` → `mcp.run_stdio_async()`.

## Dev commands

```bash
uv sync --extra dev
uv run unegui-mcp          # local stdio server
uv run pytest              # unit tests
# markers: integration = live network (not CI)
```

Node side (no deps): `node bin/cli.js --help`

## Docs conventions

- Root `README.md` = Mongolian; English mirror = `docs/en/README.md`
- Keep install docs centered on `npx -y unegui.mn-mcp` (not scoped packages)
- When changing CLI install behavior, update: `bin/cli.js`, both READMEs, `docs/*/quick-start.md`, `docs/*/mcp-configuration.md`

## Publish checklist

1. Bump `package.json` version (npm) and/or `pyproject.toml` version (Python) as needed
2. `npm publish --access public` → registry.npmjs.org as `unegui.mn-mcp`
3. Publish Python package separately if PyPI changed (`uv publish` / hatch)
4. Update `docs/CHANGELOG.md`

## Do not

- Switch npm package back to a scoped name without an explicit request
- Add secrets, personal emails, or API keys to the repo
- Change Mongolian-as-default i18n without updating docs and response shape
