import pathlib as p
import subprocess
import typing as t

if t.TYPE_CHECKING:
    from github.Repository import Repository


class Cache:
    def __init__(self, directory: t.Union[str, p.Path]) -> None:
        self._directory = p.Path(directory)
        self._mkdir(self._directory)

    def clone(self, repo: 'Repository') -> None:
        path = self._directory / repo.owner.login / repo.name
        if path.exists():
            cp = self._run('git', 'pull', cwd=path)
        else:
            self._mkdir(path.parent)
            cp = self._run('git', 'clone', repo.clone_url, path.as_posix())
        assert cp.returncode==0, cp.stderr.decode()

    def tokei(self) -> str:
        '''
        Reference:
            - https://github.com/XAMPPRocky/tokei
        '''
        cp = self._run('tokei')
        return cp.stdout.decode()

    def _run(self, *args: str, cwd: t.Optional[p.Path] = None) -> subprocess.CompletedProcess:
        cwd = cwd or self._directory
        return subprocess.run(args, cwd=cwd.as_posix(), capture_output=True)

    def _mkdir(self, path: p.Path) -> None:
        path.mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    import json
    import sys
    from github.MainClass import Github

    root = p.Path(__file__).absolute().parent
    cache = Cache(root/'cache')
    config = json.loads((root/'config'/'github.private.json').read_text())
    iydon = Github(config['access_token']).get_user()

    exclude_repos, exclude_users = config['exclude']['repos'], config['exclude']['users']
    include_repos, include_users = config['include']['repos'], config['include']['users']
    repos = list(iydon.get_repos())
    for ith, repo in enumerate(repos):
        if (
            (exclude_repos is None or repo.full_name not in exclude_repos) and
            (exclude_users is None or repo.owner.login not in exclude_users) and
            (include_repos is None or repo.full_name in include_repos) and
            (include_users is None or repo.owner.login in include_users)
        ):
            print(f'[{ith+1}/{len(repos)}]', repo.full_name, file=sys.stderr)
            cache.clone(repo)
    print(cache.tokei(), file=sys.stdout)
