from .types import RenderObjectType
# > Typing
from typing import Dict, Tuple, Any

# ! Main Class
class Render:
    def __init__(self) -> None:
        self.__visible_objects: Dict[str, RenderObjectType] = {}
        self.__unvisible_objects: Dict[str, RenderObjectType] = {}
    
    def render(self) -> Tuple[int, Tuple[Any, ...]]:
        pass