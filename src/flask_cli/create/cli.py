from typing import Optional

from cookiecutter.main import cookiecutter

from flask_cli.common import click
from flask_cli.templates.cli import get_template_by_name, prompt_template


def print_instructions(destination: str):
    from rich.console import Console

    console = Console()

    console.rule()
    console.print(f"[bold green]🏗️  Project created in {destination}")
    console.rule()
    console.print("-- Let's get flasky! --")


@click.command(name="create")
@click.option(
    "--template",
    "-t",
    help="Project template name.",
    required=False,
)
def create_project(
        template: Optional[str] = None,
):
    """
    Create a new project, with the given NAME, from a template.

    Examples:

        flask-cli create my-proj

        flask-cli create my-proj --template <template_name>
    """

    if template:
        template_obj = get_template_by_name(template)
    else:
        template_obj = prompt_template()

    destination = cookiecutter(template_obj.source)

    print_instructions(destination)
