from abc import ABC, abstractmethod
from pathlib import Path
from dataclasses import dataclass

from pydispatch import dispatcher

from .signals import Signals


class BaseSender(ABC):
    @property
    @abstractmethod
    def signal(self) -> Signals:
        pass

    def send(self):
        dispatcher.send(self.signal, sender=self)


@dataclass
class ProcessStarted(BaseSender):
    signal = Signals.PROCESS_STARTED
    min_row: int
    max_row: int


@dataclass
class ProcessStopped(BaseSender):
    signal = Signals.PROCESS_STOPPED
    message: str
    on_success: bool


@dataclass
class DataLoaded(BaseSender):
    signal = Signals.DATA_LOADED
    path: Path


@dataclass
class DataLoadingFailed(BaseSender):
    signal = Signals.DATA_LOADING_FAILED
    message: str
    path: Path


@dataclass
class DataSaved(BaseSender):
    signal = Signals.DATA_SAVED
    path: Path


@dataclass
class DataSavingFailed(BaseSender):
    signal = Signals.DATA_SAVING_FAILED
    message: str
    path: Path


@dataclass
class SensorValidated(BaseSender):
    signal = Signals.SENSOR_VALIDATED
    name: str
    row: int
    column: str


@dataclass
class SensorValidationFailed(BaseSender):
    signal = Signals.SENSOR_VALIDATION_FAILED
    message: str
    error_counter: int
    row: int
    column: str


@dataclass
class SkipFlagDetected(BaseSender):
    signal = Signals.SKIP_FLAG_DETECTED
    row: int
    column: str


@dataclass
class UserInputValidationFailed(BaseSender):
    signal = Signals.USER_INPUT_VALIDATION_FAILED
    message: str
