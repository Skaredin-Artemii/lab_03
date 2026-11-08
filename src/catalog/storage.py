"""Сохранение и загрузка каталога в JSON."""

import json

from .catalog import Catalog
from .errors import (
    CorruptedFileError,
    InvalidItemError,
    UnsupportedFormatVersionError,
)
from .models import Classroom

FORMAT_VERSION = 1
ITEM_FIELDS = ("item_id", "name", "category", "year", "capacity", "building")


def item_to_dict(item):
    """Сделать из аудитории словарь для json."""
    return {
        "item_id": item.item_id,
        "name": item.name,
        "category": item.category,
        "year": item.year,
        "capacity": item.capacity,
        "building": item.building,
    }


def item_from_dict(data, context=""):
    """Собрать Classroom из словаря."""
    for field in ITEM_FIELDS:
        if field not in data:
            raise InvalidItemError(f"в элементе нет поля '{field}'{context}")
    return Classroom(**data)


def save_catalog(catalog, path):
    """Сохранить каталог в файл."""
    data = {
        "format_version": FORMAT_VERSION,
        "items": [item_to_dict(x) for x in catalog],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_catalog(path):
    """Загрузить каталог из файла."""
    with open(path, encoding="utf-8") as f:
        try:
            raw = json.load(f)
        except json.JSONDecodeError:
            raise CorruptedFileError(str(path), "невалидный JSON")

    if not isinstance(raw, dict):
        raise CorruptedFileError(str(path), "в корне должен быть объект")

    version = raw.get("format_version")
    if version is None:
        raise CorruptedFileError(str(path), "нет поля format_version")
    if not isinstance(version, int):
        raise CorruptedFileError(str(path), "format_version должен быть числом")
    if version != FORMAT_VERSION:
        raise UnsupportedFormatVersionError(version, supported=FORMAT_VERSION)

    items = raw.get("items")
    if items is None:
        raise CorruptedFileError(str(path), "нет поля items")
    if not isinstance(items, list):
        raise CorruptedFileError(str(path), "items должен быть списком")

    cat = Catalog()
    for i, elem in enumerate(items):
        if not isinstance(elem, dict):
            raise CorruptedFileError(str(path), f"элемент items[{i}] не объект")
        cat.add(item_from_dict(elem, context=f" (items[{i}])"))
    return cat


def load_into(catalog, path):
    """Добавить содержимое файла в уже существующий каталог."""
    loaded = load_catalog(path)
    for item in loaded:
        if item.item_id in catalog:
            raise InvalidItemError(
                f"id '{item.item_id}' уже есть в каталоге", field="item_id"
            )
    for item in loaded:
        catalog.add(item)