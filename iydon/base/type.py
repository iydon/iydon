__all__ = [
    'Ta', 'Tb', 'Tc',
    'DictStr', 'Func0', 'Func1', 'Func2', 'Pair', 'Triple',
    'Any', 'DictStr2', 'Strings',
    'Path',
]


import pathlib as p
import typing as t


# type variables (private, public)
T1, T2, T3 = t.TypeVar('T1'), t.TypeVar('T2'), t.TypeVar('T3')
Ta, Tb, Tc = t.TypeVar('Ta'), t.TypeVar('Tb'), t.TypeVar('Tc')

# generics
DictStr = t.Dict[str, T1]  # type: ignore [valid-type]
Func0 = t.Callable[[], T1]  # type: ignore [valid-type]
Func1 = t.Callable[[T1], T2]  # type: ignore [valid-type]
Func2 = t.Callable[[T1, T2], T3]  # type: ignore [valid-type]
Pair = t.Tuple[T1, T2]  # type: ignore [valid-type]
Triple = t.Tuple[T1, T2, T3]  # type: ignore [valid-type]

# types with abstract names
Any = t.Any
DictStr2 = DictStr[str]  # type: ignore [type-arg]
Strings = t.List[str]

# types with specific names (if several files use this type, put it here)
Path = t.Union[str, p.Path]
