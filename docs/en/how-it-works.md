# How it works

[← Back](../../README.en.md)

unegui.mn blocks plain HTTP clients (HTTP 403). This server uses [`curl_cffi`](https://github.com/lexiforest/curl_cffi) to impersonate a real browser TLS fingerprint.

- **Rate limiting:** 1 second between requests (built-in)
- **Parsing:** BeautifulSoup + lxml against current unegui.mn HTML
- **Transport:** MCP over stdio
