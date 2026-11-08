"""Каталог учебных аудиторий."""

from .errors import DuplicateIdError, ItemNotFoundError


class Catalog:
    """Каталог аудиторий. Внутри - словарь id -> Classroom."""

    def __init__(self):
        self._items = {}

    def add(self, item):
        """Добавить аудиторию в каталог."""
        if item.item_id in self._items:
            raise DuplicateIdError(item.item_id)
        self._items[item.item_id] = item

    def get(self, item_id):
        """Получить аудиторию по id."""
        if item_id not in self._items:
            raise ItemNotFoundError(item_id)
        return self._items[item_id]

    def remove(self, item_id):
        """Удалить аудиторию по id."""
        if item_id not in self._items:
            raise ItemNotFoundError(item_id)
        del self._items[item_id]

    def find_by_category(self, category):
        """Найти все аудитории указанной категории."""
        result = []
        for item in self._items.values():
            if item.category == category:
                result.append(item)
        return result

    def find_by_name(self, stroka):
        """Найти аудитории, в названии которых есть stroka (без регистра)."""
        result = []
        needle = stroka.lower()
        for item in self._items.values():
            if needle in item.name.lower():
                result.append(item)
        return result

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items.values())

    def __contains__(self, item_id):
        return item_id in self._items