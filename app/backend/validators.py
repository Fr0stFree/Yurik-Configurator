from typing import Optional

from .exceptions import ValidationError


def value_is_not_none_or_empty(value: Optional[str]) -> None:
    if value is None or value == "":
        raise ValidationError("Пустое значение.")


def value_is_digit_or_none(value: Optional[str]) -> None:
    if value is None or value == "":
        return
    if not isinstance(value, str) or not value.isdigit():
        raise ValidationError("Значение нельзя привести к числу.")


def validate_min_max_values(min_value: str, max_value: str) -> tuple[int, int]:
    try:
        min_value = int(min_value)
        max_value = int(max_value)
    except TypeError:
        raise ValidationError("Минимальное и максимальное значения строк должны быть числами")

    if max_value < min_value:
        raise ValidationError("Минимальное значение строки должно быть больше минимального.")

    return min_value, max_value
