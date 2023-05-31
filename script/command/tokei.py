import pathlib as p
import shutil
import sys

from ..config import CACHE, CARGO, GIT, STATIC
from ..util import run


def api() -> p.Path:
    assert sys.platform == 'win32'

    tokei = CACHE / 'tokei'
    if not tokei.exists():
        tokei.parent.mkdir(parents=True, exist_ok=True)
        run(f'{GIT} clone --depth 1 --branch v12.1.2 https://github.com/XAMPPRocky/tokei {tokei}')
    shutil.copyfile(STATIC/'languages.json', tokei/'languages.json')
    run(f'{CARGO} build --release', cwd=tokei)
    target = CACHE / 'tokei.exe'
    shutil.copyfile(tokei/'target'/'release'/'tokei.exe', target)
    return target
