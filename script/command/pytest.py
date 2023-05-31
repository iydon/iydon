from ..config import PYTEST
from ..util import run


def api() -> None:
    run(f'{PYTEST} --pyargs iydon')
