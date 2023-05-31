import pathlib as p
import subprocess as sp
import typing as t

from .config import PYPROJECT, ROOT
from .type import Any, Command, DictStr, Path

if t.TYPE_CHECKING:
    import typing_extensions as te

    from tomlkit.toml_document import TOMLDocument

    P = te.ParamSpec('P')
    Kwargs = te.ParamSpecKwargs(P)


_pyproject = None


def config() -> DictStr[Any]:
    return pyproject()['tool']['script']['config']

def mkdir(path: Path) -> p.Path:
    directory = p.Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory

def pure(command: Command, **kwargs: 'Kwargs') -> sp.CompletedProcess:
    kwargs = {'shell': True, 'cwd': ROOT, **kwargs}
    return sp.run(command, **kwargs)

def pyproject() -> 'TOMLDocument':
    global _pyproject

    if _pyproject is None:
        from tomlkit import parse

        _pyproject = parse(PYPROJECT.read_text())
    return _pyproject

def run(command: Command, **kwargs: 'Kwargs') -> None:
    cp = pure(command, **kwargs)
    assert cp.returncode == 0, cp.stderr
