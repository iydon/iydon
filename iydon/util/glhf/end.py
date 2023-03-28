__all__ = ['END', 'End', 'end']


class end:
    '''End of indented code block.

    Examples:
        >>> import io
        >>> import sys
        >>> from iydon.util.glhf.end import end

        >>> # if_stmt
        >>> if 1 + 1 == 2:
        ...     pass
        >>> end.if_

        >>> # while_stmt
        >>> while False:
        ...     pass
        >>> end.while_

        >>> # for_stmt
        >>> for _ in range(9):
        ...     pass
        >>> end.for_

        >>> # try_stmt
        >>> try:
        ...     1 / 0
        ... except ZeroDivisionError:
        ...     pass
        >>> end.try_

        >>> # with_stmt
        >>> with io.StringIO() as f:
        ...     pass
        >>> end.with_

        >>> # match_stmt
        >>> if sys.version_info >= (3, 10):
        ...     exec(\'\'\'
        ... match 0:
        ...     case 1:
        ...         pass
        ...     case _:
        ...         pass
        ... end.match_
        ...     \'\'\')

        >>> # funcdef
        >>> def f() -> None:
        ...     pass
        >>> end.def_

        >>> # classdef
        >>> class C:
        ...     pass
        >>> end.class_

    References:
        - https://docs.python.org/3/reference/compound_stmts.html

    TODO:
        - async_with_stmt
        - async_for_stmt
        - async_funcdef
    '''

    IF = If = if_ = None
    WHILE = While = while_ = None
    FOR = For = for_ = None
    TRY = Try = try_ = None
    WITH = With = with_ = None
    MATCH = Match = match_ = None
    DEF = Def = def_ = None
    CLASS = Class = class_ = None
    ASYNC_WITH = AsyncWith = async_with = None
    ASYNC_FOR = AsyncFor = async_for = None
    ASYNC_DEF = AsyncDef = async_def = None


END = End = end
