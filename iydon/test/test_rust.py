import doctest

from iydon.util.rust.std import option, result


def test_option() -> None:
    ans = doctest.testmod(option)
    assert ans.failed == 0

def test_result() -> None:
    ans = doctest.testmod(result)
    assert ans.failed == 0
