from flask_cli.common import click
from json import dumps
from typing import Optional

import questionary

from flask_cli.common import click
from flask_cli.templates.domain import (
    Template,
    TemplateNotFoundError,
    TemplatesManager,
)


def pretty(data):
    return dumps(data, ensure_ascii=False, indent=4)


@click.group()
def templates():
    """
    Commands to handle templates.
    """


def _display_source_details(template: Template):
    from rich.text import Text

    text = Text(template.source)

    if template.tag:
        text.append(f"\ntag: {template.tag}", style="yellow")
    if template.folder:
        text.append(f"\nfolder: {template.folder}", style="yellow")
    return text


@click.command(name="details")
def describe_templates():
    """
    Display details about the configured templates.
    """
    from rich.console import Console
    from rich.table import Table

    manager = TemplatesManager()
    templates = manager.get_templates()

    table = Table()
    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Source", style="magenta")
    table.add_column("Description", justify="left", style="green")

    for template in templates:
        table.add_row(
            template.id, _display_source_details(template), template.description
        )

    console = Console()
    console.print(table)


@click.command(name="list")
@click.option("--source", "-s", is_flag=True, help="Include the source in the output.")
def list_templates(source: bool):
    """
    Lists all available templates.
    """
    manager = TemplatesManager()
    templates = manager.get_templates()

    for template in templates:
        if source:
            click.echo(f"{template.id}\t{template.source}")
        else:
            click.echo(f"{template.id}")


@click.command(name="add")
@click.argument("name")
@click.argument("source")
@click.argument("folder", required=False)
@click.option(
    "-d",
    "--description",
    default="",
    show_default=True,
    help="Template description.",
)
@click.option("-f", "--force", is_flag=True, help="Force update if the template exists")
def add_template(
    name: str, source: str, folder: Optional[str], description: str, force: bool
):
    """
    Add a template, by name and source, with optional description. If a specific tag
    should be used for a Git repository, it can be specified at the end of the source,
    using an "@" sign. Example: 'https://github.com/xxxx/xxxxxx'

    This command fails if a template exists with the same name. To overwrite an existing
    template, use the -f, or --force flag. Templates can later be used to scaffold new
    projects.

    Examples:

    flask-cli templates add foo 'https://github.com/xxxx/xxxxxx'
        -d 'Some nice template! 🐃'

    flask-cli templates add foo2 'https://github.com/xxxx/xxxxxx$v2'
    """
    manager = TemplatesManager()
    manager.add_template(name, source, folder, description, force)


@click.command(name="remove")
@click.argument("name")
def remove_template(name: str):
    """
    Remove a template.
    """
    manager = TemplatesManager()
    manager.remove_template(name)


def prompt_template() -> Template:
    """
    Prompts the user to select one of the available templates.
    """
    manager = TemplatesManager()
    templates = manager.get_templates_dict()

    chosen_name = questionary.select(
        "Project template:",
        choices=[template.id for template in templates.values()],
        qmark="🚀",
    ).unsafe_ask()

    return templates[chosen_name]


def get_template_by_name(name) -> Template:
    manager = TemplatesManager()
    for template in manager.get_templates():
        if template.id == name:
            return template

    raise TemplateNotFoundError(name)


templates.add_command(list_templates)
templates.add_command(describe_templates)
templates.add_command(add_template)
templates.add_command(remove_template)
