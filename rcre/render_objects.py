from PIL import Image
from OpenGL.GL import GL_RGBA, GL_UNSIGNED_BYTE
# > Local Import's
from .units import IMAGE_RENDER_TYPE
# > Typing
from typing import Any, Tuple, Optional

# ! Render Objects Base
class RenderObjectBase:
    def __init__(self, render_type: int, pos: Tuple[int, int], visible: bool) -> None:
        self.__render_type = render_type
        self.__pos = pos
        self.__visible = visible
    
    # ? Property
    @property
    def render_type(self) -> int: return self.__render_type
    @property
    def visible(self) -> bool: return self.__visible
    @property
    def pos(self) -> Tuple[int, int]: return self.__pos
    
    # ? Vars Methods
    def update(
        self,
        visible: Optional[bool]=None,
        pos: Optional[Tuple[int, int]]=None
    ) -> None:
        if visible is not None:
            assert isinstance(visible, bool)
            self.__visible = visible
        if pos is not None:
            assert isinstance(pos, tuple)
            assert isinstance(pos[0], int)
            assert isinstance(pos[1], int)
            self.__pos = pos[:2]
    
    # ? Main Functions
    def render(self) -> Tuple[Any, ...]: return ()

# ! Objects
class ImageRenderObject(RenderObjectBase):
    def __init__(
        self,
        image: Image.Image,
        pos: Tuple[int, int]=(0, 0),
        visible: bool=True
    ) -> None:
        super().__init__(IMAGE_RENDER_TYPE, pos, visible)
        
        self.__image = image
        
        if self.__image.mode != "RGBA":
            self.__image = self.__image.convert("RGBA")
        
        self.__data: bytes = self.__image.tobytes("raw", "RGBA", 0, -1)
    
    # ? Initialization Methods
    @staticmethod
    def from_filepath(filepath: str, *args, **kwargs): return ImageRenderObject(Image.open(filepath), *args, **kwargs)
    
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
