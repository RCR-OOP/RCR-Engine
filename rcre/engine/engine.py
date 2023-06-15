import glfw
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from typing import Tuple

# ! Main Class
class Engine:
    def __init__(
            self,
            title: str=None,
            size: Tuple[int, int]=None,
            **kwargs
        ) -> None:
        # * Загрузка настроек
        self.title = title or "RCR Engine Window"
        self.size = size or (800, 600)

        # * Настройка OpenGL
        OpenGL.ERROR_CHECKING = kwargs.get("checking_error", True)
        OpenGL.ERROR_LOGGING = kwargs.get("logging_error", True)
        OpenGL.FULL_LOGGING = kwargs.get("logging_full", True)
        OpenGL.ERROR_ON_COPY = kwargs.get("copy_on_error", True)

        # * Создание окна
        self._loop()
    
    def _loop(self) -> None:
        # * Initialized glfw
        glfw.init()

        # * Создание окна
        self.root = glfw.create_window(*self.size, self.title, None, None)

        # * Настройка окна
        glfw.set_window_pos(self.root, 100, 100)
        glfw.make_context_current(self.root)

        while not glfw.window_should_close(self.root):
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT)
            glfw.swap_buffers(self.root)
        glfw.terminate()
