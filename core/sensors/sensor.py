import uuid
from typing import Type
from datetime import datetime

from openpyxl.worksheet.worksheet import Worksheet

from core import settings
from core.settings import ProcessTypes
from core.exceptions import UnknownSensorTypeError
from core.fields import Field

"""
| Яч.+переменная     | Атрибут                       | Пример           | Блоки               | Комментарий                |
| ------------------ |:----------------------------- |:---------------- | ------------------- | -------------------------- |
| [D**]NAME**        | Имя датчика                   | GPA_QT_100       | Все                 |                            |
| [N]SIREN_TYPE      | Тип оповещателя               | Свет             | SHOP                |                            |
| [Q]COLOR_ON        | Цвет при сработке             | Красный          | SHPS SHOP DI DO     |                            |
| [J]GP              | Мнемосхема                    | ГПА31            | Все                 |                            |
| [P]SOUND_ON        | Звук при сработке             | Пожар            | SHPS SHOP DI DO     | Под вопросом нужно или нет |
| [E]DESCRIPTION     | Описание                      | ГПА-31.Г-р QT202 | Все                 |                            |
| [-]SEVERITY        | Важность при сработке         | 2                | SHPS SHOP DI DO     | Формируется из SOUND_ON    |
| [Y]IVXX_TP         | Входн. знач./Адр. подкл.      | 2+7              | SHPS SHOP QSA DI AI |                            |
| [L]E_UNIT          | Единицы измерения             | %                | QSA AI              |                            |
| [N]SENSOR_POSITION | Позиция датчика               | QT100            | QSA AI              |                            |
| [O,N]SENSOR_TYPE   | Тип датчика                   | КТД-50           | SHPS QSA DI AI      | 2 SHPS AI проверить        |
| [N]SUBSTANCE       | Тип вещества                  | Метан            | QSA                 |                            |
| [AD]IFEX_TP        | Неисправность   пер.          | 3+1              | QSA                 | (3 модуль TREI, 1 канал)   |
| [Z]IT1X_TP         | 1 порог                       | 3+2              | QSA                 |                            |
| [AA]IT2X_TP        | 2 порог                       | 3+3              | QSA                 |                            |
| [O]MESSAGE_ON      | Сообщение при сработке        | .Пожар           | SHPS DI             |                            |
| [K]PAR_NAME        | Обозначение пар-ра в СИ       | T                | AI                  | Тип.изм.(P,L,dP,F)         |
| [N]SECOND_QUEUE    | Нал. второй оч. г. туш.       | 1                | UPG                 |                            |
| [-]FRAC_DIGITS     | кол-во цифр после зап. у ан-х | 2                | QSA AI              | По умолч. в функц - 2      |

<ct:object name="DO" access-level="public" uuid="54cd6969-f334-4893-b36b-dc9293cd4cba">
  <attribute type="unit.Server.Attributes.NodeRelativePath" />
  <attribute type="unit.Server.Attributes.IsObject" value="false" />

Эти строчки создают папку в DevStudio, для определенного типа устройств в данном случае DO.
Они необходимы только в первом блоке набора одного типа датчиков.
"""

class Sensor:
    CLASS_NAME: str
    BASE_TYPE: str

    def __init__(self, **kwargs) -> None:
        self.pk = uuid.uuid5(uuid.NAMESPACE_DNS, kwargs.get('name')+str(datetime.now()))
        self.row = kwargs.get('row')
        for field in self.__class__.__dict__.values():
            if isinstance(field, Field):
                setattr(self, field.key, kwargs.get(field.key, None))
                kwargs.get(field.key, None)

    def __str__(self):
        return f'<{getattr(self, self.Name.key)} {getattr(self, self.GP.key)}>'

    def __repr__(self):
        return f'<{getattr(self, self.Name.key)}>'

    @classmethod
    def create(cls, sheet: Worksheet, row: int) -> 'Sensor':
        """
        Метод для обработки строк из Excel-файла. Данный метод публичный и предназначен для
        вызова извне. Получает на вход строку из Excel-таблицы, парсит её, определяет тип датчика,
        сериализирует его в питоновский объект и возвращает.
        """
        sensor_name = sheet[f'{settings.SENSOR_TYPE_COLUMN}{row}'].value
        sensor_type = cls._recognize_signature(sensor_name)
        return sensor_type._parse_row(sheet, row)

    @classmethod
    def clusterize(cls, sensors: list['Sensor'], process_type: ProcessTypes) -> str:
        """
        Метод для группировки датчиков по типу. На вход получает список объектов датчиков,
        возвращает строку
        """
        group_pk = uuid.uuid5(uuid.NAMESPACE_DNS, cls.CLASS_NAME + str(datetime.now()))
        start_string = {
            ProcessTypes.OMX: (
                f'  <ct:object name="{cls.CLASS_NAME}" access-level="public" uuid="{group_pk}">\n'
                 '    <attribute type="unit.Server.Attributes.NodeRelativePath" />\n'
                 '    <attribute type="unit.Server.Attributes.IsObject" value="false" />\n'
            ),
            ProcessTypes.HMI: '',
        }
        end_string = {
            ProcessTypes.OMX: '  </ct:object>\n',
            ProcessTypes.HMI: '',
        }
        return (start_string[process_type]
                + ''.join([sensor.to_block(process_type) for sensor in sensors])
                + end_string[process_type])

    @classmethod
    def _parse_row(cls, sheet: Worksheet, row: int):
        """
        Функция получения значений ячеек из строки. Так же функция применяет валидаторы к
        значениям, и в случае их валидности, возвращает экземпляр класса датчика.
        """
        kwargs = {'row': row}
        for field in cls.__dict__.values():
            if isinstance(field, Field) and field.column:
                value = field.get_value(sheet, row)
                kwargs[field.key] = value
        return cls(**kwargs)

    @classmethod
    def _recognize_signature(cls, name: str) -> Type['Sensor']:
        """Метод сопоставления имени датчика из excel-файла с классом датчика"""
        for subclass in cls.__subclasses__():
            if subclass.__name__ == name:
                return subclass
        raise UnknownSensorTypeError(f"неизвестный тип датчика <{name}>. Проверьте правильность "
                                     f"написания имени датчика и проверьте, что он импортирован "
                                     f"в файле __init__.py")

    def to_block(self, process_type: ProcessTypes) -> str:
        result = {
            ProcessTypes.OMX: self.to_omx,
            ProcessTypes.HMI: self.to_hmi,
        }
        return result[process_type]()

    def to_omx(self):
        """Метод для сериализации датчика в формат OMX. Реализован в каждом датчике отдельно"""
        raise NotImplementedError('Метод to_omx должен быть реализован для дочерних классов')

    def to_hmi(self):
        """Метод для сериализации датчика в формат HMI. Реализован в каждом датчике отдельно"""
        raise NotImplementedError('Метод to_hmi должен быть реализован для дочерних классов')
