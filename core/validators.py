from typing import Optional

from .exceptions import InvalidValueError


def value_is_not_none_or_empty(value: Optional[str]) -> None:
    if value is None or value == '':
        raise InvalidValueError('пустое значение.')


def value_is_digit_or_none(value: Optional[str]) -> None:
    if value is None or value == '':
        return
    if not isinstance(value, str):
        raise ValueError
    if not value.isdigit():
        raise ValueError
