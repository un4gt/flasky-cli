import pytest
from click.testing import CliRunner

from flask_cli.cli.main import main
from flask_cli.templates.exception import TemplateNotFoundError
from flask_cli.templates.cli import get_template_by_name
from flask_cli.templates.templates import TEMPLATES


def test_list_templates():
    # for flask-cli templates list
    runner = CliRunner()
    result = runner.invoke(main, ["templates", "list"])
    assert result.exit_code == 0
    result_output_lst = result.output.strip().split()
    assert len(result_output_lst) == 5
    assert result_output_lst[0] == "Flask-API"
    assert result_output_lst[-1] == "cookiecutter-flask-skeleton"


def test_templates_not_found():
    # for flask-cli create --template <template>
    runner = CliRunner()
    res = runner.invoke(main, ['create', '--template', 'not-found'])
    assert res.exit_code != 0


def test_get_template_by_name_exception():
    with pytest.raises(TemplateNotFoundError):
        get_template_by_name("qwer")


def test_get_template_by_name():
    template = get_template_by_name('cookiecutter-flask')
    assert template == TEMPLATES['cookiecutter-flask']
