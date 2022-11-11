import time
from .Engine import RCREngine
from rich.console import Console

c = Console()
e = RCREngine(show_fps=True)
e.start()

e.render.render_image(
    "img:error:test",
    "error",
    (50, 50),
    (50, 50),
    -1
)
for i in range(1, 7):
    e.render.render_image(
        "img:error:test",
        "error",
        (50+(50*i), 50),
        (50, 50),
        1
    )
    time.sleep(3)

e.mainloop()