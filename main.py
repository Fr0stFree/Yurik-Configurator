import sys
from typing import Optional
from threading import Thread
import os

import PySimpleGUI as GUI
from openpyxl.worksheet.worksheet import Worksheet

from core.gui import GraphicalUserInterface
from core.utils import save_data, load_sheet, get_calculation_limits, get_progress
from core.sensors import Sensor
from core.exceptions import ValidationError, InvalidValueError
from core import settings



class Configurator(GraphicalUserInterface):
    def __init__(self):
        super().__init__()
        self.min_row: Optional[int] = None
        self.max_row: Optional[int] = None
        self.sheet: Optional[Worksheet] = None
        self.omx_file_path = os.path.join(os.getcwd(), 'buffer.txt')
        self.is_processing: bool = True

    def run(self):
        while True:
            event, values = self.window.read()

            # Загрузка данных
            if event == self.load_data_btn.key:
                path = GUI.popup_get_file('Load data', file_types=(('Excel files', '*.xlsm'),))
                if path:
                    self.sheet = load_sheet(file_path=path)
                    if self.sheet:
                        self.window[self.process_data_btn.key].update(disabled=False)
                        self.is_processing = True
                        print(f'Данные из "{self.sheet.title}" успешно загружены.')
                    else:
                        print('Ошибка загрузки таблицы.')

            # Обработка данных
            elif event == self.process_data_btn.key:
                try:
                    min_row, max_row = get_calculation_limits(self.sheet, self.min_row, self.max_row)
                except InvalidValueError as exc:
                    print('Ошибка в полях диапазона расчёта:', exc)
                    continue
                Thread(target=self.process_data, args=(min_row, max_row)).start()

            # Сохранение данных
            elif event == self.save_data_btn.key:
                path = GUI.popup_get_file(message='Сохранить данные',
                                          save_as=True,
                                          file_types=(('OMX files', '*.omx-export'),))
                if path:
                    if not path.endswith('.omx-export'):
                        path += '.omx-export'
                    save_data(self.omx_file_path, path)
                    print(f'Файл "{path}" успешно сохранён.')

            # Остановка обработки данных
            elif event == self.stop_process_btn.key:
                self.is_processing = False

            # Получение минимального и максимального номеров строк
            elif event == self.min_row_input.key:
                self.min_row = values[self.min_row_input.key]

            elif event == self.max_row_input.key:
                self.max_row = values[self.max_row_input.key]

            # Побочное
            elif event == 'Об авторе':
                GUI.popup('Автор', settings.ABOUT_POPUP_TEXT)

            # Побочное
            elif event == 'Клик':
                GUI.popup('Инструкция', settings.INSTRUCTION_POPUP_TEXT)
            elif event == GUI.WIN_CLOSED:
                break

        self.window.close()

    # Внутренний метод для обработки данных
    def process_data(self, min_row: int, max_row: int):
        self.stop_process_btn.update(disabled=False)
        failures = 0
        sensors = {}
        with open(self.omx_file_path, 'w') as omx_file:
            omx_file.write(settings.OMX_FILE_START_STRING)
            for row in range(min_row, max_row+1):
                if not self.is_processing:
                    break
                skip_flag = self.sheet[f'{settings.SKIP_FLAG_COLUMN}{row}'].value
                if not self.is_processing or skip_flag not in (0, 1):
                    print('Ваша остановочка, господа.')
                    break
                if not skip_flag:
                    print(f'В строке {row} опознан флаг пропуска ...пропускаю.')
                    continue
                try:
                    sensor = Sensor.create(self.sheet, row)
                    print(f'В строке {row} опознан {sensor}', end=' ')
                except ValidationError as exc:
                    print(f'Ошибка в строке {row}: {exc}')
                    failures += 1
                    if failures >= settings.MAX_FAILURES_PER_RUN:
                        print('Хуета какая-то, проверь данные в таблице, они нихуя не валидны.')
                        break
                else:
                    failures = 0
                    sensors.setdefault(sensor.__class__.__name__, []).append(sensor)
                    print(f'...обработано')
                finally:
                    self.progress_bar.update_bar(get_progress(row, min_row, max_row))
            for sensor_type, sensor_list in sensors.items():
                sensor_class = sensor_list[0].__class__
                cluster = sensor_class.clusterize(sensor_list)
                omx_file.write(cluster)
                
            omx_file.write(settings.OMX_FILE_END_STRING)
            print('Обработка завершена.')
        
        self.window[self.process_data_btn.key].update(disabled=False)
        self.window[self.stop_process_btn.key].update(disabled=True)
        self.window[self.save_data_btn.key].update(disabled=False)


if __name__ == '__main__':
    program = Configurator()
    program.run()
