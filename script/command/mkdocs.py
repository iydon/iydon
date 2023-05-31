from ..config import MKDOCS
from ..util import run


def api() -> None:
    run(f'{MKDOCS} build')
