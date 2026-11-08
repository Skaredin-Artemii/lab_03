"""Демонстрация всех возможностей пакета catalog.

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


def main() -> None:
    print("Демонстрация работы пакета catalog\n")

    # 1. Модель (Classroom)
    rooms = [
        Classroom("A-101", "Компьютерный класс", "computer", 2015, 30, "А"),
        Classroom("  B-202  ", "Лаборатория физики", "lab", 2010, 20, "Б"),
        Classroom("C-303", "Лекционный зал", "lecture", 2020, 100, "В"),
        Classroom("D-404", "Семинарская комната", "seminar", 2005, 15, "Г"),
        Classroom("E-505", "Спортивный зал", "sport", 2018, 50, "Д"),
        Classroom("F-606", "Компьютерная лаборатория", "computer", 2022, 25, "А"),
        Classroom("G-707", "Лекционный зал 'Физика'", "lecture", 1999, 80, "Б"),
    ]
    print(f"1. Модель: успешно создано {len(rooms)} аудиторий")

    # Ошибка валидации
    try:
        Classroom("X-1", "Ошибка", "lab", 1800, 10, "X")
    except InvalidItemError as e:
        print(f"   Защита модели: {e}")

    # 2. Каталог: базовые операции 
    cat = Catalog()
    for room in rooms:
        cat.add(room)
    
    print(f"\n2. Каталог: добавлено {len(cat)} аудиторий. len = {len(cat)}")
    print(f"   'A-101' in cat: {'A-101' in cat}")
    print(f"   get('B-202'): {cat.get('B-202').name}")

    # Дубликат ID
    try:
        cat.add(rooms[0])
    except DuplicateIdError as e:
        print(f"   Защита от дубликата: {e}")

    # 3. Итерация и поиск 
    print("\n3. Итерация (все аудитории в порядке добавления):")
    for item in cat:
        print(f"   [{item.item_id}] {item.name} | {item.category} | мест: {item.capacity}")
    
    print("\n   Поиск по категории 'computer':")
    for item in cat.find_by_category("computer"):
        print(f"      -> {item.name}")
        
    print("   Поиск по имени 'физик' (без учета регистра):")
    for item in cat.find_by_name("физик"):
        print(f"      -> {item.name}")

    #  4. Хранение (JSON) 
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "data.json"
        
        save_catalog(cat, path)
        print(f"\n4. Хранение: сохранено в JSON ({path.stat().st_size} байт)")
        
        loaded = load_catalog(path)
        print(f"   load_catalog: загружено обратно {len(loaded)} аудиторий")
        
        # load_into (успешное слияние)
        new_cat = Catalog()
        new_cat.add(Classroom("Z-999", "Новая аудитория", "lecture", 2024, 40, "Е"))
        print(f"   В новом каталоге перед слиянием: {len(new_cat)} аудитория (Z-999)")
        
        try:
            load_into(new_cat, path)
            print(f" load_into: успешное слияние! Теперь в новом каталоге {len(new_cat)} аудиторий")
        except InvalidItemError as e:
            print(f"   Ошибка при слиянии (проверь ID в new_cat): {e}")
        
        # Конфликт при load_into 
        print("   Попытка слить тот же файл еще раз (ожидаем ошибку)...")
        try:
            load_into(new_cat, path)
        except InvalidItemError as e:
            print(f"      Защита load_into сработала: {e}")

    # 5. Удаление 
    cat.remove("A-101")
    print(f"\n5. Удаление: 'A-101' удален, осталось {len(cat)} аудиторий")
    
    try:
        cat.remove("A-101")
    except ItemNotFoundError as e:
        print(f"   Защита удаления: {e}")

    print("\nВсе функции успешно продемонстрированы.")


if __name__ == "__main__":
    main()