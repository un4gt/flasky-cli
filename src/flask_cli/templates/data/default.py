"""
This module provides the default implementation of TemplatesDataProvider, which uses a
JSON file stored in a user's folder.
"""
import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import List, Union

from flask_cli.templates.domain import Template, TemplatesDataProvider


def _default_templates():
    return {
        "templates": [
            {
                "id": "cookiecutter-flask",
                "source": "https://github.com/cookiecutter-flask/cookiecutter-flask",
                "description": (
                    "A flask template with Bootstrap, asset bundling+minification with webpack,"
                    "starter templates, and registration/authentication. For use with cookiecutter."
                ),
            },
            {
                "id": "cookiecutter-Flask-Foundation",
                "source": "https://github.com/JackStouffer/cookiecutter-Flask-Foundation",
                "description": (
                    "Cookiecutter fork of Flask Foundation"
                ),
            },
            {
                "id": "cookiecutter-flask-minimal",
                "source": "https://github.com/candidtim/cookiecutter-flask-minimal",
                "description": (
                    "A minimalist's production-ready Flask project template."
                    "A micro template for a microframework."
                )
            },
            {
                "id": "cookiecutter-flask-skeleton",
                "source": "https://github.com/testdrivenio/cookiecutter-flask-skeleton",
                "description": (
                    "Flask Starter Project"
                )
            }
        ]
    }


class JSONTemplatesDataProvider(TemplatesDataProvider):
    """
    Default data provider for Templates, using a JSON file stored in a user's folder.
    """

    def __init__(self, file_path: Union[str, Path, None] = None) -> None:
        self._file_path = (
            Path(file_path)
            if file_path is not None
            else Path.home()
                 / ".flaskcli"
                 / os.environ.get("FLASKCLI_FOLDER", "flask-cli")
                 / "templates.json"
        )
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_default()

    def _ensure_default(self):
        if not self._file_path.exists():
            self._file_path.write_text(
                json.dumps(_default_templates(), indent=4, ensure_ascii=False),
                encoding="utf8",
            )

    def _get_settings(self):
        # NOTE: if a json.JSONDecodeError happens, maybe because the user edited the
        # settings file by hand, let the application crash, so the user can handle
        # the information and no information gets lost.
        try:
            with open(self._file_path, mode="rt", encoding="utf8") as source_file:
                return json.loads(source_file.read())
        except FileNotFoundError:
            return {}

    def _write_settings(self, data):
        with open(self._file_path, mode="wt", encoding="utf8") as source_file:
            return source_file.write(json.dumps(data, indent=4, ensure_ascii=False))

    def add_template(self, template: Template):
        data = self._get_settings()
        templates = data.get("templates", [])
        templates.append(asdict(template))
        data["templates"] = sorted(templates, key=lambda item: item["id"])
        self._write_settings(data)

    def update_template(self, template: Template):
        templates = self.get_templates()
        current = next((value for value in templates if value.id == template.id), None)
        if current:
            current.source = template.source
            current.tag = template.tag
            current.description = template.description
        else:
            current = template
        data = self._get_settings()
        values = [asdict(item) for item in templates]
        data["templates"] = sorted(values, key=lambda item: item["id"])
        self._write_settings(data)

    def remove_template(self, name: str):
        data = self._get_settings()
        templates = data.get("templates", [])
        data["templates"] = [item for item in templates if item["id"] != name]
        self._write_settings(data)

    def get_templates(self) -> List[Template]:
        data = self._get_settings()
        try:
            templates = data["templates"]
        except KeyError:
            return []
        return [
            Template(
                item["id"],
                item["source"],
                item.get("description", ""),
                item.get("tag", ""),
                folder=item.get("folder"),
            )
            for item in sorted(templates, key=lambda item: item["id"])
        ]
