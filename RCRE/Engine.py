import time
import os
import pygame
from tempfile import mkstemp
from PIL import Image
from threading import Thread
from typing import Tuple, Optional, NoReturn, Dict, Any, List, Union
from rich.console import Console

# ! Import PyGame and Settings
import pygame
from pygame.colordict import THECOLORS
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
os.environ['RCR_ENGINE_MSG'] = 'True'

# ! Local Imports
try:
    from . import Units
    from . import EngineTypes as Types
    from . import Functional
    from . import Player
except:
    import Units
    import EngineTypes as Types
    import Functional
    import Player

# ! Initialized
console = Console()

class Loader:
    def __init__(self) -> None:
        self.fonts: Dict[str, pygame.font.Font] = {
            "std": pygame.font.Font(None, 18),
            "fpstimer": pygame.font.Font(None, 20)
        }
        self.images: Dict[str, pygame.Surface] = {
            "engine_icon": pygame.image.load(Units.PATH_ENGINE_ICON),
            "error": pygame.image.load(Units.PATH_ERROR_IMAGE)
        }
        self.colors: Dict[str, pygame.Color] = {}
        for i in THECOLORS:
            self.colors[i] = pygame.Color(*THECOLORS[i])
        self.sounds: Dict[str, Player.Sound] = {}
        self.tempfiles: List[str] = []
    
    def __del__(self) -> None:
        self.fonts.clear()
        self.images.clear()
        self.colors.clear()
        for i in self.tempfiles:
            try:
                os.remove(i)
            except:
                pass
    
    def add_color(self, tag: str, color: Any) -> None:
        self.colors[tag] = pygame.Color(color)

    def load_image_file(self, tag: str, fp: Types.PATH) -> None:
        self.images[tag] = pygame.image.load(fp)
    
    def load_image_pillow(self, tag: str, fp: Image.Image) -> None:
        path = mkstemp(suffix=".png")[1];fp.save(path)
        self.images[tag] = pygame.image.load(path)
        self.tempfiles.append(path)
    
    def load_font_file(self, tag: str, fp: Types.PATH, size: int=20) -> None:
        """
        Loads `Font` into Python by file path. You can also use file names from:

        - `Windows` `->` `C:\Windows\Fonts`
        """
        self.fonts[tag] = pygame.font.Font(fp, size)
    
    def load_sound(self, tag: str, fp: Player.SOUND_FP) -> None:
        self.sounds[tag] = Player.Sound(fp)

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
        try:
            for i in self.time_render.copy():
                if self.time_render[i].frames == 0:
                    self.time_render.pop(i, None)
        except:
            console.print_exception()
    
    def _arobj(self, obj_tag: str, obj: Types.RENDER_OBJECT, timer: str) -> None:
        if timer < 0:
            self.endless_render[obj_tag] = obj
        else:
            self.time_render[obj_tag] = obj
    
    def delete_obj(self, obj_tag: str) -> None:
        for i in self.endless_render.copy():
            if obj_tag == i:
                self.endless_render.pop(i, None)
                return None
        for i in self.time_render.copy():
            if obj_tag == i:
                self.time_render.pop(i, None)
                return None
    
    def get_render_datas(self) -> List[Tuple[Tuple, Dict[str, Any]]]:
        try:
            return \
                [er.get_render_datas() for er in self.endless_render.values()] +\
                [nr.get_render_datas() for nr in self.time_render.values()]
        except:
            console.print_exception()
    
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
        obj_tag: str,
        font_tag: str,
        pos: Tuple[int, int],
        color: pygame.Color,
        text: str="",
        timer: Union[float, int]=-1,
        visible: bool=True
    ) -> None:
        self._arobj(
            obj_tag,
            Types.FontRender(
                self.loader.fonts.get(font_tag, self.loader.fonts["std"]),
                pygame.Color(color),
                pos,
                text,
                Functional.ntd(int(timer*self.max_fps), -1),
                visible
            )
        )
    
    def render_image(
        self,
        obj_tag: str,
        img_tag: str,
        pos: Tuple[int, int],
        resize: Tuple[int, int]=None,
        rotate: float=None,
        timer: Union[float, int]=-1
    ) -> None:
        img = self.loader.images.get(img_tag, self.loader.images["error"])
        img: pygame.Surface = pygame.transform.scale(img, resize) if (resize is not None) else img
        if rotate is not None:
            img = pygame.transform.rotate(rotate)
        self._arobj(
            obj_tag,
            Types.ImageRender(
                img,
                img.get_size(),
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
        self.console = kwargs.get("console", console)

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
    
    def mainloop(self) -> None:
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
                # TODO: Обработчик Event
            self.root.fill(self.loader.colors["white"])
            if self.show_fps:
                self.render.endless_render["fps-counter"].update(f"{round(self.clock.get_fps(), 1)} fps")
            for rargs, rkwargs in self.render.get_render_datas():
                try:
                    if (len(rargs)+len(rkwargs)) > 0:
                        self.root.blit(*rargs, **rkwargs)
                except:
                    console.print_exception()
            self.render._objc()
            pygame.display.update()

if bool(os.environ['RCR_ENGINE_MSG']):
    console.print(f"[#42036F]*[/] [#00FF00]{Units.__name__}[/] (v[#33CCCC]{Units.__version__}[/]) [yellow]is loaded[/]!")