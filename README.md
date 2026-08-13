# Unegui.mn MCP Сервер

**Монгол** | [English](docs/en/README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![npm](https://img.shields.io/npm/v/unegui.mn-mcp.svg)](https://www.npmjs.com/package/unegui.mn-mcp)
[![npm downloads](https://img.shields.io/npm/dm/unegui.mn-mcp.svg)](https://www.npmjs.com/package/unegui.mn-mcp)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-purple.svg)](https://modelcontextprotocol.io)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#хөгжүүлэлт)

> [unegui.mn](https://www.unegui.mn) — Монголын хамгийн том онлайн зарын платформд зориулсан MCP сервер.

Машин, үл хөдлөх, электрон бараа, ажлын байр, үйлчилгээ зэрэг **зарыг AI туслахаараа шууд хайж, үзэж, дэлгэрэнгүй мэдээлэл** авах боломжтой. **Монгол хэлээр** ажилладаг, англи хайлт ч дэмжинэ.

![MCP идэвхгүй vs unegui-mn MCP идэвхтэй харьцуулалт](docs/demo-mcp-comparison.png)

## Боломжууд

| Хэрэгсэл | Үүрэг |
|---|---|
| 🔍 `search_listings` | Түлхүүр үгээр зар хайх (Toyota, 2 өрөө гэх мэт) |
| 📂 `browse_category` | Ангиллаар зар харах (машин, үл хөдлөх, гэх мэт) |
| 📋 `get_listing_details` | Нэг зарын бүтэн мэдээлэл авах |
| 🗂️ `list_categories` | Бүх ангилал, дэд ангиллыг жагсаах |
| 🆕 `get_recent_listings` | Нүүр хуудасны хамгийн сүүлийн заруудыг авах |

## Суулгах

Шаардлага: [Node.js 18+](https://nodejs.org) болон [uv](https://astral.sh/uv).

```bash
npx -y unegui.mn-mcp install
```

Claude Desktop болон Cursor-ийн тохиргоог **автоматаар** хийнэ. Дараа нь аппыг дахин асаана уу.

## Ажиллуулах

```bash
npx -y unegui.mn-mcp
```

## MCP тохиргоо (гар аргаар)

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

> npm registry: [unegui.mn-mcp](https://www.npmjs.com/package/unegui.mn-mcp)

## Хэрэглээний жишээ

Claude Desktop эсвэл Cursor дээр MCP идэвхжсэний дараа дараах мэтийн асуулт тавьж болно:

- *"Toyota Land Cruiser 300 машин хайж өгнө үү"*
- *"Улаанбаатарт 2 өрөө орон сууц зарж байгаа байна уу?"*
- *"Хамгийн сүүлийн 10 зарыг харуулна уу"*
- *"Электрон бараа ангиллаас iPhone хайж өгнө үү"*

## Баримт бичиг

| | |
|---|---|
| [Боломжууд](docs/mn/features.md) | MCP хэрэгслүүд, дэмжигдсэн ангиллууд |
| [Хурдан эхлэл](docs/mn/quick-start.md) | Суулгах, ажиллуулах |
| [MCP тохиргоо](docs/mn/mcp-configuration.md) | Cursor, VS Code, Claude Desktop |
| [Хэрэглээний жишээ](docs/mn/usage-examples.md) | AI туслахтай харилцах жишээ |
| [Ажиллах зарчим](docs/mn/how-it-works.md) | Техникийн тойм |
| [Төслийн бүтэц](docs/mn/project-structure.md) | Файлын бүтэц |
| [Хөгжүүлэлт](docs/mn/development.md) | Тест, хувь нэмэр оруулах |
| [Анхааруулга](docs/mn/disclaimer.md) | Хариуцлага, хязгаарлалт |

## Төсөл

| | |
|---|---|
| [Хамтран хөгжүүлэх](docs/CONTRIBUTING.md) | Хувь нэмэр оруулах заавар |
| [Өөрчлөлтийн түүх](docs/CHANGELOG.md) | Хувилбарын түүх |
| [Аюулгүй байдал](docs/SECURITY.md) | Эмзэг байдлыг мэдээлэх |
| [Зөвлөмж](docs/CODE_OF_CONDUCT.md) | Оролцогчдын ёс зүй |

## Лиценз

[MIT](LICENSE) © [Enkhbold Ganbold](https://github.com/enkhbold470)

**Зохиогч:** [Enkhbold Ganbold](https://github.com/enkhbold470)
