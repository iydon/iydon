import pathlib as p
import shutil
import sys

from ..config import CACHE, CARGO, GIT, STATIC
from ..util import run


def api() -> p.Path:
    tokei = CACHE / 'tokei'
    if not tokei.exists():
        tokei.parent.mkdir(parents=True, exist_ok=True)
        run(f'{GIT} clone --depth 1 --branch v12.1.2 https://github.com/XAMPPRocky/tokei {tokei}')
    shutil.copyfile(STATIC/'languages.json', tokei/'languages.json')
    run(f'{CARGO} build --release', cwd=tokei)
    return tokei/'target'/'release'/{
        'win32': 'tokei.exe',
        'linux': 'tokei',
    }[sys.platform]
