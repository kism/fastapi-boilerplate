"""Tests config loading and writing."""

import json
from typing import TYPE_CHECKING

import pytest
from pydantic import ValidationError

from my_cool_app.config import CONFIG_FILE_NAME, Config

if TYPE_CHECKING:
    from pathlib import Path


def test_load_missing_config(tmp_path: Path) -> None:
    """TEST: A missing config file results in defaults, written out to the instance directory."""
    config = Config.load(tmp_path)
    assert config.app.my_message == "Hello, World!"

    config_path = tmp_path / CONFIG_FILE_NAME
    assert config_path.is_file()
    assert json.loads(config_path.read_text())["app"]["my_message"] == "Hello, World!"


def test_load_existing_config(tmp_path: Path) -> None:
    """TEST: An existing config file is loaded, missing fields are filled in and written back."""
    config_path = tmp_path / CONFIG_FILE_NAME
    config_path.write_text('{"app": {"my_message": "Hello, PyTest!"}}')

    config = Config.load(tmp_path)
    assert config.app.my_message == "Hello, PyTest!"
    assert json.loads(config_path.read_text())["logging"]["level"] == "INFO"


def test_invalid_message(tmp_path: Path) -> None:
    """TEST: An empty message fails validation."""
    (tmp_path / CONFIG_FILE_NAME).write_text('{"app": {"my_message": ""}}')

    with pytest.raises(ValidationError, match="my_message cannot be empty"):
        Config.load(tmp_path)
