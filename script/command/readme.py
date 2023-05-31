import json
import pathlib as p
import typing as t

import tqdm

from github.MainClass import Github

from ..config import CACHE, ROOT, STATIC
from ..stub import _import
from ..util import mkdir, pure, run


Config = t.TypedDict(
    'Config',
    exclude=t.TypedDict('exclude', repos=t.List[str], users=t.List[str]),
    include=t.TypedDict('include', repos=t.List[str], users=t.List[str]),
    access_token=str,
)


def loads(*paths: p.Path) -> Config:
    for path in paths:
        if path.exists():
            return Config(json.loads(path.read_text()))
    raise FileNotFoundError


def api() -> None:
    tokei = _import('.command.tokei').api()
    directory = CACHE / 'github'
    config = loads(STATIC/'github.private.json', STATIC/'github.public.json')
    template = (STATIC / 'readme.template.md').read_text()
    readme = ROOT / 'README.md'

    exclude, include = config.get('exclude', {}), config.get('include', {})
    exclude_repos, exclude_users = exclude.get('repos', None), exclude.get('users', None)
    include_repos, include_users = include.get('repos', None), include.get('users', None)
    iydon = Github(config['access_token']).get_user()
    repos = iydon.get_repos()
    for repo in tqdm.tqdm(repos, total=repos.totalCount):
        if (
            (exclude_repos is None or repo.full_name not in exclude_repos) and
            (exclude_users is None or repo.owner.login not in exclude_users) and
            (include_repos is None or repo.full_name in include_repos) and
            (include_users is None or repo.owner.login in include_users)
        ):
            path = directory / repo.owner.login / repo.name
            if path.exists():
                run('git pull', capture_output=True, cwd=path)
            else:
                mkdir(path.parent)
                run(f'git clone {repo.clone_url} {path}', capture_output=True)
    cp = pure(f'{tokei} --num-format commas', capture_output=True, cwd=directory)
    readme.write_text(template.format(tokei=cp.stdout.decode().strip()))
