import os
import time
import RCRE

# ! Initialized
e = RCRE.RCREngine(show_fps=True)

# ! Functions
def gv(per: float, max_value: float, min_value: float) -> float:
    return ((max_value-min_value)/100)*per

def gp(value: float, max_value: float, min_value: float) -> float:
    return (value/(max_value-min_value))*100


# ! Starting
e.start()

# ! Loading
e.loader.load_sound("alugalug-cat", os.path.join(RCRE.PATH_ASSETS_DIR, "alugalug-cat.mp3"))

# ! Render
e.render.render_image(
    "img-test",
    "error",
    (0, 50),
    (50, 50)
)

# ! Set Targets
@e.linker.mouse("fps-counter", RCRE.MOUSEBUTTONUP, RCRE.M_LEFT_CLICK, auto_on_me=True)
def um(obj: RCRE.RENDER_OBJECT, pos: tuple):
    if obj.on_me(pos):
        if obj.pos == (0, 0):
            obj.update(pos=(10, 10))
        elif obj.pos == (10, 10):
            obj.update(pos=(0, 0))

@e.linker.keyboard("img-test", RCRE.KEYUP, RCRE.K_s)
def um(obj: RCRE.RENDER_OBJECT):
    if obj.size == (50, 50):
        obj.update(size=(50, 100))
    elif obj.size == (50, 100):
        obj.update(size=(50, 50))

# ! Code
e.loader.sounds["alugalug-cat"].play()

while e.loader.sounds["alugalug-cat"].playing:
    x = int(gv(gp(e.loader.sounds["alugalug-cat"].get_pos(), e.loader.sounds["alugalug-cat"].duration, 0.0), 750.0, 0.0))
    e.render.is_rendered["img-test"].update(pos=(x, 50))
    time.sleep(1/e.max_fps)

# ! Blocking so that Python does not close
e.mainloop()