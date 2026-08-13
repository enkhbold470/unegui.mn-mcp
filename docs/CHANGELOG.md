# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Mongolian is now the default language** across docs, MCP instructions, and API messages
- `README.md` is Mongolian; English landing page at `docs/en/README.md`
- Project docs (`CONTRIBUTING`, `CHANGELOG`, etc.) moved under `docs/`
- API responses use `message` (MN) + `message_en` (EN) instead of the reverse
- Improved README (MN + EN) with feature table and example prompts
- Expanded npm keywords for better discoverability (added `mongolian`, `ai-assistant`, `llm-tools`, `zar`, `zarlaga`, etc.)
- Improved npm package description (bilingual, more descriptive)

### Added
- MCP on/off comparison screenshot in README and usage examples
- All 8 unit tests passing (including live integration test against unegui.mn)

## [1.0.3] - 2026-08-11

### Fixed
- `npx -y unegui.mn-mcp` failed because PyPI package `unegui-mcp` was missing; CLI now runs the Python server from the npm-bundled source via `uvx --from <package>`
- Cursor/Claude launches with a minimal PATH: CLI prepends common `uv` install locations

### Changed
- npm package now ships `src/`, `pyproject.toml`, and `uv.lock`

## [1.0.2] - 2026-08-11

### Changed
- Docs and README simplified around `npx -y unegui.mn-mcp`
- `npx -y unegui.mn-mcp install` now writes `npx -y unegui.mn-mcp` into Claude Desktop / Cursor configs (was `uvx`)
- Added `CLAUDE.md` for AI assistant guidance
- English quick-start / MCP configuration docs aligned with Mongolian docs

## [1.0.0] - 2026-08-04

### Added
- Initial MCP server with five tools:
  - `search_listings`
  - `browse_category`
  - `get_listing_details`
  - `list_categories`
  - `get_recent_listings`
