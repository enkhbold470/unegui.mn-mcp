"""
unegui.mn MCP сервер / Unegui.mn MCP Server
============================================

Монголын хамгийн том зарын платформ unegui.mn-д зориулсан MCP сервер.
Model Context Protocol server for Mongolia's largest classifieds platform.

Зохиогч / Author: Enkhbold Ganbold (https://github.com/enkhbold470)
"""

import json

from mcp.server import MCPServer

from unegui_mcp.categories import categories_for_api
from unegui_mcp.i18n import SERVER_INSTRUCTIONS, bilingual
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
    unegui.mn дээр түлхүүр үгээр зар хайна.
    Search unegui.mn for listings matching a query.

    Args:
        query: Хайлтын үг / Search term
               (жишээ: "Toyota Prius", "2 өрөө орон сууц", "Land Cruiser 300")
        category: Сонголттой ангилал / Optional category key
                  (vehicles, real_estate, electronics, jobs, services,
                   clothing, furniture, pets, hobby, education)
        page: Хуудасны дугаар / Page number (default: 1)

    Returns:
        Тохирох заруудын JSON (гарчиг, үнэ, холбоос, байршил, огноо).
        JSON with matching listings (title, price, URL, location, date).
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
                    **bilingual("no_listings"),
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
    unegui.mn дээр тодорхой ангиллын заруудыг үзнэ.
    Browse listings in a specific category on unegui.mn.

    Args:
        category: Ангиллын түлхүүр / Category key
                  (vehicles, real_estate, electronics, jobs, services,
                   clothing, furniture, pets, hobby, education)
        subcategory: Дэд ангилал / Optional subcategory key
                     list_categories хэрэгслээр жагсаалтыг харна.
                     Жишээ: vehicles → cars_for_sale, car_parts
        page: Хуудасны дугаар / Page number (default: 1)

    Returns:
        Тухайн ангиллын заруудын JSON.
        JSON with listings from the specified category.
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
    Нэг зарын дэлгэрэнгүй мэдээллийг авна.
    Get detailed information about a specific listing on unegui.mn.

    Args:
        url: Зарын бүтэн холбоос / Full listing URL
             (жишээ: "https://www.unegui.mn/adv/12345_...")

    Returns:
        Гарчиг, үнэ, тайлбар, байршил, зураг, үзүүлэлтүүд бүхий JSON.
        JSON with title, price, description, location, images, and specs.
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
    unegui.mn-ийн бүх ангилал, дэд ангиллыг жагсаана.
    List all available categories and subcategories on unegui.mn.

    Returns:
        Монгол, англи хэлээр ангиллын нэрс бүхий JSON.
        JSON with bilingual category names (Mongolian default).
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
    unegui.mn нүүр хуудасны хамгийн сүүлийн заруудыг авна.
    Get the most recent listings from the unegui.mn homepage.

    Args:
        limit: Буцаах зарын дээд тоо / Maximum listings to return
               (default: 20, max: 50)

    Returns:
        Бүх ангиллын сүүлийн заруудын JSON.
        JSON with recent listings across all categories.
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
    """MCP серверийг stdio-оор ажиллуулна / Run the MCP server via stdio."""
    import asyncio

    asyncio.run(mcp.run_stdio_async())


if __name__ == "__main__":
    main()
