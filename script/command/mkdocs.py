from ..config import MKDOCS
from ..util import run


def api(build: bool = False, serve: bool = False) -> None:
    if build:
        run(f'{MKDOCS} build')
    if serve:
        run(f'{MKDOCS} serve')
