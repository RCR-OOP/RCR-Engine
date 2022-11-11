import pygame
from typing import Tuple, Dict, Any

# ! Const
PATH = str

# ! Functions
def callback() -> str: return "None"

# ! Classes
class FontRender:
    def __init__(
        self,
        font: pygame.font.Font,
        color: pygame.Color,
        pos: Tuple[int, int],
        text_callback=callback
    ) -> None:
        self.font = font
        self.color = color
        self.pos = pos
        self.callback = text_callback
    
    def get_render_datas(self) -> Tuple[Tuple, Dict[str, Any]]:
        return (self.font.render(self.callback(), True, self.color), self.pos), {}