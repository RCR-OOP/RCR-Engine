from pathlib import Path
from typing import Union, Any
# > Local Import's
from .render_objects import ImageRenderObject

# ! Type Alias
PathType = Union[str, Path]
RenderObjectType = Union[ImageRenderObject, Any]
