from pathlib import Path

import pytest

from flask.testing import FlaskClient

from {{cookiecutter.__app_package}} import create_app
from {{cookiecutter.__app_package}}.flask_helpers import Flask{{cookiecutter.__app_camel_case}}

@pytest.fixture
def app(tmp_path: Path, get_test_config) -> Flask{{cookiecutter.__app_camel_case}}:
    """This fixture uses the default config within the flask app."""
    return create_app(test_config=get_test_config("testing_true_valid.toml"), instance_path=str(tmp_path))


@pytest.fixture
def client(app: Flask{{cookiecutter.__app_camel_case}}) -> FlaskClient:
    """This returns a test client for the default app()."""
    return app.test_client()
