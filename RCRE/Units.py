import os
import pygame

COLOR_WHITE = pygame.Color(*(255, 255, 255))
COLOR_BLACK = pygame.Color(*(0, 0, 0))

PATH_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PATH_ENGINE_ICON_ICO = os.path.join(PATH_ASSETS_DIR, "icon.ico")
PATH_ENGINE_ICON_PNG = os.path.join(PATH_ASSETS_DIR, "icon.png")