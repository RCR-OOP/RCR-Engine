from io import BufferedReader
from typing import overload

class Sound:
    @overload
    def __init__(self, fp: str) -> None: ...
    @overload
    def __init__(self, fp: bytes) -> None: ...
    @overload
    def __init__(self, fp: BufferedReader) -> None: ...