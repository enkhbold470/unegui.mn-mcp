# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **Mongolian is now the default language** across docs, MCP instructions, and API messages
- `README.md` is Mongolian; English docs moved to `README.en.md`
- API responses use `message` (MN) + `message_en` (EN) instead of the reverse

## [1.0.0] - 2026-08-04

### Added
- Initial MCP server with five tools:
  - `search_listings`
  - `browse_category`
  - `get_listing_details`
  - `list_categories`
  - `get_recent_listings`
