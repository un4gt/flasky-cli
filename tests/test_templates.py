import pytest
from click.testing import CliRunner

from flask_cli.cli.main import main
from flask_cli.templates.domain import Template


def test_list_templates():
    runner = CliRunner()
    result = runner.invoke(main, ["templates", "list"])
    assert result.exit_code == 0
    assert result.output == "cookiecutter-Flask-Foundation\ncookiecutter-flask\ncookiecutter-flask-minimal" \
                            "\ncookiecutter-flask-skeleton\n"


@pytest.mark.parametrize(
    "source,expected_tag",
    [
        ["~/projects/github/flask-api", ""],
        ["~/projects/github/flask-api$v2", "v2"],
        ["https://github.com/xxxx/xxxxxxx", ""],
        ["https://github.com/xxxxxxx/xxxxxxx$", ""],
        ["https://github.com/xxxxxxxxxx/xxxxx$v2", "v2"],
    ],
)
def test_template_source_tag(source, expected_tag):
    template = Template("test", source)
    assert template.tag == expected_tag
