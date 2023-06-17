from PIL import Image
from OpenGL.GL import GL_RGBA, GL_UNSIGNED_BYTE
# > Typing
from typing import Any, Tuple

# ! Render Objects Base
class RenderObjectBase:
    _render_type: int = -1
    
    @property
    def render_type(self) -> int: return self._render_type
    def render(self) -> Tuple[Any, ...]: return ()

# ! Objects
class ImageRenderObject(RenderObjectBase):
    _render_type = 0
    
    def __init__(self, image: Image.Image) -> None:
        self.__image = image
        if self.__image.mode != "RGBA":
            self.__image = self.__image.convert("RGBA")
        
        self.__data: bytes = self.__image.tobytes("raw", "RGBA", 0, -1)
    
    # ? Private Functions
    def __update_arguments(self) -> None:
        self.__data = self.__image.tobytes("raw", "RGBA", 0, -1)
    
    # ? Image Actions
    def resize(self, size: Tuple[int, int]) -> None:
        self.__image = self.__image.resize(size)
        self.__update_arguments()
    
    # ? Main Functions
    def render(self):
        return (self.__image.size[0], self.__image.size[1], GL_RGBA, GL_UNSIGNED_BYTE, self.__data)
