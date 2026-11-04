"""Исключения пакета catalog."""


class CatalogError(Exception):
    """Базовая ошибка пакета."""


class InvalidItemError(CatalogError):
    """Сущность не прошла валидацию."""

    def __init__(
        self,
        message: str,
        *,
        field: str | None = None,
    ) -> None:
        self.field = field
        if field is None:
            final = message
        else:
            final = f"{message} (поле: '{field}')"
        super().__init__(final)


class DuplicateIdError(CatalogError):
    """Попытка добавить аудиторию с существующим id."""

    def __init__(self, item_id: str) -> None:
        self.item_id = item_id
        super().__init__(f"Аудитория с id '{item_id}' уже есть в каталоге")


class ItemNotFoundError(CatalogError):
    """Аудитория с указанным id не найдена."""

    def __init__(self, item_id: str) -> None:
        self.item_id = item_id
        super().__init__(f"Аудитория с id '{item_id}' не найдена")


class UnsupportedFormatVersionError(CatalogError):
    """Версия формата в файле не поддерживается."""

    def __init__(self, version: int, *, supported: int) -> None:
        self.version = version
        self.supported = supported
        super().__init__(
            f"Версия формата {version} не поддерживается, ожидается {supported}"
        )


class CorruptedFileError(CatalogError):
    """Файл каталога поврежден или не соответствует формату"""

    def __init__(self, path: str, reason: str) -> None:
        self.path = path
        self.reason = reason
        super().__init__(f"Файл '{path}' поврежден: {reason}")
        