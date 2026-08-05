"""
Scraper for unegui.mn — HTTP fetching and HTML parsing.
unegui.mn-ийн скрапер — HTTP хүсэлт, HTML задлах.

Uses polite rate limiting. TLS browser impersonation is required because
unegui.mn returns HTTP 403 to plain Python HTTP clients.
"""

import asyncio
import re
from dataclasses import dataclass, field
from urllib.parse import urlencode, urljoin

from bs4 import BeautifulSoup, Tag
from curl_cffi.requests import AsyncSession, RequestsError

from unegui_mcp.categories import CATEGORIES
from unegui_mcp.i18n import MESSAGES

BASE_URL = "https://www.unegui.mn"

# unegui.mn blocks plain httpx/curl (HTTP 403). curl_cffi impersonates a real
# browser TLS fingerprint, which is what Playwright uses under the hood.
BROWSER_IMPERSONATE = "chrome120"


@dataclass
class Listing:
    """Represents a single listing/ad on unegui.mn."""
    title: str
    price: str = ""
    url: str = ""
    image_url: str = ""
    location: str = ""
    date: str = ""
    description: str = ""
    category: str = ""
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        result = {
            "title": self.title,
            "price": self.price,
            "url": self.url,
            "location": self.location,
            "date": self.date,
        }
        if self.image_url:
            result["image_url"] = self.image_url
        if self.description:
            result["description"] = self.description
        if self.category:
            result["category"] = self.category
        if self.details:
            result["details"] = self.details
        return result


