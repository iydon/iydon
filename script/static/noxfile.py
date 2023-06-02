import pathlib as p
import subprocess as sp
import sys
import typing as t

import nox

from nox_poetry.sessions import Session, session

if t.TYPE_CHECKING:
    import typing_extensions as te

    P = te.ParamSpec('P')
    Kwargs = te.ParamSpecKwargs(P)


class Config:
    root = p.Path(__file__).absolute().parent
    options = {
        'envdir': (root/'.nox'/sys.platform).as_posix(),
        'reuse_existing_virtualenvs': True,
    }
    pythons = [(3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12)]

    def __init__(self) -> None:
        for key, value in self.options.items():
            setattr(nox.options, key, value)

    def versions(self) -> t.List[str]:
        records: t.Dict[int, t.Dict[int, t.List]] = {}  # major.minor.micro
        stdout: bytes = self._pyenv('install', '--list', capture_output=True).stdout
        for version in stdout.decode().splitlines():
            if version.count('.') == 2:
                major, minor, micro = version.strip().split('.')
                if major.isdecimal() and minor.isdecimal() and micro.isdecimal():
                    records \
                        .setdefault(int(major), {}) \
                        .setdefault(int(minor), []) \
                        .append(int(micro))
        versions: t.List[str] = []
        for major, minor in self.pythons:
            micros = records.get(major, {}).get(minor, None)
            if micros is not None:
                version = f'{major}.{minor}.{max(micros)}'
                versions.append(version)
                self._pyenv('install', '--skip-existing', version)
        self._pyenv('local', *versions)
        return versions

    def _pyenv(self, *args: str, **kwargs: 'Kwargs') -> sp.CompletedProcess:
        kwargs = {'cwd': self.root, **kwargs}
        return sp.run(['pyenv', *args], **kwargs)


config = Config()


@session(python=config.versions())
def all(sess: Session) -> None:
    '''Run type checks and unit tests
    '''
    script = ('python', '-m', 'script')
    sess.run_always(*script, 'poetry', '--install', external=True)
    sess.run(*script, 'mkdocs', '--build')
    sess.run(*script, 'mypy')
    sess.run(*script, 'pytest')
