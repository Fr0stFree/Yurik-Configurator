from .exceptions import InvalidSkipFlag
from .settings import VALID_SKIP_FLAG_VALUES


def to_snake_case(string: str) -> str:
    """Функция преобразования строки в snake_case."""
    return "".join([s.lower() if s.islower() else f"_{s.lower()}" for s in string])


def is_skip(flag) -> bool:
    if flag not in VALID_SKIP_FLAG_VALUES:
        print(flag)
        raise InvalidSkipFlag()

    if flag:
        return False

    return True
