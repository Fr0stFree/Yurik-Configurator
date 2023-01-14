import openpyxl
from openpyxl.worksheet.worksheet import Worksheet


def load_sheet(file_path: str) -> Worksheet | None:
    """Функция загрузки excel-листа из файла."""
    try:
        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        sheet = wb.active
    except FileNotFoundError:
        print(f'Файл {file_path} не найден.')
        return None
    return sheet


def save_data(file_path: str, data: str) -> None:
    """Функция сохранения текстового файла с omx-объектами по указанному пути в формате str."""
    with open(file_path, 'w') as f:
        f.write(data)


# def create_omx_obj_for_SHOP(name: str, siren_type: str, sound_on: str, severity: str,
#                    color_on: str = '-', gp: str = '-', description: str = '-',
#                    ivxx_tp: str = '-') -> str:
#     """Функция создания omx-объекта с заданными параметрами для записи в текстовый файл."""
#     _id = uuid.uuid5(uuid.NAMESPACE_DNS, name)
#     omx_block = (
#         f'  <ct:object {NAME.name}="{name}" base-type="Types.FB_SHOP_S.FB_SHOP_S_PLC" aspect="Aspects.PLC" access-level="public" uuid="{_id}">\n'
#         f'    <attribute type="Attributes.{SIREN_TYPE.name}" value="{siren_type}" />\n'
#         f'    <attribute type="Attributes.{COLOR_ON.name}" value="{color_on}" />\n'
#         f'    <attribute type="Attributes.{GP.name}" value="{gp}" />\n'
#         f'    <attribute type="Attributes.{SOUND_ON.name}" value="{sound_on}" />\n'
#         f'    <attribute type="unit.System.Attributes.{DESCRIPTION.name}" value="{description}" />\n'
#         f'    <attribute type="Attributes.{SEVERITY.name}" value="{severity}" />\n'
#         f'    <attribute type="Attributes.{IVXX_TP.name}" value="{ivxx_tp}" />\n'
#         f'  </ct:object>\n'
#     )
#     return omx_block
#
# def create_omx_obj_for_QSA(name: str,
#                            e_unit: str,
#                            sensor_position: str,
#                            sensor_type: str,
#                            description: str,
#                            substance: str,
#                            gp: str,
#                            ifex_tp: str,
#                            it1x_tp: str,
#                            it2x_tp: str,
#                            ivxx_tp: str = '-') -> str:
#     """Функция создания omx-объекта с заданными параметрами для записи в текстовый файл."""
#     _id = uuid.uuid5(uuid.NAMESPACE_DNS, name)
#     omx_block = (
#         f'  <ct:object {NAME.name}="{name}" base-type="Types.FB_QSA_S.FB_QSA_S_PLC" aspect="Aspects.PLC" access-level="public" uuid="{_id}">\n'
#         f'    <attribute type="Attributes.{E_UNIT.name}" value="{e_unit}" />\n'
#         f'    <attribute type="Attributes.FracDigits" value="2" />\n'
#         f'    <attribute type="Attributes.{SENSOR_POSITION.name}" value="{sensor_position}" />\n'
#         f'    <attribute type="Attributes.{SENSOR_TYPE.name}" value="{sensor_type}" />\n'
#         f'    <attribute type="Attributes.{DESCRIPTION.name}" value="{description}" />\n'
#         f'    <attribute type="Attributes.{IVXX_TP.name}" value="{ivxx_tp}" />\n'
#         f'    <attribute type="Attributes.{SUBSTANCE.name}" value="{substance}" />\n'
#         f'    <attribute type="Attributes.{GP.name}" value="{gp}" />\n'
#         f'    <attribute type="Attributes.{IFEX_TP.name}" value="{ifex_tp}" />\n'
#         f'    <attribute type="Attributes.{IT1X_TP.name}" value="{it1x_tp}" />\n'
#         f'    <attribute type="Attributes.{IT2X_TP.name}" value="{it2x_tp}" />\n'
#         f'  </ct:object>\n'
#     )
#     return omx_block
#
# def create_omx_obj_for_DI(name: str, sensor_type: str, sound_on: str, message_on: str, severity: str,
#                    color_on: str = '-', gp: str = '-', description: str = '-',
#                    ivxx_tp: str = '-') -> str:
#     """Функция создания omx-объекта с заданными параметрами для записи в текстовый файл."""
#     _id = uuid.uuid5(uuid.NAMESPACE_DNS, name)
#     omx_block = (
#         f'  <ct:object {NAME.name}="{name}" base-type="Types.FB_DI_S.FB_DI_S_PLC" aspect="Aspects.PLC" access-level="public" uuid="{_id}">\n'
#         f'    <attribute type="Attributes.ColorOff" value="серый" />\n'
#         f'    <attribute type="Attributes.{COLOR_ON.name}" value="{color_on}" />\n'
#         f'    <attribute type="Attributes.{MESSAGE_ON.name}" value="{message_on}" />\n'
#         f'    <attribute type="Attributes.{SEVERITY.name}" value="{severity}" />\n'
#         f'    <attribute type="Attributes.{SOUND_ON.name}" value="{sound_on}" />\n'
#         f'    <attribute type="unit.System.Attributes.{DESCRIPTION.name}" value="{description}" />\n'
#         f'    <attribute type="Attributes.{GP.name}" value="{gp}" />\n'
#         f'    <attribute type="Attributes.{SENSOR_TYPE.name}" value="{sensor_type}" />\n'
#         f'    <attribute type="Attributes.{IVXX_TP.name}" value="{ivxx_tp}" />\n'
#         f'  </ct:object>\n'
#     )
#     return
#
#
# def create_omx_obj_for_DO(name: str,
#
#                         sound_on: str, severity: str,
#                    color_on: str = '-', gp: str = '-', description: str = '-') -> str:
#     """Функция создания omx-объекта с заданными параметрами для записи в текстовый файл."""
#     _id = uuid.uuid5(uuid.NAMESPACE_DNS, name)
#     omx_block = (
#         f'  <ct:object {NAME.name}="{name}" Types.FB_DO_STB_S.FB_DO_STB_S_PLC" aspect="Aspects.PLC" access-level="public" uuid="{_id}">\n'
#         f'    <attribute type="Attributes.{GP.name}" value="{gp}" />\n'
#         f'    <attribute type="Attributes.{COLOR_ON.name}" value="{color_on}" />\n'
#         f'    <attribute type="Attributes.{SOUND_ON.name}" value="{sound_on}" />\n'
#         f'    <attribute type="Attributes.{DESCRIPTION.name}" value="{description}" />\n'
#         f'    <attribute type="Attributes.{SEVERITY.name}" value="{severity}" />\n'
#         f'    <attribute type="Attributes.{OXON_TP.name}" value="{oxon_tp}" />\n'
#         f'  </ct:object>\n'
#     )
#     return omx_block
#
#
# def create_omx_obj_for_AI(name: str,
#                            e_unit: str,
#                            sensor_position: str,
#                            sensor_type: str,
#                            description: str,
#                            substance: str,
#                            gp: str,
#                            ifex_tp: str,
#                            it1x_tp: str,
#                            it2x_tp: str,
#                            ivxx_tp: str = '-') -> str:
#     """Функция создания omx-объекта с заданными параметрами для записи в текстовый файл."""
#     _id = uuid.uuid5(uuid.NAMESPACE_DNS, name)
#     omx_block = (
#         f'  <ct:object {NAME.name}="{name}" base-type="Types.FB_AI_S.FB_AI_S_PLC" aspect="Aspects.PLC" access-level="public" uuid="{_id}">\n'
#         f'    <attribute type="Attributes.{E_UNIT.name}" value="{e_unit}" />\n'
#         f'    <attribute type="Attributes.FracDigits" value="2" />
#         f'    <attribute type="Attributes.{SENSOR_POSITION.name}" value="{sensor_position}" />\n'
#         f'    <attribute type="Attributes.{SENSOR_TYPE.name}" value="{sensor_type}" />\n'
#         f'    <attribute type="Attributes.{DESCRIPTION.name}" value="{description}" />\n'
#         f'    <attribute type="Attributes.{IVXX_TP.name}" value="{ivxx_tp}" />\n'
#         f'    <attribute type="Attributes.{SUBSTANCE.name}" value="{substance}" />\n'
#         f'    <attribute type="Attributes.{GP.name}" value="{gp}" />\n'
#         f'    <attribute type="Attributes.{IFEX_TP.name}" value="{ifex_tp}" />\n'
#         f'    <attribute type="Attributes.{IT1X_TP.name}" value="{it1x_tp}" />\n'
#         f'    <attribute type="Attributes.{IT2X_TP.name}" value="{it2x_tp}" />\n'
#         f'  </ct:object>\n'
#     )
#     return omx_block
#
#
#
# def create_omx_obj_for_UPG(name: str,
#                            description: str,
#                            second_queue: str,
#                            e_unit: str,
#                            gp: str,
#                            ) -> str:
#     """Функция создания omx-объекта с заданными параметрами для записи в текстовый файл."""
#     _id = uuid.uuid5(uuid.NAMESPACE_DNS, name)
#     omx_block = (
#         f'  <ct:object {NAME.name}="{name}" base-type="Types.FB_UPG_S.FB_UPG_S_PLC" aspect="Aspects.PLC" access-level="public" uuid="{_id}">\n'
#         f'    <attribute type="unit.System.Attributes.{DESCRIPTION.name}" value="{description}" />\n'
#         f'    <attribute type="Attributes.{SECOND_QUEUE.name}" value="{second_queue}" />\n'
#         f'    <attribute type="Attributes.{E_UNIT.name}" value="{e_unit}" />\n'
#         f'    <attribute type="Attributes.{GP.name}" value="{gp}" />\n'
#         f'  </ct:object>\n'
#     )
#     return omx_block
#

