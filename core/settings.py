from typing import Final, Tuple


SKIP_FLAG_COLUMN = 'B'
SENSOR_TYPE_COLUMN = 'C'
OMX_FILE_START_STRING = '<omx xmlns="system" xmlns:ct="automation.control">\n'
OMX_FILE_END_STRING = '</omx>'
MAX_FAILURES_PER_RUN = 1000
WINDOW_SIZE = 700, 420
LABEL_SIZE = 10, 1
INPUT_SIZE = 10, 1
WINDOW_TITLE = 'GA Parser'
BUTTON_SIZE = 10, 1
EVENT_BOX_SIZE = 0, 10
PROGRESS_BAR_SIZE = 10, 20
ABOUT_POPUP_TEXT = 'Бета-версия парсера. Свободное распространение разрешено.' \
                   ' Юрик Андрей. +7 (999) 671-89-94, tg: @yurjo'
INSTRUCTION_POPUP_TEXT = 'Значения "Начальная строка" и "Конечная строка" по дефолту можно оставить пустыми. ' \
                         ' Желательно удалить лишние галочки в конце EXCEL таблицы конфигуратора'
SUPPORTED_LOAD_FILE_TYPES: Final[Tuple[Tuple[str, str], ...]] = (
    ('Excel files', '*.xlsm'),
    ('Excel files', '*.xlsx'),
    ('Excel files', '*.xls'),
)
SUPPORTED_SAVE_FILE_TYPES: Final[Tuple[Tuple[str, str], ...]] = (
    ('OMX files', '*.omx-export'),
)
