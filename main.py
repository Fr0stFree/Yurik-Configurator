import openpyxl


from core.utils import create_omx_file, load_sheet
from core.gui import Configurator

INPUT_FILE_PATH = 'input_data.xlsx'
SHEET_NAME = 'Таблица'
OUTPUT_FILE_PATH = 'output.omx-export'
LOOKING_VALUE = 'FB_SHPS_S'


if __name__ == '__main__':
    configurator = Configurator()
    configurator.run()
#     sheet = load_sheet(file_path=INPUT_FILE_PATH, sheet_name=SHEET_NAME)
#     if sheet:
#         create_omx_file(file_path=OUTPUT_FILE_PATH, sheet=sheet)

