"""Тесты Classroom."""

import pytest

from catalog.errors import InvalidItemError
from catalog.models import YEAR_MAX, YEAR_MIN, Classroom


def make_classroom(**overrides):
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


def test_ok():
    item = make_classroom()
    assert item.item_id == "A-101"
    assert item.name == "Информатика"


def test_strip():
    item = make_classroom(item_id=" A-101 ", name="  Инфа  ", building=" A ")
    assert item.item_id == "A-101"
    assert item.name == "Инфа"
    assert item.building == "A"


def test_empty_id():
    with pytest.raises(InvalidItemError) as e:
        make_classroom(item_id="  ")
    assert e.value.field == "item_id"


def test_empty_name():
    with pytest.raises(InvalidItemError) as e:
        make_classroom(name="")
    assert e.value.field == "name"


def test_bad_category():
    with pytest.raises(InvalidItemError) as e:
        make_classroom(category="gym")
    assert e.value.field == "category"


def test_year_ok_on_borders():
    assert make_classroom(year=YEAR_MIN).year == YEAR_MIN
    assert make_classroom(year=YEAR_MAX).year == YEAR_MAX


def test_year_out_of_range():
    with pytest.raises(InvalidItemError):
        make_classroom(year=YEAR_MIN - 1)
    with pytest.raises(InvalidItemError):
        make_classroom(year=YEAR_MAX + 1)


def test_bad_capacity():
    with pytest.raises(InvalidItemError):
        make_classroom(capacity=0)
    with pytest.raises(InvalidItemError):
        make_classroom(capacity=-5)


def test_empty_building():
    with pytest.raises(InvalidItemError) as e:
        make_classroom(building="  ")
    assert e.value.field == "building"


def test_frozen():
    item = make_classroom()
    with pytest.raises(Exception):
        item.name = "другое"