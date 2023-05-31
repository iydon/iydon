import pathlib as p
import typing as t


T1, T2, T3 = t.TypeVar('T1'), t.TypeVar('T2'), t.TypeVar('T3')

Any = t.Any
Command = t.Union[str, t.List[str]]
Path = t.Union[str, p.Path]
StrOrNone = t.Optional[str]

DictStr = t.Dict[str, T1]
