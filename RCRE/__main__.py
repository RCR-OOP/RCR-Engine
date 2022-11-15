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
e.start("multi")
#e_debag.start()

# ! Loading
e.loader.load_sound(
    "alugalug-cat",
    os.path.join(RCRE.PATH_ASSETS_DIR, "alugalug-cat.mp3")
)

# ! Render
e.loader.sounds["alugalug-cat"].play()
e.render.render_image(
    "img-test",
    "error",
    (0, 50),
    (50, 50)
)
while e.loader.sounds["alugalug-cat"].playing:
    x = int(gv(gp(e.loader.sounds["alugalug-cat"].get_pos(), e.loader.sounds["alugalug-cat"].duration, 0.0), 750.0, 0.0))
    e.render.endless_render["img-test"].update(pos=(x, 50))
    time.sleep(1/e.max_fps)

# ! Blocking so that Python does not close
e.mainloop()
#e_debag.stop()