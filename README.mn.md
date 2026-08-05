# Unegui.mn MCP Сервер

[English](README.md) | **Монгол**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-purple.svg)](https://modelcontextprotocol.io)

> [unegui.mn](https://www.unegui.mn) — Монголын хамгийн том онлайн зарын платформд зориулсан MCP сервер.

Машин, үл хөдлөх, электрон бараа, ажлын байр зэрэг заруудыг AI туслахаараа шууд хайж, үзэж, дэлгэрэнгүй мэдээлэл авах боломжтой. **Англи болон Монгол** хэлээр хайлт хийхэд бэлэн.

**Зохиогч:** [Enkhbold Ganbold](https://github.com/enkhbold470)

---

## Боломжууд

| Хэрэгсэл | Тайлбар |
|----------|---------|
| `search_listings` | Түлхүүр үгээр хайх (EN/MN) |
| `browse_category` | Ангилал, дэд ангиллаар үзэх |
| `get_listing_details` | Зарын бүтэн мэдээлэл |
| `list_categories` | Хоёр хэлээр ангиллын жагсаалт |
| `get_recent_listings` | Нүүр хуудасны сүүлийн зарууд |

### Дэмжигдсэн ангиллууд

| Түлхүүр | Англи | Монгол |
|---------|-------|--------|
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

## Хурдан эхлэл

### Шаардлага

- [uv](https://docs.astral.sh/uv/) (зөвлөмж) эсвэл pip
- Python 3.12+

### Суулгах

```bash
git clone https://github.com/enkhbold470/unegui.mn-mcp.git
cd unegui.mn-mcp
uv sync
```

### Ажиллуулах

```bash
uv run unegui-mcp
```

---

## MCP тохиргоо

### Cursor / VS Code

`.cursor/mcp.json` эсвэл `.vscode/mcp.json` файлд нэмнэ:

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

> `/absolute/path/to/unegui.mn-mcp`-ийг өөрийн компьютер дээрх бодит замаар солино.

---

## Хэрэглээний жишээ

```
unegui.mn дээр "Land Cruiser 300" хай
Автомашин зарна ангиллыг харуул
https://www.unegui.mn/adv/12345_... зарын дэлгэрэнгүйг ав
Ямар ангиллууд байдаг вэ?
```

---

## Ажиллах зарчим

unegui.mn энгийн HTTP клиентүүдийг блоклодог (HTTP 403). Энэ сервер [`curl_cffi`](https://github.com/lexiforest/curl_cffi) ашиглан жинхэнэ хөтчийн TLS хээ ялгах боломжтой.

- **Хурдны хязгаар:** Хүсэлт хооронд 1 секунд
- **Задлах:** BeautifulSoup + lxml
- **Холболт:** MCP stdio

---

## Хөгжүүлэлт

```bash
uv sync --extra dev
uv run pytest
```

Дэлгэрэнгүй: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Анхааруулга

Энэ төсөл unegui.mn-ийн **нийтийн** мэдээллийг цуглуулдаг. Хариуцлагатай ашиглана уу:

- [unegui.mn](https://www.unegui.mn) үйлчилгээний нөхцлийг дагана уу
- Арилжааны өгөгдөл цуглуулахад бүү ашигла
- Энэ төсөл unegui.mn-тай **холбоогүй**, албан бус

---

## Лиценз

[MIT](LICENSE) © [Enkhbold Ganbold](https://github.com/enkhbold470)
