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

__version__ = "0.1.0"

__all__ = [
    "ALLOWED_CATEGORIES",
    "FORMAT_VERSION",
    "YEAR_MAX",
    "YEAR_MIN",
    "Catalog",
    "CatalogError",
    "Classroom",
    "CorruptedFileError",
    "DuplicateIdError",
    "InvalidItemError",
    "ItemNotFoundError",
    "UnsupportedFormatVersionError",
    "__version__",
    "load_catalog",
    "load_into",
    "save_catalog",
]