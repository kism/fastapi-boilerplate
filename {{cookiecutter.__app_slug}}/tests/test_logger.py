"""Test the logger of the app."""

import logging
from collections.abc import Callable
from pathlib import Path

import pytest
from flask import Flask

from {{cookiecutter.__app_package}} import create_app
from {{cookiecutter.__app_package}}.config import {{cookiecutter.__app_camel_case}}Config


def test_config_invalid_log_level(tmp_path: Path, get_test_config: Callable[[str], {{cookiecutter.__app_camel_case}}Config], caplog: pytest.LogCaptureFixture) -> None:
    """Test if logging to file works."""
    caplog.set_level(logging.WARNING)
    app = create_app(get_test_config("logging_invalid_log_level.toml"), instance_path=str(tmp_path))
    # TEST: App still starts
    assert isinstance(app, Flask)
    # TEST: Assert that the invalid logging level message gets logged
    assert "Invalid logging level" in caplog.text
