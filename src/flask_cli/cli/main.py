from flask_cli.common import click
from flask_cli.create.cli import create_project
from flask_cli.templates.cli import templates


@click.group()
def main():
    """
    🛠️   CLI to start Flask projects
    """


main.add_command(create_project)
main.add_command(templates)
