__all__ = ['Result']


import typing as t

from ..base.type import Ta, Tb, Tc, Func1

if t.TYPE_CHECKING:
    import typing_extensions as te

    from .option import Option


class Result(t.Generic[Ta, Tb]):  # type: ignore [misc]
    '''
    Example:
        >>> try:
        ...     1 / 0
        ... except Exception as e:
        ...     x = Result.err(e)
        >>> y, z = x.get_ok(), x.get_err()
        >>> print(x, y, z, sep='\n')
        Result::Err(ZeroDivisionError('division by zero'))
        Option::None
        Option::Some(ZeroDivisionError('division by zero'))

    Reference:
        - https://doc.rust-lang.org/std/result/
        - https://doc.rust-lang.org/src/core/result.rs.html
    '''

    __slots__ = ('_ok', '_err')

    def __init__(self, ok: t.Optional[Ta] = None, err: t.Optional[Tb] = None) -> None:  # type: ignore [valid-type]
        assert ok is not None or err is not None

        self._ok = ok
        self._err = err

    def __eq__(self, other: 'te.Self[Ta]') -> bool:  # type: ignore [misc, override]
        if not isinstance(other, self.__class__):
            return False
        return self._match(lambda o: other._ok==o, lambda e: other._err==e)  # type: ignore [has-type]

    def __repr__(self) -> str:
        return self._match(lambda o: f'Result::Ok({o!r})', lambda e: f'Result::Err({e!r})')

    @classmethod
    def default(cls) -> 'te.Self[Ta, Tb]':  # type: ignore [misc]
        raise NotImplementedError

    @classmethod
    def new(cls, ok: t.Optional[Ta] = None, err: t.Optional[Tb] = None) -> 'te.Self[Ta, Tb]':  # type: ignore [misc, valid-type]
        assert (ok is None and err is not None) or (ok is not None and err is None)

        return cls(ok, err)

    @classmethod
    def ok(cls, ok: Ta) -> 'te.Self[Ta, Tb]':  # type: ignore [misc, valid-type]
        return cls(ok, None)

    @classmethod
    def err(cls, err: Tb) -> 'te.Self[Ta, Tb]':  # type: ignore [misc, valid-type]
        return cls(None, err)

    def is_ok(self) -> bool:
        return self._ok is not None  # type: ignore [has-type]

    def is_ok_and(self, f: Func1[Ta, bool]) -> bool:  # type: ignore [type-arg, valid-type]
        return self.is_ok() and f(self._ok)  # type: ignore [has-type]

    def is_err(self) -> bool:
        return not self.is_ok()

    def is_err_and(self, f: Func1[Tb, bool]) -> bool:  # type: ignore [type-arg, valid-type]
        return self.is_err() and f(self._err)  # type: ignore [has-type]

    def get_ok(self) -> 'Option[Ta]':  # type: ignore [type-arg, valid-type]
        # pub const fn ok(self) -> Option<T>
        from .option import Option

        return Option.new(self._ok)  # type: ignore [has-type]

    def get_err(self) -> 'Option[Tb]':  # type: ignore [type-arg, valid-type]
        # pub const fn err(self) -> Option<E>
        from .option import Option

        return Option.new(self._err)  # type: ignore [has-type]

    def map(self, op: Func1[Ta, Tc]) -> 'te.Self[Tc, Tb]':  # type: ignore [misc, type-arg, valid-type]
        return self._match(lambda o: self.ok(op(o)), lambda e: self)

    def map_or(self, default: Tc, f: Func1[Ta, Tc]) -> Tc:  # type: ignore [type-arg, valid-type]
        return self._match(lambda o: f(o), lambda e: default)

    def map_or_else(self, default: Func1[Tb, Tc], f: Func1[Ta, Tc]) -> Tc:  # type: ignore [type-arg, valid-type]
        return self._match(lambda o: f(o), lambda e: default(e))

    def map_err(self, op: Func1[Tb, Tc]) -> 'te.Self[Ta, Tc]':  # type: ignore [misc, type-arg, valid-type]
        return self._match(lambda o: self, lambda e: self.err(op(e)))

    def inspect(self, f: Func1[Ta, None]) -> 'te.Self[Ta, Tb]':  # type: ignore [misc, type-arg, valid-type]
        if self.is_ok():
            f(self._ok)  # type: ignore [has-type]
        return self

    def inspect_err(self, f: Func1[Tb, None]) -> 'te.Self[Ta, Tb]':  # type: ignore [misc, type-arg, valid-type]
        if self.is_err():
            f(self._err)  # type: ignore [has-type]
        return self

    def expect(self, msg: str) -> Ta:  # type: ignore [valid-type]
        assert self.is_ok(), msg

        return self._ok  # type: ignore [has-type]

    def unwrap(self) -> Ta:  # type: ignore [valid-type]
        return self.expect('called `Result::unwrap()` on an `Err` value')

    def expect_err(self, msg: str) -> Tb:  # type: ignore [valid-type]
        assert self.is_err(), msg

        return self._err  # type: ignore [has-type]

    def unwrap_err(self) -> Tb:  # type: ignore [valid-type]
        return self.expect_err('called `Result::unwrap_err()` on an `Ok` value')

    def and_(self, res: 'te.Self[Tc, Tb]') -> 'te.Self[Tc, Tb]':  # type: ignore [misc]
        return self._match(lambda o: res, lambda e: self)

    def and_then(self, op: Func1[Ta, 'te.Self[Tc, Tb]']) -> 'te.Self[Tc, Tb]':  # type: ignore [misc, type-arg, valid-type]
        return self._match(lambda o: op(o), lambda e: self)

    def or_(self, res: 'te.Self[Ta, Tc]') -> 'te.Self[Ta, Tc]':  # type: ignore [misc]
        return self._match(lambda o: self, lambda e: res)

    def or_else(self, op: Func1[Tb, 'te.Self[Ta, Tc]']) -> 'te.Self[Ta, Tc]':  # type: ignore [misc, type-arg, valid-type]
        return self._match(lambda o: self, lambda e: op(e))

    def unwrap_or(self, default: Ta) -> Ta:  # type: ignore [valid-type]
        return self._match(lambda o: o, lambda e: default)

    def unwrap_or_else(self, op: Func1[Tb, Ta]) -> Ta:  # type: ignore [type-arg, valid-type]
        return self._match(lambda o: o, lambda e: op(e))

    def contains(self, x: Ta) -> bool:  # type: ignore [valid-type]
        return self._match(lambda o: o==x, lambda e: False)  # type: ignore [operator]

    def contains_err(self, f: Tb) -> bool:  # type: ignore [valid-type]
        return self._match(lambda o: False, lambda e: e==f)  # type: ignore [operator]

    def _match(self, f4ok: Func1[Ta, Tc], f4err: Func1[Tb, Tc]) -> Tc:  # type: ignore [type-arg, valid-type]
        if self.is_ok():
            return f4ok(self._ok)  # type: ignore [has-type]
        else:
            return f4err(self._err)  # type: ignore [has-type]
