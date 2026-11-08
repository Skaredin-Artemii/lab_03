"""Тесты сохранения/загрузки."""

import json

import pytest

from catalog.catalog import Catalog
from catalog.errors import (
    CorruptedFileError,
    DuplicateIdError,
    InvalidItemError,
    UnsupportedFormatVersionError,
)
from catalog.models import Classroom
from catalog.storage import FORMAT_VERSION, load_catalog, load_into, save_catalog


def make_classroom(id_="A-101"):
    return Classroom(
        item_id=id_,
        name="Аудитория",
        category="lecture",
        year=2000,
        capacity=20,
        building="A",
    )


def test_save_and_load(tmp_path):
    cat = Catalog()
    cat.add(make_classroom("A"))
    cat.add(make_classroom("B"))
    path = tmp_path / "cat.json"
    save_catalog(cat, path)
    loaded = load_catalog(path)
    assert len(loaded) == 2
    assert [x.item_id for x in loaded] == ["A", "B"]
    assert loaded.get("A") == cat.get("A")


def test_unicode(tmp_path):
    cat = Catalog()
    cat.add(Classroom(
        item_id="A", name="Привет", category="lecture",
        year=2000, capacity=10, building="А",
    ))
    path = tmp_path / "cat.json"
    save_catalog(cat, path)
    text = path.read_text(encoding="utf-8")
    assert "Привет" in text


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_catalog(tmp_path / "nope.json")


def test_bad_json(tmp_path):
    p = tmp_path / "x.json"
    p.write_text("{bad}", encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        load_catalog(p)


def test_root_not_object(tmp_path):
    p = tmp_path / "x.json"
    p.write_text("[]", encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        load_catalog(p)


def test_no_version(tmp_path):
    p = tmp_path / "x.json"
    p.write_text('{"items": []}', encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        load_catalog(p)


def test_wrong_version(tmp_path):
    p = tmp_path / "x.json"
    p.write_text('{"format_version": 999, "items": []}', encoding="utf-8")
    with pytest.raises(UnsupportedFormatVersionError) as e:
        load_catalog(p)
    assert e.value.version == 999
    assert e.value.supported == FORMAT_VERSION


def test_items_not_list(tmp_path):
    p = tmp_path / "x.json"
    p.write_text('{"format_version": 1, "items": {}}', encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        load_catalog(p)


def test_item_not_dict(tmp_path):
    p = tmp_path / "x.json"
    p.write_text('{"format_version": 1, "items": [123]}', encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        load_catalog(p)


def test_missing_item_field(tmp_path):
    p = tmp_path / "x.json"
    data = {"format_version": 1, "items": [{"item_id": "A"}]}
    p.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(InvalidItemError):
        load_catalog(p)


def test_duplicate_in_file(tmp_path):
    item = {
        "item_id": "A", "name": "x", "category": "lecture",
        "year": 2000, "capacity": 10, "building": "A",
    }
    data = {"format_version": 1, "items": [item, item]}
    p = tmp_path / "x.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(DuplicateIdError):
        load_catalog(p)


def test_load_into_conflict(tmp_path):
    cat = Catalog()
    cat.add(make_classroom("A"))
    item = {
        "item_id": "A", "name": "x", "category": "lecture",
        "year": 2000, "capacity": 10, "building": "A",
    }
    data = {"format_version": 1, "items": [item]}
    p = tmp_path / "x.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(InvalidItemError):
        load_into(cat, p)
    # каталог не должен поменяться
    assert len(cat) == 1
    assert "A" in cat


def test_load_into_ok(tmp_path):
    cat = Catalog()
    cat.add(make_classroom("Z"))
    item = {
        "item_id": "A", "name": "Ауд", "category": "lecture",
        "year": 2000, "capacity": 10, "building": "A",
    }
    data = {"format_version": 1, "items": [item]}
    p = tmp_path / "x.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    load_into(cat, p)
    assert len(cat) == 2
    assert "A" in cat
    assert "Z" in cat