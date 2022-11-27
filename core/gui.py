import PySimpleGUI as GUI

from . import settings


class GraphicalUserInterface:
    GUI.theme('LightGreen5')
    GUI.set_options(font='Franklin 10')

    def __init__(self):
        self.load_data_btn = GUI.Button('Загрузить', key='-LOAD_DATA-', size=settings.BUTTON_SIZE)
        self.min_row_title = GUI.Text('Начальная строка')
        self.min_row_input = GUI.InputText(key='-MIN_ROW-', size=settings.BUTTON_SIZE,
                                           default_text=None, enable_events=True)
        self.max_row_title = GUI.Text('Конечная строка')
        self.max_row_input = GUI.InputText(key='-MAX_ROW-', size=settings.BUTTON_SIZE,
                                           default_text=None, enable_events=True)
        self.event_box = GUI.Multiline(key='-OUTPUT-', disabled=True, size=settings.EVENT_BOX_SIZE,
                                       reroute_stdout=True, autoscroll=True, no_scrollbar=True,
                                       expand_x=True, expand_y=True)
        self.process_data_btn = GUI.Button(button_text='Обработать', key='-PROCESS_DATA-',
                                           size=settings.BUTTON_SIZE, disabled=True)
        self.stop_process_btn = GUI.Button(button_text='Стоп', key='-STOP_PROCESS-',
                                           size=settings.BUTTON_SIZE, disabled=True)
        self.save_data_btn = GUI.Button(button_text='Сохранить', key='-SAVE_DATA-',
                                        size=settings.BUTTON_SIZE, disabled=True)
        self.progress_bar = GUI.ProgressBar(max_value=100, key='-PROGRESS_BAR-',
                                            size=settings.PROGRESS_BAR_SIZE, expand_x=True)

        menu = GUI.Menu([
            ['Разное', 'Об авторе'],
        ])
        layout = [
            [menu],
            [self.load_data_btn, GUI.Push(), self.min_row_title, self.min_row_input, self.max_row_title, self.max_row_input],
            [self.event_box],
            [self.progress_bar],
            [self.process_data_btn, self.stop_process_btn, GUI.Push(), self.save_data_btn],
        ]
        self.window = GUI.Window(title=settings.WINDOW_TITLE, layout=layout,
                                 size=settings.WINDOW_SIZE)
