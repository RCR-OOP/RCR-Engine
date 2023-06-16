import time
import glfw
import threading
from fpstimer import FPSTimer
# > OpenGL Import
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
# > Typing
from typing import Tuple, Optional

# ! Main Class
class Engine:
    def __init__(
        self,
        title: Optional[str]=None,
        size: Optional[Tuple[int, int]]=None,
        fps: Optional[int]=None,
        **kwargs
    ) -> None:
        # * Загрузка настроек
        self.__title = title or "RCR Engine Window"
        self.__size = size or (800, 600)
        self.__fps = fps or 60

        # * Другие переменые
        self.__fps_timer = FPSTimer(self.__fps)
        self.__root: Optional[glfw._GLFWwindow] = None
        
        # * Настройка OpenGL
        OpenGL.ERROR_CHECKING = kwargs.get("checking_error", True)
        OpenGL.ERROR_LOGGING = kwargs.get("logging_error", True)
        OpenGL.FULL_LOGGING = kwargs.get("logging_full", True)
        OpenGL.ERROR_ON_COPY = kwargs.get("copy_on_error", True)

        # * Регестрация потока
        self.__started = True
        self.__loop_stream = threading.Thread(target=self.__loop, name="MAIN_LOOP", daemon=True)
    
    # ? Property
    @property
    def started(self) -> bool: return self.__started
    @property
    def size(self) -> Tuple[int, int]: return self.__size
    @property
    def title(self) -> str: return self.__title
    @title.setter
    def set_title(self, value: str) -> None:
        self.__title = value
        if self.__root is not None:
            glfw.set_window_title(self.__root, self.__title)
    
    # ? Main Loop
    def __loop(self) -> None:
        # * Initialized glfw
        glfw.init()

        # * Создание окна
        self.__root = glfw.create_window(*self.__size, self.__title, None, None)

        # * Настройка окна
        glfw.set_window_pos(self.__root, 100, 100)
        glfw.make_context_current(self.__root)

        while (not glfw.window_should_close(self.__root)) and (self.__started):
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT)
            glfw.swap_buffers(self.__root)
            
            self.__fps_timer.sleep()
        
        # * Closing
        glfw.terminate()
        self.stop()
    
    # ? Functions
    def start(self) -> None:
        self.__started = True
        self.__loop_stream.start()
    
    def join(self) -> None:
        """Waiting for the end of the main cycle."""
        if self.started:
            while self.started: time.sleep(0.01)
    
    def stop(self) -> None:
        self.__started = False
        self.__root = None
