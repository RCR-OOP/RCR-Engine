import os
import time
import RCRE

# ! Initialized
e = RCRE.RCREngine(show_fps=True)
#e_debag = RCRE.Debag(e)

# ! Functions
def gv(per: float, max_value: float, min_value: float) -> float:
    return ((max_value-min_value)/100)*per

def gp(value: float, max_value: float, min_value: float) -> float:
    return (value/(max_value-min_value))*100

# ! Starting
e.start()
#e_debag.start()

# ! Loading
e.loader.load_sound(
    "alugalug-cat",
    os.path.join(RCRE.PATH_ASSETS_DIR, "alugalug-cat.mp3")
)

def lattr(obj: object):
    oa = {}
    for i in dir(obj):
        if not i.startswith("_"):
            oa[i] = eval(f"obj.{i}")
    return oa

# ! Render
e.loader.sounds["alugalug-cat"].play(1)
e.render.render_image(
    "img-test",
    "error",
    (0, 50),
    (50, 50)
)

# ! Set Targets
@e.events.mouse("fps-counter", RCRE.MOUSEBUTTONUP, RCRE.M_LEFT_CLICK)
def um(obj: RCRE.RENDER_OBJECT, pos: tuple):
    if obj.on_me(pos):
        if obj.pos == (0, 0):
            obj.update(pos=(10, 10))
        elif obj.pos == (10, 10):
            obj.update(pos=(0, 0))

@e.events.keyboard("img-test", RCRE.KEYUP, RCRE.K_s)
def um(obj: RCRE.RENDER_OBJECT):
    if obj.size == (50, 50):
        obj.update(size=(50, 100))
    elif obj.size == (50, 100):
        obj.update(size=(50, 50))

# ! Code
while e.loader.sounds["alugalug-cat"].playing:
    x = int(gv(gp(e.loader.sounds["alugalug-cat"].get_pos(), e.loader.sounds["alugalug-cat"].duration, 0.0), 750.0, 0.0))
    e.render.endless_render["img-test"].update(pos=(x, 50))
    time.sleep(1/e.max_fps)

# ! Blocking so that Python does not close
e.mainloop()
#e_debag.stop()