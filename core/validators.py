from typing import Any, Optional

from openpyxl.worksheet.worksheet import Worksheet

from .exceptions import InvalidValueError


def non_empty_value(value: Optional[str]) -> None:
    if value is None or value == '':
        raise InvalidValueError('Ошибка. Пустое значение.')


def min_max_rows(sheet: Worksheet, min_row: Optional[str],
                 max_row: Optional[str]) -> tuple[int, int]:
    try:
        min_row = validate_row_value(min_row)
    except ValueError:
        raise InvalidValueError('Ошибка. Некорректное значение минимальной строки.')
    try:
        max_row = validate_row_value(max_row)
    except ValueError:
        raise InvalidValueError('Ошибка. Некорректное значение максимальной строки.')

    if min_row is None:
        min_row = 2
    if max_row is None:
        max_row = sheet.max_row
    if min_row > max_row:
        raise InvalidValueError('Ошибка. Минимальная строка больше максимальной.')
    return min_row, max_row # Валидаторы не должны возвращать ничего, поправьте


def validate_row_value(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError
    if not value.isdigit():
        raise ValueError
    return int(value) # Валидаторы не должны возвращать ничего, поправьте
