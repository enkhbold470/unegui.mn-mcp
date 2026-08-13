# Project structure

[← Back](README.md)

```
unegui.mn-mcp/
├── bin/cli.js           # npm CLI (npx -y unegui.mn-mcp)
├── package.json         # npm: unegui.mn-mcp
├── pyproject.toml       # Python: unegui-mcp
├── src/unegui_mcp/
│   ├── server.py        # MCP tools
│   ├── scraper.py       # HTTP + HTML parsing
│   ├── categories.py    # Category list (MN/EN)
│   └── i18n.py          # Mongolian/English strings
├── tests/
├── docs/                # All documentation
│   ├── mn/              # Mongolian guides
│   ├── en/              # English guides
│   ├── CONTRIBUTING.md
│   ├── CHANGELOG.md
│   └── ...
├── README.md            # Mongolian landing page
├── CLAUDE.md            # Guidance for AI assistants
└── LICENSE
```
