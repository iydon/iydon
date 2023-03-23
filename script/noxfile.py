import pathlib as p
import subprocess as sp
import sys
import typing as t

import nox

from nox_poetry.sessions import Session, session


# parameters
root = p.Path(__file__).absolute().parent
options = {
    'envdir': (root/'.nox'/sys.platform).as_posix(),
    'reuse_existing_virtualenvs': True,
}
pyenvs = {
    'linux': ['pyenv'],
    'win32': ['pyenv.bat', 'pyenv.ps1'],
}
pythons = [(3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12)]


# options
for key, value in options.items():
    setattr(nox.options, key, value)
# pyenvs, pythons
for pyenv in pyenvs[sys.platform]:
    status, result = sp.getstatusoutput(pyenv)
    if status in {0, 1}:
        break
else:
    raise FileNotFoundError('No available pyenv command')
records: t.Dict[int, t.Dict[int, t.List]] = {}  # major.minor.micro
for version in sp.run([pyenv, 'install', '--list'], capture_output=True).stdout.decode().splitlines():
    if version.count('.') == 2:
        major, minor, micro = version.strip().split('.')
        if major.isdecimal() and minor.isdecimal() and micro.isdecimal():
            records \
                .setdefault(int(major), {}) \
                .setdefault(int(minor), []) \
                .append(int(micro))
versions: t.List[str] = []
for major, minor in pythons:
    micros = records.get(major, {}).get(minor, None)
    if micros is not None:
        version = f'{major}.{minor}.{max(micros)}'
        versions.append(version)
        print(f'Install Python @ {version}')
        sp.run([pyenv, 'install', '--skip-existing', version])
sp.run([pyenv, 'local', *versions], cwd=root.as_posix())


# decorators
@session(python=versions)
def all(sess: Session) -> None:
    '''Run type checks and unit tests
    '''
    sess.run_always('poetry', 'install', '--extras', 'full', external=True)
    sess.run('mypy', '--warn-unused-ignores', 'iydon')
    sess.run('pytest', '--pyargs', 'iydon')
