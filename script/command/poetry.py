import getpass

from ..config import POETRY
from ..util import run


def api(
    graph: bool = False,
    install: bool = False,
    publish: bool = False,
    update: bool = False,
) -> None:
    if graph:
        run(f'{POETRY} show --tree')
    if install:
        run(f'{POETRY} install --extras full')
    if publish:
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        run(f'{POETRY} build')
        run(f'{POETRY} publish --username="{username}" --password="{password}"')
    if update:
        run(f'{POETRY} update')
