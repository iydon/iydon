'''Remove __pycache__ directories

Code:
    >>> list(map(__import__('shutil').rmtree, __import__('pathlib').Path('.').rglob('__pycache__')))
'''


import pathlib as p
import shutil


root = p.Path(__file__).absolute().parents[1]
for path in root.rglob('__pycache__'):
    shutil.rmtree(path.as_posix())
