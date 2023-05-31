from pathlib import Path
from typing import Any

import PySimpleGUI as GUI

from pydispatch import dispatcher

from . import settings
from . import signals
from .exceptions import InvalidValueError, ValidationError
from .sensors import Sensor


class GraphicalUserInterface:
    GUI.theme('LightGrey1')
    GUI.set_options(font='Franklin 10')

    def __init__(self):
        self.load_data_btn = GUI.Button('Загрузить', key='-LOAD_DATA-', size=settings.BUTTON_SIZE)
        self.file_path_title = GUI.Text('Файл')
        self.file_path_bar = GUI.Multiline(key='-FILE_NAME_OUTPUT-', disabled=True, size=(30, 3),
                                           reroute_stdout=True, autoscroll=True, no_scrollbar=True,
                                           expand_x=True)
        self.min_row_title = GUI.Text('Начальная строка')
        self.min_row_input = GUI.InputText(key='-MIN_ROW-', size=settings.BUTTON_SIZE,
                                           default_text=None, enable_events=True)
        self.max_row_title = GUI.Text('Конечная строка')
        self.max_row_input = GUI.InputText(key='-MAX_ROW-', size=settings.BUTTON_SIZE,
                                           default_text=None, enable_events=True)
        self.error_counter_title = GUI.Text('Число ошибок')
        self.error_counter_bar = GUI.Multiline(key='-ERROR_COUNTER-', size=(9, 1),
                                               disabled=True, reroute_stdout=True, autoscroll=False,
                                               no_scrollbar=True, expand_x=True, do_not_clear=False)
        self.event_box = GUI.Multiline(key='-OUTPUT-', disabled=True, size=settings.EVENT_BOX_SIZE,
                                       reroute_stdout=True, autoscroll=True, no_scrollbar=True,
                                       expand_x=True, expand_y=True)
        self.process_data_btn = GUI.Button(button_text='Обработать', key='-PROCESS_DATA-',
                                           size=settings.BUTTON_SIZE, disabled=True)
        self.stop_process_btn = GUI.Button(button_text='Стоп', key='-STOP_PROCESS-',
                                           size=settings.BUTTON_SIZE, disabled=True)
        self.hmi_process_btn = GUI.Button(button_text='HMI', key='-HMI_PROCESS-',
                                          size=settings.BUTTON_SIZE, disabled=True)
        self.save_data_btn = GUI.Button(button_text='Сохранить', key='-SAVE_DATA-',
                                        size=settings.BUTTON_SIZE, disabled=True)
        self.progress_bar = GUI.ProgressBar(max_value=100, key='-PROGRESS_BAR-',
                                            size=settings.PROGRESS_BAR_SIZE, expand_x=True)
        menu = GUI.Menu([
            ['Разное', ['Инструкция', '---', 'Об авторе']],
        ])
        layout = [
            [menu],
            [self.file_path_title, self.file_path_bar, self.load_data_btn],
            [GUI.HSep()],
            [self.min_row_title, self.min_row_input, self.max_row_title, self.max_row_input, self.error_counter_title,
             self.error_counter_bar, GUI.Push()],
            [self.event_box],
            [self.progress_bar],
            [self.process_data_btn, self.stop_process_btn, GUI.Push(), self.save_data_btn, self.hmi_process_btn],
        ]
        self.window = GUI.Window(title=settings.WINDOW_TITLE, layout=layout,
                                 size=settings.WINDOW_SIZE)

    def init_signals(self):
        dispatcher.connect(self.handle_data_loaded, signal=signals.DATA_LOADED)
        dispatcher.connect(self.handle_start_processing, signal=signals.START_PROCESSING)
        dispatcher.connect(self.handle_sensor_processing, signal=signals.SENSOR_DETECTED)
        dispatcher.connect(self.handle_skip_flag_processing, signal=signals.SKIP_FLAG_DETECTED)
        dispatcher.connect(self.handle_stop_processing, signal=signals.STOP_PROCESSING)
        dispatcher.connect(self.handle_data_saved, signal=signals.DATA_SAVED)

        # Обработка ошибок
        dispatcher.connect(self.handle_data_loading_failure, signal=signals.DATA_LOADING_FAILED)
        dispatcher.connect(self.handle_invalid_input_value, signal=signals.INVALID_INPUT_VALUE)
        dispatcher.connect(self.handle_validation_failure, signal=signals.VALIDATION_FAILED)

    def handle_data_loaded(self, sender: Any, file_path: Path) -> None:
        self.load_data_btn.update(disabled=False)
        self.process_data_btn.update(disabled=False)
        self.stop_process_btn.update(disabled=True)
        self.save_data_btn.update(disabled=True)
        self.file_path_bar.update(file_path)
        self.event_box.print(f'Данные из файла {file_path.name} успешно загружены.',
                             text_color='green')

    def handle_start_processing(self, sender: Any, min_row: int, max_row: int, **kwargs) -> None:
        self.load_data_btn.update(disabled=True)
        self.process_data_btn.update(disabled=True)
        self.stop_process_btn.update(disabled=False)
        self.save_data_btn.update(disabled=True)
        self.min_row_input.update(value=str(min_row), disabled=True)
        self.max_row_input.update(value=str(max_row), disabled=True)
        self.progress_bar.update(0, max=max_row - min_row)
        self.event_box.print(f'Начинаю обработку данных с {min_row} по {max_row} строку...',
                             text_color='blue')

    def handle_sensor_processing(self, sender: Sensor, error_counter: int, row: int, **kwargs) -> None:
        self.error_counter_bar.update(error_counter)
        self.progress_bar.update(row)
        self.event_box.print(f'В строке {row} опознан {sender}')

    def handle_skip_flag_processing(self, sender: Any, row: int, **kwargs) -> None:
        self.progress_bar.update(row)
        self.event_box.print(f'В строке {row} опознан флаг пропуска ...пропускаю.',
                             text_color='orange')

    def handle_stop_processing(self, sender: Any, reason: str, **kwargs) -> None:
        self.load_data_btn.update(disabled=False)
        self.process_data_btn.update(disabled=True)
        self.stop_process_btn.update(disabled=True)
        self.save_data_btn.update(disabled=False)
        self.min_row_input.update(disabled=False)
        self.max_row_input.update(disabled=False)
        self.event_box.print('Процесс обработки данных остановлен.\n'
                             f'Причина: {reason}.',
                             text_color='blue')

    def handle_data_saved(self, sender: Any, file_path: Path) -> None:
        self.event_box.print(f'Данные успешно сохранены в файл {file_path.name}.\n',
                             text_color='green')

    def handle_data_loading_failure(self, sender: Any, file_path: Path) -> None:
        self.event_box.print(f'Не удалось загрузить данные из файла {file_path.name}.',
                             text_color='red')

    def handle_invalid_input_value(self, sender: Exception, **kwargs) -> None:
        self.event_box.print('Ошибка в полях диапазона расчёта:', str(sender),
                             text_color='red')

    def handle_validation_failure(self, sender: Exception, error_counter: int, row: int, **kwargs) -> None:
        self.error_counter_bar.update(error_counter)
        self.progress_bar.update(row)
        self.event_box.print(f'Ошибка в строке {row}: {str(sender)}\n',
                             text_color='red')

    def handle_processing_error(self, sender: Any, exception: Exception) -> None:
        print('Ошибка при обработке данных:', str(exception))
