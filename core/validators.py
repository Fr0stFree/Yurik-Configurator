from types import NoneType
from typing import Any, Optional

from openpyxl.worksheet.worksheet import Worksheet

from .const import SEVERITY_SIGNALS, SEVERITY, SOUND_ON


def empty_value(value, location):
    if not value:
        raise ValueError(f'Ошибка. Ячейка одна из ячеек в строке {location} пуста.')


def sound_on(value, location):
    if value not in SEVERITY_SIGNALS.keys():
        raise ValueError(
            f'Ошибка. Ячейка {SOUND_ON.column}{location} имеет некорректное значение {value}'
        )


def severity_on(value, location):
    if value not in SEVERITY_SIGNALS.keys():
        raise ValueError(
            f'Ошибка. Ячейка {SEVERITY.column}{location} имеет некорректное значение {value}'
        )


def min_max_rows(sheet: Worksheet, min_row: Optional[str],
                 max_row: Optional[str]) -> tuple[int, NoneType]:
    try:
        min_row = validate_row_value(min_row)
    except ValueError:
        raise ValueError('Ошибка. Некорректное значение минимальной строки.')
    try:
        max_row = validate_row_value(max_row)
    except ValueError:
        raise ValueError('Ошибка. Некорректное значение максимальной строки.')

    if min_row is None:
        min_row = 2
    if max_row is None:
        max_row = sheet.max_row
    if min_row > max_row:
        raise ValueError('Ошибка. Минимальная строка больше максимальной.')
    return min_row, max_row


def validate_row_value(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError
    if not value.isdigit():
        raise ValueError
    return int(value)
