"""Unit tests for unegui.mn MCP (offline, no network)."""

from pathlib import Path

import pytest

from unegui_mcp.categories import CATEGORIES, categories_for_api, format_bilingual_name
from unegui_mcp.scraper import UneguiScraper

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def scraper() -> UneguiScraper:
    return UneguiScraper()


def test_categories_have_bilingual_names() -> None:
    assert "vehicles" in CATEGORIES
    vehicles = CATEGORIES["vehicles"]
    assert vehicles["name_en"] == "Vehicles"
    assert vehicles["name_mn"] == "Тээврийн хэрэгсэл"
    assert "cars_for_sale" in vehicles["subcategories"]


def test_categories_for_api_shape() -> None:
    api = categories_for_api()
    assert api["vehicles"]["name_en"] == "Vehicles"
    assert api["vehicles"]["name_mn"] == "Тээврийн хэрэгсэл"
    assert "Тээврийн хэрэгсэл (Vehicles)" == api["vehicles"]["name"]
    assert "cars_for_sale" in api["vehicles"]["subcategories"]


def test_bilingual_messages_default_mongolian() -> None:
    from unegui_mcp.i18n import DEFAULT_LANG, bilingual, t

    assert DEFAULT_LANG == "mn"
    assert t("no_listings").startswith("Зар олдсонгүй")
    msgs = bilingual("no_listings")
    assert msgs["message"] == t("no_listings", "mn")
    assert msgs["message_en"] == t("no_listings", "en")


def test_format_bilingual_name() -> None:
    assert format_bilingual_name("Тээврийн хэрэгсэл", "Vehicles") == "Тээврийн хэрэгсэл (Vehicles)"


def test_parse_listing_card_from_fixture(scraper: UneguiScraper) -> None:
    html = (FIXTURES / "listing_card.html").read_text(encoding="utf-8")
    listings = scraper._parse_listings_page(html)

    assert len(listings) == 1
    listing = listings[0]
    assert listing.title == "Toyota Land Cruiser 300, 2023/2023"
    assert "270" in listing.price
    assert listing.date == "Өнөөдөр"
    assert listing.location == "Хан-Уул, King Tower"
    assert listing.url.endswith("/adv/12345_toyota-land-cruiser-300-2023-2023/")


def test_parse_empty_page_returns_empty_list(scraper: UneguiScraper) -> None:
    assert scraper._parse_listings_page("<html><body></body></html>") == []


def test_unknown_category_raises(scraper: UneguiScraper) -> None:
    with pytest.raises(ValueError, match="Unknown category"):
        import asyncio

        asyncio.run(scraper.browse_category("not_a_category"))


@pytest.mark.integration
@pytest.mark.asyncio
async def test_live_search_smoke(scraper: UneguiScraper) -> None:
    """Optional live test — skipped in CI by default."""
    listings = await scraper.search("Toyota", page=1)
    await scraper.close()
    assert len(listings) > 0
