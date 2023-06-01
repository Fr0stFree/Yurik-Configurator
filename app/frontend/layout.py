import PySimpleGUI as GUI

from app.base import ProcessTypes
from . import settings, constants


class Layout:
    GUI.theme("LightGrey1")
    GUI.set_options(font="Franklin 10")

    def __init__(self) -> None:
        self.progress_bar_max_value: int = 100
        self.progress_bar_min_value: int = 0

        self.load_data_btn = GUI.Button("Загрузить", key="-LOAD_DATA-", size=settings.BUTTON_SIZE)
        self.file_path_title = GUI.Text("Файл")
        self.file_path_bar = GUI.Multiline(
            key="-FILE_NAME_OUTPUT-",
            disabled=True,
            size=(30, 3),
            autoscroll=True,
            no_scrollbar=True,
            expand_x=True,
        )
        self.min_row_title = GUI.Text("Начальная строка")
        self.min_row_input = GUI.InputText(
            key="-MIN_ROW-", size=settings.BUTTON_SIZE, default_text=None, enable_events=True
        )
        self.max_row_title = GUI.Text("Конечная строка")
        self.max_row_input = GUI.InputText(
            key="-MAX_ROW-", size=settings.BUTTON_SIZE, default_text=None, enable_events=True
        )
        self.error_counter_title = GUI.Text("Число ошибок")
        self.error_counter_bar = GUI.Multiline(
            key="-ERROR_COUNTER-",
            size=settings.BUTTON_SIZE,
            disabled=True,
            autoscroll=False,
            no_scrollbar=True,
            expand_x=True,
            do_not_clear=False,
        )
        self.event_box = GUI.Multiline(
            key="-OUTPUT-",
            disabled=True,
            size=settings.EVENT_BOX_SIZE,
            autoscroll=True,
            no_scrollbar=True,
            expand_x=True,
            expand_y=True,
        )
        self.process_type_dropdown = GUI.DropDown(
            key="-PROCESS_TYPE-",
            values=[type.value for type in ProcessTypes],
            default_value=ProcessTypes.default().value,
            enable_events=True,
            size=settings.BUTTON_SIZE,
            disabled=True,
            readonly=True,
        )
        self.start_process_btn = GUI.Button(
            button_text="Обработать", key="-PROCESS_DATA-", size=settings.BUTTON_SIZE, disabled=True
        )
        self.stop_process_btn = GUI.Button(
            button_text="Стоп", key="-STOP_PROCESS-", size=settings.BUTTON_SIZE, disabled=True
        )
        self.save_data_btn = GUI.Button(
            button_text="Сохранить", key="-SAVE_DATA-", size=settings.BUTTON_SIZE, disabled=True
        )
        self.progress_bar = GUI.ProgressBar(
            max_value=self.progress_bar_max_value,
            key="-PROGRESS_BAR-",
            size=settings.PROGRESS_BAR_SIZE,
            expand_x=True,
        )
        self.menu = GUI.Menu(
            [
                [
                    "Разное",
                    [constants.MENU_INSTRUCTION_TITLE, "---", constants.MENU_ABOUT_TITLE],
                ],
            ]
        )

        layout = [
            [self.menu],
            [self.file_path_title, self.file_path_bar, self.load_data_btn],
            [GUI.HSep()],
            [
                self.min_row_title,
                self.min_row_input,
                self.max_row_title,
                self.max_row_input,
                self.error_counter_title,
                self.error_counter_bar,
                GUI.Push(),
            ],
            [self.event_box],
            [self.progress_bar],
            [
                self.process_type_dropdown,
                self.start_process_btn,
                self.stop_process_btn,
                GUI.Push(),
                self.save_data_btn,
            ],
        ]
        self.window = GUI.Window(constants.WINDOW_TITLE, layout, size=settings.WINDOW_SIZE)
