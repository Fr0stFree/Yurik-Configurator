from pathlib import Path
from enum import Enum


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

    @property
    def extension(self) -> str:
        options = {
            ProcessTypes.OMX: '.omx-export',
            ProcessTypes.HMI: '.omobj',
        }
        return options[self]


def save_data(path_from: Path, path_to: Path) -> None:
    """Функция сохранения текстового файла с omx-объектами по указанному пути."""
    with open(path_from, 'r', encoding='utf-8') as file_from, open(path_to, 'w', encoding='utf-8') as file_to:
        file_to.write(file_from.read())


def convert_to_file_path(path: str, extension: str = None) -> Path:
    file_path = Path(path)
    if extension:
        if not file_path.suffix:
            file_path = file_path.with_suffix(extension)
        else:
            file_path = file_path.parent / f'{file_path.stem}{extension}'

    return file_path


def to_snake_case(string: str) -> str:
    """Функция преобразования строки в snake_case."""
    return ''.join([s.lower() if s.islower() else f'_{s.lower()}' for s in string])
