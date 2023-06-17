import os
import time
import glfw
import threading
from PIL import Image
from fpstimer import FPSTimer
# > OpenGL
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
# > Local Import's
from .render import Render
from .units import IMAGE_RENDER_TYPE
# > Typing
from typing import Tuple, Optional

# ! Initialization
OpenGL.ERROR_CHECKING = True
OpenGL.ERROR_LOGGING = True
OpenGL.FULL_LOGGING = True
OpenGL.ERROR_ON_COPY = True

# ! Main Class
class Engine:
    def __init__(
        self,
        title: Optional[str]=None,
        size: Optional[Tuple[int, int]]=None,
        fps: Optional[int]=None,
        **kwargs
    ) -> None:
        """"""
        # * Загрузка настроек
        self.__title = title or "RCR Engine Window"
        self.__size = size or (800, 600)
        self.__fps = fps or 60

        # * Другие переменые
        self.render = Render()
        self.__fps_timer = FPSTimer(self.__fps)
        self.__root: Optional[glfw._GLFWwindow] = None

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
    
    # ? Private Methods
    def __loop_end(self) -> None:
        self.__started = False
        self.__root = None
    
    # ? Main Loop
    def __loop(self) -> None:
        """"""
        # * Initialization GLFW
        glfw.init()
        
        # * Create Window
        self.__root = glfw.create_window(*self.__size, self.__title, None, None)

        # * Settings Window
        glfw.set_window_pos(self.__root, 100, 100)
        glfw.make_context_current(self.__root)

        #i = Image.open(get_asset_path("neko.jpg")).convert("RGBA").resize( (300, 300) )
        #bmp = i.tobytes("raw", "RGBA", 0, -1)
        
        # * OpenGL Render Settings
        glEnable(GL_ALPHA_TEST)
        glAlphaFunc(GL_GREATER, 0)
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        
        # * Main Loop
        while (not glfw.window_should_close(self.__root)) and (self.__started):
            glfw.poll_events()
            self.__size = glfw.get_window_size(self.__root)
            
            # ? Window Clear
            glClearColor(0.0, 0.0, 1.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # ? Processing
            glMatrixMode(GL_PROJECTION)
            matrix = glGetDouble(GL_PROJECTION_MATRIX)
            glLoadIdentity()
            glOrtho(0.0, self.__size[0] or 32, 0.0, self.__size[1] or 32, -1.0, 1.0)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()
            
            # ? Render
            for render_type, pos, args in self.render.rendering():
                if render_type == IMAGE_RENDER_TYPE:
                    glRasterPos2i(pos[0], pos[1])
                    glDrawPixels(*args)
            
            # ? Production
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glLoadMatrixd( matrix )
            glMatrixMode(GL_MODELVIEW)
            glfw.swap_buffers(self.__root)
            self.__fps_timer.sleep()
        
        # * Closing
        glfw.terminate()
        self.__loop_end()
    
    # ? Functions
    def start(self) -> None:
        """Starts the main cycle."""
        self.__started = True
        self.__loop_stream.start()
    
    def join(self) -> None:
        """Waiting for the end of the main cycle."""
        if self.started:
            while self.started: time.sleep(0.01)
    
    def stop(self) -> None:
        """Stopping the main cycle."""
        self.started = False
