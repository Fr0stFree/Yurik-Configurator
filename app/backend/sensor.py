import uuid
from datetime import datetime
from typing import Type

from openpyxl.worksheet.worksheet import Worksheet

from ..base import ProcessTypes
from .field import Field
from . import settings, constants


class Sensor:
    CLASS_NAME: str
    BASE_TYPE: str

    def __init__(self, **kwargs) -> None:
        self.pk = uuid.uuid5(uuid.NAMESPACE_DNS, kwargs.get("name") + str(datetime.now()))
        self.row = kwargs.get("row")
        for field in self.__class__.__dict__.values():
            if isinstance(field, Field):
                setattr(self, field.key, kwargs.get(field.key, None))
                kwargs.get(field.key, None)

    def __str__(self):
        return f"<{getattr(self, self.Name.key)} {getattr(self, self.GP.key)}>"

    def __repr__(self):
        return f"<{getattr(self, self.Name.key)}>"

    @classmethod
    def create(cls, sheet: Worksheet, row: int) -> "Sensor":
        """
        Метод для обработки строк из Excel-файла. Данный метод публичный и предназначен для
        вызова извне. Получает на вход строку из Excel-таблицы, парсит её, определяет тип датчика,
        сериализирует его в питоновский объект и возвращает.
        """
        sensor_name = sheet[f"{settings.SENSOR_TYPE_COLUMN}{row}"].value
        sensor_type = cls._recognize_signature(sensor_name)
        return sensor_type._parse_row(sheet, row)

    @classmethod
    def _parse_row(cls, sheet: Worksheet, row: int):
        """
        Функция получения значений ячеек из строки. Так же функция применяет валидаторы к
        значениям, и в случае их валидности, возвращает экземпляр класса датчика.
        """
        kwargs = {"row": row}
        for field in cls.__dict__.values():
            if isinstance(field, Field) and field.column:
                value = field.get_value(sheet, row)
                kwargs[field.key] = value
        return cls(**kwargs)

    @classmethod
    def _recognize_signature(cls, name: str) -> Type["Sensor"]:
        """Метод сопоставления имени датчика из excel-файла с классом датчика"""
        for subclass in cls.__subclasses__():
            if subclass.__name__ == name:
                return subclass
        raise ValueError(
            f"неизвестный тип датчика <{name}>. Проверьте правильность "
            f"написания имени датчика и проверьте, что он импортирован "
            f"в файле app/backend/sensors/__init__.py"
        )

    def to_omx(self) -> str:
        """Метод для сериализации датчика в формат OMX. Реализован в каждом датчике отдельно"""
        raise NotImplementedError("Метод to_omx должен быть реализован для дочерних классов")

    def to_hmi(self, index: int) -> str:
        """Метод для сериализации датчика в формат HMI. Реализован в каждом датчике отдельно"""
        raise NotImplementedError("Метод to_hmi должен быть реализован для дочерних классов")


class SensorGroup:
    def __init__(self, sensor_class: Type[Sensor], start_index: int = 0):
        self._name = sensor_class.__name__
        self._pk = uuid.uuid5(uuid.NAMESPACE_DNS, self._name + str(datetime.now()))
        self._type = sensor_class
        self._sensors: list[Sensor] = []

    def add(self, sensor: Sensor) -> None:
        if not isinstance(sensor, self._type):
            raise TypeError(f"Cannot handle sensor {sensor.__class__}. Group only for {self._type} sensors")
        self._sensors.append(sensor)

    def to_block(self, type: ProcessTypes, group_position: int) -> str:
        options = {
            ProcessTypes.OMX: self.to_omx,
            ProcessTypes.HMI: self.to_hmi,
        }
        return options[type](group_position)

    def to_omx(self, group_position: int) -> str:
        start_string = constants.GROUP_OMX_START_STRING.format(self._type.CLASS_NAME, self._pk)
        end_string = constants.GROUP_OMX_END_STRING
        return start_string + "".join([sensor.to_omx() for sensor in self._sensors]) + end_string

    def to_hmi(self, group_position: int) -> str:
        result = constants.GROUP_HMI_START_STRING
        for index, sensor in enumerate(self._sensors):
            result += sensor.to_hmi(group_position + index)
        result += constants.GROUP_HMI_END_STRING
        return result

    @property
    def sensor_count(self) -> int:
        return len(self._sensors)


class SensorCluster:
    def __init__(self, sensor_interval_x: int = 25, sensor_interval_y: int = 50, sensor_panel_width: int = 500) -> None:
        self._sensors: dict[str, SensorGroup] = {}
        self._delta_x = sensor_interval_x
        self._delta_y = sensor_interval_y
        self._width = sensor_panel_width

    def add(self, sensor: Sensor):
        key: str = sensor.__class__.__name__
        self._sensors.setdefault(key, SensorGroup(sensor.__class__)).add(sensor)

    def join(self, type: ProcessTypes) -> str:
        start_string = constants.START_STRING[type]
        end_string = constants.END_STRING[type]

        result = start_string
        sensor_index: int = 0
        for group_index, group in enumerate(self._sensors.values()):
            result += group.to_block(type, ...)
            sensor_index += group.sensor_count

        return result + end_string
