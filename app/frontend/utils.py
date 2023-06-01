from pathlib import Path


def convert_to_file_path(path: str, extension: str = None) -> Path:
    file_path = Path(path)
    if extension:
        if not file_path.suffix:
            file_path = file_path.with_suffix(extension)
        else:
            file_path = file_path.parent / f"{file_path.stem}{extension}"

    return file_path
