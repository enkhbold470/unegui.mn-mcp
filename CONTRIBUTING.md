# Contributing / Хамтран хөгжүүлэх

**English** | [Монгол доор](#монгол)

Thank you for your interest in contributing to **unegui.mn-mcp**!

## How to contribute

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. Create a **feature branch**: `git checkout -b feat/my-feature`
4. Make your changes with tests where appropriate
5. Run tests: `uv sync --extra dev && uv run pytest`
6. **Commit** with a clear message (English or Mongolian is fine)
7. Open a **Pull Request** against `main`

## Development setup

```bash
git clone https://github.com/enkhbold470/unegui.mn-mcp.git
cd unegui.mn-mcp
uv sync --extra dev
uv run unegui-mcp   # smoke test the server starts
uv run pytest       # run unit tests
```

## Code guidelines

- **Python 3.12+** with type hints
- Keep user-facing strings bilingual (EN/MN) in `i18n.py` and `categories.py`
- Tool docstrings in `server.py` should include both English and Mongolian
- Do not commit secrets, API keys, or personal paths
- Prefer small, focused PRs

## Reporting issues

- Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) for bugs
- Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) for ideas
- Include MCP client (Cursor, Claude Desktop, etc.) and Python version

## Scraping changes

If unegui.mn changes its HTML structure:

1. Update selectors in `src/unegui_mcp/scraper.py`
2. Add or update fixtures in `tests/fixtures/`
3. Note the change in `CHANGELOG.md`

---

## Монгол

**unegui.mn-mcp** төсөлд хувь нэмэр оруулах сонирхол тавьсанд баярлалаа!

### Хэрхэн хувь нэмэр оруулах вэ

1. GitHub дээр **fork** хийнэ
2. Локал компьютер руу **clone** хийнэ
3. **Салбар** үүсгэнэ: `git checkout -b feat/minii-shine-zuil`
4. Шаардлагатай бол тест нэмж өөрчлөлт хийнэ
5. Тест ажиллуулна: `uv run pytest`
6. **Commit** хийнэ
7. `main` руу **Pull Request** нээнэ

### Кодын зарчим

- Хэрэглэгчид харагдах текстийг `i18n.py`, `categories.py` дээр хоёр хэлээр хадгална
- Нууц түлхүүр, хувийн замыг commit хийхгүй
- Жижиг, тодорхой PR илүүд үзнэ

### Алдаа мэдэгдэх

- [Bug report](.github/ISSUE_TEMPLATE/bug_report.md) загвар ашиглана
- MCP клиент (Cursor, Claude Desktop г.м.) болон Python хувилбарыг заавал бичнэ
