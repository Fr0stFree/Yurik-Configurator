from typing import NamedTuple, Optional

from openpyxl.worksheet.worksheet import Worksheet

from core.utils import to_snake_case
from core.exceptions import ValidationError, UnknownSignalTypeError


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
        value = sheet[f'{self.column}{row}'].value
        try:
            self._validate(value)
        except ValidationError as exc:
            raise ValidationError(f'невалидное поле в столбце {self.column} {exc}')
        if value is None or value == '':
            return '-'
        return value


class SeverityField(Field):
    severities = {"Тушение": 1, "Пожар": 2, "Порог 2": 3, "Авария": 4, "Тревога": 5,
                  "Порог 1": 6, "Предупреждение": 8, "Недостоверность": 10,
                  "Неисправность": 12, "Отключение": 13, "Ремонт": 14, "Имитация": 16,
                  "Телесигнализация": 18, "Команда оператора": 20, "Информация": 22}
    
    def get_value(self, sheet: Worksheet, row: int) -> str:
        value = super().get_value(sheet, row)
        if value not in self.severities:
            raise UnknownSignalTypeError(f'неизвестный тип сигнала {value}.')
        return str(self.severities[value])