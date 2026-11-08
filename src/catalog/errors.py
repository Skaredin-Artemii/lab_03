"""Исключения пакета catalog."""


class CatalogError(Exception):
    """Общая ошибка пакета."""


class InvalidItemError(CatalogError):
    """Аудитория не прошла проверку."""

    def __init__(self, message, field=None):
        self.field = field
        if field is not None:
            message = f"{message} (поле: {field})"
        super().__init__(message)


class DuplicateIdError(CatalogError):
    """Такой id уже есть в каталоге."""

    def __init__(self, item_id):
        self.item_id = item_id
        super().__init__(f"Аудитория с id '{item_id}' уже есть в каталоге")


class ItemNotFoundError(CatalogError):
    """Аудитории с таким id нет."""

    def __init__(self, item_id):
        self.item_id = item_id
        super().__init__(f"Аудитория с id '{item_id}' не найдена")


class UnsupportedFormatVersionError(CatalogError):
    """Версия формата в файле не поддерживается."""

    def __init__(self, version, supported):
        self.version = version
        self.supported = supported
        super().__init__(
            f"Версия формата {version} не поддерживается, нужна {supported}"
        )


class CorruptedFileError(CatalogError):
    """Файл поврежден или не того формата."""

    def __init__(self, path, reason):
        self.path = path
        self.reason = reason
        super().__init__(f"Файл '{path}' поврежден: {reason}")