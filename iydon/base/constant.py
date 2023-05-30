__all__ = ['author', 'description', 'license', 'root', 'url', 'version']


import pathlib as p


author = 'Iydon Liang'
description = 'Iydon\'s common tools'
license = 'GPL-3.0-only'  # SPDX short identifier
root = p.Path(__file__).absolute().parents[1]
url = 'https://github.com/iydon/iydon'
version = '2023.0'
