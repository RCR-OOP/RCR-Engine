import os
from pygame.constants import *

__name__ = "RCREngine"
__version__ = "0.1.0-alpha"

PATH_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
PATH_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PATH_ENGINE_ICON = os.path.join(PATH_ASSETS_DIR, "icon.png")
PATH_ERROR_IMAGE = os.path.join(PATH_ASSETS_DIR, "error.png")
PATH_FLUID_SYNTH = os.path.join(PATH_DATA_DIR, "fluidsynth-win10x64", "fluidsynth.exe")
PATH_MIDI_SOUND_FONTS = os.path.join(PATH_DATA_DIR, "fluidsynth-win10x64", "default.sf2")

MOLITVA: str = \
"""
Отче наш, иже еси в моем PC.
Да святится имя и расширение Твое.
Да придет прерывание Твое и да будет воля твоя.
PYTHON наш насущный дай нам;
И прости нам дизассемблеры и антивирусы наши,
как Копиpайты прощаем мы.
И не введи нас в Exception Error,
но избавь нас от зависания,
ибо Твое есть адpессное пространство,
порты и регистры.
Во имя CTRLа, ALTa и Святого DELa,
всемогущего RESETa
во веки веков,
ENTER.
"""

M_LEFT_CLICK: int = 1
M_MIDDLE_CLICK: int = 2
M_RIGHT_CLICK: int = 3
M_SCROLL_UP: int = 4
M_SCROLL_DOWN: int = 5