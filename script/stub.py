import importlib as _i
import types as _t

import click as _c


def _import(name: str, package: str = __package__) -> _t.ModuleType:
    return _i.import_module(name, package)


@_c.command()
def mkdocs() -> None:
    '''Build the MkDocs documentation'''
    _import('.command.mkdocs').api()


@_c.command()
def mypy() -> None:
    '''Check static type for Python'''
    _import('.command.mypy').api()


@_c.command()
def nox() -> None:
    '''Use nox for automate and standardize testing'''
    _import('.command.nox').api()

@_c.command()
@_c.option('-g', '--graph', is_flag=True)
@_c.option('-i', '--install', is_flag=True)
@_c.option('-p', '--publish', is_flag=True)
@_c.option('-u', '--update', is_flag=True)
def poetry(graph: bool, install: bool, publish: bool, update: bool) -> None:
    '''Run poetry through wrapper'''
    _import('.command.poetry').api(graph, install, publish, update)


@_c.command()
def pytest() -> None:
    '''Use pytest framework for unit testing'''
    _import('.command.pytest').api()


@_c.command()
def readme() -> None:
    '''Get code statistics with Tokei'''
    _import('.command.readme').api()


@_c.command()
def tokei() -> None:
    '''Build personal Tokei'''
    _import('.command.tokei').api()


@_c.command()
def uncache() -> None:
    '''Remove __pycache__ directories'''
    _import('.command.uncache').api()


@_c.command()
@_c.option('--sure', is_flag=True, prompt=True)
def upgrade(sure: bool) -> None:
    '''Bump semantic version (simple)'''
    _import('.command.upgrade').api(sure)
