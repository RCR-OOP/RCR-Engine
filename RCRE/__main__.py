import time
import RCRE
from rich.live import Live
from threading import Thread

# ! Initialized
e, objs_view = RCRE.RCREngine(show_fps=True), True

def generate_text() -> str:
    tlines = [
        f"╔▼ [#FF9000]Render objects[/]",
        f"╠═══▶ [green]render.endless_render[/] ([yellow]len[/]): {len(e.render.endless_render)}",
        f"╠═══▶ [green]render.time_render[/] ([yellow]len[/]): {len(e.render.time_render)}",
        f"╠▼ [#FF9000]Loader Objects[/]",
        f"╠═══▼ [#A63100]Images[/]"
    ]
    for i in e.loader.images:
        tlines.append(
            f"╠══════▶ [#56026E]e.loader.images[/][ [green]'{i}'[/] ]"
        )
    tlines.append("╠═══▼ [#A63100]Fonts[/]")
    for i in e.loader.fonts:
        tlines.append(
            f"╠══════▶ [#56026E]e.loader.fonts[/][ [green]'{i}'[/] ]"
        )
    tlines[-1] = tlines[-1].replace("╠", "╚")
    return "\n".join(tlines)

def objects_view():
    with Live("- \n- \n") as tlive:
        while objs_view:
            try:
                tlive.update(
                    generate_text(),
                    refresh=True
                )
            except:
                pass
    tlive.stop()

# ! Ρεύμα
th = Thread(target=objects_view)

# ! Starting
e.start()
th.start()

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

time.sleep(3)
e.render.endless_render["img-test"].update(visible=False)

# ! Blocking so that Python does not close
e.mainloop()
objs_view = False