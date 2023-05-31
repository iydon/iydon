import shutil

from ..config import ROOT


def api() -> None:
    for path in ROOT.rglob('__pycache__'):
        shutil.rmtree(path)
