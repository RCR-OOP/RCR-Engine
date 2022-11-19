from typing import TypeVar, Union

# ! Const Typing Vars
T = TypeVar('T')
NT = TypeVar('NT', int, float)
NTP = Union[None, Ellipsis, NotImplemented]

# ! Functions Typing
def neni(value: Union[T, NTP], default: T=None) -> T: ...
def ntd(value: NT, default: NT=0) -> NT: ...