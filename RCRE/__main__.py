import time
import RCRE

# ! Initialized
e = RCRE.RCREngine(show_fps=True)
#e_debag = RCRE.Debag(e)

# ! Starting
e.start()
#e_debag.start()

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

time.sleep(1)
e.render.endless_render["img-test"].update(visible=False)
time.sleep(2)
e.render.delete_obj("img-test")

# ! Blocking so that Python does not close
e.mainloop()
#e_debag.stop()