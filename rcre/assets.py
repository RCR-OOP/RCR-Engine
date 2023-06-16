from PIL import Image
from pathlib import Path
from dataclasses import dataclass
# > Local Import's
from .tree import Tree
# > Typing Import's
from typing import Union, Any

# ! Assets Types
@dataclass
class ImageAsset:
    image: Image.Image

# ! Type Alias
AssetType = Union[ImageAsset, Any]

# ! Main Class
class Assets:
    def __init__(self, dirpath: Union[str, Path]) -> None:
        self.__dirpath = Path(dirpath)
        self.__assets: Tree[AssetType] = Tree()
        
        if self.__dirpath.is_dir():
            raise NotADirectoryError(f"The path must be the path to the directory: {self.__dirpath.name}")
    
    def __setitem__(self, key: str, value: AssetType) -> None: self.__assets.set(key, value)
    def __getitem__(self, key: str) -> None:
        if (item:=self.__assets.get(key, None)) is not None:
            return item
        raise KeyError(f"No value for key {repr(key)}")
    def __delitem__(self, key: str) -> None: self.__assets.delete(key)
    
    