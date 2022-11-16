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
