"""Тесты каталога."""

import pytest

from catalog.catalog import Catalog
from catalog.errors import DuplicateIdError, ItemNotFoundError
from catalog.models import Classroom

def make_classroom(id_="A-101", name="Аудитория", category="lecture") -> Classroom:
    return Classroom(
        item_id=id_,
        name=name,
        category=category,
        year=2000,
        capacity=20,
        building="A",
    )

def test_empty_catalog():
    cat = Catalog()
    assert len(cat) == 0
    assert list(cat) == []
    assert "A-101" not in cat

def test_add_and_get():
    cat = Catalog()
    item = make_classroom()
    cat.add(item)
    assert len(cat) == 1
    assert cat.get("A-101") is item
    assert "A-101" in cat

def test_add_duplicate_raises():
    cat = Catalog()
    cat.add(make_classroom())
    with pytest.raises(DuplicateIdError) as exc_info:
        cat.add(make_classroom())
    assert exc_info.value.item_id == "A-101"

def test_get_missing_raises():
    cat = Catalog()
    with pytest.raises(ItemNotFoundError) as exc_info:
        cat.get("missing")
    assert exc_info.value.iten_id == "missing"

def test_remove():
    cat = Catalog()
    cat.add(make_classroom())
    cat.remove("A-101")
    assert len(cat) == 0
    assert "A-101" not in cat

def test_remove_missing_raises():
    cat = Catalog()
    with pytest.raises(ItemNotFoundError):
        cat.remove("missing")

def test_iteration_order_is_insertion_order():
    cat = Catalog()
    cat.add(make_classroom("A"))
    cat.add(make_classroom("B"))
    cat.add(make_classroom("C"))
    assert [x.item_id for x in cat] == ["A", "B", "C"]

def test_iteration_after_remove_and_add():
    cat = Catalog()
    cat.add(make_classroom("A"))
    cat.add(make_classroom("B"))
    cat.add(make_classroom("C")) 
    cat.remove("B")
    cat.add(make_classroom("D"))
    assert [x.item_id for x in cat] == ["A", "B", "D"]

def test_find_by_category():
    cat = Catalog()
    cat.add(make_classroom("A", category="computer"))
    cat.add(make_classroom("B", category="lab"))
    cat.add(make_classroom("C", category="computer"))
    found = cat.find_by_category("computer")
    assert {x.item_id for x in found} == {"A", "C"}
    assert len(found) == 2

def test_find_by_name_case_insensitive():
    cat = Catalog()
    cat.add(make_classroom("A", name="Аудитория информатики"))
    cat.add(make_classroom("B", name="Лаборатория физики"))
    found = cat.find_by_name("ИНФОРМ")
    assert len(found) == 1
    assert found[0].item_id == "A"

def test_find_returns_new_list():
    cat = Catalog()
    cat.add(make_classroom("A", category="lecture"))
    found = cat.find_by_category("lecture")
    found.clear()
    assert len(cat) == 1
    