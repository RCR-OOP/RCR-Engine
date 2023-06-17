from PIL import Image
from pathlib import Path
# > Local Import's
from .tree import Tree
from .types import PathType
from .functional import is_path
# > Typing
from typing import Union, Any

# ! Type Alias
AssetType = Union[Image.Image, Any]

# ! Main Class
class Assets:
    def __init__(self, dirpath: Union[str, Path]) -> None:
        self.__dirpath = Path(dirpath)
        self.__assets: Tree[AssetType] = Tree()
        
        if self.__dirpath.is_dir():
            raise NotADirectoryError(f"The path must be the path to the directory: {self.__dirpath.name}")
    
    # ? Dander-methods
    def __setitem__(self, key: str, data: AssetType) -> None: self.__assets.set(key, data)
    def __getitem__(self, key: str) -> AssetType:
        if (item:=self.__assets.get(key, None)) is not None:
            return item
        raise KeyError(f"No value for key {repr(key)}")
    def __delitem__(self, key: str) -> None: self.__assets.delete(key)
    
    # ? Methods
    def load_image(self, key: str, data: Union[PathType, Image.Image]) -> Image.Image:
        if is_path(data):
            self.__setitem__(key, Image.open(data).convert("RGBA"))
        elif isinstance(data, Image.Image):
            self.__setitem__(key, data.convert("RGBA"))
        raise TypeError("This type for loading an asset is not supported.")
