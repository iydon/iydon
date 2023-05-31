import click

from . import stub


@click.group()
def cli() -> None:
    pass


for name in dir(stub):
    if not name.startswith('_'):
        attr = getattr(stub, name)
        if isinstance(attr, click.Command):
            cli.add_command(attr)


if __name__ == '__main__':
    cli()
