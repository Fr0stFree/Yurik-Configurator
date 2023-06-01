from typing import NamedTuple, Optional

from openpyxl.worksheet.worksheet import Worksheet

from .utils import to_snake_case
from .exceptions import ValidationError, InvalidFieldError


class Field(NamedTuple):
    name: str
    column: Optional[str]
    validators: Optional[list] = None

    @property
    def key(self) -> str:
        return to_snake_case(self.name)

    def _validate(self, value) -> None:
        if not self.validators:
            return
        for validator in self.validators:
            validator(value)

    def get_value(self, sheet: Worksheet, row: int) -> str:
        value = sheet[f"{self.column}{row}"].value
        try:
            self._validate(value)
        except ValidationError as exc:
            raise InvalidFieldError(message=str(exc), name=self.name, column=self.column)
        if value is None or value == "":
            return "-"
        return value


class SeverityField(Field):
    severities = {
        "Тушение": 1,
        "Пожар": 2,
        "Порог 2": 3,
        "Авария": 4,
        "Тревога": 5,
        "Порог 1": 6,
        "Предупреждение": 8,
        "Недостоверность": 10,
        "Неисправность": 12,
        "Отключение": 13,
        "Ремонт": 14,
        "Имитация": 16,
        "Телесигнализация": 18,
        "Команда оператора": 20,
        "Информация": 22,
    }


class MessageField(Field):
    severities = {"Пожар": "Пожар", "Тревога": "Сработка"}

    def get_value(self, sheet: Worksheet, row: int) -> str:
        value = super().get_value(sheet, row)
        if value not in self.severities:
            message = f"Неизвестный тип сигнала <{value}>."
            raise InvalidFieldError(message, name=self.name, column=self.column)
        return str(self.severities[value])
