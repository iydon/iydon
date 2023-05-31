from ..config import MYPY
from ..util import run


def api() -> None:
    run(f'{MYPY} --warn-unused-ignores iydon')
