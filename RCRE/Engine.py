import os
import pygame
from PIL import Image
from queue import Queue
from threading import Thread
from typing import Tuple, Optional, NoReturn, Dict, Any, Union, List
# ! PyGame Settings
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# ! Local Imports
try:
    from . import Units
    from . import Types
    from . import Functional
except:
    import Units
    import Types
    import Functional

class Loader:
    def __init__(self) -> None:
        self.fonts: Dict[str, pygame.font.Font] = {"fpstimer": pygame.font.Font(None, 20)}
        self.images: Dict[str, pygame.Surface] = {}
    
    def load_image_file(self, fp: Types.PATH, tag: str) -> None:
        self.images[tag] = pygame.image.load(fp)
    
    def load_font(self, fp, tag: str) -> None:
        pass

class Render:
    def __init__(
        self,
        root: pygame.Surface,
        clock: pygame.time.Clock,
        loader: Loader,
        max_fps: int=None
    ) -> None:
        self.root = root
        self.clock = clock
        self.loader = loader
        self.max_fps = max_fps
        self.queue = Queue()
        self.endless_render: Dict[str, Types.FontRender] = {}
    
    def _fpsc(self) -> str:
        return f"{round(self.clock.get_fps(), 1)} fps"
    
    def get_render_datas(self) -> List[Tuple[Tuple, Dict[str, Any]]]:
        return [i.get_render_datas() for i in self.endless_render.values()]
    
    def render_fps(
        self,
        pos: Optional[Tuple[int, int]]=None
    ) -> None:
        pos = pos or (0, 0)
        self.endless_render["fps-counter"] = Types.FontRender(
            self.loader.fonts["fpstimer"],
            Units.COLOR_BLACK,
            pos,
            self._fpsc
        )
    
    def render_image(self, tag: str, time: float) -> Image.Image:
        pass

class RCREngine:
    def __init__(
        self,
        title: Optional[str]=None,
        window_size: Optional[Tuple[int, int]]=None,
        max_fps: Optional[int]=None,
        show_fps: Optional[bool]=None,
        vsync: Optional[bool]=None
    ) -> None:
        # ! Initialized PyGame
        pygame.init()
        pygame.mixer.init()
        
        # ! Settings for Window
        self.title = title or "RCRE Window"
        self.window_size = window_size or (800, 600)
        self.max_fps = max_fps or 60
        self.show_fps = show_fps or False
        self.vsync = (vsync or False)

        # ! Applying settings
        self.root = pygame.display.set_mode(self.window_size, vsync=int(self.vsync))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.loader = Loader()
        self.render = Render(self.root, self.clock, self.loader, max_fps)

        if show_fps:
            self.render.render_fps()

        # ! Create Thread
        self.loop_thread = Thread(name="Loop", target=self._loop)
        self.loop_running = True

        # ! Start Loop
        self.loop_thread.run()

    def _loop(self) -> NoReturn:
        while self.loop_running:
            self.clock.tick(self.max_fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.loop_running = False
            self.root.fill(Units.COLOR_WHITE)
            for rargs, rkwargs in self.render.get_render_datas():
                self.root.blit(*rargs, **rkwargs)
            pygame.display.update()
