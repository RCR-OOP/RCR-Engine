from io import BufferedReader
from pygame import Surface
from PIL import Image
from typing import List, overload

# TODO: Till do
class AnimatedImage:
    @overload
    def __init__(self, fp: str, fps: float) -> None: ...
    @overload
    def __init__(self, fp: bytes, fps: float) -> None: ...
    @overload
    def __init__(self, fp: BufferedReader, fps: float) -> None: ...
    @overload
    def __init__(self, fp: Image.Image, fps: float) -> None: ...
    @overload
    def __init__(self, fp: List[Surface], fps: float) -> None: ...
    @overload
    def __init__(self, fp: List[Image.Image], fps: float) -> None: ...