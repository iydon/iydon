import datetime

import click

from . import poetry
from ..config import ROOT
from ..util import pyproject, run


def api(sure: bool = False) -> None:
    today = datetime.date.today()
    config = pyproject()
    ver_old = config['tool']['poetry']['version']
    paths = config['tool']['script']['config']['upgrade']
    year, iota = map(int, ver_old.split('.'))
    # ver_old -> ver_new
    if today.year > year:
        ver_new = f'{today.year}.0'
    elif today.year == year:
        ver_new = f'{today.year}.{iota+1}'
    else:
        raise NotImplementedError
    # replace versions
    for path in map(ROOT.__truediv__, paths):
        if sure:
            path.write_text(path.read_text().replace(ver_old, ver_new))
        else:
            click.echo(f'[LOG] {ver_old} -> {ver_new} @ {path}')
    # git
    if sure:
        call = lambda cmd: run(cmd)
    else:
        call = lambda cmd: click.echo(f'[CMD] {cmd}')
    call(f'git add {" ".join(paths)}')
    call(f'git commit -m ":tada: iydon @ v{ver_new}"')
    call(f'git tag v{ver_new}')
    call(f'git push')
    call(f'git push --tags')
    # publish
    if sure:
        poetry.api(publish=True)
    else:
        click.echo('[CMD] poetry publish')
