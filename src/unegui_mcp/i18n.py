"""Bilingual UI strings for the unegui.mn MCP server. Default: Mongolian."""

DEFAULT_LANG = "mn"

SERVER_INSTRUCTIONS = (
    "Монголын хамгийн том зарын сайт unegui.mn-ээс зар хайх, ангиллаар үзэх. "
    "Машин, үл хөдлөх, электрон бараа, ажлын байр зэрэг. "
    "Монгол болон англи хэлээр хайлт дэмжинэ. "
    "Search and browse listings on unegui.mn — Mongolia's largest classifieds marketplace."
)

MESSAGES = {
    "no_listings": {
        "mn": "Зар олдсонгүй. Өөр түлхүүр үг эсвэл ангилал ашиглаж үзнэ үү.",
        "en": "No listings found. Try different search terms or category.",
    },
    "invalid_url": {
        "mn": "URL нь unegui.mn домэйнтэй байх ёстой",
        "en": "URL must be from unegui.mn",
    },
}


def t(key: str, lang: str = DEFAULT_LANG) -> str:
    """Return a message in the requested language."""
    entry = MESSAGES[key]
    return entry.get(lang) or entry[DEFAULT_LANG]


def bilingual(key: str) -> dict[str, str]:
    """Return both languages with Mongolian as the primary `message` field."""
    entry = MESSAGES[key]
    return {
        "message": entry["mn"],
        "message_en": entry["en"],
    }
