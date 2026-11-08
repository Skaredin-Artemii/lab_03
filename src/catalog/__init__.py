"""Пакет catalog - каталог учебных аудиторий."""

from .catalog import Catalog
from .errors import (
    CatalogError,
    CorruptedFileError,
    DuplicateIdError,
    InvalidItemError,
    ItemNotFoundError,
    UnsupportedFormatVersionError,
)
from .models import ALLOWED_CATEGORIES, YEAR_MAX, YEAR_MIN, Classroom
from .storage import FORMAT_VERSION, load_catalog, load_into, save_catalog

__all__ = [
    "Catalog",
    "CatalogError",
    "Classroom",
    "CorruptedFileError",
    "DuplicateIdError",
    "InvalidItemError",
    "ItemNotFoundError",
    "UnsupportedFormatVersionError",
    "ALLOWED_CATEGORIES",
    "YEAR_MIN",
    "YEAR_MAX",
    "FORMAT_VERSION",
    "load_catalog",
    "load_into",
    "save_catalog",
]

__version__ = "0.1.0"