__all__ = ['Err', 'Ok', 'Result']


import typing as t

from ....base.type import Ta, Tb, Tc, Func1

if t.TYPE_CHECKING:
    import typing_extensions as te

    from .option import Option


class Result(t.Generic[Ta, Tb]):  # type: ignore [misc]
    '''Error handling with the `Result` type.

    References:
        - https://doc.rust-lang.org/std/result/
        - https://doc.rust-lang.org/src/core/result.rs.html
        - https://github.com/iydon/iydon/blob/main/static/rust/result.rs
    '''

    __slots__ = ('_ok', '_err')

    def __init__(self, ok: t.Optional[Ta] = None, err: t.Optional[Tb] = None) -> None:  # type: ignore [valid-type]
        self._ok = ok
        self._err = err

    def __eq__(self, other: 'te.Self[Ta]') -> bool:  # type: ignore [misc, override]
        if not isinstance(other, self.__class__):
            return False
        return self._match(lambda o: other._ok==o, lambda e: other._err==e)  # type: ignore [operator]

    def __repr__(self) -> str:
        return self._match(lambda o: f'Result.ok({o!r})', lambda e: f'Result.err({e!r})')

    def __str__(self) -> str:
        return self._match(lambda o: f'Result::Ok({o!r})', lambda e: f'Result::Err({e!r})')

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
        '''Returns `true` if the result is `Ok`.

        Returns:
            ans: ...

        Examples:
            >>> x = Result.ok(-3)
            >>> assert x.is_ok()

            >>> x = Result.err('Some error message')
            >>> assert not x.is_ok()
        '''
        return self._ok is not None

    def is_ok_and(self, f: Func1[Ta, bool]) -> bool:  # type: ignore [type-arg, valid-type]
        '''Returns `true` if the result is `Ok` and the value inside of it matches a predicate.

        Args:
            f: ...

        Returns:
            ans: ...

        Examples:
            >>> x = Result.ok(2)
            >>> assert x.is_ok_and(lambda x: x>1)

            >>> x = Result.ok(0)
            >>> assert not x.is_ok_and(lambda x: x>1)

            >>> x = Result.err('hey')
            >>> assert not x.is_ok_and(lambda x: x>1)
        '''
        return self.is_ok() and f(self._ok)

    def is_err(self) -> bool:
        '''Returns `true` if the result is `Err`.

        Returns:
            ans: ...

        Examples:
            >>> x = Result.ok(-3)
            >>> assert not x.is_err()

            >>> x = Result.err('Some error message')
            >>> assert x.is_err()
        '''
        return not self.is_ok()

    def is_err_and(self, f: Func1[Tb, bool]) -> bool:  # type: ignore [type-arg, valid-type]
        '''Returns `true` if the result is `Err` and the value inside of it matches a predicate.

        Args:
            f: ...

        Returns:
            ans: ...

        Examples:
            >>> x = Result.err(FileNotFoundError('!'))
            >>> assert x.is_err_and(lambda x: type(x) is FileNotFoundError)

            >>> x = Result.err(PermissionError('!'))
            >>> assert not x.is_err_and(lambda x: type(x) is FileNotFoundError)

            >>> x = Result.ok(123)
            >>> assert not x.is_err_and(lambda x: type(x) is FileNotFoundError)
        '''
        return self.is_err() and f(self._err)

    def get_ok(self) -> 'Option[Ta]':  # type: ignore [type-arg, valid-type]
        '''Converts from `Result<T, E>` to `Option<T>`.

        Converts `self` into an `Option<T>`, consuming `self`,
        and discarding the error, if any.

        Returns:
            ans: ...

        Examples:
            >>> from iydon.util.rust.std.option import Option

            >>> x = Result.ok(2)
            >>> assert x.get_ok() == Option.some(2)

            >>> x = Result.err('Nothing here')
            >>> assert x.get_ok() == Option.none()

        Origin:
            - `pub const fn ok(self) -> Option<T>`
        '''
        from .option import Option

        return Option.new(self._ok)

    def get_err(self) -> 'Option[Tb]':  # type: ignore [type-arg, valid-type]
        '''Converts from `Result<T, E>` to `Option<E>`.

        Converts `self` into an `Option<E>`, consuming `self`,
        and discarding the success value, if any.

        Returns:
            ans: ...

        Examples:
            >>> from iydon.util.rust.std.option import Option

            >>> x = Result.ok(2)
            >>> assert x.get_err() == Option.none()

            >>> x = Result.err('Nothing here')
            >>> assert x.get_err() == Option.some('Nothing here')

        Origin:
            - `pub const fn err(self) -> Option<E>`
        '''
        from .option import Option

        return Option.new(self._err)

    def map(self, op: Func1[Ta, Tc]) -> 'te.Self[Tc, Tb]':  # type: ignore [misc, type-arg, valid-type]
        '''Maps a `Result<T, E>` to `Result<U, E>` by applying a function to a
            contained `Ok` value, leaving an `Err` value untouched.

        This function can be used to compose the results of two functions.

        Args:
            op: ...

        Returns:
            ans: ...

        Examples:
            >>> lines = '1\\n2\\n3\\n4\\n'

            >>> for line in lines.splitlines():
            ...     try:
            ...         ans = Result.ok(int(line))
            ...     except Exception as e:
            ...         ans = Result.err(e)
            ...     ans \\
            ...         .map(lambda i: i*2) \\
            ...         ._match(  # Test only
            ...             lambda o: print(f'Ok: {o}'),
            ...             lambda e: print(f'Err: {e}'),
            ...         )
            Ok: 2
            Ok: 4
            Ok: 6
            Ok: 8
        '''
        return self._match(lambda o: self.ok(op(o)), lambda e: self)

    def map_or(self, default: Tc, f: Func1[Ta, Tc]) -> Tc:  # type: ignore [type-arg, valid-type]
        '''Returns the provided default (if `Err`), or
            applies a function to the contained value (if `Ok`).

        Arguments passed to `map_or` are eagerly evaluated; if you are passing
        the result of a function call, it is recommended to use `map_or_else`,
        which is lazily evaluated.

        Args:
            default: ...
            f: ...

        Returns:
            ans: ...

        Examples:
            >>> x = Result.ok('foo')
            >>> assert x.map_or(42, len) == 3

            >>> x = Result.err('bar')
            >>> assert x.map_or(42, len) == 42

        TODO:
            - Typo @ https://github.com/iydon/iydon/blob/main/static/rust/result.rs#L768
        '''
        return self._match(lambda o: f(o), lambda e: default)

    def map_or_else(self, default: Func1[Tb, Tc], f: Func1[Ta, Tc]) -> Tc:  # type: ignore [type-arg, valid-type]
        '''Maps a `Result<T, E>` to `U` by applying fallback function `default` to
            a contained `Err` value, or function `f` to a contained `Ok` value.

        This function can be used to unpack a successful result
        while handling an error.

        Args:
            default: ...
            f: ...

        Returns:
            ans: ...

        Examples:
            >>> k = 21

            >>> x = Result.ok('foo')
            >>> assert x.map_or_else(lambda e: k*2, len) == 3

            >>> x = Result.err('bar')
            >>> assert x.map_or_else(lambda e: k*2, len) == 42
        '''
        return self._match(lambda o: f(o), lambda e: default(e))

    def map_err(self, op: Func1[Tb, Tc]) -> 'te.Self[Ta, Tc]':  # type: ignore [misc, type-arg, valid-type]
        '''Maps a `Result<T, E>` to `Result<T, F>` by applying a function to a
            contained `Err` value, leaving an `Ok` value untouched.

        This function can be used to pass through a successful result while handling
        an error.

        Args:
            op: ...

        Returns:
            ans: ...

        Examples:
            >>> def stringify(x: int) -> str: return f'error code: {x}'

            >>> x = Result.ok(2)
            >>> assert x.map_err(stringify) == Result.ok(2)

            >>> x = Result.err(13)
            >>> assert x.map_err(stringify) == Result.err('error code: 13')
        '''
        return self._match(lambda o: self, lambda e: self.err(op(e)))

    def inspect(self, f: Func1[Ta, None]) -> 'te.Self[Ta, Tb]':  # type: ignore [misc, type-arg, valid-type]
        '''Calls the provided closure with a reference to the contained value (if `Ok`).

        Args:
            f: ...

        Returns:
            ans: ...

        Examples:
            >>> x = Result.ok(4)
            >>> y = x \\
            ...     .inspect(lambda x: print(f'original: {x}')) \\
            ...     .map(lambda x: x**3) \\
            ...     .expect('failed to parse number')
            original: 4
            >>> assert y == 64
        '''
        if self.is_ok():
            f(self._ok)
        return self

    def inspect_err(self, f: Func1[Tb, None]) -> 'te.Self[Ta, Tb]':  # type: ignore [misc, type-arg, valid-type]
        '''Calls the provided closure with a reference to the contained error (if `Err`).

        Args:
            f: ...

        Returns:
            ans: ...

        Examples:
            >>> x = Result.err('address.txt') \\
            ...     .inspect_err(lambda e: print(f'failed to read file: {e}'))
            failed to read file: address.txt
            >>> assert x.is_err()
        '''
        if self.is_err():
            f(self._err)
        return self

    def expect(self, msg: str) -> Ta:  # type: ignore [valid-type]
        '''Returns the contained `Ok` value, consuming the `self` value.

        Because this function may panic, its use is generally discouraged.
        Instead, prefer to use pattern matching and handle the `Err`
        case explicitly, or call `unwrap_or`, `unwrap_or_else`.

        Args:
            msg: ...

        Returns:
            ans: ...

        Raises:
            AssertionError: Panics if the value is an `Err`, with a panic message including the
                passed message, and the content of the `Err`.

        Examples:
            >>> x = Result.err('emergency failure')
            >>> x.expect('Testing expect')
            Traceback (most recent call last):
                ...
            AssertionError: Testing expect
        '''
        assert self.is_ok(), msg

        return self._ok

    def unwrap(self) -> Ta:  # type: ignore [valid-type]
        '''Returns the contained `Ok` value, consuming the `self` value.

        Because this function may panic, its use is generally discouraged.
        Instead, prefer to use pattern matching and handle the `Err`
        case explicitly, or call `unwrap_or`, `unwrap_or_else`.

        Returns:
            ans: ...

        Raises:
            AssertionError: Panics if the value is an `Err`, with a panic message provided by the
                `Err`'s value.

        Examples:
            >>> x = Result.ok(2)
            >>> assert x.unwrap() == 2

            >>> x = Result.err('emergency failure')
            >>> x.unwrap()
            Traceback (most recent call last):
                ...
            AssertionError: called `Result::unwrap()` on an `Err` value
        '''
        return self.expect('called `Result::unwrap()` on an `Err` value')

    def expect_err(self, msg: str) -> Tb:  # type: ignore [valid-type]
        '''Returns the contained `Err` value, consuming the `self` value.

        Args:
            msg: ...

        Returns:
            ans: ...

        Raises:
            AssertionError: Panics if the value is an `Ok`, with a panic message including the
                passed message, and the content of the `Ok`.

        Examples:
            >>> x = Result.ok(10)
            >>> x.expect_err('Testing expect_err')
            Traceback (most recent call last):
                ...
            AssertionError: Testing expect_err
        '''
        assert self.is_err(), msg

        return self._err

    def unwrap_err(self) -> Tb:  # type: ignore [valid-type]
        '''Returns the contained `Err` value, consuming the `self` value.

        Returns:
            ans: ...

        Raises:
            AssertionError: Panics if the value is an `Ok`, with a custom panic message provided
                by the `Ok`'s value.

        Examples:
            >>> x = Result.ok(2)
            >>> x.unwrap_err()
            Traceback (most recent call last):
                ...
            AssertionError: called `Result::unwrap_err()` on an `Ok` value

            >>> x = Result.err('emergency failure')
            >>> assert x.unwrap_err() == 'emergency failure'
        '''
        return self.expect_err('called `Result::unwrap_err()` on an `Ok` value')

    def and_(self, res: 'te.Self[Tc, Tb]') -> 'te.Self[Tc, Tb]':  # type: ignore [misc]
        '''Returns `res` if the result is `Ok`, otherwise returns the `Err` value of `self`.

        Arguments passed to `and` are eagerly evaluated; if you are passing the
        result of a function call, it is recommended to use `and_then`, which is
        lazily evaluated.

        Args:
            res: ...

        Returns:
            ans: ...

        Examples:
            >>> x = Result.ok(2)
            >>> y = Result.err('late error')
            >>> assert x.and_(y) == Result.err('late error')

            >>> x = Result.err('early error')
            >>> y = Result.ok('foo')
            >>> assert x.and_(y) == Result.err('early error')

            >>> x = Result.err('not a 2')
            >>> y = Result.err('late error')
            >>> assert x.and_(y) == Result.err('not a 2')

            >>> x = Result.ok(2)
            >>> y = Result.ok('different result type')
            >>> assert x.and_(y) == Result.ok('different result type')
        '''
        return self._match(lambda o: res, lambda e: self)

    def and_then(self, op: Func1[Ta, 'te.Self[Tc, Tb]']) -> 'te.Self[Tc, Tb]':  # type: ignore [misc, type-arg, valid-type]
        '''Calls `op` if the result is `Ok`, otherwise returns the `Err` value of `self`.

        This function can be used for control flow based on `Result` values.

        Args:
            op: ...

        Returns:
            ans: ...

        Examples:
            >>> from iydon.util.rust.std.option import Option
            >>> u32 = int
            >>> def sq_then_to_string(x: u32) -> Result[str, str]:
            ...     # u32::checked_mul
            ...     if 0 <= x < 65536:
            ...         ans = Option.some(x*x)
            ...     else:
            ...         ans = Option.none()
            ...     return ans.map(str).ok_or('overflowed')

            >>> assert Result.ok(2).and_then(sq_then_to_string) == Result.ok('4')
            >>> assert Result.ok(1_000_000).and_then(sq_then_to_string) == Result.err('overflowed')
            >>> assert Result.err('not a number').and_then(sq_then_to_string) == Result.err('not a number')
        '''
        return self._match(lambda o: op(o), lambda e: self)

    def or_(self, res: 'te.Self[Ta, Tc]') -> 'te.Self[Ta, Tc]':  # type: ignore [misc]
        '''Returns `res` if the result is `Err`, otherwise returns the `Ok` value of `self`.

        Arguments passed to `or` are eagerly evaluated; if you are passing the
        result of a function call, it is recommended to use `or_else`, which is
        lazily evaluated.

        Args:
            res: ...

        Returns:
            ans: ...

        Examples:
            >>> x = Result.ok(2)
            >>> y = Result.err('late error')
            >>> assert x.or_(y) == Result.ok(2)

            >>> x = Result.err('early error')
            >>> y = Result.ok(2)
            >>> assert x.or_(y) == Result.ok(2)

            >>> x = Result.err('not a 2')
            >>> y = Result.err('late error')
            >>> assert x.or_(y) == Result.err('late error')

            >>> x = Result.ok(2)
            >>> y = Result.ok('different result type')
            >>> assert x.or_(y) == Result.ok(2)
        '''
        return self._match(lambda o: self, lambda e: res)

    def or_else(self, op: Func1[Tb, 'te.Self[Ta, Tc]']) -> 'te.Self[Ta, Tc]':  # type: ignore [misc, type-arg, valid-type]
        '''Calls `op` if the result is `Err`, otherwise returns the `Ok` value of `self`.

        This function can be used for control flow based on result values.

        Args:
            op: ...

        Returns:
            ans: ...

        Examples:
            >>> def sq(x: int) -> Result[int, int]: return Result.ok(x*x)
            >>> def err(x: int) -> Result[int, int]: return Result.err(x)

            >>> assert Result.ok(2).or_else(sq).or_else(sq) == Result.ok(2)
            >>> assert Result.ok(2).or_else(err).or_else(sq) == Result.ok(2)
            >>> assert Result.err(3).or_else(sq).or_else(err) == Result.ok(9)
            >>> assert Result.err(3).or_else(err).or_else(err) == Result.err(3)
        '''
        return self._match(lambda o: self, lambda e: op(e))

    def unwrap_or(self, default: Ta) -> Ta:  # type: ignore [valid-type]
        '''Returns the contained `Ok` value or a provided default.

        Arguments passed to `unwrap_or` are eagerly evaluated; if you are passing
        the result of a function call, it is recommended to use `unwrap_or_else`,
        which is lazily evaluated.

        Args:
            default: ...

        Returns:
            ans: ...

        Examples:
            >>> default = 2

            >>> x = Result.ok(9)
            >>> assert x.unwrap_or(default) == 9

            >>> x = Result.err('error')
            >>> assert x.unwrap_or(default) == default
        '''
        return self._match(lambda o: o, lambda e: default)

    def unwrap_or_else(self, op: Func1[Tb, Ta]) -> Ta:  # type: ignore [type-arg, valid-type]
        '''Returns the contained `Ok` value or computes it from a closure.

        Args:
            op: ...

        Returns:
            ans: ...

        Examples:
            >>> def count(x: str) -> int: return len(x)

            >>> assert Result.ok(2).unwrap_or_else(count) == 2
            >>> assert Result.err('foo').unwrap_or_else(count) == 3
        '''
        return self._match(lambda o: o, lambda e: op(e))

    def contains(self, x: Ta) -> bool:  # type: ignore [valid-type]
        '''Returns `true` if the result is an `Ok` value containing the given value.

        Args:
            x: ...

        Returns:
            ans: ...

        Examples:
            >>> x = Result.ok(2)
            >>> assert x.contains(2)

            >>> x = Result.ok(3)
            >>> assert not x.contains(2)

            >>> x = Result.err('Some error message')
            >>> assert not x.contains(2)
        '''
        return self._match(lambda o: o==x, lambda e: False)  # type: ignore [operator]

    def contains_err(self, f: Tb) -> bool:  # type: ignore [valid-type]
        '''Returns `true` if the result is an `Err` value containing the given value.

        Args:
            f: ...

        Returns:
            ans: ...

        Examples:
            >>> x = Result.ok(2)
            >>> assert not x.contains_err('Some error message')

            >>> x = Result.err('Some error message')
            >>> assert   x.contains_err('Some error message')

            >>> x = Result.err('Some other error message')
            >>> assert not x.contains_err('Some error message')
        '''
        return self._match(lambda o: False, lambda e: e==f)  # type: ignore [operator]

    def _match(self, f4ok: Func1[Ta, Tc], f4err: Func1[Tb, Tc]) -> Tc:  # type: ignore [type-arg, valid-type]
        '''
        Prototype:
            ```Rust
            return match self {
                Ok(o) => f4ok(o),
                Err(e) => f4err(e),
            };
            ```
        '''
        if self.is_ok():
            return f4ok(self._ok)
        else:
            return f4err(self._err)


Ok = Result.ok
Err = Result.err
