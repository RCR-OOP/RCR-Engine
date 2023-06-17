from pathlib import Path, PosixPath, PurePath, WindowsPath, PurePosixPath, PureWindowsPath
from typing import Any

# ! Functions
def is_path(path) -> bool:
    return \
        isinstance(path, str) or \
        isinstance(path, PosixPath) or \
        isinstance(path, PurePath) or \
        isinstance(path, WindowsPath) or \
        isinstance(path, PurePosixPath) or \
        isinstance(path, PureWindowsPath)