"""Category and subcategory definitions for unegui.mn (bilingual EN/MN)."""

from __future__ import annotations

from typing import Any, TypedDict


class Subcategory(TypedDict):
    name_en: str
    name_mn: str
    path: str


class Category(TypedDict):
    name_en: str
    name_mn: str
    path: str
    subcategories: dict[str, Subcategory]


def _sub(
    name_en: str,
    name_mn: str,
    path: str,
) -> Subcategory:
    return {"name_en": name_en, "name_mn": name_mn, "path": path}


CATEGORIES: dict[str, Category] = {
    "vehicles": {
        "name_en": "Vehicles",
        "name_mn": "Тээврийн хэрэгсэл",
        "path": "/avto-mashin/",
        "subcategories": {
            "cars_for_sale": _sub(
                "Cars for Sale",
                "Автомашин зарна",
                "/avto-mashin/-avtomashin-zarna/",
            ),
            "cars_wanted": _sub(
                "Cars Wanted",
                "Автомашин авна",
                "/avto-mashin/avtomashin-avna/",
            ),
            "car_parts": _sub(
                "Car Parts",
                "Сэлбэг",
                "/avto-mashin/avtoselbegbusad/",
            ),
            "motorcycles": _sub(
                "Motorcycles & Mopeds",
                "Мотоцикл, мопед",
                "/avto-mashin/mototsikl-moped-/",
            ),
        },
    },
    "real_estate": {
        "name_en": "Real Estate",
        "name_mn": "Үл хөдлөх",
        "path": "/l-hdlh/",
        "subcategories": {
            "apartments_sale": _sub(
                "Apartments for Sale",
                "Орон сууц зарна",
                "/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/",
            ),
            "apartments_rent": _sub(
                "Apartments for Rent",
                "Орон сууц түрээслүүлнэ",
                "/l-hdlh/oron-suuts-treesllne/",
            ),
            "houses_sale": _sub(
                "Houses for Sale",
                "Хашаа байшин зарна",
                "/l-hdlh/l-hdlh-zarna/hasaa-baishin-zarna/",
            ),
            "land_sale": _sub(
                "Land for Sale",
                "Газар зарна",
                "/l-hdlh/l-hdlh-zarna/gazar-zarna/",
            ),
            "commercial": _sub(
                "Commercial Property",
                "Үйлдвэр, агуулах",
                "/l-hdlh/l-hdlh-zarna/ildver-aguulah-zarna/",
            ),
        },
    },
    "electronics": {
        "name_en": "Electronics",
        "name_mn": "Электрон бараа",
        "path": "/elektronik-baraa/",
        "subcategories": {
            "phones": _sub(
                "Mobile Phones",
                "Гар утас",
                "/elektronik-baraa/gar-utas/",
            ),
            "computers": _sub(
                "Computers",
                "Компьютер",
                "/kompyuter-internet/",
            ),
            "tablets": _sub(
                "Tablets",
                "Таблет",
                "/elektronik-baraa/tablet/",
            ),
            "tv_audio": _sub(
                "TV & Audio",
                "ТВ, аудио",
                "/elektronik-baraa/tv-audio/",
            ),
        },
    },
    "jobs": {
        "name_en": "Jobs",
        "name_mn": "Ажлын байр",
        "path": "/azhild-avna/",
        "subcategories": {
            "job_offers": _sub("Job Offers", "Ажилд авна", "/azhild-avna/"),
            "job_seekers": _sub(
                "Job Seekers",
                "Ажил хайж байна",
                "/ajil-haij-baina/",
            ),
        },
    },
    "services": {
        "name_en": "Services",
        "name_mn": "Үйлчилгээ",
        "path": "/jlchilgee/",
        "subcategories": {},
    },
    "clothing": {
        "name_en": "Clothing & Fashion",
        "name_mn": "Хувцас",
        "path": "/huvtsas-hereglel/",
        "subcategories": {},
    },
    "furniture": {
        "name_en": "Home & Furniture",
        "name_mn": "Гэр ахуй",
        "path": "/ger-ahujn-baraa/",
        "subcategories": {},
    },
    "pets": {
        "name_en": "Pets & Animals",
        "name_mn": "Амьтан",
        "path": "/mal-amitan/",
        "subcategories": {},
    },
    "hobby": {
        "name_en": "Hobby & Leisure",
        "name_mn": "Хобби, чөлөөт цаг",
        "path": "/hobbi-sport/",
        "subcategories": {},
    },
    "education": {
        "name_en": "Education",
        "name_mn": "Боловсрол",
        "path": "/bolovsrol/",
        "subcategories": {},
    },
}


def format_bilingual_name(name_mn: str, name_en: str) -> str:
    """Return a display name with Mongolian first, English in parentheses."""
    return f"{name_mn} ({name_en})"


def categories_for_api() -> dict[str, Any]:
    """Serialize categories for MCP tool responses."""
    result: dict[str, Any] = {}
    for key, info in CATEGORIES.items():
        entry: dict[str, Any] = {
            "key": key,
            "name_en": info["name_en"],
            "name_mn": info["name_mn"],
            "name": format_bilingual_name(info["name_mn"], info["name_en"]),
        }
        subcats = info.get("subcategories", {})
        if subcats:
            entry["subcategories"] = {
                sub_key: {
                    "key": sub_key,
                    "name_en": sub_info["name_en"],
                    "name_mn": sub_info["name_mn"],
                    "name": format_bilingual_name(
                        sub_info["name_mn"],
                        sub_info["name_en"],
                    ),
                }
                for sub_key, sub_info in subcats.items()
            }
        result[key] = entry
    return result
