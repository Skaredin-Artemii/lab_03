"""Модель учебной аудитории."""

from dataclasses import dataclass

from .errors import InvalidItemError

ALLOWED_CATEGORIES: frozenset[str] = frozenset({
    "lecture",
    "lab",
    "seminar",
    "computer",
    "sport",
})

YEAR_MIN = 1950
YEAR_MAX = 2026

@dataclass(frozen = True)
class Classroom:
    """Учебная аудитория.
    Поле year - год последнего ремонта.
    Инварианты проверяются в __post_init__.
    Строковые поля (item_id, name, building) нормализуются: strip по краям.
    """

    item_id: str
    name: str
    category: str
    year: int
    capacity: int
    building: str

    def __post_init__(self) -> None:
        if not isinstance(self.item_id, str):
            raise InvalidItemError("item_id должен быть строкой", field="item_id")
        stripped = self.item_id.strip()
        if not stripped:
            raise InvalidItemError("item_id не может быть пустым", field="item_id")
        object.__setattr__(self, "item_id", stripped)

        if not isinstance(self.name, str):
            raise InvalidItemError("name должен быть строкой", field="name")
        stripped = self.name.strip()
        if not stripped:
            raise InvalidItemError("name не может быть пустым", field="name")
        object.__setattr__(self, "name", stripped)

        if not isinstance(self.category, str):
            raise InvalidItemError("category должен быть строкой", field="category")
        if self.category not in ALLOWED_CATEGORIES:
            raise InvalidItemError(
                f"недопустиимая категория '{self.category}'",
                field="category",
            )

        if isinstance(self.year, bool) or not isinstance(self.year, int):
            raise InvalidItemError("year должен быть целым числом", field="year")
        if not (YEAR_MIN <= self.year <= YEAR_MAX):
            raise InvalidItemError(
                f"year должен быть в диапазоне {YEAR_MIN}..{YEAR_MAX}",
                field="year",
            )

        if isinstance(self.capacity, bool) or not isinstance(self.capacity, int):
            raise InvalidItemError("capacity должен быть целым числом", field="capacity")
        if self.capacity <= 0:
            raise InvalidItemError("capacity должен быть больше 0", field="capacity")

        if not isinstance(self.building, str):
            raise InvalidItemError("building должен быть строкой", field="building")
        stripped = self.building.strip()
        if not stripped:
            raise InvalidItemError("building не может быть пустым", field="building")
        object.__setattr__(self, "building", stripped)


