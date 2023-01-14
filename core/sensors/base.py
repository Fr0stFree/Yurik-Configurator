import uuid
from typing import NamedTuple, Optional

from openpyxl.worksheet.worksheet import Worksheet

from core.exceptions import UnknownSensorTypeError


class Field(NamedTuple):
    name: str
    column: Optional[str]
    key: str
    validators: Optional[list] = None
    
    def validate(self, value):
        if self.validators:
            for validator in self.validators:
                validator(value)


class Sensor:
    SEVERITY_SIGNALS = {"Тушение": 1, "Пожар": 2, "Порог 2": 3, "Авария": 4, "Тревога": 5,
                        "Порог 1": 6, "Предупреждение": 8, "Недостоверность": 10,
                        "Неисправность": 12, "Отключение": 13, "Ремонт": 14, "Имитация": 16,
                        "Телесигнализация": 18, "Команда оператора": 20, "Информация": 22}

    def __init__(self, **kwargs) -> None:
        for field in self.__class__.__dict__.values():
            if isinstance(field, Field):
                setattr(self, field.key, kwargs.get(field.key, None))
        try:
            self.pk = uuid.uuid5(uuid.NAMESPACE_DNS, kwargs.get(getattr(self, 'NAME').key))
        except TypeError:
            print(f'Не указано имя датчика. Primary key (id) выбран согласно протоколу uuid4')
            self.pk = uuid.uuid4()

    @classmethod
    def process(cls, sheet: Worksheet, row: int) -> str:
        """
        Метод для обработки строк из Excel-файла. Данный метод публичный и предназначен для
        вызова извне. Возвращает строку в формате OMX. Метод должен вызываться из дочерних классов.
        """
        sensor = cls._parse_row(sheet, row)
        return sensor._to_omx()

    @classmethod
    def _parse_row(cls, sheet: Worksheet, row: int):
        """
        Функция получения значений ячеек из строки. Так же функция применяет валидаторы к
        значениям и в случае валидности всех значений возвращает экземпляр класса датчика.
        """
        kwargs = {}
        for field in cls.__dict__.values():
            if isinstance(field, Field) and field.column:
                value = sheet[f'{field.column}{row}'].value
                field.validate(value)
                kwargs[field.key] = value
        return cls(**kwargs)

    @staticmethod
    def recognize_signature(name: str) -> object:
        """Метод сопоставления имени датчика из excel-файла с классом датчика"""
        for subclass in Sensor.__subclasses__():
            if subclass.__name__ == name:
                return subclass
        raise UnknownSensorTypeError(f"Неизвестный тип датчика: {name}")
    
    def _to_omx(self):
        raise NotImplementedError('Метод _to_omx должен быть реализован для дочерних классов')