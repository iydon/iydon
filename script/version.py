import pathlib as p
import re
import time


root = p.Path(__file__).absolute().parents[1]
path = root / 'pyproject.toml'
pattern = re.compile(r'(?<=version = ")(\d{4}\.\d{1,2})(?=")')
now = time.localtime()
version = f'{now.tm_year}.{now.tm_mon}'
path.write_text(pattern.sub(version, path.read_text()))
