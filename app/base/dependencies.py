from pathlib import Path
from typing import Protocol

from .constants import ProcessTypes


class BackendProtocol(Protocol):
    def load(self, file_path: Path) -> None:
        ...

    def start(self, min_row: str, max_row: str) -> None:
        ...

    def stop(self) -> None:
        ...

    def save(self, save_to: Path) -> None:
        ...

    def set_type(self, process_type: str) -> None:
        ...

    def get_type(self) -> ProcessTypes:
        ...
