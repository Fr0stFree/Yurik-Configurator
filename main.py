from pathlib import Path
from typing import Optional, Any, Dict, List, TextIO
from threading import Thread


import PySimpleGUI as GUI
from pydispatch import dispatcher

from core.gui import GraphicalUserInterface
from core.utils import save_data, convert_to_file_path
from core.sensors import Sensor
from core.exceptions import InvalidValueError
from core.processor import Processor
from core import signals, settings


class Configurator(GraphicalUserInterface):
    def __init__(self):
        super().__init__()
        self.processor: Processor = Processor()
        self.buffer_path: Path = Path(__file__).parent / 'buffer.txt'
        self.buffer: Optional[TextIO] = None
        self.error_counter: int = 0
        self.sensors: Dict[str, List[Sensor]] = {}
        self.init_signals()

    def handle_start_processing(self, sender: Any, min_row: int, max_row: int, **kwargs) -> None:
        self.buffer = open(self.buffer_path, 'w', encoding='utf-8')
        self.buffer.write(self.processor.type.start_string)
        super().handle_start_processing(sender, min_row, max_row, **kwargs)
        Thread(target=self.processor.run, args=(min_row, max_row)).start()

    def handle_sensor_processing(self, sender: Sensor, **kwargs) -> None:
        self.error_counter = 0
        self.sensors.setdefault(sender.__class__.__name__, []).append(sender)
        super().handle_sensor_processing(sender, self.error_counter, **kwargs)

    def handle_stop_processing(self, sender: Any, **kwargs) -> None:
        self.processor.stop()
        super().handle_stop_processing(sender, **kwargs)

        for sensor_type, sensor_list in self.sensors.items():
            sensor_class = sensor_list[0].__class__
            cluster = sensor_class.clusterize(sensor_list, self.processor.type)
            self.buffer.write(cluster)

        self.buffer.write(self.processor.type.end_string)
        self.buffer.close()
        self.buffer = None
        self.sensors.clear()

    def handle_data_saved(self, sender: Any, file_path: Path) -> None:
        save_data(self.buffer_path, file_path)
        self.buffer_path.unlink()
        super().handle_data_saved(sender, file_path)

    def handle_validation_failure(self, sender: Exception, **kwargs) -> None:
        self.error_counter += 1
        super().handle_validation_failure(sender, self.error_counter, **kwargs)
        if self.error_counter >= settings.MAX_FAILURES_PER_RUN:
            dispatcher.send(signals.STOP_PROCESSING,
                            reason=f'Превышено максимальное количество ошибок ({settings.MAX_FAILURES_PER_RUN}).')

    def run(self):
        while True:
            event, values = self.window.read()

            # Загрузка данных
            if event == self.load_data_btn.key:
                file_path = GUI.popup_get_file(message='Загрузить данные',
                                               file_types=settings.SUPPORTED_LOAD_FILE_TYPES,
                                               no_window=True)
                if not file_path:
                    continue

                try:
                    file_path = convert_to_file_path(file_path)
                    self.processor.load_sheet(file_path)
                    dispatcher.send(signals.DATA_LOADED, file_path=file_path)

                except FileNotFoundError:
                    dispatcher.send(signals.DATA_LOADING_FAILED, file_path=file_path)

            # Обработка данных
            elif event == self.process_data_btn.key:
                try:
                    min_row, max_row = self.processor.get_calculation_limits(
                        min_row=values[self.min_row_input.key],
                        max_row=values[self.max_row_input.key],
                    )

                except InvalidValueError as exc:
                    dispatcher.send(signals.INVALID_INPUT_VALUE, exc)
                    continue

                dispatcher.send(signals.START_PROCESSING, min_row=min_row, max_row=max_row)

            # Изменение типа обработки данных (OMX, HMI)
            elif event == self.process_type_dropdown.key:
                self.processor.type = values[self.process_type_dropdown.key]

            # Сохранение данных
            elif event == self.save_data_btn.key:
                file_path = GUI.popup_get_file(message='Сохранить данные',
                                               save_as=True,
                                               file_types=settings.SUPPORTED_SAVE_FILE_TYPES[self.processor.type],
                                               no_window=True)
                if not file_path:
                    continue

                file_path = convert_to_file_path(file_path, extension=self.processor.type.extension)
                dispatcher.send(signals.DATA_SAVED, file_path=file_path)

            # Остановка обработки данных
            elif event == self.stop_process_btn.key:
                dispatcher.send(signals.STOP_PROCESSING, reason='Обработка прервана пользователем.')

            # Побочное
            elif event == 'Об авторе':
                GUI.popup(event, settings.ABOUT_POPUP_TEXT)

            elif event == 'Инструкция':
                GUI.popup(event, settings.INSTRUCTION_POPUP_TEXT)

            elif event == GUI.WIN_CLOSED:
                break

        self.window.close()


if __name__ == '__main__':
    program = Configurator()
    program.run()
