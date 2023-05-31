from ..config import NOX, STATIC
from ..util import run


def api() -> None:
    src = STATIC / 'noxfile.py'
    run(f'{NOX} --noxfile {src}')