#
#
# def get_row_values_for_SHOP(sheet: Worksheet, row: int) -> dict[str, str]:
#     """Функция получения значений ячеек из строки."""
#     kwargs = dict(name=sheet[f"{NAME.column}{row}"].value,
#                   siren_type=sheet[f"{SIREN_TYPE.column}{row}"].value,
#                   color_on=sheet[f"{COLOR_ON.column}{row}"].value,
#                   gp=sheet[f"{GP.column}{row}"].value,
#                   sound_on=sheet[f"{SOUND_ON.column}{row}"].value,
#                   description=sheet[f"{DESCRIPTION.column}{row}"].value,
#                   severity=sheet[f"{SEVERITY.column}{row}"].value,
#                   ivxx_tp=sheet[f"{IVXX_TP.column}{row}"].value)
#     return kwargs
#
#
# def get_row_values_for_QSA(sheet: Worksheet, row: int) -> dict[str, str]:
#     """Функция получения значений ячеек из строки."""
#     kwargs = dict(name=sheet[f"{NAME.column}{row}"].value,
#                   e_unit=sheet[f"{E_UNIT.column}{row}"].value,
#                   frac_digits=sheet[f"{FRAC_DIGITS.column}{row}"].value,
#                   sensor_position=sheet[f"{SENSOR_POSITION.column}{row}"].value,
#                   sensor_type=sheet[f"{SENSOR_TYPE.column}{row}"].value,
#                   description=sheet[f"{DESCRIPTION.column}{row}"].value,
#                   ivxx_tp=sheet[f"{IVXX_TP.column}{row}"].value,
#                   substance=sheet[f"{SUBSTANCE.column}{row}"].value),
#                   gp=sheet[f"{GP.column}{row}"].value,
#                   ifex_tp=sheet[f"{IFEX_TP.column}{row}"].value,
#                   it1x_tp=sheet[f"{IT1X_TP.column}{row}"].value,
#                   it2x_tp=sheet[f"{IT2X_TP.column}{row}"].value)
#     return kwargs
#
#
# def get_row_values_for_DI(sheet: Worksheet, row: int) -> dict[str, str]:
#     """Функция получения значений ячеек из строки."""
#     kwargs = dict(name=sheet[f"{NAME.column}{row}"].value,
#                   color_off=sheet[f"{COLOR_OFF.column}{row}"].value,
#                   color_on=sheet[f"{COLOR_ON.column}{row}"].value,
#                   message_on=sheet[f"{MESSAGE_ON.column}{row}"].value,
#                   severity=sheet[f"{SEVERITY.column}{row}"].value,
#                   sound_on=sheet[f"{SOUND_ON.column}{row}"].value,
#                   description=sheet[f"{DESCRIPTION.column}{row}"].value,
#                   gp=sheet[f"{IVXX_TP.column}{row}"].value,
#                   sensor_type=sheet[f"{SENSOR_TYPE.column}{row}"].value,
#                   ivxx_tp = sheet[f"{IVXX_TP.column}{row}"].value)
#     return kwargs
#
#
# def get_row_values_for_DO(sheet: Worksheet, row: int) -> dict[str, str]:
#     """Функция получения значений ячеек из строки."""
#     kwargs = dict(name=sheet[f"{NAME.column}{row}"].value,
#                   gp=sheet[f"{GP.column}{row}"].value,
#                   color_on=sheet[f"{COLOR_ON.column}{row}"].value,
#                   sound_on=sheet[f"{SOUND_ON.column}{row}"].value,
#                   description=sheet[f"{DESCRIPTION.column}{row}"].value,
#                   severity=sheet[f"{SEVERITY.column}{row}"].value,
#                   oxon_tp = sheet[f"{OXON_TP.column}{row}"].value)
#     return kwargs
#
#
# def get_row_values_for_AI(sheet: Worksheet, row: int) -> dict[str, str]:
#     """Функция получения значений ячеек из строки."""
#     kwargs = dict(name=sheet[f"{NAME.column}{row}"].value,
#                   e_unit=sheet[f"{E_UNIT.column}{row}"].value,
#                   frac_digits=sheet[f"{FRAC_DIGITS.column}{row}"].value,
#                   par_name=sheet[f"{PAR_NAME.column}{row}"].value,
#                   sensor_position=sheet[f"{SENSOR_POSITION.column}{row}"].value,
#                   sensor_type=sheet[f"{SENSOR_TYPE.column}{row}"].value,
#                   description=sheet[f"{DESCRIPTION.column}{row}"].value,
#                   ivxx_tp=sheet[f"{IVXX_TP.column}{row}"].value,
#                   gp=sheet[f"{GP.column}{row}"].value)
#
#     return kwargs
#
#
# def get_row_values_for_UPG(sheet: Worksheet, row: int) -> dict[str, str]:
#     """Функция получения значений ячеек из строки."""
#     kwargs = dict(name=sheet[f"{NAME.column}{row}"].value,
#                   description=sheet[f"{DESCRIPTION.column}{row}"].value,
#                   second_queue=sheet[f"{SECOND_QUEUE.column}{row}"].value,
#                   gp=sheet[f"{GP.column}{row}"].value)
#
#     return kwargs
#
