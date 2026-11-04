"""Сохранение и загрузка каталога в JSON."""

import json
from dataclasses import fields
from pathlib import Path

from .catalog import Catalog
from .errors import (
    CorruptedFileError,
    InvalidItemError,
    UnsupportedFormatVersionError,
)
from .models import Classroom

FORMAT_VERSION = 1

_ITEM_FIELDS = frozenset(f.name for f in fields(Classroom))

def item_to_dict(item: Classroom) -> dict:
    """Сериализовать аудиторию в dict, пригодный для JSON."""
    return {
        "item_id": item.item_id,
        "name": item.name,
        "category": item.category,
        "year": item.year,
        "capacity": item.capacity,
        "building": item.building,
    }

def item_from_dict(data: dict, *, context: str = "") -> Classroom:
    """Собрать Classroom из dict."""
    if not isinstance(data, dict):
        raise InvalidItemError(
            f"элемент items должен быть объектом{context}"
        )
    keys = set(data.keys())
    if keys != _ITEM_FIELDS:
        missing = _ITEM_FIELDS - keys
        extra = keys - _ITEM_FIELDS
        parts = []
        if missing:
            parts.append(f"нет полей: {sorted(missing)}")
        if extra:
            parts.append(f"лишние поля: {sorted(extra)}")
        raise InvalidItemError(
            f"неверный набор полей ({'; '.join(parts)}){context}"
        )
    return Classroom(**data)

def save_catalog(catalog: Catalog, path: str | Path) -> None:
    """Сохранить каталог в JSON-файл."""
    data = {
        "format_version": FORMAT_VERSION,
        "items": [item_to_dict(item) for item in catalog],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_catalog(path: str | Path) -> Catalog:
    """Загрузить каталог из JSON-файла."""
    path_str = str(path)
    try:
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError:
        raise CorruptedFileError(path_str, "невалидный JSON") from None

    if not isinstance(raw, dict):
        raise CorruptedFileError(path_str, "корень должен быть объектом")

    if "format_version" not in raw:
        raise CorruptedFileError(path_str, "отсутствует поле format_version")

    version = raw["format_version"]
    if isinstance(version, bool) or not isinstance(version, int):
        raise CorruptedFileError(
            path_str, "format_version должен быть целым числом"
        )
    if version != FORMAT_VERSION:
        raise UnsupportedFormatVersionError(version, supported=FORMAT_VERSION)

    if "items" not in raw:
        raise CorruptedFileError(path_str, "отсутствует поле items")
    if not isinstance(raw["items"], list):
        raise CorruptedFileError(path_str, "items должен быть списком")

    catalog = Catalog()
    for index, element in enumerate(raw["items"]):
        context = f" (элемент items[{index}])"
        if not isinstance(element, dict):
            raise CorruptedFileError(
                path_str, f"элемент items[{index}] должен быть объектом"
            )
        item = item_from_dict(element, context=context)
        catalog.add(item)
    return catalog

def load_into(catalog: Catalog, path: str | Path) -> None:
    """Добавить содержимое файла в существующий каталог."""
    loaded = load_catalog(path)
    for item in loaded:
        if item.item_id in catalog:
            raise InvalidItemError(
                f"id '{item.item_id}' уже есть в каталоге",
                field="item_id",
            )
        for item in loaded:
            catalog.add(item)