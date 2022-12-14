import psutil
from . import Engine
from rich.tree import Tree
from rich.live import Live
from threading import Thread

class Debag:
    def __init__(self, engine: Engine.RCREngine) -> None:
        self.engine = engine
        self.console = self.engine.console
        self.view_running = True
        self.view_thread = Thread(target=self._objs_view, daemon=True)
        self.progress = psutil.Process()
    
    def start(self) -> None:
        self.view_thread.start()
    
    def stop(self) -> None:
        self.view_running = False

    def _gt(self, e: Engine.RCREngine) -> str:
        t = Tree(f"[green]{Engine.Units.__name__}[/]")
        t.add(f"[#FF9000]FPS:[/] [#37B6CE]{round(e.clock.get_fps(),1)}[/]")
        t.add(f"[#FF9000]CPU Load:[/] [#37B6CE]{self.progress.cpu_percent()}[/] %")
        r_objs = t.add("[#FF9000]Render Object[/]")
        r_objs_endless = r_objs.add("[#A63100]render.is_rendered[/]")
        for i in list(e.render.is_rendered.keys()):
            r_objs_endless.add(f"[green]'{i}'[/]")
        r_objs_time = r_objs.add("[#A63100]render.is_not_rendered[/]")
        for i in list(e.render.is_not_rendered.keys()):
            r_objs_time.add(f"[green]'{i}'[/]")
        l_objs = t.add("[#FF9000]Loader Objects[/]")
        l_objs_images = l_objs.add("[#A63100]loader.images[/]")
        for i in list(e.loader.images.keys()):
            l_objs_images.add(f"[green]'{i}'[/]")
        l_objs_fonts = l_objs.add("[#A63100]loader.fonts[/]")
        for i in list(e.loader.fonts.keys()):
            l_objs_fonts.add(f"[green]'{i}'[/]")
        l_objs_sounds = l_objs.add("[#A63100]loader.sounds[/]")
        for i in list(e.loader.sounds.keys()):
            l_objs_sounds.add(f"[green]'{i}'[/]")
        l_objs.add(f"[#A63100]loader.colors[/] ([yellow]len[/]): [#37B6CE]{len(e.loader.colors)}[/]")
        return t

    def _objs_view(self):
        with Live("(...)", console=self.console) as tlive:
            while self.view_running:
                try:
                    tlive.update(self._gt(self.engine), refresh=True)
                except:
                    pass
        tlive.stop()