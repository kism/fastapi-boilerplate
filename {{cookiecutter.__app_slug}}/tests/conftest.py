"""The conftest.py file serves as a means of providing fixtures for an entire directory.

Fixtures defined in a conftest.py can be used by any test in that package without needing to import them.
"""

import os
import shutil
from collections.abc import Callable

import pytest
import tomlkit
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner

from {{cookiecutter.__app_package}} import create_app

TEST_CONFIGS_LOCATION = os.path.join(os.getcwd(), "tests", "configs")


def pytest_configure():
    """This is a magic function for adding things to pytest?"""
    pytest.TEST_CONFIGS_LOCATION = TEST_CONFIGS_LOCATION


@pytest.fixture
def app(tmp_path, get_test_config):
    """This fixture uses the default config within the flask app."""
    return create_app(test_config=get_test_config("testing_true_valid.toml"), instance_path=tmp_path)


@pytest.fixture
def client(app):
    """This returns a test client for the default app()."""
    return app.test_client()


@pytest.fixture
def get_test_config():
    """Function returns a function, which is how it needs to be."""
    from . import testing_true_valid
    return testing_true_valid



@pytest.fixture
def place_test_config():
    """Fixture that places a config in the tmp_path.

    Returns: a function to place a config in the tmp_path.
    """

    def _place_test_config(config_name: str, path: str) -> None:
        """Place config in tmp_path by name."""
        filepath = os.path.join(TEST_CONFIGS_LOCATION, config_name)

        shutil.copyfile(filepath, os.path.join(path, "config.toml"))

    return _place_test_config
