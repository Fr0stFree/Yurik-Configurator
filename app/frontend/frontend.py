import PySimpleGUI as GUI

from app.base import BackendProtocol
from .utils import convert_to_file_path
from .signals_handler import SignalsHandler
from . import settings, constants


class Frontend(SignalsHandler):
    def __init__(self, backend: BackendProtocol) -> None:
        super().__init__()
        self._backend = backend

    def run(self):
        while True:
            event, values = self.window.read()

            # Загрузка данных
            if event == self.load_data_btn.key:
                file_path = GUI.popup_get_file(
                    message="Загрузить данные",
                    file_types=settings.SUPPORTED_LOAD_FILE_TYPES,
                    no_window=True,
                )
                if file_path:
                    self._backend.load(convert_to_file_path(file_path))

            # Обработка данных
            elif event == self.start_process_btn.key:
                min_row = values[self.min_row_input.key]
                max_row = values[self.max_row_input.key]
                self._backend.start(min_row, max_row)

            # Изменение типа обработки данных (OMX, HMI)
            elif event == self.process_type_dropdown.key:
                self._backend.set_type(values[self.process_type_dropdown.key])

            # Сохранение данных
            elif event == self.save_data_btn.key:
                process_type = self._backend.get_type()
                file_path = GUI.popup_get_file(
                    message="Сохранить данные",
                    save_as=True,
                    file_types=settings.SUPPORTED_SAVE_FILE_TYPES[process_type],
                    no_window=True,
                )
                if file_path:
                    file_path = convert_to_file_path(file_path, extension=process_type.extension)
                    self._backend.save(file_path)

            # Остановка обработки данных
            elif event == self.stop_process_btn.key:
                self._backend.stop()

            # Побочное
            elif event == constants.MENU_ABOUT_TITLE:
                GUI.popup(event, constants.ABOUT_POPUP_TEXT)

            elif event == constants.MENU_INSTRUCTION_TITLE:
                GUI.popup(event, constants.INSTRUCTION_POPUP_TEXT)

            elif event == GUI.WIN_CLOSED:
                break

        self.window.close()
