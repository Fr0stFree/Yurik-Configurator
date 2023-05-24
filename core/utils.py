from typing import Union

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

from core.exceptions import InvalidValueError
from core.validators import value_is_digit_or_none


def load_sheet(file_path: str) -> Union[Worksheet, None]:
    """Функция загрузки excel-листа из файла."""
    try:
        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        sheet = wb['Таблица']
    except FileNotFoundError:
        print(f'Файл {file_path} не найден.')
        return None
    return sheet


def save_data(path_from: str, path_to: str) -> None:
    """Функция сохранения текстового файла с omx-объектами по указанному пути."""
    with open(path_from, 'r', encoding='utf-8') as file_from:
        with open(path_to, 'w', encoding='utf-8') as file_to:
            file_to.write(file_from.read())


def get_calculation_limits(sheet: Worksheet, min_row: Union[str],
                           max_row: Union[str]) -> tuple[int, int]:
    """Функция получения диапазона расчёта из GUI."""
    for value in (min_row, max_row):
        try:
            value_is_digit_or_none(value)
        except ValueError:
            raise InvalidValueError('введите число или оставьте поле пустым.')

    if min_row is None or min_row == '':
        min_row = 2
    else:
        min_row = int(min_row)
    if max_row is None or max_row == '':
        max_row = sheet.max_row
    else:
        max_row = int(max_row)
    if min_row > max_row:
        raise InvalidValueError('минимальная строка больше максимальной.')
    return min_row, max_row


def get_progress(current: int, start: int, finish: int) -> int:
    """Функция получения прогресса выполнения."""
    try:
        progress = int((current - start) / (finish - start) * 100)
    except ZeroDivisionError:
        progress = 100
    return progress


def to_snake_case(string: str) -> str:
    """Функция преобразования строки в snake_case."""
    return ''.join([s.lower() if s.islower() else f'_{s.lower()}' for s in string])
