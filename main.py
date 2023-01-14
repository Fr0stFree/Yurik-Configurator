from typing import Optional
from threading import Thread

import PySimpleGUI as GUI
from openpyxl.worksheet.worksheet import Worksheet

from core.gui import GraphicalUserInterface
from core.utils import save_data, load_sheet
from core.sensors import Sensor, FB_SHPS_S
from core.exceptions import InvalidValueError, UnknownSensorTypeError
from core import settings
from core import validators


class Configurator(GraphicalUserInterface):
    def __init__(self):
        super().__init__()
        self.min_row: Optional[int] = None
        self.max_row: Optional[int] = None
        self.sheet: Optional[Worksheet] = None
        self.omx_file: Optional[str] = None
        self.process: bool = True

    def run(self):
        while True:
            event, values = self.window.read()

            # Загрузка данных
            if event == self.load_data_btn.key:
                path = GUI.popup_get_file('Load data', file_types=(('Excel files', '*.xlsx'),))
                if path:
                    self.sheet = load_sheet(file_path=path)
                    if self.sheet:
                        self.window[self.process_data_btn.key].update(disabled=False)
                        self.process = True
                        print(f'Таблица "{self.sheet.title}" успешно загружена.')
                    else:
                        print('Ошибка загрузки таблицы.')

            # Обработка данных
            elif event == self.process_data_btn.key:
                try:
                    min_row, max_row = validators.min_max_rows(self.sheet, self.min_row, self.max_row)
                except ValueError as exc:
                    print(exc)
                    continue
                Thread(target=self._process_data, args=(min_row, max_row)).start()

            # Сохранение данных
            elif event == self.save_data_btn.key:
                path = GUI.popup_get_file('Save data', save_as=True,
                                          file_types=(('OMX files', '*.omx-export'),))
                if path:
                    path = path if path.endswith('.omx-export') else path + '.omx-export'
                    if self.omx_file is not None:
                        save_data(path, self.omx_file)
                        print(f'Данные успешно сохранены по адресу {path}.')
                    self.omx_file = None
                    self.process_data_btn.update(disabled=True)
                    self.save_data_btn.update(disabled=True)

            # Остановка обработки данных
            elif event == self.stop_process_btn.key:
                self.process = False

            # Получение минимального и максимального номеров строк
            elif event == self.min_row_input.key:
                self.min_row = values[self.min_row_input.key]
            elif event == self.max_row_input.key:
                self.max_row = values[self.max_row_input.key]

            # Побочное
            elif event == 'Об авторе':
                GUI.popup('Автор', settings.ABOUT_POPUP_TEXT)
            elif event == GUI.WIN_CLOSED:
                break

        self.window.close()

    # Внутренний метод для обработки данных
    def _process_data(self, min_row: int, max_row: int):
        self.stop_process_btn.update(disabled=False)
        self.omx_file = '<omx xmlns="system" xmlns:ct="automation.control">\n'
        for row in range(int(min_row), int(max_row) + 1):
            if not self.process:
                break
            try:
                sensor_name = self.sheet[f'C{row}'].value
                try:
                    sensor_type = Sensor.recognize_signature(name=sensor_name)
                    print(f'В строке {row} опознан датчик типа "{sensor_type.__name__}"...', end=' ')
                except UnknownSensorTypeError:
                    print(f'Ошибка. Неизвестный тип датчика - "{sensor_name}" в строке {row}.')
                    continue
                
                self.omx_file += sensor_type.process(self.sheet, row)
                print(f'Строка {row} обработана.')
            except InvalidValueError as exc:
                print(f'В строке {row} обнаружена ошибка: {exc}')
            finally:
                try:
                    progress = int((row - min_row) / (max_row - min_row) * 100)
                except ZeroDivisionError:
                    progress = 100
                self.progress_bar.update_bar(progress)
        self.omx_file += '</omx>'
        print('Обработка завершена.')
        self.stop_process_btn.update(disabled=False)
        self.window[self.process_data_btn.key].update(disabled=True)
        self.window[self.stop_process_btn.key].update(disabled=True)
        self.window[self.save_data_btn.key].update(disabled=False)


if __name__ == '__main__':
    program = Configurator()
    program.run()
