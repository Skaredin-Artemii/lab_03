"""Тесты сохранения и загрузки в JSON."""

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


def make_classroom(id_="A-101") -> Classroom:
    return Classroom(
        item_id=id_,
        name="Аудитория",
        category="lecture",
        year=2000,
        capacity=20,
        building="A",
    )

def test_round_trip(tmp_path):
    cat = Catalog()
    cat.add(make_classroom("A"))
    cat.add(make_classroom("B"))
    path = tmp_path / "cat.json"
    save_catalog(cat, path)
    loaded = load_catalog(path)
    assert len(loaded) == 2
    assert [x.item_id for x in loaded] == ["A", "B"]
    assert loaded.get("A") == cat.get("A")

def test_unicode_preserved(tmp_path):
    cat = Catalog()
    cat.add(Classroom(
        item_id="A",
        name="Привет",
        category="lecture",
        year=2000,
        capacity=10,
        building="А"
    ))
    path = tmp_path / "cat.json"
    save_catalog(cat, path)
    text = path.read_text(encoding="utf-8")
    assert "Привет" in text
    assert "\\u" not in text 

def test_missing_file_raises(tmp_path):
    path = tmp_path / "nonexistent.json"
    with pytest.raises(FileNotFoundError):
        load_catalog(path)


@pytest.mark.parametrize(
    "content, expected_reason",
    [
        ("{bad}", "невалидный JSON"),
        ("[]", "корень должен быть объектом"),
        ('{"items": []}', "отсутствует поле format_version"),
        ('{"format_version": "1", "items": []}', "format_version должен быть целым числом"),
        ('{"format_version": true, "items": []}', "format_version должен быть целым числом"),
        ('{"format_version": 1}', "отсутствует поле items"),
        ('{"format_version": 1, "items": {}}', "items должен быть списком"),
        ('{"format_version": 1, "items": [123]}', "элемент items[0] должен быть объектом"),
    ],
)
def test_corrupted_file_raises(tmp_path, content, expected_reason):
    path = tmp_path / "bad.json"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(CorruptedFileError) as exc_info:
        load_catalog(path)
    assert expected_reason in str(exc_info.value)


def test_unsupported_version_raises(tmp_path):
    path = tmp_path / "bad_version.json"
    path.write_text('{"format_version": 999, "items": []}', encoding="utf-8")
    with pytest.raises(UnsupportedFormatVersionError) as exc_info:
        load_catalog(path)
    assert exc_info.value.version == 999
    assert exc_info.value.supported == FORMAT_VERSION


def test_invalid_item_fields_raises(tmp_path):
    path = tmp_path / "bad_item.json"
    data = {
        "format_version": 1,
        "items": [{"item_id": "A"}],
    }
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(InvalidItemError):
        load_catalog(path)


def test_duplicate_id_in_file_raises(tmp_path):
    path = tmp_path / "dup.json"
    item = {
        "item_id": "A",
        "name": "x",
        "category": "lecture",
        "year": 2000,
        "capacity": 10,
        "building": "A",
    }
    data = {"format_version": 1, "items": [item, item]}
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(DuplicateIdError):
        load_catalog(path)


def test_load_into_transactional(tmp_path):
    cat = Catalog()
    cat.add(make_classroom("A"))
    path = tmp_path / "conflict.json"
    data = {
        "format_version": 1,
        "items": [
            {
                "item_id": "A",
                "name": "x",
                "category": "lecture",
                "year": 2000,
                "capacity": 10,
                "building": "A"
            }
        ],
    }
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(InvalidItemError):
        load_into(cat, path)
    assert len(cat) == 1
    assert "A" in cat