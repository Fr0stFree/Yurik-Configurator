from typing import Final, Union

SKIP_FLAG_COLUMN: Final[str] = "B"
VALID_SKIP_FLAG_VALUES: tuple[Union[int, str, bool], ...] = (0, 1, "0", "1", True, False)
SENSOR_TYPE_COLUMN: Final[str] = "C"
MAX_FAILURES_PER_RUN: Final[int] = 1000
