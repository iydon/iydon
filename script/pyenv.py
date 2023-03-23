import typing as t
import subprocess
import sys
import warnings as w

try:
    from tqdm import tqdm
except ModuleNotFoundError:
    tqdm = lambda x: x


pyenv = {
    'linux': 'pyenv',
    'win32': 'pyenv.bat',
}[sys.platform]
pythons = [(3, 7), (3, 8), (3, 9), (3, 10), (3, 11), (3, 12)]


def run(*args: str, output: bool = True) -> t.Optional[bytes]:
    cp = subprocess.run(args, capture_output=output)
    if cp.returncode != 0:
        w.warn(cp.stderr)
    return cp.stdout


if __name__ == '__main__':
    records: t.Dict[int, t.Dict[int, t.List]] = {}  # major.minor.micro
    for version in run(pyenv, 'install', '--list').decode().splitlines():
        if version.count('.') == 2:
            major, minor, micro = parts = version.strip().split('.')
            if all(part.isdecimal() for part in parts):
                records \
                    .setdefault(int(major), {}) \
                    .setdefault(int(minor), []) \
                    .append(int(micro))
    versions = []
    for major, minor in tqdm(pythons):
        micros = records.get(major, {}).get(minor, None)
        if micros is not None:
            version = f'{major}.{minor}.{max(micros)}'
            versions.append(version)
            print('Install:', version)
            run(pyenv, 'install', '--skip-existing', version, output=False)
    run(pyenv, 'local', *versions, output=False)
