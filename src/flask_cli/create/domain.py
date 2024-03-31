import re
from typing import Optional

value_pattern = re.compile("^[a-zA-Z_]{1}[0-9a-zA-Z_]+$")


def validate_name(value: Optional[str]):
    if not value:
        raise ValueError("Missing value")
    if not value_pattern.match(value):
        raise ValueError("Invalid value")


class ProjectManager:
    def bootstrap(
        self,
        source: str,
        checkout: Optional[str] = None,
        folder: Optional[str] = None,
        data=None,
    ):
        # Lazy import, to not slow down the CLI start-up for every command
        from flask_cli.common.cookiemod import cookiecutter

        # https://cookiecutter.readthedocs.io/en/stable/advanced/calling_from_python.html

        cookiecutter(source, checkout=checkout, directory=folder, extra_context=data)
