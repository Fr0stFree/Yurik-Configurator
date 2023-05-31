from pathlib import Path
from typing import Optional

import openpyxl
from pydispatch import dispatcher
from openpyxl.worksheet.worksheet import Worksheet

from . import settings, signals
from .sensors import Sensor
from .exceptions import ValidationError, InvalidValueError
from .validators import value_is_digit_or_none
from .utils import ProcessTypes


class Processor:
    def __init__(self) -> None:
        self._is_running: bool = False
        self._sheet: Optional[Worksheet] = None
        self._type: ProcessTypes = ProcessTypes.OMX

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = ProcessTypes(value)

    @property
    def is_running(self) -> bool:
        return self._is_running

    def load_sheet(self, file_path: Path):
        """Функция загрузки excel-листа из файла."""
        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        self._sheet = wb['Таблица']

    def get_calculation_limits(self, min_row: str, max_row: str) -> tuple[int, int]:
        """Функция получения диапазона расчёта из GUI."""
        for value in (min_row, max_row):
            try:
                value_is_digit_or_none(value)
            except ValueError:
                raise InvalidValueError('Введите число или оставьте поле пустым.')

        if min_row is None or min_row == '':
            min_row = 2
        else:
            min_row = int(min_row)
        if max_row is None or max_row == '':
            max_row = self._sheet.max_row
        else:
            max_row = int(max_row)
        if min_row > max_row:
            raise InvalidValueError('Минимальная строка больше максимальной.')
        return min_row, max_row

    def stop(self):
        self._is_running = False

    def run(self, min_row: int, max_row: int):
        self._is_running = True

        for row in range(min_row, max_row + 1):
            if not self.is_running:
                break

            skip_flag = self._sheet[f'{settings.SKIP_FLAG_COLUMN}{row}'].value
            if skip_flag not in (0, 1):
                dispatcher.send(signals.STOP_PROCESSING,
                                reason=f'Неверное значение флага пропуска на строке {row}.')
                break

            if skip_flag == 0:
                dispatcher.send(signals.SKIP_FLAG_DETECTED, row=row)
                continue

            try:
                sensor = Sensor.create(self._sheet, row)
                dispatcher.send(signals.SENSOR_DETECTED, sensor, row=row)

            except ValidationError as exc:
                dispatcher.send(signals.VALIDATION_FAILED, exc, row=row)

        if self.is_running:
            dispatcher.send(signals.STOP_PROCESSING, reason='Обработка успешно завершена.')
