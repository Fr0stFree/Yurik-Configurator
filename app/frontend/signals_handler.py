from pydispatch import dispatcher

from app.base import senders
from .layout import Layout


class SignalsHandler(Layout):
    def __init__(self):
        super().__init__()
        dispatcher.connect(self.handle_process_started, senders.ProcessStarted.signal)
        dispatcher.connect(self.handle_process_stopped, senders.ProcessStopped.signal)

        dispatcher.connect(self.handle_data_loaded, senders.DataLoaded.signal)
        dispatcher.connect(self.handle_data_loading_failed, senders.DataLoadingFailed.signal)

        dispatcher.connect(self.handle_data_saved, senders.DataSaved.signal)
        dispatcher.connect(self.handle_data_saving_failed, senders.DataSavingFailed.signal)

        dispatcher.connect(self.handle_sensor_validated, senders.SensorValidated.signal)
        dispatcher.connect(self.handle_sensor_validation_failed, senders.SensorValidationFailed.signal)

        dispatcher.connect(self.handle_skip_flag_detected, senders.SkipFlagDetected.signal)
        dispatcher.connect(self.handle_user_input_validation_failed, senders.UserInputValidationFailed.signal)

    def handle_process_started(self, sender: senders.ProcessStarted) -> None:
        self.progress_bar_max_value = sender.max_row
        self.progress_bar_min_value = sender.min_row
        self.load_data_btn.update(disabled=True)
        self.start_process_btn.update(disabled=True)
        self.process_type_dropdown.update(disabled=True)
        self.stop_process_btn.update(disabled=False)
        self.save_data_btn.update(disabled=True)
        self.min_row_input.update(value=str(sender.min_row), disabled=True)
        self.max_row_input.update(value=str(sender.max_row), disabled=True)
        self.progress_bar.update(0, sender.max_row - sender.min_row)

        message = f"Начинаю обработку данных с {sender.min_row} по {sender.max_row} строку..."
        self.event_box.print(message, text_color="blue")

    def handle_process_stopped(self, sender: senders.ProcessStopped) -> None:
        self.load_data_btn.update(disabled=False)
        self.start_process_btn.update(disabled=True)
        self.stop_process_btn.update(disabled=True)
        self.save_data_btn.update(disabled=False)
        self.min_row_input.update(disabled=False)
        self.max_row_input.update(disabled=False)

        message = f"Процесс обработки данных остановлен.\nПричина: {sender.message}."
        self.event_box.print(message, text_color="green" if sender.on_success else "red")

    def handle_data_loaded(self, sender: senders.DataLoaded) -> None:
        self.load_data_btn.update(disabled=False)
        self.start_process_btn.update(disabled=False)
        self.process_type_dropdown.update(disabled=False)
        self.stop_process_btn.update(disabled=True)
        self.save_data_btn.update(disabled=True)
        self.file_path_bar.update(sender.path)
        self.progress_bar.update(0)

        message = f"Данные из файла {sender.path.name} успешно загружены."
        self.event_box.print(message, text_color="green")

    def handle_data_loading_failed(self, sender: senders.DataLoadingFailed) -> None:
        message = f"Не удалось загрузить данные из файла {sender.path.name}.\nОшибка: {sender.message}"
        self.event_box.print(message, text_color="red")

    def handle_data_saved(self, sender: senders.DataSaved) -> None:
        message = f"Данные успешно сохранены в файл {sender.path.name}."
        self.event_box.print(message, text_color="green")

    def handle_data_saving_failed(self, sender: senders.DataSavingFailed) -> None:
        message = f"Не удалось сохранить данные в файл {sender.path.name}\nОшибка: {sender.message}"
        self.event_box.print(message, text_color="red")

    def handle_sensor_validated(self, sender: senders.SensorValidated) -> None:
        self.progress_bar.update(sender.row - self.progress_bar_min_value)

        message = f"В строке {sender.row} опознан {sender.name}"
        self.event_box.print(message)

    def handle_sensor_validation_failed(self, sender: senders.SensorValidationFailed) -> None:
        self.error_counter_bar.update(sender.error_counter)
        self.progress_bar.update(sender.row - self.progress_bar_min_value)

        message = f"Ошибка в ячейке {sender.column}:{sender.row}\n" f"Ошибка: {sender.message}"
        self.event_box.print(message, text_color="red")

    def handle_skip_flag_detected(self, sender: senders.SkipFlagDetected) -> None:
        self.progress_bar.update(sender.row - self.progress_bar_min_value)

        message = f"В строке {sender.row} опознан флаг пропуска ...пропускаю."
        self.event_box.print(message, text_color="orange")

    def handle_user_input_validation_failed(self, sender: senders.UserInputValidationFailed) -> None:
        message = f"Ошибка в полях диапазона расчёта: {sender.message}"
        self.event_box.print(message, text_color="red")
