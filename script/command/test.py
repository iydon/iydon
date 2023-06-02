from . import mypy, pytest


def api() -> None:
    mypy.api()
    pytest.api()
