from PIL import Image
from pathlib import Path, PurePath, PosixPath, PurePosixPath, PureWindowsPath, WindowsPath
from typing import Union
# > Local Import's
from .render_objects import ImageRenderObject, RenderObjectBase

# ! Type Alias
PathType = Union[str, Path, PurePath, PosixPath, PurePosixPath, PureWindowsPath, WindowsPath]
LoadImageType = Union[PathType, Image.Image]
RenderObjectType = Union[RenderObjectBase, ImageRenderObject]
