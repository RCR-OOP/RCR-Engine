import io
import sounddevice as sd
import soundfile as sf
from threading import Thread
from tempfile import mkstemp
from dataclasses import dataclass
from typing import Optional

# ! Other
@dataclass
class Device:
    name: str
    device_id: int
    samplerate: float

# ! Functions
def get_devices():
    return [Device(i["name"], idx, i["default_samplerate"]) for idx, i in enumerate(list(sd.query_devices(kind='output')))]

# ! Classes
class Sound:
    def __init__(self, fp, **kwargs) -> None:
        if isinstance(fp, io.BufferedReader):
            self._SOUND = sf.SoundFile(fp)
        elif isinstance(fp, bytes):
            path = mkstemp(suffix=".wav")[1]
            with open(path, "wb") as file:
                file.write(fp)
            self._SOUND = sf.SoundFile(path)
        elif isinstance(fp, str):
            self._SOUND = sf.SoundFile(fp)
        else:
            raise TypeError(f"Type of argument 'fp', cannot be '{type(fp)}'.")
        
        self._S: float = self._SOUND.samplerate
        self._BS: int = int(self._S * 0.0022675736961451248)
        self._DT: str = kwargs.get("dtype", "float32")
        self._DID: Optional[int] = kwargs.get("device_id", None)
        self._D: float = self._SOUND.frames / self._S
        self._POS: float = 0.0
        self._V: float = kwargs.get("volume", 1.0)
        self._P = False
    
    @property
    def playing(self) -> bool:
        return self._P
    
    @property
    def samplerate(self) -> float:
        return self._S

    @property
    def duration(self) -> float:
        return self._D

    @property
    def position(self) -> float:
        return self._POS
    
    @position.setter
    def position(self, value: float):
        if self._D >= value >= 0.0:
            self._POS = value
            self._SOUND.seek(int((self._POS)*self._S))

    @property
    def volume(self) -> float:
        return self._V
    
    @volume.setter
    def volume(self, value: float):
        if value >= 0.0:
            self._V = value
    
    def _play(self, mode: int) -> None:
        with sd.OutputStream(self._S, dtype=self._DT, device=self._DID) as output_stream:
            self._SOUND.seek(0);self._POS = 0.0
            while mode != 0:
                while self._P:
                    if len(data:=self._SOUND.read(self._BS, self._DT)) != 0:
                        output_stream.write(data*self._V)
                        self._POS+=self._BS/self._S
                    else:
                        break
                self._SOUND.seek(0);self._POS = 0.0
                mode -= 1
        self._SOUND.seek(0);self._POS = 0.0
        self._P = False

    def play(self, mode: int=1) -> None:
        if not self._P:
            self._P = True
            Thread(target=self._play, args=(mode,), daemon=True).start()
    
    def stop(self) -> None:
        if self._P:
            self._P = False
            sd.stop()