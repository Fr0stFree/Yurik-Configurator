from pathlib import Path
from typing import Optional
from threading import Thread

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

from app.base import BackendProtocol, ProcessTypes, senders

from .exceptions import InvalidFieldError, InvalidSkipFlag, ValidationError
from .sensor import SensorCluster, Sensor
from .utils import is_skip
from .validators import validate_min_max_values
from . import settings


class Backend(BackendProtocol):
    def __init__(self) -> None:
        self._error_counter: int = 0
        self._cluster = SensorCluster(settings.SENSOR_INTERVAL_X, settings.SENSOR_INTERVAL_Y, settings.SENSOR_MAX_X)
        self._process_type: ProcessTypes = ProcessTypes.default()
        self._is_running: bool = False
        self._data: Optional[Worksheet] = None

    def load(self, file_path: Path) -> None:
        try:
            workbook = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
            self._data = workbook["Таблица"]
        except Exception as exc:
            signal = senders.DataLoadingFailed(message=str(exc), path=file_path)
        else:
            signal = senders.DataLoaded(path=file_path)
        finally:
            signal.send()

    def start(self, min_row: Optional[str], max_row: Optional[str]) -> None:
        if not min_row:
            min_row = 2
        if not max_row:
            max_row = self._data.max_row

        try:
            min_row, max_row = validate_min_max_values(min_row, max_row)
        except ValidationError as error:
            signal = senders.UserInputValidationFailed(message=str(error))
        else:
            Thread(target=self._process, args=(min_row, max_row)).start()
            signal = senders.ProcessStarted(min_row, max_row)
        finally:
            signal.send()

    def stop(self) -> None:
        self._is_running = False
        message = "Обработка остановлена пользователем"
        signal = senders.ProcessStopped(message, on_success=True)
        signal.send()

    def save(self, save_to: Path) -> None:
        try:
            data = self._cluster.join(self._process_type)
            with open(save_to, "w", encoding="utf-8") as file:
                file.write(data)
        except Exception as exc:
            signal = senders.DataLoadingFailed(message=str(exc), path=save_to)
        else:
            signal = senders.DataSaved(path=save_to)
        finally:
            signal.send()

    def set_type(self, process_type: str) -> None:
        self._process_type = ProcessTypes(process_type)

    def get_type(self) -> ProcessTypes:
        return self._process_type

    def _process(self, min_row: int, max_row: int):
        self._is_running = True

        for row in range(min_row, max_row + 1):
            try:
                if not self._is_running:
                    break

                skip_flag = self._data[f"{settings.SKIP_FLAG_COLUMN}{row}"].value
                if is_skip(skip_flag):
                    signal = senders.SkipFlagDetected(row, column=settings.SKIP_FLAG_COLUMN)
                    signal.send()
                    continue

                sensor = Sensor.create(self._data, row)
                self._cluster.add(sensor)
                signal = senders.SensorValidated(str(sensor), row, column=settings.SENSOR_TYPE_COLUMN)
                signal.send()

                self._error_counter = 0

            except InvalidSkipFlag:
                message = f"Недопустимое значение флага пропуска на строке {row}."
                signal = senders.ProcessStopped(message, on_success=False)
                signal.send()
                break

            except InvalidFieldError as error:
                self._error_counter += 1
                if self._error_counter < settings.MAX_FAILURES_PER_RUN:
                    signal = senders.SensorValidationFailed(
                        message=str(error),
                        error_counter=self._error_counter,
                        row=row,
                        column=error.column,
                    )
                    signal.send()
                    continue

                message = f"Превышено максимальное количество ошибок ({settings.MAX_FAILURES_PER_RUN})."
                signal = senders.ProcessStopped(message, on_success=False)
                signal.send()
                break

        if self._is_running:
            signal = senders.ProcessStopped("Обработка успешно завершена", on_success=True)
            signal.send()
