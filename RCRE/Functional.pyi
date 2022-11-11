from rich.console import Console
from typing import TypeVar, Any

# ! Const Typing Vars
T = TypeVar('T')
NT = TypeVar('NT', int, float)

# ! Functions Typing
def neni(value: Any, default: T=None) -> T: ...
def ntd(value: NT, default: NT=0) -> NT: ...
def print_exception(console: Console) -> None: ...