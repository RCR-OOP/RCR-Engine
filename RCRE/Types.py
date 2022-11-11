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
        frames: int=-1
    ) -> None:
        self.font = font
        self.color = color
        self.pos = pos
        self.text = text
        self.frames = frames
    
    def update(self, text: str=None, color: pygame.Color=None, pos: Tuple[int, int]=None) -> None:
        self.text = neni(text, self.text)
        self.color = neni(color, self.color)
        self.pos = neni(pos, self.pos)
    
    def get_render_datas(self) -> Tuple[Tuple, Dict[str, Any]]:
        if self.frames > 0:
            self.frames -= 1
        return (self.font.render(self.text, True, self.color), self.pos), {}

class ImageRender():
    def __init__(
        self,
        img: pygame.Surface,
        pos: Tuple[int, int],
        frames: int=-1
    ) -> None:
        self.img = img
        self.pos = pos
        self.frames = frames
    
    def update(self, pos: Tuple[int, int]) -> None:
        self.pos = neni(pos, self.pos)

    def get_render_datas(self) -> Tuple[Tuple, Dict[str, Any]]:
        if self.frames > 0:
            self.frames -= 1
        return (self.img, self.pos), {}

# ! Const
PATH = str
RENDER_OBJECT = Union[FontRender, ImageRender, Any]