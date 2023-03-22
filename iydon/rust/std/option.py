__all__ = ['NONE', 'Option', 'Some']


import copy
import typing as t
import warnings as w

from ...base.type import Ta, Tb, Tc, Func0, Func1, Func2

if t.TYPE_CHECKING:
    import typing_extensions as te

    from .result import Result


class Option(t.Generic[Ta]):  # type: ignore [misc]
    '''Optional values.

    Reference:
        - https://doc.rust-lang.org/std/option/
        - https://doc.rust-lang.org/src/core/option.rs.html
        - https://github.com/iydon/iydon/blob/main/static/rust/option.rs
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
        return self._match(lambda v: f'Option.some({v!r})', lambda: 'Option.none()')

    def __str__(self) -> str:
        return self._match(lambda v: f'Option::Some({v!r})', lambda: 'Option::None')

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
        '''Returns `true` if the option is a [`Some`] value.

        Example:
            >>> x = Option.some(2)
            >>> assert x.is_some()

            >>> x = Option.none()
            >>> assert not x.is_some()
        '''
        return not self.is_none()

    def is_some_and(self, f: Func1[Ta, bool]) -> bool:  # type: ignore [type-arg, valid-type]
        '''Returns `true` if the option is a [`Some`] and the value inside of it matches a predicate.

        Example:
            >>> x = Option.some(2)
            >>> assert x.is_some_and(lambda x: x>1)

            >>> x = Option.some(0)
            >>> assert not x.is_some_and(lambda x: x>1)

            >>> x = Option.none()
            >>> assert not x.is_some_and(lambda x: x>1)
        '''
        return self.is_some() and f(self._value)

    def is_none(self) -> bool:
        '''Returns `true` if the option is a [`None`] value.

        Example:
            >>> x = Option.some(2)
            >>> assert not x.is_none()

            >>> x = Option.none()
            >>> assert x.is_none()
        '''
        return self._value is None

    def expect(self, msg: str) -> Ta:  # type: ignore [valid-type]
        '''Returns the contained [`Some`] value, consuming the `self` value.

        Example:
            >>> x = Option.some('value')
            >>> assert x.expect('fruits are healthy') == 'value'

            >>> x = Option.none()
            >>> x.expect('fruits are healthy')
            Traceback (most recent call last):
                ...
            AssertionError: fruits are healthy
        '''
        assert self.is_some(), msg

        return self._value

    def unwrap(self) -> Ta:  # type: ignore [valid-type]
        '''Returns the contained [`Some`] value, consuming the `self` value.

        Example:
            >>> x = Option.some('air')
            >>> assert x.unwrap() == 'air'

            >>> x = Option.none()
            >>> x.unwrap()
            Traceback (most recent call last):
                ...
            AssertionError: called `Option::unwrap()` on a `None` value
        '''
        return self.expect('called `Option::unwrap()` on a `None` value')

    def unwrap_or(self, default: Ta) -> Ta:  # type: ignore [valid-type]
        '''Returns the contained [`Some`] value or a provided default.

        Example:
            >>> assert Option.some('car').unwrap_or('bike') == 'car'
            >>> assert Option.none().unwrap_or('bike') == 'bike'
        '''
        return self._match(lambda v: v, lambda: default)

    def unwrap_or_else(self, f: Func0[Ta]) -> Ta:  # type: ignore [type-arg, valid-type]
        '''Returns the contained [`Some`] value or computes it from a closure.

        Example:
            >>> k = 10
            >>> assert Option.some(4).unwrap_or_else(lambda: 2*k) == 4
            >>> assert Option.none().unwrap_or_else(lambda: 2*k) == 20
        '''
        return self._match(lambda v: v, f)

    def map(self, f: Func1[Ta, Tb]) -> 'te.Self[Tb]':  # type: ignore [misc, type-arg, valid-type]
        '''Maps an `Option<T>` to `Option<U>` by applying a function to a contained value (if `Some`) or returns `None` (if `None`).

        Example:
            >>> maybe_some_string = Option.some('Hello, World!')
            >>> maybe_some_len = maybe_some_string.map(len)
            >>> assert maybe_some_len == Option.some(13)

            >>> x = Option.none()
            >>> assert x.map(len) == Option.none()
        '''
        # TODO: self.some or self.new?
        return self._match(lambda v: self.some(f(v)), lambda: self)

    def inspect(self, f: Func1[Ta, None]) -> 'te.Self[Ta]':  # type: ignore [misc, type-arg, valid-type]
        '''Calls the provided closure with a reference to the contained value (if [`Some`]).

        Example:
            >>> x = Option.some(4).inspect(lambda x: print(f'got: {x}'))
            got: 4

            >>> x = Option.none().inspect(lambda x: print(f'got: {x}'))
        '''
        if self.is_some():
            f(self._value)
        return self

    def map_or(self, default: Tb, f: Func1[Ta, Tb]) -> Tb:  # type: ignore [type-arg, valid-type]
        '''Returns the provided default result (if none), or applies a function to the contained value (if any).

        Example:
            >>> x = Option.some('foo')
            >>> assert x.map_or(42, len) == 3

            >>> x = Option.none()
            >>> assert x.map_or(42, len) == 42
        '''
        return self._match(lambda v: f(v), lambda: default)

    def map_or_else(self, default: Func0[Tb], f: Func1[Ta, Tb]) -> Tb:  # type: ignore [type-arg, valid-type]
        '''Computes a default function result (if none), or applies a different function to the contained value (if any).

        Example:
            >>> k = 21

            >>> x = Option.some('foo')
            >>> assert x.map_or_else(lambda: 2*k, len) == 3

            >>> x = Option.none()
            >>> assert x.map_or_else(lambda: 2*k, len) == 42
        '''
        return self._match(lambda v: f(v), default)

    def ok_or(self, err: Tb) -> 'Result[Ta, Tb]':  # type: ignore [type-arg, valid-type]
        '''Transforms the `Option<T>` into a [`Result<T, E>`], mapping [`Some(v)`] to [`Ok(v)`] and [`None`] to [`Err(err)`].

        Example:
            >>> from iydon.rust.std.result import Result

            >>> x = Option.some('foo')
            >>> assert x.ok_or(0) == Result.ok('foo')

            >>> x = Option.none()
            >>> assert x.ok_or(0) == Result.err(0)
        '''
        from .result import Result

        return self._match(lambda v: Result.ok(v), lambda: Result.err(err))

    def ok_or_else(self, err: Func0[Tb]) -> 'Result[Ta, Tb]':  # type: ignore [type-arg, valid-type]
        '''Transforms the `Option<T>` into a [`Result<T, E>`], mapping [`Some(v)`] to [`Ok(v)`] and [`None`] to [`Err(err())`].

        Example:
            >>> from iydon.rust.std.result import Result

            >>> x = Option.some('foo')
            >>> assert x.ok_or_else(lambda: 0) == Result.ok('foo')

            >>> x = Option.none()
            >>> assert x.ok_or_else(lambda: 0) == Result.err(0)
        '''
        from .result import Result

        return self._match(lambda v: Result.ok(v), lambda: Result.err(err()))

    def and_(self, optb: 'te.Self[Tb]') -> 'te.Self[Tb]':  # type: ignore [misc]
        '''Returns [`None`] if the option is [`None`], otherwise returns `optb`.

        Example:
            >>> x = Option.some(2)
            >>> y = Option.none()
            >>> assert x.and_(y) == Option.none()

            >>> x = Option.none()
            >>> y = Option.some('foo')
            >>> assert x.and_(y) == Option.none()

            >>> x = Option.some(2)
            >>> y = Option.some('foo')
            >>> assert x.and_(y) == Option.some('foo')

            >>> x = Option.none()
            >>> y = Option.none()
            >>> assert x.and_(y) == Option.none()
        '''
        return self._match(lambda v: optb, lambda: self)

    def and_then(self, f: Func1[Ta, 'te.Self[Tb]']) -> 'te.Self[Tb]':  # type: ignore [misc, type-arg, valid-type]
        '''Returns [`None`] if the option is [`None`], otherwise calls `f` with the wrapped value and returns the result.

        Example:
            >>> u32 = int
            >>> def sq_then_to_string(x: u32) -> Option[str]:
            ...     # u32::checked_mul
            ...     if 0 <= x < 65536:
            ...         ans = Option.some(x*x)
            ...     else:
            ...         ans = Option.none()
            ...     return ans.map(str)

            >>> assert Option.some(2).and_then(sq_then_to_string) == Option.some('4')
            >>> assert Option.some(1_000_000).and_then(sq_then_to_string) == Option.none()  # overflowed!
            >>> assert Option.none().and_then(sq_then_to_string) == Option.none()
        '''
        return self._match(lambda v: f(v), lambda: self)

    def filter(self, predicate: Func1[Ta, bool]) -> 'te.Self[Ta]':  # type: ignore [misc, type-arg, valid-type]
        '''Returns [`None`] if the option is [`None`], otherwise calls `predicate` with the wrapped value and returns:
        - [`Some(t)`] if `predicate` returns `true` (where `t` is the wrapped value), and
        - [`None`] if `predicate` returns `false`.

        Example:
            >>> def is_even(n: int) -> bool:
            ...     return n % 2 == 0

            >>> assert Option.none().filter(is_even) == Option.none()
            >>> assert Option.some(3).filter(is_even) == Option.none()
            >>> assert Option.some(4).filter(is_even) == Option.some(4)
        '''
        if self.is_some():
            if predicate(self._value):
                return self
        return self.none()

    def or_(self, optb: 'te.Self[Ta]') -> 'te.Self[Ta]':  # type: ignore [misc]
        '''Returns the option if it contains a value, otherwise returns `optb`.

        Example:
            >>> x = Option.some(2)
            >>> y = Option.none()
            >>> assert x.or_(y) == Option.some(2)

            >>> x = Option.none()
            >>> y = Option.some(100)
            >>> assert x.or_(y) == Option.some(100)

            >>> x = Option.some(2)
            >>> y = Option.some(100)
            >>> assert x.or_(y) == Option.some(2)

            >>> x = Option.none()
            >>> y = Option.none()
            >>> assert x.or_(y) == Option.none()
        '''
        return self._match(lambda v: self, lambda: optb)

    def or_else(self, f: Func0['te.Self[Ta]']) -> 'te.Self[Ta]':  # type: ignore [misc, type-arg]
        '''Returns the option if it contains a value, otherwise calls `f` and returns the result.

        Example:
            >>> def nobody() -> Option[str]: return Option.none()
            >>> def vikings() -> Option[str]: return Option.some('vikings')

            >>> assert Option.some('barbarians').or_else(vikings) == Option.some('barbarians')
            >>> assert Option.none().or_else(vikings) == Option.some('vikings')
            >>> assert Option.none().or_else(nobody) == Option.none()
        '''
        return self._match(lambda v: self, f)

    def xor(self, opt: 'te.Self[Ta]') -> 'te.Self[Ta]':  # type: ignore [misc]
        '''Returns [`Some`] if exactly one of `self`, `optb` is [`Some`], otherwise returns [`None`].

        Example:
            >>> x = Option.some(2)
            >>> y = Option.none()
            >>> assert x.xor(y) == Option.some(2)

            >>> x = Option.none()
            >>> y = Option.some(2)
            >>> assert x.xor(y) == Option.some(2)

            >>> x = Option.some(2)
            >>> y = Option.some(2)
            >>> assert x.xor(y) == Option.none()

            >>> x = Option.none()
            >>> y = Option.none()
            >>> assert x.xor(y) == Option.none()
        '''
        return self._match(
            lambda v1: opt._match(lambda v2: self.none(), lambda: self),
            lambda: opt._match(lambda v2: opt, self.none),
        )

    def insert(self, value: Ta) -> Ta:  # type: ignore [valid-type]
        '''Inserts `value` into the option, then returns a mutable reference to it.

        Example:
            >>> opt = Option.none()
            >>> val = opt.insert(1)
            >>> assert opt == Option.none()
            >>> assert val == 1
            >>> val = opt.insert(2)
            >>> assert val == 2
            >>> val = opt.insert(3)
            >>> assert opt == Option.none()

        TODO:
            - `Some` and `None` are not convertible
        '''
        if self.is_none():
            w.warn('`Some` and `None` are not convertible')
            return value
        else:
            self._value = value
            return value

    def get_or_insert(self, value: Ta) -> Ta:  # type: ignore [valid-type]
        '''Inserts `value` into the option if it is [`None`], then returns a mutable reference to the contained value.

        Example:
            >>> x = Option.none()
            >>> y = x.get_or_insert(5)
            >>> assert y == 5
            >>> assert x == Option.none()

        TODO:
            - `Some` and `None` are not convertible
        '''
        if self.is_none():
            w.warn('`Some` and `None` are not convertible')
            return value
        else:
            return self._value

    def get_or_insert_with(self, f: Func0[Ta]) -> Ta: # type: ignore [type-arg, valid-type]
        '''Inserts a value computed from `f` into the option if it is [`None`], then returns a mutable reference to the contained value.

        Example:
            >>> x = Option.none()
            >>> y = x.get_or_insert_with(lambda: 5)
            >>> assert y == 5
            >>> assert x == Option.none()

        TODO:
            - `Some` and `None` are not convertible
        '''
        if self.is_none():
            w.warn('`Some` and `None` are not convertible')
            return f()
        else:
            return self._value

    def take(self) -> 'te.Self[Ta]':  # type: ignore [misc]
        '''Takes the value out of the option, leaving a [`None`] in its place.

        Example:
            >>> x = Option.some(2)
            >>> y = x.take()
            >>> assert x == Option.some(2)
            >>> assert y == Option.some(2)

            >>> x = Option.none()
            >>> y = x.take()
            >>> assert x == Option.none()
            >>> assert y == Option.none()

        TODO:
            - `Some` and `None` are not convertible
        '''
        if self.is_some():
            w.warn('`Some` and `None` are not convertible')
        return self

    def replace(self, value: Ta) -> 'te.Self[Ta]':  # type: ignore [misc, valid-type]
        '''Replaces the actual value in the option by the value given in parameter, returning the old value if present, leaving a [`Some`] in its place without deinitializing either one.

        Example:
            >>> x = Option.some(2)
            >>> old = x.replace(5)
            >>> assert x == Option.some(5)
            >>> assert old == Option.some(2)

            >>> x = Option.none()
            >>> old = x.replace(3)
            >>> assert x == Option.none()
            >>> assert old == Option.none()

        TODO:
            - `Some` and `None` are not convertible
        '''
        if self.is_none():
            w.warn('`Some` and `None` are not convertible')
            return self
        else:
            ans, self._value = self.some(self._value), value
            return ans

    def contains(self, x: Ta) -> bool:  # type: ignore [valid-type]
        '''Returns `true` if the option is a [`Some`] value containing the given value.

        Example:
            >>> x = Option.some(2)
            >>> assert x.contains(2)

            >>> x = Option.some(3)
            >>> assert not x.contains(2)

            >>> x = Option.none()
            >>> assert not x.contains(2)
        '''
        return self._match(lambda v: x==v, lambda: False)  # type: ignore [operator]

    def zip(self, other: 'te.Self[Tb]') -> 'te.Self[t.Tuple[Ta, Tb]]':  # type: ignore [misc]
        '''Zips `self` with another `Option`.

        Example:
            >>> x = Option.some(1)
            >>> y = Option.some('hi')
            >>> z = Option.none()

            >>> assert x.zip(y) == Option.some((1, 'hi'))
            >>> assert x.zip(z) == Option.none()
        '''
        if self.is_some() and other.is_some():
            return self.some((self._value, other._value))
        else:
            return self.none()

    def zip_with(self, other: 'te.Self[Tb]', f: Func2[Ta, Tb, Tc]) -> 'te.Self[Tc]':  # type: ignore [misc, type-arg, valid-type]
        '''Zips `self` and another `Option` with function `f`.

        Example:
            >>> class Point:
            ...     def __init__(self, x: float, y: float) -> None:
            ...         self.x, self.y = x, y
            ...
            ...     def __eq__(self, other: 'Point') -> bool:
            ...         return self.x == other.x and self.y == other.y

            >>> x = Option.some(17.5)
            >>> y = Option.some(42.7)

            >>> assert x.zip_with(y, Point) == Option.some(Point(17.5, 42.7))
            >>> assert x.zip_with(Option.none(), Point) == Option.none()
        '''
        if self.is_some() and other.is_some():
            return self.some(f(self._value, other._value))
        else:
            return self.none()

    def _match(self, f4some: Func1[Ta, Tb], f4none: Func0[Tb]) -> Tb:  # type: ignore [type-arg, valid-type]
        '''
        Principle:
            ```Rust
            return match self {
                Some(v) => f4some(v),
                None => f4none(),
            };
            ```
        '''
        if self.is_none():
            return f4none()
        else:
            return f4some(self._value)

    def _copy(self) -> 'te.Self[Ta]':  # type: ignore [misc]
        return self._match(lambda v: self.some(copy.deepcopy(v)), self.none)


Some = Option.some
NONE = Option.none()
