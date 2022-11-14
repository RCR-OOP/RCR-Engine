from io import BufferedReader
from typing import overload, List
from dataclasses import dataclass

@dataclass
class Device:
    name: str
    device_id: int
    samplerate: float

def get_devices() -> List[Device]: ...

class Sound:
    @overload
    def __init__(self, fp: str, **kwargs) -> None: ...
    @overload
    def __init__(self, fp: bytes, **kwargs) -> None: ...
    @overload
    def __init__(self, fp: BufferedReader, **kwargs) -> None: ...

    @property
    def playing(self) -> bool: ...
    @property
    def samplerate(self) -> float: ...
    @property
    def duration(self) -> float: ...
    @property
    def position(self) -> float: ...
    @property
    def volume(self) -> float: ...
    @volume.setter
    def volume(self, value: float): ...

    def play(self, mode: int=1) -> None: ...
    def stop(self) -> None: ...