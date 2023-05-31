from pathlib import Path
from typing import Optional

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

from core.exceptions import InvalidValueError
from core.settings import ProcessTypes
from core.validators import value_is_digit_or_none


def load_sheet(file_path: Path) -> Optional[Worksheet]:
    """Функция загрузки excel-листа из файла."""
    try:
        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        sheet = wb['Таблица']
    except FileNotFoundError:
        print(f'Файл {file_path} не найден.')
        return None
    return sheet


def save_data(path_from: Path, path_to: Path) -> None:
    """Функция сохранения текстового файла с omx-объектами по указанному пути."""
    with open(path_from, 'r', encoding='utf-8') as file_from:
        with open(path_to, 'w', encoding='utf-8') as file_to:
            file_to.write(file_from.read())
    path_from.unlink()

def convert_to_file_path(path: str, extension: str = None) -> Path:
    file_path = Path(path)
    if extension:
        if not file_path.suffix:
            file_path = file_path.with_suffix(extension)
        else:
            file_path = file_path.parent / f'{file_path.stem}{extension}'

    return file_path


def get_calculation_limits(sheet: Worksheet,
                           min_row: str,
                           max_row: str) -> tuple[int, int]:
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


def to_snake_case(string: str) -> str:
    """Функция преобразования строки в snake_case."""
    return ''.join([s.lower() if s.islower() else f'_{s.lower()}' for s in string])


def match_extension(process_type: str) -> str:
    """Функция соответствия расширения файла типу обработки."""
    extensions = {
        ProcessTypes.OMX.value: '.omx-export',
        ProcessTypes.HMI.value: '.omobj',
    }
    return extensions[process_type]
