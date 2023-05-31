from ..config import NOX, ROOT, STATIC
from ..util import run


def api() -> None:
    src = STATIC / 'noxfile.py'
    dst = ROOT / src.name
    if not dst.exists():
        src.link_to(dst)
    try:
        run(f'{NOX}')
    finally:
        dst.unlink()
