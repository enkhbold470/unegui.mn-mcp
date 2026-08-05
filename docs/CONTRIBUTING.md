# Хамтран хөгжүүлэх / Contributing

**Монгол** | [English](#english)

**unegui.mn-mcp** төсөлд хувь нэмэр оруулах сонирхол тавьсанд баярлалаа!

## Хэрхэн хувь нэмэр оруулах вэ

1. GitHub дээр **fork** хийнэ
2. Локал компьютер руу **clone** хийнэ
3. **Салбар** үүсгэнэ: `git checkout -b feat/minii-shine-zuil`
4. Шаардлагатай бол тест нэмж өөрчлөлт хийнэ
5. Тест ажиллуулна: `uv sync --extra dev && uv run pytest`
6. **Commit** хийнэ (монгол эсвэл англи мессеж)
7. `main` руу **Pull Request** нээнэ

## Хөгжүүлэлтийн тохиргоо

```bash
git clone https://github.com/enkhbold470/unegui.mn-mcp.git
cd unegui.mn-mcp
uv sync --extra dev
uv run unegui-mcp   # сервер асаж байгаа эсэхийг шалгах
uv run pytest       # unit тест
```

## Кодын зарчим

- **Python 3.12+**, type hint ашиглана
- Хэрэглэгчид харагдах текстийг `i18n.py`, `categories.py` дээр хоёр хэлээр хадгална
- **Монгол хэл default** — `message` талбар монгол, `message_en` англи
- Tool docstring-үүдэд эхлээд монгол, дараа нь англи тайлбар бичнэ
- Нууц түлхүүр, хувийн замыг commit хийхгүй
- Жижиг, тодорхой PR илүүд үзнэ

## Алдаа мэдэгдэх

- [Bug report](../.github/ISSUE_TEMPLATE/bug_report.md) загвар ашиглана
- [Feature request](../.github/ISSUE_TEMPLATE/feature_request.md) загвар ашиглана
- MCP клиент (Cursor, Claude Desktop г.м.) болон Python хувилбарыг заавал бичнэ

## Scraper өөрчлөлт

unegui.mn HTML бүтэц өөрчлөгдвөл:

1. `src/unegui_mcp/scraper.py` дээр selector шинэчилнэ
2. `tests/fixtures/` дээр fixture нэмнэ
3. `CHANGELOG.md` дээр тэмдэглэнэ

---

## English

Thank you for contributing to **unegui.mn-mcp**!

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. Create a **feature branch**: `git checkout -b feat/my-feature`
4. Make changes with tests where appropriate
5. Run tests: `uv sync --extra dev && uv run pytest`
6. **Commit** with a clear message (Mongolian or English)
7. Open a **Pull Request** against `main`

### Code guidelines

- Keep user-facing strings bilingual in `i18n.py` and `categories.py`
- **Mongolian is the default** — primary `message` fields should be in Mongolian
- Tool docstrings: Mongolian first, then English
- Do not commit secrets or personal paths
