import pygame
from .Functional import neni
from typing import Tuple, Dict, Any, Union

# ! Functions
def callback() -> str: return "None"

# ! Classes
class FontRender:
    def __init__(
        self,
        font: pygame.font.Font,
        color: pygame.Color,
        pos: Tuple[int, int],
        text: str="",
        frames: int=-1,
        visible: bool=True
    ) -> None:
        self.font = font
        self.color = color
        self.pos = pos
        self.text = text
        self.frames = frames
        self.visible = visible
    
    def update(
        self,
        text: str=None,
        color: pygame.Color=None,
        pos: Tuple[int, int]=None,
        visible: bool=None
    ) -> None:
        self.text = neni(text, self.text)
        self.color = neni(color, self.color)
        self.pos = neni(pos, self.pos)
        self.visible = neni(visible, self.visible)
    
    def get_render_datas(self) -> Tuple[Tuple, Dict[str, Any]]:
        if self.frames > 0:
            self.frames -= 1
        if self.visible:
            return (self.font.render(self.text, True, self.color), self.pos), {}
        return (), {}

class ImageRender():
    def __init__(
        self,
        img: pygame.Surface,
        size: Tuple[int, int],
        pos: Tuple[int, int],
        frames: int=-1,
        visible: bool=True
    ) -> None:
        self.img = img
        self.size = size
        self.pos = pos
        self.frames = frames
        self.visible = visible
    
    def update(
        self,
        img: pygame.Surface=None,
        size: Tuple[int, int]=None,
        pos: Tuple[int, int]=None,
        visible: bool=None
    ) -> None:
        self.img = neni(img, self.img)
        self.pos = neni(pos, self.pos)
        self.visible = neni(visible, self.visible)

        if neni(size, self.size) != self.size:
            pygame.transform.scale(self.img, size)
        self.size = neni(size, self.size)

    def get_render_datas(self) -> Tuple[Tuple, Dict[str, Any]]:
        if self.frames > 0:
            self.frames -= 1
        if self.visible:
            return (self.img, self.pos), {}
        return (), {}

# ! Const
PATH = str
RENDER_OBJECT = Union[FontRender, ImageRender]