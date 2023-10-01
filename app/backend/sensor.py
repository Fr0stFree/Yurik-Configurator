import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Type, Self

from openpyxl.worksheet.worksheet import Worksheet

from ..base import ProcessTypes
from .field import Field
from . import settings, constants


@dataclass
class Position:
    x: int
    y: int

    def shift(self, delta_x: int, delta_y: int, max_width: int) -> None:
        self.x += delta_x

        if self.x > max_width:
            self.x = 0
            self.y += delta_y


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

    def to_hmi(self, x: int, y: int) -> str:
        """Метод для сериализации датчика в формат HMI. Реализован в каждом датчике отдельно"""
        raise NotImplementedError("Метод to_hmi должен быть реализован для дочерних классов")


class SensorGroup:
    def __init__(self, sensor_class: Type[Sensor]) -> None:
        self._name = sensor_class.__name__
        self._pk = uuid.uuid5(uuid.NAMESPACE_DNS, self._name + str(datetime.now()))
        self._type = sensor_class
        self._sensors: list[Sensor] = []

    def add(self, sensor: Sensor) -> None:
        if not isinstance(sensor, self._type):
            raise TypeError(f"Cannot handle sensor {sensor.__class__}. Group only for {self._type} sensors")
        self._sensors.append(sensor)

    def to_block(self, type: ProcessTypes, group_positions: list[Position]) -> str:
        options = {
            ProcessTypes.OMX: self.to_omx,
            ProcessTypes.HMI: self.to_hmi,
        }
        return options[type](group_positions)

    def to_omx(self, group_positions: list[Position]) -> str:
        start_string = constants.GROUP_OMX_START_STRING.format(self._type.CLASS_NAME, self._pk)
        end_string = constants.GROUP_OMX_END_STRING
        return start_string + "".join([sensor.to_omx() for sensor in self._sensors]) + end_string

    def to_hmi(self, group_positions: list[Position]) -> str:
        result = constants.GROUP_HMI_START_STRING
        for sensor, position in zip(self._sensors, group_positions):
            result += sensor.to_hmi(position.x, position.y)
        return result + constants.GROUP_HMI_END_STRING

    @property
    def size(self) -> int:
        return len(self._sensors)


class SensorCluster:
    def __init__(self, sensor_interval_x, sensor_interval_y, sensor_panel_width) -> None:
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

        group_position = Position(x=0, y=0)
        result = start_string

        for group_index, group in enumerate(self._sensors.values()):
            group_positions = self.calculate_group_position(group_position, sensor_count=group.size)
            result += group.to_block(type, group_positions)
            group_position = Position(x=group_positions[-1].x, y=group_positions[-1].y)
            group_position.shift(self._delta_x, self._delta_y, self._width)

        return result + end_string

    def calculate_group_position(self, start_group_position: Position, sensor_count: int) -> list[Position]:
        positions: list[Position] = []
        sensor_position = start_group_position

        for _ in range(sensor_count):
            sensor_position = Position(x=sensor_position.x, y=sensor_position.y)
            positions.append(sensor_position)
            sensor_position.shift(self._delta_x, self._delta_y, self._width)

        return positions
