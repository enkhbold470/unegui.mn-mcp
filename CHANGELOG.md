# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Bilingual English/Mongolian documentation (`README.md`, `README.mn.md`)
- `categories.py` and `i18n.py` modules for structured EN/MN support
- Unit tests with HTML fixtures (offline)
- GitHub issue templates, PR template, and CI workflow
- `CONTRIBUTING.md` and `CODE_OF_CONDUCT.md`

### Changed
- Replaced `httpx` with `curl_cffi` for TLS browser impersonation (fixes HTTP 403)
- Updated HTML selectors for current unegui.mn layout
- Fixed category URL paths (`/avto-mashin/` etc.)
- Search now uses `/search/?q=` endpoint

## [1.0.0] - 2026-08-04

### Added
- Initial MCP server with five tools:
  - `search_listings`
  - `browse_category`
  - `get_listing_details`
  - `list_categories`
  - `get_recent_listings`
