import pygame
from .Functional import neni
from typing import Tuple, Dict, Any, Union, Literal, Optional

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
    
    def on_me(self, pos: Tuple[int, int]) -> bool:
        size = self.font.render(self.text, True, self.color).get_size()
        rect = (*self.pos, self.pos[0]+size[0], self.pos[1]+size[1])
        if rect[0] <= pos[0] <= rect[2]:
            if rect[1] <= pos[1] <= rect[3]:
                return True
        return False

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
    
    def on_me(self, pos: Tuple[int, int]) -> bool:
        size = self.img.get_size()
        rect = (*self.pos, self.pos[0]+size[0], self.pos[1]+size[1])
        if rect[0] <= pos[0] <= rect[2]:
            if rect[1] <= pos[1] <= rect[3]:
                return True
        return False
    
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
            self.img = pygame.transform.scale(self.img, size)
        self.size = neni(size, self.size)

    def get_render_datas(self) -> Tuple[Tuple, Dict[str, Any]]:
        if self.frames > 0:
            self.frames -= 1
        if self.visible:
            return (self.img, self.pos), {}
        return (), {}

class FramesRender:
    def __init__(
        self,
        size: Tuple[int, int],
        pos: Tuple[int, int],
        frames: int=-1,
        visible: bool=True
    ) -> None:
        self.size = size
        self.pos = pos
        self.frames = frames
        self.visible = visible
    
    def update(self, pos: Tuple[int, int]=None, visible: bool=None) -> None:
        self.pos = neni(pos, self.pos)
        self.visible = neni(visible, self.visible)
    
    def get_render_datas(self) -> Tuple[Tuple, Dict[str, Any]]:
        return (), {}

# ! Types
PATH = str
RENDER_OBJECT = Union[FontRender, ImageRender]
RENDER_OBJECT_TAG = str
MOUSE_ACTION = int
MOUSE_BUTTON = int
KEYBOARD_BUTTON = int
KEYBOARD_ACTION = int
EVENTS_TARGET = Union[
    Tuple[Literal["mouse"], MOUSE_ACTION, Optional[MOUSE_BUTTON], RENDER_OBJECT_TAG, Any],
    Tuple[Literal["keyboard"], KEYBOARD_ACTION, Optional[KEYBOARD_BUTTON], RENDER_OBJECT_TAG, Any]
]
