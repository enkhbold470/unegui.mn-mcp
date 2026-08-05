# Unegui.mn MCP Server

**English** | [Монгол (Mongolian)](README.mn.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-purple.svg)](https://modelcontextprotocol.io)

> MCP server for [unegui.mn](https://www.unegui.mn) — Mongolia's largest online classifieds marketplace.

Search, browse, and retrieve detailed listings for vehicles, real estate, electronics, jobs, and more — directly from your AI assistant. Built for **English and Mongolian** queries out of the box.

**Author:** [Enkhbold Ganbold](https://github.com/enkhbold470)

---

## Features

| Tool | Description |
|------|-------------|
| `search_listings` | Search by keyword (EN/MN) |
| `browse_category` | Browse categories and subcategories |
| `get_listing_details` | Full listing details from a URL |
| `list_categories` | All categories with bilingual names |
| `get_recent_listings` | Latest listings from the homepage |

### Supported categories

| Key | English | Mongolian |
|-----|---------|-----------|
| `vehicles` | Vehicles | Тээврийн хэрэгсэл |
| `real_estate` | Real Estate | Үл хөдлөх |
| `electronics` | Electronics | Электрон бараа |
| `jobs` | Jobs | Ажлын байр |
| `services` | Services | Үйлчилгээ |
| `clothing` | Clothing & Fashion | Хувцас |
| `furniture` | Home & Furniture | Гэр ахуй |
| `pets` | Pets & Animals | Амьтан |
| `hobby` | Hobby & Leisure | Хобби, чөлөөт цаг |
| `education` | Education | Боловсрол |

---

## Quick start

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Python 3.12+

### Install

```bash
git clone https://github.com/enkhbold470/unegui.mn-mcp.git
cd unegui.mn-mcp
uv sync
```

### Run locally

```bash
uv run unegui-mcp
```

---

## MCP configuration

### Cursor / VS Code

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

### Claude Desktop

Add to `claude_desktop_config.json`:

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

> Replace `/absolute/path/to/unegui.mn-mcp` with your local clone path.

---

## Usage examples

**English**

```
Search for "Land Cruiser 300" on unegui.mn
Browse vehicles, subcategory cars_for_sale
Get details for https://www.unegui.mn/adv/12345_...
What categories are available on unegui.mn?
```

**Монгол**

```
unegui.mn дээр "Toyota Prius" хай
Орон сууц түрээслүүлэх заруудыг харуул
Өнөөдөр нэмэгдсэн машины заруудыг харуул
```

---

## How it works

unegui.mn blocks plain HTTP clients (HTTP 403). This server uses [`curl_cffi`](https://github.com/lexiforest/curl_cffi) to impersonate a real browser TLS fingerprint — the same class of protection that requires Playwright in a browser.

- **Rate limiting:** 1 second between requests (built-in)
- **Parsing:** BeautifulSoup + lxml against current unegui.mn HTML
- **Transport:** MCP over stdio

---

## Project structure

```
unegui.mn-mcp/
├── src/unegui_mcp/
│   ├── server.py        # MCP tool definitions
│   ├── scraper.py       # HTTP + HTML parsing
│   ├── categories.py    # Bilingual category map
│   └── i18n.py          # EN/MN strings
├── tests/
├── .github/             # Issue templates + CI
├── pyproject.toml
├── README.md            # English (this file)
├── README.mn.md         # Mongolian
├── CONTRIBUTING.md
└── LICENSE
```

---

## Development

```bash
# Install with dev dependencies
uv sync --extra dev

# Run unit tests (offline, no network)
uv run pytest

# Smoke test against live site (optional)
uv run pytest -m integration
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Disclaimer

This project scrapes **publicly available** data from unegui.mn. Please use responsibly:

- Respect [unegui.mn](https://www.unegui.mn) terms of service
- Do not use for commercial data harvesting
- This tool is **not affiliated with or endorsed by** unegui.mn
- Listing data belongs to its original posters

---

## License

[MIT](LICENSE) © [Enkhbold Ganbold](https://github.com/enkhbold470)
