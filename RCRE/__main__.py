import time
from .Engine import RCREngine

# ! Initialized
e = RCREngine(show_fps=True)

# ! Starting
e.start()

# ! Render
e.render.render_image(
    "img-test",
    "error",
    (0, 50),
    (50, 50)
)
for i in range(0, 750):
    e.render.endless_render["img-test"].update(pos=(i, 50))
    time.sleep(0.02)
for i in list(range(0, 750))[::-1]:
    e.render.endless_render["img-test"].update(pos=(i, 50))
    time.sleep(0.02)

# ! Blocking so that Python does not close
e.mainloop()