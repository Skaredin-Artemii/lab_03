"""Демонстрация работы пакета catalog.

Запуск: python -m catalog
"""

import tempfile
from pathlib import Path

from . import (
    Catalog,
    Classroom,
    DuplicateIdError,
    InvalidItemError,
    ItemNotFoundError,
    load_catalog,
    load_into,
    save_catalog,
)


def main():
    print("Демонстрация работы пакета catalog")
    print("=" * 50)

    rooms = [
        Classroom("A-101", "Компьютерный класс", "computer", 2015, 30, "А"),
        Classroom("  B-202  ", "Лаборатория физики", "lab", 2010, 20, "Б"),
        Classroom("C-303", "Лекционный зал", "lecture", 2020, 100, "В"),
        Classroom("D-404", "Семинарская комната", "seminar", 2005, 15, "Г"),
        Classroom("E-505", "Спортивный зал", "sport", 2018, 50, "Д"),
        Classroom("F-606", "Компьютерная лаборатория", "computer", 2022, 25, "А"),
        Classroom("G-707", "Лекционный зал 'Физика'", "lecture", 1999, 80, "Б"),
    ]
    print(f"Создано {len(rooms)} аудиторий")

    # проверка валидации модели
    try:
        Classroom("X-1", "Плохая", "lab", 1800, 10, "X")
    except InvalidItemError as e:
        print(f"Валидация модели сработала: {e}")

    # работа с каталогом
    cat = Catalog()
    for room in rooms:
        cat.add(room)

    print(f"\nВ каталоге {len(cat)} аудиторий")
    print(f"'A-101' in cat: {'A-101' in cat}")
    print(f"cat.get('B-202').name = {cat.get('B-202').name}")

    # дубликат
    try:
        cat.add(rooms[0])
    except DuplicateIdError as e:
        print(f"Дубликат не добавился: {e}")

    # итерация
    print("\nВсе аудитории:")
    for item in cat:
        print(f"  [{item.item_id}] {item.name} | {item.category} | мест: {item.capacity}")

    print("\nКатегория 'computer':")
    for item in cat.find_by_category("computer"):
        print(f"  -> {item.name}")

    print("Поиск 'физик' в названии:")
    for item in cat.find_by_name("физик"):
        print(f"  -> {item.name}")

    #сохранение / загрузка
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "data.json"
        save_catalog(cat, path)
        print(f"\nСохранено в {path} ({path.stat().st_size} байт)")

        loaded = load_catalog(path)
        print(f"Загружено {len(loaded)} аудиторий")

        # load_into в новый каталог
        new_cat = Catalog()
        new_cat.add(Classroom("Z-999", "Новая аудитория", "lecture", 2024, 40, "Е"))
        print(f"До слияния в новом каталоге: {len(new_cat)} (Z-999)")

        load_into(new_cat, path)
        print(f"После load_into: {len(new_cat)} аудиторий")

        # повторный load_into того же файла - должен упасть
        print("Пробую слить тот же файл еще раз...")
        try:
            load_into(new_cat, path)
        except InvalidItemError as e:
            print(f"  ok, не дало: {e}")

    # удаление
    cat.remove("A-101")
    print(f"\nУдалил 'A-101', осталось {len(cat)}")

    try:
        cat.remove("A-101")
    except ItemNotFoundError as e:
        print(f"Повторное удаление упало: {e}")

    print("\nВсё работает.")
    print("=" * 50)


if __name__ == "__main__":
    main()