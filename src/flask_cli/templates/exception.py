from click import ClickException


class TemplateError(ClickException):
    """Base class for templates errors."""


class TemplateNotFoundError(TemplateError):
    """Exception raised when a template is not found."""

    def __init__(self, name: str) -> None:
        super().__init__(f"The template with name '{name}' could not be found.")
