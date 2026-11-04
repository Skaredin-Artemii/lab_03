"""Демонстрация работы пакета catalog.

Запуск: python -m catalog
"""

import tempfile
from pathlib import Path

from . import Catalog, Classroom, load_catalog, save_catalog


def main() -> None:
    print("Демонстрация каталога учебных аудиторий")

    cat = Catalog()
    cat.add(Classroom(
        item_id="IT-17",
        name="Аудитория информатики",
        category="computer",
        year=2024,
        capacity=45,
        building="GUK_A"
    ))
    cat.add(Classroom(
        item_id="300-A",
        name="Аудитория для мероприятий",
        category="lecture",
        year=2025,
        capacity=250,
        building="GUK_A",
    ))

    print(f"В каталоге {len(cat)} аудитории:")
    for item in cat:
        print(f" [{item.item_id}] {item.name} (мест: {item.capacity})")

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "catalog.json"
        save_catalog(cat, path)
        print(f"\nУспешно сохранено в JSON ({path.stat().st_size} байт)")

        loaded = load_catalog(path)
        print(f"Успешно загружено обратно: {len(loaded)} аудиторий")

    print("\nПоиск по категории 'computer':")
    for item in cat.find_by_category("computer"):
        print(f" Найдено: {item.item_id}")

    print("Готово")

if __name__ == "__main__":
    main()
    