class UneguiScraper:
    """Async scraper for unegui.mn classifieds."""

    def __init__(self):
        self._client: AsyncSession | None = None
        self._rate_limit_delay = 1.0  # seconds between requests

    async def _get_client(self) -> AsyncSession:
        if self._client is None:
            self._client = AsyncSession(impersonate=BROWSER_IMPERSONATE, timeout=30.0)
        return self._client

    async def _fetch(self, url: str) -> str:
        """Fetch a URL with rate limiting and return HTML content."""
        client = await self._get_client()
        await asyncio.sleep(self._rate_limit_delay)
        response = await client.get(url)
        if response.status_code >= 400:
            raise RequestsError(
                f"HTTP {response.status_code}",
                response=response,  # type: ignore[arg-type]
            )
        return response.text

    async def close(self):
        if self._client is not None:
            await self._client.close()
            self._client = None

    def _parse_listing_card(self, card: Tag) -> Listing | None:
        """Parse a single listing card from search/category results."""
        try:
            link_tag = card.select_one("a[href*='/adv/']")
            if not link_tag:
                return None

            title_tag = card.select_one(
                ".advert__content-title, .advert-grid__content-title, "
                ".announcement-block__title"
            )
            title_text = title_tag.get_text(strip=True) if title_tag else ""
            if not title_text:
                title_text = link_tag.get_text(strip=True)
            if not title_text:
                return None

            href = link_tag.get("href", "")
            full_url = urljoin(BASE_URL, href) if href else ""

            price_tag = card.select_one(
                ".advert__content-price, .advert-grid__content-price, "
                ".announcement-block__price, [class*='content-price']"
            )
            price = price_tag.get_text(strip=True) if price_tag else ""

            image_url = ""
            img_tag = card.select_one("img[src], img[data-src]")
            if img_tag:
                image_url = img_tag.get("src") or img_tag.get("data-src") or ""
            else:
                lazy_slide = card.select_one("a.swiper-slide[data-background]")
                if lazy_slide:
                    image_url = lazy_slide.get("data-background", "")
            if image_url and not image_url.startswith("http"):
                image_url = urljoin(BASE_URL, image_url)

            location_tag = card.select_one(
                ".advert__content-place, .advert-grid__content-place, "
                ".announcement-block__location, [class*='content-place']"
            )
            location = location_tag.get_text(strip=True) if location_tag else ""

            date_tag = card.select_one(
                ".advert__content-date, .advert-grid__content-date, "
                ".announcement-block__date, [class*='content-date'], time"
            )
            date = date_tag.get_text(strip=True) if date_tag else ""

            return Listing(
                title=title_text,
                price=price,
                url=full_url,
                image_url=image_url,
                location=location,
                date=date,
            )
        except Exception:
            return None

    async def search(self, query: str, category: str = "", page: int = 1) -> list[Listing]:
        """
        Search unegui.mn for listings matching the query.

        Args:
            query: Search term
            category: Optional category key (e.g. 'vehicles', 'real_estate')
            page: Page number (1-indexed)
        """
        params = {"q": query}
        if page > 1:
            params["page"] = str(page)

        # Site-wide search lives at /search/; category paths do not accept ?q=.
        url = f"{BASE_URL}/search/?{urlencode(params)}"

        try:
            html = await self._fetch(url)
            return self._parse_listings_page(html)
        except RequestsError as e:
            status = getattr(getattr(e, "response", None), "status_code", None)
            raise Exception(f"Failed to search unegui.mn: HTTP {status or e}") from e
        except Exception as e:
            raise Exception(f"Failed to search unegui.mn: {e}") from e

    async def browse_category(self, category: str, subcategory: str = "", page: int = 1) -> list[Listing]:
        """
        Browse listings in a specific category.

        Args:
            category: Category key (e.g. 'vehicles', 'real_estate')
            subcategory: Optional subcategory key (e.g. 'cars_for_sale')
            page: Page number
        """
        if category not in CATEGORIES:
            available = ", ".join(CATEGORIES.keys())
            raise ValueError(f"Unknown category '{category}'. Available: {available}")

        cat_info = CATEGORIES[category]

        if subcategory:
            subcats = cat_info.get("subcategories", {})
            if subcategory not in subcats:
                available = ", ".join(subcats.keys()) if subcats else "none"
                raise ValueError(
                    f"Unknown subcategory '{subcategory}' in '{category}'. Available: {available}"
                )
            path = subcats[subcategory]["path"]
        else:
            path = cat_info["path"]

        url = f"{BASE_URL}{path}"
        if page > 1:
            url += f"?page={page}"

        try:
            html = await self._fetch(url)
            return self._parse_listings_page(html)
        except RequestsError as e:
            status = getattr(getattr(e, "response", None), "status_code", None)
            raise Exception(f"Failed to browse category: HTTP {status or e}") from e
        except Exception as e:
            raise Exception(f"Failed to browse category: {e}") from e

    def _parse_listings_page(self, html: str) -> list[Listing]:
        """Parse a listings page and extract all listing cards."""
        soup = BeautifulSoup(html, "lxml")
        listings: list[Listing] = []

        # Try current and legacy selectors for listing cards
        card_selectors = [
            ".js-item-listing",
            ".advert-grid.js-advert-desktop",
            ".announcement-block",
            ".advert-list-item",
            ".list-announcement-block",
        ]

        cards: list[Tag] = []
        for selector in card_selectors:
            cards = soup.select(selector)
            if cards:
                break

        # Fallback: find all links to /adv/ pages
        if not cards:
            seen_urls: set[str] = set()
            for link in soup.find_all("a", href=re.compile(r"/adv/")):
                href = link.get("href", "")
                if href in seen_urls:
                    continue
                seen_urls.add(href)
                # Try to get the parent container
                parent = link.find_parent(["div", "li", "article"])
                if parent:
                    cards.append(parent)
                else:
                    cards.append(link)

        for card in cards:
            listing = self._parse_listing_card(card)
            if listing:
                listings.append(listing)

        return listings

    async def get_listing_detail(self, url: str) -> Listing:
        """
        Get detailed information about a specific listing.

        Args:
            url: Full URL to the listing page (must be a unegui.mn URL)
        """
        if "unegui.mn" not in url:
            raise ValueError(
                f"{MESSAGES['invalid_url']['en']} / {MESSAGES['invalid_url']['mn']}"
            )

        try:
            html = await self._fetch(url)
            return self._parse_detail_page(html, url)
        except RequestsError as e:
            status = getattr(getattr(e, "response", None), "status_code", None)
            raise Exception(f"Failed to fetch listing: HTTP {status or e}") from e
        except Exception as e:
            raise Exception(f"Failed to fetch listing: {e}") from e

    def _parse_detail_page(self, html: str, url: str) -> Listing:
        """Parse a listing detail page."""
        soup = BeautifulSoup(html, "lxml")

        # Title
        title_tag = soup.select_one(
            "h1, .announcement-title, .js-announcement-title, "
            "[class*='title'] h1, [class*='title'] h2"
        )
        title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"

        # Price
        price_tag = soup.select_one(
            ".announcement-price, .announcement-price__cost, "
            "[class*='price'], .price"
        )
        price = price_tag.get_text(strip=True) if price_tag else ""

        # Description
        desc_tag = soup.select_one(
            ".announcement-description, .js-description, "
            "[class*='description'], .announcement-body"
        )
        description = ""
        if desc_tag:
            # Get text preserving line breaks
            for br in desc_tag.find_all("br"):
                br.replace_with("\n")
            description = desc_tag.get_text(strip=True)

        # Images
        image_url = ""
        img_tag = soup.select_one(
            ".announcement-gallery img, .announcement-photo img, "
            ".gallery img, [class*='gallery'] img, "
            "meta[property='og:image']"
        )
        if img_tag:
            if img_tag.name == "meta":
                image_url = img_tag.get("content", "")
            else:
                image_url = img_tag.get("src") or img_tag.get("data-src") or ""
                if image_url and not image_url.startswith("http"):
                    image_url = urljoin(BASE_URL, image_url)

        # Location
        location_tag = soup.select_one(
            ".announcement-loc, [class*='location'], "
            "[class*='address'], .announcement-characteristics .value"
        )
        location = location_tag.get_text(strip=True) if location_tag else ""

        # Date
        date_tag = soup.select_one(
            ".announcement-createdAt, [class*='date'], time, "
            "[class*='created']"
        )
        date = date_tag.get_text(strip=True) if date_tag else ""

        # Category breadcrumb
        breadcrumbs = soup.select(".breadcrumbs a, .breadcrumb a, [class*='breadcrumb'] a")
        category = " > ".join(
            a.get_text(strip=True)
            for a in breadcrumbs
            if a.get_text(strip=True)
        )

        # Extract additional details/characteristics
        details: dict[str, str] = {}
        char_rows = soup.select(
            ".announcement-characteristics li, "
            ".announcement-characteristics tr, "
            "[class*='characteristic'] li, "
            "[class*='param'] li, "
            "table.chars tr"
        )
        for row in char_rows:
            key_tag = row.select_one(".key, .label, th, dt, span:first-child")
            val_tag = row.select_one(".value, td, dd, span:last-child, a")
            if key_tag and val_tag and key_tag != val_tag:
                key = key_tag.get_text(strip=True).rstrip(":")
                val = val_tag.get_text(strip=True)
                if key and val:
                    details[key] = val

        return Listing(
            title=title,
            price=price,
            url=url,
            image_url=image_url,
            location=location,
            date=date,
            description=description,
            category=category,
            details=details,
        )

    async def get_recent_listings(self, limit: int = 20) -> list[Listing]:
        """Get the most recent listings from the homepage."""
        try:
            html = await self._fetch(BASE_URL)
            listings = self._parse_listings_page(html)
            return listings[:limit]
        except Exception as e:
            raise Exception(f"Failed to fetch recent listings: {e}") from e
