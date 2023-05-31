import pathlib as p


ROOT = p.Path(__file__).absolute().parents[1]
CACHE = ROOT / '.cache'
SCRIPT = ROOT / 'script'
PYPROJECT = ROOT / 'pyproject.toml'
STATIC = SCRIPT / 'static'

CARGO = 'cargo'
GIT = 'git'
POETRY = 'poetry'

PYTHON = f'{POETRY} run python'
MKDOCS = f'{PYTHON} -m mkdocs'
MYPY = f'{PYTHON} -m mypy'
NOX = f'{PYTHON} -m nox'
PYTEST = f'{PYTHON} -m pytest'
