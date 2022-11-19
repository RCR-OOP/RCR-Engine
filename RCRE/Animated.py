import pygame
from io import BufferedReader
from PIL import Image
from typing import List
from rich.console import Console

c = Console()

# TODO: Till do
class AnimatedImage:
    @staticmethod
    def _load_frames_from_image(image: Image.Image) -> List[pygame.Surface]:
        fls = []
        for i in range(0, image.n_frames):
            try:
                image.seek(image.tell()+1)
                fls.append(pygame.image.load(image.tobytes()))
            except:
                c.print_exception()
                return fls

    def __init__(self, fp) -> None:
        if isinstance(fp, str):
            self.o_frames = self._load_frames_from_image(Image.open(fp))
        elif isinstance(fp, bytes):
            self.o_frames = self._load_frames_from_image(Image.frombytes(fp))
        elif isinstance(fp, BufferedReader):
            fp.seek(0) ; self.o_frames = self._load_frames_from_image(Image.frombytes(fp.read())) ; fp.seek(0)
        elif isinstance(fp, Image.Image):
            self.o_frames = self._load_frames_from_image(fp)
        elif isinstance(fp, list):
            if len(fp) > 0:
                if isinstance(fp[0], pygame.Surface):
                    self.o_frames == fp
                elif isinstance(fp[0], Image.Image):
                    self.o_frames = []
                    for img in fp:
                        self.o_frames += self._load_frames_from_image(img)
                else:
                    raise TypeError("Data types within a list are not supported")
            else:
                raise IndexError("List is empty")
        else:
            raise TypeError("This type of data is not supported")
