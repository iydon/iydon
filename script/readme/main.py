import json
import pathlib as p
import subprocess
import typing as t

import tqdm

from github.MainClass import Github


root = p.Path(__file__).absolute().parent
Config = t.TypedDict(
    'Config',
    exclude=t.TypedDict('exclude', repos=t.List[str], users=t.List[str]),
    include=t.TypedDict('include', repos=t.List[str], users=t.List[str]),
    access_token=str,
)
Path = t.Union[str, p.Path]


def loads(*paths: Path) -> Config:
    for path in map(p.Path, paths):
        if path.exists():
            return Config(json.loads(path.read_text()))
    raise FileNotFoundError

def mkdir(path: Path) -> p.Path:
    directory = p.Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory

def run(*args: str, cwd: t.Optional[Path] = None) -> str:
    path = None if cwd is None else p.Path(cwd).as_posix()
    cp = subprocess.run(args, cwd=path, capture_output=True)
    assert cp.returncode==0, cp.stderr.decode()
    return cp.stdout.decode()


if __name__ == '__main__':
    directory = mkdir(root/'cache')
    config = loads(root/'config/github.private.json', root/'config/github.public.json')
    tokei = (root/'tokei/target/release/tokei').as_posix()
    template = (root/'config/readme.template.md').read_text()
    readme = root.parents[1] / 'README.md'

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
                run('git', 'pull', cwd=path)
            else:
                mkdir(path.parent)
                run('git', 'clone', repo.clone_url, path.as_posix())
    readme.write_text(template.format(
        tokei=run(tokei, '--num-format', 'commas', cwd=directory).strip(),
    ))
