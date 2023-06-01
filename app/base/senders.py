from abc import ABC, abstractmethod
from pathlib import Path

from pydispatch import dispatcher

from .signals import Signals


class BaseSender(ABC):
    @property
    @abstractmethod
    def signal(self) -> Signals:
        pass

    def send(self):
        dispatcher.send(self.signal, sender=self)


class ProcessStarted(BaseSender):
    signal = Signals.PROCESS_STARTED

    def __init__(self, min_row: int, max_row: int) -> None:
        self.min_row = min_row
        self.max_row = max_row


class ProcessStopped(BaseSender):
    signal = Signals.PROCESS_STOPPED

    def __init__(self, message: str, on_success: bool) -> None:
        self.message = message
        self.on_success = on_success


class DataLoaded(BaseSender):
    signal = Signals.DATA_LOADED

    def __init__(self, path: Path):
        self.path = path


class DataLoadingFailed(BaseSender):
    signal = Signals.DATA_LOADING_FAILED

    def __init__(self, message: str, path: Path):
        self.message = message
        self.path = path


class DataSaved(BaseSender):
    signal = Signals.DATA_SAVED

    def __init__(self, path: Path):
        self.path = path


class DataSavingFailed(BaseSender):
    signal = Signals.DATA_SAVING_FAILED

    def __init__(self, message: str, path: Path):
        self.message = message
        self.path = path


class SensorValidated(BaseSender):
    signal = Signals.SENSOR_VALIDATED

    def __init__(self, name: str, row: int, column: str) -> None:
        self.name = name
        self.row = row
        self.column = column


class SensorValidationFailed(BaseSender):
    signal = Signals.SENSOR_VALIDATION_FAILED

    def __init__(self, message: str, error_counter: int, row: int, column: str) -> None:
        self.message = message
        self.error_counter = error_counter
        self.row = row
        self.column = column


class SkipFlagDetected(BaseSender):
    signal = Signals.SKIP_FLAG_DETECTED

    def __init__(self, row: int, column: str) -> None:
        self.row = row
        self.column = column


class UserInputValidationFailed(BaseSender):
    signal = Signals.USER_INPUT_VALIDATION_FAILED

    def __init__(self, message: str) -> None:
        self.message = message
