from PIL import Image
from .functional import is_path
from .render_objects import ImageRenderObject
from .types import RenderObjectType, LoadImageType
# > Typing
from typing import Dict, Tuple, Any, Generator

# ! Main Class
class Render:
    def __init__(self) -> None:
        self.__objects: Dict[str, RenderObjectType] = {}
    
    # ? Main Functions
    def rendering(self) -> Generator[Tuple[int, Tuple[int, int], Tuple[Any, ...]], Any, None]:
        for obj in self.__objects.values():
            if obj.visible:
                yield obj.render_type, obj.pos, obj.render()
    
    # ? Dander-methods
    def __getitem__(self, key: str) -> RenderObjectType: return self.__objects[key]
    def __setitem__(self, key: str, value: RenderObjectType) -> None: self.__objects[key] = value
    def __delitem__(self, key: str) -> None: del self.__objects[key]

    # ? Dander-methods (wrapped)
    def set_obj(self, key: str, obj: RenderObjectType) -> None: self.__setitem__(key, obj)
    def get_obj(self, key: str) -> None: return self.__getitem__(key)
    def del_obj(self, key: str) -> None: self.__delitem__(key)
    
    # ? Loading Methods
    def load_image(self, key: str, data: LoadImageType, *args, **kwargs) -> None:
        if isinstance(data, Image.Image):
            return self.set_obj(key, ImageRenderObject(data, *args, **kwargs))
        elif is_path(data):
            return self.set_obj(key, ImageRenderObject.from_filepath(data, *args, **kwargs))
        raise TypeError("The image load data type is not supported.")
