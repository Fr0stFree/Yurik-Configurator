import uuid

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

from . import validators
from .const import *


def load_sheet(file_path: str) -> Worksheet | None:
    """Функция загрузки excel-листа из файла."""
    try:
        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        sheet = wb.active
    except FileNotFoundError:
        print(f'Файл {file_path} не найден.')
        return None
    return sheet


def is_acceptable(cell_c, cell_b) -> bool:
    """Функция проверки ячеек C и B на пригодность."""
    conditions = []
    conditions.extend([cell_c ==    LOOKING_VALUE, bool(cell_b)])
    return all(conditions)


def create_omx_obj_for_SHPS(name: str, sensor_type: str, sound_on: str, message_on: str, severity: str,
                   color_on: str = '-', gp: str = '-', description: str = '-',
                   ivxx_tp: str = '-') -> str:
    """Функция создания omx-объекта с заданными параметрами для записи в текстовый файл."""
    _id = uuid.uuid5(uuid.NAMESPACE_DNS, name)
    omx_block = (
        f'  <ct:object {NAME.name}="{name}" base-type="Types.FB_SHPS_S.FB_SHPS_S_PLC" aspect="Aspects.PLC" access-level="public" uuid="{_id}">\n'
        f'    <attribute type="Attributes.{SENSOR_TYPE.name}" value="{sensor_type}" />\n'
        f'    <attribute type="Attributes.{COLOR_ON.name}" value="{color_on}" />\n'
        f'    <attribute type="Attributes.{GP.name}" value="{gp}" />\n'
        f'    <attribute type="Attributes.{SOUND_ON.name}" value="{sound_on}" />\n'
        f'    <attribute type="Attributes.{MESSAGE_ON.name}" value="{message_on}" />\n'
        f'    <attribute type="unit.System.Attributes.{DESCRIPTION.name}" value="{description}" />\n'
        f'    <attribute type="Attributes.{SEVERITY.name}" value="{severity}" />\n'
        f'    <attribute type="Attributes.{IVXX_TP.name}" value="{ivxx_tp}" />\n'
        f'  </ct:object>\n'
    )
    return omx_block


def create_omx_obj_for_SHOP(name: str, siren_type: str, sound_on: str, message_on: str, severity: str,
                   color_on: str = '-', gp: str = '-', description: str = '-',
                   ivxx_tp: str = '-') -> str:
    """Функция создания omx-объекта с заданными параметрами для записи в текстовый файл."""
    _id = uuid.uuid5(uuid.NAMESPACE_DNS, name)
    omx_block = (
        f'  <ct:object {NAME.name}="{name}" base-type="Types.FB_SHOP_S.FB_SHOP_S_PLC" aspect="Aspects.PLC" access-level="public" uuid="{_id}">\n'
        f'    <attribute type="Attributes.{SIREN_TYPE.name}" value="{siren_type}" />\n'
        f'    <attribute type="Attributes.{COLOR_ON.name}" value="{color_on}" />\n'
        f'    <attribute type="Attributes.{GP.name}" value="{gp}" />\n'
        f'    <attribute type="Attributes.{SOUND_ON.name}" value="{sound_on}" />\n'
        f'    <attribute type="unit.System.Attributes.{DESCRIPTION.name}" value="{description}" />\n'
        f'    <attribute type="Attributes.{SEVERITY.name}" value="{severity}" />\n'
        f'    <attribute type="Attributes.{IVXX_TP.name}" value="{ivxx_tp}" />\n'
        f'  </ct:object>\n'
    )
    return omx_block

def get_row_values_SHPS(sheet: Worksheet, row: int) -> dict[str, str]:
    """Функция получения значений ячеек из строки."""
    kwargs = dict(name=sheet[f"{NAME.column}{row}"].value,
                  sensor_type=sheet[f"{SENSOR_TYPE.column}{row}"].value,
                  color_on=sheet[f"{COLOR_ON.column}{row}"].value,
                  gp=sheet[f"{GP.column}{row}"].value,
                  sound_on=sheet[f"{SOUND_ON.column}{row}"].value,
                  severity=sheet[f"{SEVERITY.column}{row}"].value,
                  message_on=sheet[f"{MESSAGE_ON.column}{row}"].value,
                  description=sheet[f"{DESCRIPTION.column}{row}"].value,
                  ivxx_tp=sheet[f"{IVXX_TP.column}{row}"].value)
    return kwargs


def get_row_values_SHOP(sheet: Worksheet, row: int) -> dict[str, str]:
    """Функция получения значений ячеек из строки."""
    kwargs = dict(name=sheet[f"{NAME.column}{row}"].value,
                  siren_type=sheet[f"{SIREN_TYPE.column}{row}"].value,
                  color_on=sheet[f"{COLOR_ON.column}{row}"].value,
                  gp=sheet[f"{GP.column}{row}"].value,
                  sound_on=sheet[f"{SOUND_ON.column}{row}"].value,
                  description=sheet[f"{DESCRIPTION.column}{row}"].value,
                  # message_on=sheet[f"{MESSAGE_ON.column}{row}"].value,
                  severity=sheet[f"{SEVERITY.column}{row}"].value,
                  ivxx_tp=sheet[f"{IVXX_TP.column}{row}"].value)
    return kwargs


def is_valid(row: int, kwargs: dict[str, str]) -> bool:
    """Функция применяет валидаторы к данным, находящимся в строке."""
    try:
        [validators.empty_value(kwargs[field.key], location=row) for field in NON_EMPTY_FIELDS]
        validators.sound_on(kwargs[SOUND_ON.key], location=row)
        validators.severity_on(kwargs[SEVERITY.key], location=row)
    except ValueError as e:
        print(e)
        return False
    return True


def process_row(sheet: Worksheet, row: int) -> str:
    """Функция обработки строки."""
    c_cell, b_cell = sheet[f"C{row}"].value, sheet[f"B{row}"].value
    if not is_acceptable(c_cell, b_cell):
        raise ValueError(f'Строка {row} невалидна!')
    values = get_row_values(sheet, row)
    if is_valid(row, values):
        return create_omx_obj(**values)


def save_data(file_path: str, data: str) -> None:
    """Функция сохранения текстового файла с omx-объектами по указанному пути в формате str."""
    with open(file_path, 'w') as f:
        f.write(data)
