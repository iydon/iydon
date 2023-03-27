import doctest

from iydon.glhf import end


def test_end() -> None:
    ans = doctest.testmod(end)
    assert ans.failed == 0

def test_silver_bullet() -> None:
    try:
        from iydon.glhf import silver_bullet as _
    except SyntaxError as e:
        assert e.msg == 'No Silver Bullet.'
