"""Тесты модели Classroom."""

from dataclasses import FrozenInstanceError

import pytest

from catalog.errors import InvalidItemError
from catalog.models import YEAR_MAX, YEAR_MIN, Classroom


def make_classroom(**overrides):
    """Помощник для создания аудиторий с возможностью переопределять поля."""
    data = {
        "item_id": "A-101",
        "name": "Информатика",
        "category": "computer",
        "year": 2015,
        "capacity": 30,
        "building": "A",
    }
    data.update(overrides)
    return Classroom(**data)

def test_valid_classroom_creation():
    data = {
        "item_id": "A-101",
        "name": "Информатика",
        "category": "computer",
        "year": 2015,
        "capacity": 30,
        "building": "A",
    }
    item = Classroom(**data)
    assert item.item_id == "A-101"
    assert item.name == "Информатика"
    assert item.category == "computer"

def test_normalization_strips_whitespace():
    item = make_classroom(item_id=" A-101 ", name="Информатика   ", building="  A")
    assert item.item_id == "A-101"
    assert item.name == "Информатика"
    assert item.building == "A"

@pytest.mark.parametrize(
    "field, value, expected_field",
    [
        ("item_id", "", "item_id"),
        ("item_id", "   ", "item_id"),
        ("item_id", 123, "item_id"),
        ("name", "", "name"),
        ("name", None, "name"),
        ("category", "gym", "category"),
        ("category", "LECTURE", "category"),
        ("year", YEAR_MIN - 1, "year"),
        ("year", YEAR_MAX + 1, "year"),
        ("year", True, "year"),
        ("year", 2020.0, "year"),
        ("capacity", 0, "capacity"),
        ("capacity", -5, "capacity"),
        ("capacity", True, "capacity"),
        ("building", "", "building"),
    ],
)
def test_invalid_fields_raise_error(field, value, expected_field):
    with pytest.raises(InvalidItemError) as exc_info:
        make_classroom(**{field: value})
    assert exc_info.value.field == expected_field

def test_boundary_years():
    item_min = make_classroom(year=YEAR_MIN)
    item_max = make_classroom(year=YEAR_MAX)
    assert item_min.year == YEAR_MIN
    assert item_max.year == YEAR_MAX

def test_frozen_classroom_cannot_be_changed():
    item = make_classroom()
    with pytest.raises(FrozenInstanceError):
        item.name = "Новое имя"

def test_equality_and_hash():
    a = make_classroom(item_id="X")
    b = make_classroom(item_id="X")
    c = make_classroom(item_id="Y")
    assert a == b
    assert a != c
    assert hash(a) == hash(b)