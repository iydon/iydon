import datetime
import pathlib as p
import subprocess as sp

import tomli


input('>>> You sure?')

# 0. parameters
root = p.Path(__file__).absolute().parents[1]
cwd = root.as_posix()
paths = [
    root / 'pyproject.toml',
    root / 'iydon' / 'base' / 'constant.py',
]
today = datetime.date.today()
project = tomli.loads((root/'pyproject.toml').read_text())
ver_old = project['tool']['poetry']['version']
year, month, iota = map(int, ver_old.split('.'))

# 1. ver_old -> ver_new
if today.year > year:
    ver_new = f'{today.year}.{today.month}.0'
elif today.year == year:
    if today.month > month:
        ver_new = f'{year}.{today.month}.0'
    elif today.month == month:
        ver_new = f'{year}.{month}.{iota+1}'
    else:
        raise NotImplementedError
else:
    raise NotImplementedError

# 2. replace versions
for path in paths:
    text = path.read_text()
    if ver_old in text:
        path.write_text(text.replace(ver_old, ver_new))

# 3. git
sp.run(['git', 'add', *map(p.Path.as_posix, paths)])
sp.run(['git', 'commit', '-m', f':tada: iydon @ v{ver_new}'], cwd=cwd)
sp.run(['git', 'tag', f'v{ver_new}'], cwd=cwd)
sp.run(['git', 'push'], cwd=cwd)
sp.run(['git', 'push', '--tags'], cwd=cwd)

# 4. publish
sp.run(['make', 'publish'], cwd=cwd)
