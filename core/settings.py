from enum import Enum
from typing import Final, Tuple


class ProcessTypes(Enum):
    OMX = 'to OMX'
    HMI = 'to HMI'

    @property
    def start_string(self) -> str:
        options = {
            ProcessTypes.OMX: '<omx xmlns="system" xmlns:ct="automation.control">\n',
            ProcessTypes.HMI: '<type access-modifier="private" name="ParcerHMI" display-name="ParcerHMI" uuid="9a110b5c-0c05-4f31-b7ec-58eb4abcc96e" base-type="Form" base-type-id="ffaf5544-6200-45f4-87ec-9dd24558a9d5" ver="4">\n'
                              '    <designed target="X" value="0" ver="4"/>\n'
                              '    <designed target="Y" value="0" ver="4"/>\n'
                              '    <designed target="ZValue" value="0" ver="4"/>\n'
                              '    <designed target="Rotation" value="0" ver="4"/>\n'
                              '    <designed target="Scale" value="1" ver="4"/>\n'
                              '    <designed target="Visible" value="true" ver="4"/>\n'
                              '    <designed target="Opacity" value="1" ver="4"/>\n'
                              '    <designed target="Enabled" value="true" ver="4"/>\n'
                              '    <designed target="Tooltip" value="" ver="4"/>\n'
                              '    <designed target="Width" value="3000" ver="4"/>\n'
                              '    <designed target="Height" value="3000" ver="4"/>\n'
                              '    <designed target="PenColor" value="0xff000000" ver="4"/>\n'
                              '    <designed target="PenStyle" value="0" ver="4"/>\n'
                              '    <designed target="PenWidth" value="1" ver="4"/>\n'
                              '    <designed target="BrushColor" value="0xffc0c0c0" ver="4"/>\n'
                              '    <designed target="BrushStyle" value="1" ver="4"/>\n'
                              '    <designed target="WindowX" value="0" ver="4"/>\n'
                              '    <designed target="WindowY" value="0" ver="4"/>\n'
                              '    <designed target="WindowWidth" value="1920" ver="4"/>\n'
                              '    <designed target="WindowHeight" value="1080" ver="4"/>\n'
                              '    <designed target="WindowCaption" value="" ver="4"/>\n'
                              '    <designed target="ShowWindowCaption" value="true" ver="4"/>\n'
                              '    <designed target="ShowWindowMinimize" value="true" ver="4"/>\n'
                              '    <designed target="ShowWindowMaximize" value="true" ver="4"/>\n'
                              '    <designed target="ShowWindowClose" value="true" ver="4"/>\n'
                              '    <designed target="AlwaysOnTop" value="false" ver="4"/>\n'
                              '    <designed target="WindowSizeMode" value="0" ver="4"/>\n'
                              '    <designed target="WindowBorderStyle" value="1" ver="4"/>\n'
                              '    <designed target="WindowState" value="0" ver="4"/>\n'
                              '    <designed target="WindowScalingMode" value="0" ver="4"/>\n'
                              '    <designed target="MonitorNumber" value="0" ver="4"/>\n'
                              '    <designed target="WindowPosition" value="0" ver="4"/>\n'
                              '    <designed target="WindowCloseMode" value="0" ver="4"/>\n',
        }
        return options[self]

    @property
    def end_string(self) -> str:
        options = {
            ProcessTypes.OMX: '</omx>',
            ProcessTypes.HMI: '</type>',
        }
        return options[self]


SKIP_FLAG_COLUMN = 'B'
SENSOR_TYPE_COLUMN = 'C'
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
SUPPORTED_SAVE_FILE_TYPES = {
    ProcessTypes.OMX: (('OMX files', '*.omx-export'),),
    ProcessTypes.HMI: (('OMO files', '*.omobj'),),
}
