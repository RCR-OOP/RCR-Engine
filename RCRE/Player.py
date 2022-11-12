import io
import sounddevice
import soundfile
from tempfile import mkstemp
from typing import *

class Sound:
    def __init__(self, fp) -> None:
        if isinstance(fp, io.BufferedReader):
            self.sound = soundfile.SoundFile(fp)
        elif isinstance(fp, bytes):
            path = mkstemp(suffix=".wav")[1]
            with open(path, "wb") as file:
                file.write(fp)
            self.sound = soundfile.SoundFile(path)
        elif isinstance(fp, str):
            self.sound = soundfile.SoundFile(fp)
        else:
            raise TypeError(f"type of argument fp, cannot be '{type(fp)}'.")
    
    def play(mode) -> None:
        pass