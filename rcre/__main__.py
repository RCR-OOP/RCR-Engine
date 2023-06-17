import os
import time
from .engine import Engine
from rich.console import Console

console = Console()

def get_asset_path(filepath: str) -> str:
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "assets", filepath
    )

def main():
    # ! Initialization
    e = Engine()
    
    # ! Loading
    e.render.load_image("image.neko", get_asset_path("neko.jpg"))
    
    # ! Start
    e.start()

    # ! Code
    time.sleep(3)
    e.render["image.neko"].update(pos=(100, 0))
    
    # ! End
    e.join()

if __name__ == "__main__":
    try:
        main()
    except:
        console.print_exception(word_wrap=True, show_locals=True)