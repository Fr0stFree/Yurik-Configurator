from enum import Enum, auto


class Signals(Enum):
    PROCESS_STOPPED = auto()
    PROCESS_STARTED = auto()

    DATA_LOADED = auto()
    DATA_LOADING_FAILED = auto()

    DATA_SAVED = auto()
    DATA_SAVING_FAILED = auto()

    SENSOR_VALIDATED = auto()
    SENSOR_VALIDATION_FAILED = auto()

    SKIP_FLAG_DETECTED = auto()
    USER_INPUT_VALIDATION_FAILED = auto()
