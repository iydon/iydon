__all__ = ['Option']


import copy
import typing as t
import warnings as w

from ..base.type import Ta, Tb, Tc, Func0, Func1, Func2

if t.TYPE_CHECKING:
    import typing_extensions as te

    from .result import Result


class Option(t.Generic[Ta]):  # type: ignore [misc]
    '''
    Example:
        >>> def divide(numerator: float, denominator: float) -> Option[float]:
        ...     if denominator == 0.0:
        ...         return Option.none()
        ...     else:
        ...         return Option.some(numerator / denominator)
        >>> nan = float('nan')
        >>> for args in [(2.0, 4.0), (1.0, 0.0), (21.0, 6.0)]:
        ...     ans = divide(*args)
        ...     print(ans, ans.unwrap_or(nan), ans.unwrap_or_else(float), sep=', ')
        Option::Some(0.5), 0.5, 0.5
        Option::None, nan, 0.0
        Option::Some(3.5), 3.5, 3.5

    Reference:
        - https://doc.rust-lang.org/std/option/
        - https://doc.rust-lang.org/src/core/option.rs.html
    '''

    __slots__ = ('_value', )
    _none: t.Optional['te.Self[Ta]'] = None  # type: ignore [misc]

    def __init__(self, value: t.Optional[Ta] = None) -> None:  # type: ignore [valid-type]
        self._value = value

    def __eq__(self, other: 'te.Self[Ta]') -> bool:  # type: ignore [misc, override]
        if not isinstance(other, self.__class__):
            return False
        return self._match(lambda v: other._value==v, other.is_none)  # type: ignore [operator]

    def __repr__(self) -> str:
        return self._match(lambda v: f'Option::Some({v!r})', lambda: 'Option::None')

    @classmethod
    def default(cls) -> 'te.Self[Ta]':  # type: ignore [misc]
        raise NotImplementedError

    @classmethod
    def new(cls, value: t.Optional[Ta] = None) -> 'te.Self[Ta]':  # type: ignore [misc, valid-type]
        if value is None:
            return cls.none()
        else:
            return cls.some(value)

    @classmethod
    def some(cls, value: Ta) -> 'te.Self[Ta]':  # type: ignore [misc, valid-type]
        return cls(value)

    @classmethod
    def none(cls) -> 'te.Self[Ta]':  # type: ignore [misc]
        if cls._none is None:
            cls._none = cls()
        return cls._none  # type: ignore [return-value]

    def is_some(self) -> bool:
        return not self.is_none()

    def is_some_and(self, f: Func1[Ta, bool]) -> bool:  # type: ignore [type-arg, valid-type]
        return self.is_some() and f(self._value)

    def is_none(self) -> bool:
        return self._value is None

    def expect(self, msg: str) -> Ta:  # type: ignore [valid-type]
        assert self.is_some(), msg

        return self._value

    def unwrap(self) -> Ta:  # type: ignore [valid-type]
        return self.expect('called `Option::unwrap()` on a `None` value')

    def unwrap_or(self, default: Ta) -> Ta:  # type: ignore [valid-type]
        return self._match(lambda v: v, lambda: default)

    def unwrap_or_else(self, f: Func0[Ta]) -> Ta:  # type: ignore [type-arg, valid-type]
        return self._match(lambda v: v, f)

    def map(self, f: Func1[Ta, Tb]) -> 'te.Self[Tb]':  # type: ignore [misc, type-arg, valid-type]
        # TODO: self.some or self.new?
        return self._match(lambda v: self.some(f(v)), lambda: self)

    def inspect(self, f: Func1[Ta, None]) -> 'te.Self[Ta]':  # type: ignore [misc, type-arg, valid-type]
        if self.is_some():
            f(self._value)
        return self

    def map_or(self, default: Tb, f: Func1[Ta, Tb]) -> Tb:  # type: ignore [type-arg, valid-type]
        return self._match(lambda v: f(v), lambda: default)

    def map_or_else(self, default: Func0[Tb], f: Func1[Ta, Tb]) -> Tb:  # type: ignore [type-arg, valid-type]
        return self._match(lambda v: f(v), default)

    def ok_or(self, err: Tb) -> 'Result[Ta, Tb]':  # type: ignore [type-arg, valid-type]
        from .result import Result

        return self._match(lambda v: Result.ok(v), lambda: Result.err(err))

    def ok_or_else(self, err: Func0[Tb]) -> 'Result[Ta, Tb]':  # type: ignore [type-arg, valid-type]
        from .result import Result

        return self._match(lambda v: Result.ok(v), lambda: Result.err(err()))

    def and_(self, optb: 'te.Self[Tb]') -> 'te.Self[Tb]':  # type: ignore [misc]
        return self._match(lambda v: optb, lambda: self)

    def and_then(self, f: Func1[Ta, 'te.Self[Tb]']) -> 'te.Self[Tb]':  # type: ignore [misc, type-arg, valid-type]
        return self._match(lambda v: f(v), lambda: self)

    def filter(self, predicate: Func1[Ta, bool]) -> 'te.Self[Ta]':  # type: ignore [misc, type-arg, valid-type]
        if self.is_some():
            if predicate(self._value):
                return self
        return self.none()

    def or_(self, optb: 'te.Self[Ta]') -> 'te.Self[Ta]':  # type: ignore [misc]
        return self._match(lambda v: self, lambda: optb)

    def or_else(self, f: Func0['te.Self[Ta]']) -> 'te.Self[Ta]':  # type: ignore [misc, type-arg]
        return self._match(lambda v: self, f)

    def xor(self, opt: 'te.Self[Ta]') -> 'te.Self[Ta]':  # type: ignore [misc]
        return self._match(
            lambda v1: opt._match(lambda v2: self.none(), lambda: self),
            lambda: opt._match(lambda v2: opt, self.none),
        )

    def insert(self, value: Ta) -> 'te.Self[Ta]':  # type: ignore [misc, valid-type]
        if self.is_none():
            w.warn('`Some` and `None` are not convertible')
            return self.some(value)
        else:
            self._value = value
            return self

    def get_or_insert(self, value: Ta) -> 'te.Self[Ta]':  # type: ignore [misc, valid-type]
        if self.is_none():
            w.warn('`Some` and `None` are not convertible')
            return self.some(value)
        else:
            return self

    def get_or_insert_with(self, f: Func0[Ta]) -> 'te.Self[Ta]':  # type: ignore [misc, type-arg, valid-type]
        if self.is_none():
            w.warn('`Some` and `None` are not convertible')
            return self.some(f())
        else:
            return self

    def take(self) -> 'te.Self[Ta]':  # type: ignore [misc]
        if self.is_none():
            return self
        else:
            raise Exception('`Some` and `None` are not convertible')

    def replace(self, value: Ta) -> 'te.Self[Ta]':  # type: ignore [misc, valid-type]
        if self.is_none():
            raise Exception('`Some` and `None` are not convertible')
        else:
            ans, self._value = self.some(self._value), value
            return ans

    def contains(self, x: Ta) -> bool:  # type: ignore [valid-type]
        return self._match(lambda v: x==v, lambda: False)  # type: ignore [operator]

    def zip(self, other: 'te.Self[Tb]') -> 'te.Self[t.Tuple[Ta, Tb]]':  # type: ignore [misc]
        if self.is_some() and other.is_some():
            return self.some((self._value, other._value))
        else:
            return self.none()

    def zip_with(self, other: 'te.Self[Tb]', f: Func2[Ta, Tb, Tc]) -> 'te.Self[Tc]':  # type: ignore [misc, type-arg, valid-type]
        if self.is_some() and other.is_some():
            return self.some(f(self._value, other._value))
        else:
            return self.none()

    def _match(self, f4some: Func1[Ta, Tb], f4none: Func0[Tb]) -> Tb:  # type: ignore [type-arg, valid-type]
        if self.is_none():
            return f4none()
        else:
            return f4some(self._value)

    def _copy(self) -> 'te.Self[Ta]':  # type: ignore [misc]
        return self._match(lambda v: self.some(copy.deepcopy(v)), self.none)
