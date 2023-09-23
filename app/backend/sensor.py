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

    def to_omx(self):
        """Метод для сериализации датчика в формат OMX. Реализован в каждом датчике отдельно"""
        raise NotImplementedError("Метод to_omx должен быть реализован для дочерних классов")

    def to_hmi(self):
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

    def to_block(self, type: ProcessTypes, start_index: int) -> str:
        options = {
            ProcessTypes.OMX: self.to_omx,
            ProcessTypes.HMI: self.to_hmi,
        }
        return options[type](start_index)

    def to_omx(self, start_index: int) -> str:
        start_string = constants.GROUP_OMX_START_STRING.format(self._type.CLASS_NAME, self._pk)
        end_string = constants.GROUP_OMX_END_STRING
        return start_string + "".join([sensor.to_omx() for sensor in self._sensors]) + end_string

    def to_hmi(self, start_index: int) -> str:
        start_string = constants.GROUP_HMI_START_STRING
        end_string = constants.GROUP_HMI_END_STRING
        return start_string + "".join([sensor.to_hmi(start_index) for sensor in self._sensors]) + end_string

    @property
    def sensor_count(self) -> int:
        return len(self._sensors)


class SensorCluster:
    def __init__(self):
        self._sensors: dict[str, SensorGroup] = {}

    def add(self, sensor: Sensor):
        key: str = sensor.__class__.__name__
        self._sensors.setdefault(key, SensorGroup(sensor.__class__)).add(sensor)

    def join(self, type: ProcessTypes) -> str:
        sensor_index: int = 0
        options = {
            ProcessTypes.OMX: (
                constants.CLUSTER_OMX_START_STRING,
                constants.CLUSTER_OMX_END_STRING,
            ),
            ProcessTypes.HMI: (
                constants.CLUSTER_HMI_START_STRING,
                constants.CLUSTER_HMI_END_STRING,
            ),
        }
        result = options[type][0]
        for group_index, group in enumerate(self._sensors.values()):
            result += group.to_block(type, sensor_index)
            sensor_index += group.sensor_count

        return result + options[type][1]
