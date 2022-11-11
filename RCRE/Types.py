import pygame
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
        text_callback=callback,
        frames: int=-1
    ) -> None:
        self.font = font
        self.color = color
        self.pos = pos
        self.callback = text_callback
        self.frames = frames
    
    def get_render_datas(self) -> Tuple[Tuple, Dict[str, Any]]:
        if self.frames > 0:
            self.frames -= 1
        return (self.font.render(self.callback(), True, self.color), self.pos), {}

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

    def get_render_datas(self) -> Tuple[Tuple, Dict[str, Any]]:
        if self.frames > 0:
            self.frames -= 1
        return (self.img, self.pos), {}

# ! Const
PATH = str
RENDER_OBJECT = Union[FontRender, ImageRender, Any]