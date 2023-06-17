from pathlib import (
    Path, PosixPath,
    PurePath, PurePosixPath,
    PureWindowsPath, WindowsPath
)

# ! Type Test
def is_path(path) -> bool:
    return \
        isinstance(path, str) or \
        isinstance(path, Path) or \
        isinstance(path, PurePath) or \
        isinstance(path, PosixPath) or \
        isinstance(path, WindowsPath) or \
        isinstance(path, PurePosixPath) or \
        isinstance(path, PureWindowsPath)