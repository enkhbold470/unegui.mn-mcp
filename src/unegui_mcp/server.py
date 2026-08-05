"""
Unegui.mn MCP Server / unegui.mn MCP сервер
============================================

Model Context Protocol server for Mongolia's largest classifieds platform.
Монголын хамгийн том зарын платформ unegui.mn-д зориулсан MCP сервер.

Author / Зохиогч: Enkhbold Ganbold (https://github.com/enkhbold470)
"""

import json

from mcp.server import MCPServer

from unegui_mcp.categories import categories_for_api
from unegui_mcp.i18n import MESSAGES, SERVER_INSTRUCTIONS
from unegui_mcp.scraper import UneguiScraper

mcp = MCPServer(
    name="unegui-mn",
    instructions=SERVER_INSTRUCTIONS,
)

scraper = UneguiScraper()


@mcp.tool()
async def search_listings(
    query: str,
    category: str = "",
    page: int = 1,
) -> str:
    """
    Search unegui.mn for listings matching a query.
    unegui.mn дээр түлхүүр үгээр зар хайна.

    Args:
        query: Search term / Хайлтын үг
               (e.g. "Toyota Prius", "2 өрөө орон сууц", "Land Cruiser 300")
        category: Optional category key / Сонголттой ангилал
                  (vehicles, real_estate, electronics, jobs, services,
                   clothing, furniture, pets, hobby, education)
        page: Page number / Хуудасны дугаар (default: 1)

    Returns:
        JSON with matching listings (title, price, URL, location, date).
        Тохирох заруудын JSON (гарчиг, үнэ, холбоос, байршил, огноо).
    """
    try:
        listings = await scraper.search(query=query, category=category, page=page)

        if not listings:
            return json.dumps(
                {
                    "status": "success",
                    "query": query,
                    "category": category or "all",
                    "page": page,
                    "count": 0,
                    "listings": [],
                    "message": MESSAGES["no_listings"]["en"],
                    "message_mn": MESSAGES["no_listings"]["mn"],
                },
                ensure_ascii=False,
                indent=2,
            )

        return json.dumps(
            {
                "status": "success",
                "query": query,
                "category": category or "all",
                "page": page,
                "count": len(listings),
                "listings": [listing.to_dict() for listing in listings],
            },
            ensure_ascii=False,
            indent=2,
        )

    except Exception as e:
        return json.dumps(
            {
                "status": "error",
                "error": str(e),
                "query": query,
            },
            ensure_ascii=False,
            indent=2,
        )


@mcp.tool()
async def browse_category(
    category: str,
    subcategory: str = "",
    page: int = 1,
) -> str:
    """
    Browse listings in a specific category on unegui.mn.
    unegui.mn дээр тодорхой ангиллын заруудыг үзнэ.

    Args:
        category: Category key / Ангиллын түлхүүр
                  (vehicles, real_estate, electronics, jobs, services,
                   clothing, furniture, pets, hobby, education)
        subcategory: Optional subcategory key / Дэд ангилал
                     Use list_categories to see available keys.
                     Жишээ: vehicles → cars_for_sale, car_parts
        page: Page number / Хуудасны дугаар (default: 1)

    Returns:
        JSON with listings from the specified category.
        Тухайн ангиллын заруудын JSON.
    """
    try:
        listings = await scraper.browse_category(
            category=category,
            subcategory=subcategory,
            page=page,
        )

        return json.dumps(
            {
                "status": "success",
                "category": category,
                "subcategory": subcategory or "all",
                "page": page,
                "count": len(listings),
                "listings": [listing.to_dict() for listing in listings],
            },
            ensure_ascii=False,
            indent=2,
        )

    except ValueError as e:
        return json.dumps(
            {
                "status": "error",
                "error": str(e),
            },
            ensure_ascii=False,
            indent=2,
        )
    except Exception as e:
        return json.dumps(
            {
                "status": "error",
                "error": str(e),
            },
            ensure_ascii=False,
            indent=2,
        )


@mcp.tool()
async def get_listing_details(url: str) -> str:
    """
    Get detailed information about a specific listing on unegui.mn.
    Нэг зарын дэлгэрэнгүй мэдээллийг авна.

    Args:
        url: Full listing URL / Зарын бүтэн холбоос
             (e.g. "https://www.unegui.mn/adv/12345_...")

    Returns:
        JSON with title, price, description, location, images, and specs.
        Гарчиг, үнэ, тайлбар, байршил, зураг, үзүүлэлтүүд бүхий JSON.
    """
    try:
        listing = await scraper.get_listing_detail(url)

        return json.dumps(
            {
                "status": "success",
                "listing": listing.to_dict(),
            },
            ensure_ascii=False,
            indent=2,
        )

    except ValueError as e:
        return json.dumps(
            {
                "status": "error",
                "error": str(e),
            },
            ensure_ascii=False,
            indent=2,
        )
    except Exception as e:
        return json.dumps(
            {
                "status": "error",
                "error": str(e),
            },
            ensure_ascii=False,
            indent=2,
        )


@mcp.tool()
async def list_categories() -> str:
    """
    List all available categories and subcategories on unegui.mn.
    unegui.mn-ийн бүх ангилал, дэд ангиллыг жагсаана.

    Returns:
        JSON with bilingual category names (English and Mongolian).
        Англи, Монгол хэлээр ангиллын нэрс бүхий JSON.
    """
    return json.dumps(
        {
            "status": "success",
            "categories": categories_for_api(),
        },
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
async def get_recent_listings(limit: int = 20) -> str:
    """
    Get the most recent listings from the unegui.mn homepage.
    unegui.mn нүүр хуудасны хамгийн сүүлийн заруудыг авна.

    Args:
        limit: Maximum listings to return / Буцаах зарын дээд тоо
               (default: 20, max: 50)

    Returns:
        JSON with recent listings across all categories.
        Бүх ангиллын сүүлийн заруудын JSON.
    """
    limit = min(max(1, limit), 50)

    try:
        listings = await scraper.get_recent_listings(limit=limit)

        return json.dumps(
            {
                "status": "success",
                "count": len(listings),
                "listings": [listing.to_dict() for listing in listings],
            },
            ensure_ascii=False,
            indent=2,
        )

    except Exception as e:
        return json.dumps(
            {
                "status": "error",
                "error": str(e),
            },
            ensure_ascii=False,
            indent=2,
        )


def main() -> None:
    """Run the MCP server via stdio / MCP серверийг stdio-оор ажиллуулна."""
    import asyncio

    asyncio.run(mcp.run_stdio_async())


if __name__ == "__main__":
    main()
