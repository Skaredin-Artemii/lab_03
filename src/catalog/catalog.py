"""Каталог учебных аудиторий."""

from collections.abc import Iterator

from .errors import DuplicateIdError, ItemNotFoundError
from .models import Classroom


class Catalog:
    """Каталог учебных аудиторий.

    Внутри - dict[str, Calssroom]. 
    При удалении и повторном добавлении элемент уходит в конец.
    Методы поиска возвращают новый список.
    При мутировании внутренний dict каталога не затрагивается.
    """

    def __init__(self) -> None:
        self._items:dict[str, Classroom] = {}

    def add(self, item: Classroom) -> None:
        """Добавить аудиторию."""
        if item.item_id in self._items:
            raise DuplicateIdError(item.item_id)
        self._items[item.item_id] = item

    def get(self, item_id: str) -> Classroom:
        """Вернуть аудиторию по id."""
        try:
            return self._items[item_id]
        except KeyError:
            raise ItemNotFoundError(item_id) from None

    def remove(self, item_id: str) -> None:
        """Удалить аудиторию по id."""
        try:
            del self._items[item_id]
        except KeyError:
            raise ItemNotFoundError(item_id) from None

    def find_by_category(self, category: str) -> list[Classroom]:
        """Все аудитории указанной категории."""
        return [item for item in self._items.values() if item.category == category]

    def find_by_name(self, stroka: str) -> list[Classroom]:
        """Все аудитории, в названии которых есть подстрока stroka.
        Поиск нечувствителен к регистру.
        """
        needstr = stroka.casefold()
        return [item for item in self._items.values() if needstr in item.name.casefold()]

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[Classroom]:
        return iter(self._items.values())

    def __contains__(self, item_id: str) -> bool:
        return item_id in self._items

