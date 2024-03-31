from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from click import ClickException


@dataclass
class Template:
    id: str
    source: str
    description: str = ""
    tag: str = ""
    folder: Optional[str] = None

    def __post_init__(self):
        if "$" in self.source:
            tag = self.source.split("$")[-1]
            self.tag = tag
            self.source = self.source[: -(len(tag) + 1)]


class TemplateError(ClickException):
    """Base class for templates errors."""


class TemplateNotFoundError(TemplateError):
    """Exception raised when a template is not found."""

    def __init__(self, name: str) -> None:
        super().__init__(f"The template with name '{name}' could not be found.")


class TemplateConflictError(TemplateError):
    """Exception raised when a template is already configured."""

    def __init__(self, name: str) -> None:
        super().__init__(f"A template with name '{name}' is already configured.")


class TemplatesDataProvider(ABC):
    @abstractmethod
    def add_template(self, template: Template):
        ...

    @abstractmethod
    def update_template(self, template: Template):
        ...

    @abstractmethod
    def remove_template(self, template: str):
        ...

    @abstractmethod
    def get_templates(self) -> List[Template]:
        ...


def _get_default_data_provider() -> TemplatesDataProvider:
    from flask_cli.templates.data.default import JSONTemplatesDataProvider

    return JSONTemplatesDataProvider()


class TemplatesManager:
    def __init__(self, provider: Optional[TemplatesDataProvider] = None) -> None:
        self._provider = provider or _get_default_data_provider()

    def add_template(
            self,
            name: str,
            source: str,
            folder: Optional[str],
            description: str,
            force: bool,
    ):
        try:
            self.get_template_by_name(name)
        except TemplateNotFoundError:
            # good
            self._provider.add_template(
                Template(name, source, description, folder=folder)
            )
        else:
            if force:
                self._provider.update_template(
                    Template(name, source, description, folder=folder)
                )
            else:
                raise TemplateConflictError(name)

    def remove_template(self, name: str):
        self._provider.remove_template(name)

    def get_template_by_name(self, name: str) -> Template:
        template = next(
            (item for item in self.get_templates() if item.id == name), None
        )

        if template is None:
            raise TemplateNotFoundError(name)

        return template

    def get_templates(self) -> Iterable[Template]:
        yield from self._provider.get_templates()

    def get_templates_dict(self) -> Dict[str, Template]:
        return {template.id: template for template in self.get_templates()}
