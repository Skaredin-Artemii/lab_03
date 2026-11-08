"""Модель учебной аудитории."""

from dataclasses import dataclass

from .errors import InvalidItemError

ALLOWED_CATEGORIES = ("lecture", "lab", "seminar", "computer", "sport")

YEAR_MIN = 1950
YEAR_MAX = 2026


@dataclass(frozen=True)
class Classroom:
    """Учебная аудитория. year - год последнего ремонта."""

    item_id: str
    name: str
    category: str
    year: int
    capacity: int
    building: str

    def __post_init__(self):

        if not isinstance(self.item_id, str) or not self.item_id.strip():
            raise InvalidItemError("item_id должен быть непустой строкой", field="item_id")
        object.__setattr__(self, "item_id", self.item_id.strip())

        if not isinstance(self.name, str) or not self.name.strip():
            raise InvalidItemError("name должен быть непустой строкой", field="name")
        object.__setattr__(self, "name", self.name.strip())

        if self.category not in ALLOWED_CATEGORIES:
            raise InvalidItemError(f"недопустимая категория: {self.category}", field="category")

        if not isinstance(self.year, int):
            raise InvalidItemError("year должен быть целым числом", field="year")
        if self.year < YEAR_MIN or self.year > YEAR_MAX:
            raise InvalidItemError(
                f"year должен быть в диапазоне {YEAR_MIN}..{YEAR_MAX}", field="year"
            )

        if not isinstance(self.capacity, int):
            raise InvalidItemError("capacity должен быть целым числом", field="capacity")
        if self.capacity <= 0:
            raise InvalidItemError("capacity должен быть больше нуля", field="capacity")

        if not isinstance(self.building, str) or not self.building.strip():
            raise InvalidItemError("building не может быть пустым", field="building")
        object.__setattr__(self, "building", self.building.strip())