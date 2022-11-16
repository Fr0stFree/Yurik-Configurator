from typing import Optional

import PySimpleGUI as gui
from openpyxl.worksheet.worksheet import Worksheet

from . import settings
from .utils import save_omx_file, create_omx_file, load_sheet

class Configurator:
    gui.theme('LightGreen5')
    gui.set_options(font='Franklin 10')


    def __init__(self):
        load_data_btn = gui.Button('Загрузить', key='-LOAD_DATA-', size=settings.BUTTON_SIZE)
        save_data_btn = gui.Button('Сохранить', key='-SAVE_DATA-', size=settings.BUTTON_SIZE, disabled=True)
        event_box = gui.Multiline(key='-OUTPUT-', disabled=True, size=settings.EVENT_BOX_SIZE,
                                  reroute_stdout=True, autoscroll=True, no_scrollbar=True, expand_x=True)
        menu = gui.Menu([
            ['Configuration', ['Load::conf', 'Save::conf']],
            ['Help', ['About']]
        ])
        layout = [
            [menu],
            [load_data_btn],
            [gui.HorizontalSeparator()],
            [event_box],
            [save_data_btn],
        ]
        self.window = gui.Window(
            title=settings.WINDOW_TITLE,
            layout=layout,
            size=settings.WINDOW_SIZE,
        )
        self.sheet: Optional[Worksheet] = None
        self.omx_file: Optional[str] = None

    def run(self):
        while True:
            event, values = self.window.read()
            if event == gui.WIN_CLOSED:
                break
            elif event == 'About':
                gui.popup('About', settings.ABOUT_POPUP_TEXT)

            elif event == '-LOAD_DATA-':
                path = gui.popup_get_file('Load data', file_types=(('Excel files', '*.xlsx'),))
                if path:
                    self.sheet = load_sheet(file_path=path)
                    if self.sheet:
                        self.window['-SAVE_DATA-'].update(disabled=False)
                        print(f'Таблица "{self.sheet.title}" успешно загружена.')
                    else:
                        print('Ошибка загрузки таблицы.')

            elif event == '-SAVE_DATA-':
                path = gui.popup_get_file('Save data', save_as=True, file_types=(('OMX files', '*.omx-export'),))
                if path:
                    if not path.endswith('.omx-export'):
                        path += '.omx-export'
                    omx_file = create_omx_file(self.sheet)
                    save_omx_file(file_path=path, omx_file=omx_file)


            elif event in (gui.WIN_CLOSED, '-CLOSE-'):
                break
        self.window.close()
