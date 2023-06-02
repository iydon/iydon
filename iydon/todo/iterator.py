__all__ = ['Iterator']


import copy
import functools as f
import operator as op
import typing as t

from ..base.type import Ta, Tb, Func1, Func2, Pair

if t.TYPE_CHECKING:
    import typing_extensions as te


class Iterator(t.Generic[Ta]):  # type: ignore [misc]
    '''Iterator (map, filter, reduce)
    '''

    __slots__ = ('_iterator', )

    def __init__(self, iterator: t.Iterator[Ta]) -> None:  # type: ignore [valid-type]
        self._iterator = iterator

    def __iter__(self) -> t.Iterator[Ta]:  # type: ignore [valid-type]
        return self._iterator

    @classmethod
    def new(cls, iterator: t.Iterator[Ta]) -> 'te.Self[Ta]':  # type: ignore [misc, valid-type]
        return cls(iterator)

    @classmethod
    def fromDict(cls, iterable: t.Dict[Ta, Tb]) -> 'te.Self[Pair[Ta, Tb]]':  # type: ignore [misc, valid-type]
        return cls.fromIterable(iterable.items())

    @classmethod
    def fromIterable(cls, iterable: t.Iterable[Ta]) -> 'te.Self[Ta]':  # type: ignore [misc, valid-type]
        return cls(iter(iterable))

    @classmethod
    def fromList(cls, iterable: t.List[Ta]) -> 'te.Self[Ta]':  # type: ignore [misc, valid-type]
        return cls.fromIterable(iterable)

    def collect(self, func: Func1[t.Iterator[Ta], Tb]) -> Tb:  # type: ignore [type-arg, valid-type]
        return func(self._iterator)

    def collect_as_dict(self: 'te.Self[Pair[Ta, Tb]]') -> t.Dict[Ta, Tb]:  # type: ignore [misc, valid-type]
        return self.collect(dict)

    def collect_as_list(self) -> t.List[Ta]:  # type: ignore [valid-type]
        return self.collect(list)

    def copy(self) -> 'te.Self[Ta]':  # type: ignore [misc]
        return self.__class__(copy.deepcopy(self._iterator))

    def filter(self, func: t.Optional[Func1[Ta, bool]] = None) -> 'te.Self[Ta]':  # type: ignore [misc, type-arg, valid-type]
        return self.__class__(filter(func, self._iterator))

    def map(self, func: Func1[Ta, Tb]) -> 'te.Self[Tb]':  # type: ignore [misc, type-arg, valid-type]
        return self.__class__(map(func, self._iterator))

    def reduce(self, func: Func2[Tb, Ta, Tb], initial: t.Optional[Tb] = None) -> Tb:  # type: ignore [type-arg, valid-type]
        if initial is None:
            return f.reduce(func, self._iterator)
        else:
            return f.reduce(func, self._iterator, initial)

    def reduce_with_operator(self, attr: str) -> Ta:  # type: ignore [valid-type]
        return self.reduce(getattr(op, attr))
