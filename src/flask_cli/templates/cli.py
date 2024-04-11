import questionary

from flask_cli.common import click
from flask_cli.templates.exception import (
    TemplateNotFoundError,
)
from flask_cli.templates.templates import TEMPLATES


@click.group()
def templates():
    """
    Commands to handle templates.
    """


def _display_source_details(template_source: str):
    from rich.text import Text

    text = Text(template_source)
    return text


@click.command(name="details")
def describe_templates():
    """
    Display details about the configured templates.
    """
    from rich.console import Console
    from rich.table import Table

    table = Table()
    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Source", style="magenta")
    table.add_column("Description", justify="left", style="green")

    for template_id in TEMPLATES:
        current_template = TEMPLATES[template_id]
        table.add_row(
            template_id, _display_source_details(current_template['source']), current_template["description"]
        )

    console = Console()
    console.print(table)


@click.command(name="list")
@click.option("--source", "-s", is_flag=True, help="Include the source in the output.")
def list_templates(source: bool):
    """
    Lists all available templates.
    """
    for template_id in TEMPLATES:
        click.echo(f"{template_id}")


def prompt_template() -> dict[str, str]:
    """
    Prompts the user to select one of the available templates.
    """

    chosen_name = questionary.select(
        "Project template:",
        choices=[template_id for template_id in TEMPLATES],
        qmark="🚀",
    ).unsafe_ask()

    return TEMPLATES[chosen_name]


def get_template_by_name(name) -> dict[str, str] | TemplateNotFoundError:
    for template_id in TEMPLATES:
        if template_id == name:
            return TEMPLATES[template_id]

    raise TemplateNotFoundError(name)


templates.add_command(list_templates)
templates.add_command(describe_templates)
