import time
import os
import pygame
from pygame.colordict import THECOLORS
from threading import Thread
from typing import Tuple, Optional, NoReturn, Dict, Any, List, Union
try:
    from rich.console import Console
    console = Console()
except:
    console = None
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
        self.fonts: Dict[str, pygame.font.Font] = {
            "fpstimer": pygame.font.Font(None, 20)
        }
        self.images: Dict[str, pygame.Surface] = {
            "engine_icon": pygame.image.load(Units.PATH_ENGINE_ICON),
            "error": pygame.image.load(Units.PATH_ERROR_IMAGE)
        }
        self.colors: Dict[str, pygame.Color] = {}

        for i in THECOLORS:
            self.colors[i] = pygame.Color(*THECOLORS[i])

    def load_image_file(self, fp: Types.PATH, tag: str) -> None:
        self.images[tag] = pygame.image.load(fp)

class Render:
    def __init__(
        self,
        root: pygame.Surface,
        clock: pygame.time.Clock,
        loader: Loader,
        max_fps: int
    ) -> None:
        self.root = root
        self.clock = clock
        self.loader = loader
        self.max_fps = max_fps
        self.endless_render: Dict[str, Types.RENDER_OBJECT] = {}
        self.time_render: Dict[str, Types.RENDER_OBJECT] = {}
    
    def _fpsc(self) -> str:
        return f"{round(self.clock.get_fps(), 1)} fps"
    
    def _objc(self) -> None:
        for i in self.time_render.copy():
            if self.time_render[i].frames == 0:
                self.time_render.pop(i, None)
    
    def _arobj(self, obj_tag: str, obj: Types.RENDER_OBJECT, timer: str) -> None:
        if timer < 0:
            self.endless_render[obj_tag] = obj
        else:
            self.time_render[obj_tag] = obj
    
    def get_render_datas(self) -> List[Tuple[Tuple, Dict[str, Any]]]:
        return \
            [er.get_render_datas() for er in self.endless_render.values()] +\
            [nr.get_render_datas() for nr in self.time_render.values()]
    
    def render_fps(
        self,
        pos: Optional[Tuple[int, int]]=None
    ) -> None:
        self._arobj(
            "fps-counter",
            Types.FontRender(
                self.loader.fonts["fpstimer"],
                self.loader.colors["black"],
                pos or (0, 0),
                f"{round(self.clock.get_fps(), 1)} fps",
                -1
            ),
            -1
        )
    
    def render_font(
        self,
        font_tag: str,
        pos: Tuple[int, int],
        color: pygame.Color,
        text_callback=_fpsc,
        timer: Union[float, int]=-1
    ) -> None:
        pass
    
    def render_image(
        self,
        obj_tag: str,
        img_tag: str,
        pos: Tuple[int, int],
        resize: Tuple[int, int]=None,
        timer: Union[float, int]=-1
    ) -> None:
        img = pygame.transform.scale(self.loader.images.get(img_tag, self.loader.images["error"]), resize) \
            if (resize is not None) \
            else self.loader.images.get(img_tag, self.loader.images["error"])
        self._arobj(
            obj_tag,
            Types.ImageRender(
                img,
                pos,
                Functional.ntd(int(timer*self.max_fps), -1)
            ),
            timer
        )

class RCREngine:
    def __init__(
        self,
        title: Optional[str]=None,
        window_size: Optional[Tuple[int, int]]=None,
        max_fps: Optional[int]=None,
        show_fps: Optional[bool]=None,
        vsync: Optional[bool]=None,
        **kwargs
    ) -> None:
        # ! Settings for Window
        self.title = title or "RCRE Window"
        self.window_size = window_size or (800, 600)
        self.max_fps = max_fps or 60
        self.show_fps = show_fps or False
        self.vsync = (vsync or False)

        # ! Initialized
        self.root: pygame.Surface = None
        self.clock: pygame.time.Clock = None
        self.loader: Loader = None
        self.render: Render = None

        # ! Create Thread
        self.loop_thread = Thread(
            target=self._loop,
            daemon=True
        )
        self.loop_running = True
    
    def __del__(self) -> None:
        self.stop()
    
    def start(self) -> None:
        self.loop_running = True
        self.loop_thread.start()
        while self.render is None:
            time.sleep(0.1)
    
    def stop(self) -> None:
        if self.loop_running:
            self.render.endless_render.clear()
            self.render.time_render.clear()
            self.loop_running = False
            self.render = None
            self.loader = None
            self.clock = None
            self.root = None
    
    def mainloop(self) -> NoReturn:
        while self.loop_running:
            time.sleep(0.1)
        self.stop()
    
    def _loop(self) -> NoReturn:
        """Main Loop"""
        # ! Initialized PyGame
        pygame.init()
        pygame.mixer.init()

        # ! Applying settings
        self.root = pygame.display.set_mode(self.window_size, vsync=int(self.vsync))
        self.clock = pygame.time.Clock()
        self.loader = Loader()
        self.render = Render(self.root, self.clock, self.loader, self.max_fps)

        # ! Other Settings
        pygame.display.set_caption(self.title, self.title)
        pygame.display.set_icon(self.loader.images["engine_icon"])

        # ! Other Commands
        if self.show_fps:
            self.render.render_fps()
        
        # ! Loop
        while self.loop_running:
            self.clock.tick(self.max_fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                    return 0
            try:
                self.root.fill(self.loader.colors["white"])
            except:
                Functional.print_exception(console)
            try:
                if self.show_fps:
                    self.render.endless_render["fps-counter"].update(f"{round(self.clock.get_fps(), 1)} fps")
            except:
                Functional.print_exception(console)
            try:
                for rargs, rkwargs in self.render.get_render_datas():
                    try:
                        self.root.blit(*rargs, **rkwargs)
                    except:
                        Functional.print_exception(console)
            except:
                Functional.print_exception(console)
            try:
                self.render._objc()
            except:
                Functional.print_exception(console)
            pygame.display.update()
