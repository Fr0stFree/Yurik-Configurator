from typing import Final

from app.base import ProcessTypes


SUPPORTED_LOAD_FILE_TYPES: Final[tuple[tuple[str, str], ...]] = (
    ("Excel files", "*.xlsm"),
    ("Excel files", "*.xlsx"),
    ("Excel files", "*.xls"),
)
SUPPORTED_SAVE_FILE_TYPES: Final[dict[ProcessTypes, tuple[tuple[str, str], ...]]] = {
    ProcessTypes.OMX: (("OMX files", ProcessTypes.OMX.extension),),
    ProcessTypes.HMI: (("HMI files", ProcessTypes.HMI.extension),),
}
WINDOW_SIZE: Final[tuple[int, int]] = 700, 420
LABEL_SIZE: Final[tuple[int, int]] = 10, 1
INPUT_SIZE: Final[tuple[int, int]] = 10, 1
BUTTON_SIZE: Final[tuple[int, int]] = 10, 1
EVENT_BOX_SIZE: Final[tuple[int, int]] = 1, 10
PROGRESS_BAR_SIZE: Final[tuple[int, int]] = 10, 20
