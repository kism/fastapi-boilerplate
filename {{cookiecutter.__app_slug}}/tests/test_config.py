from collections.abc import Callable
from pathlib import Path

import pytest

from {{cookiecutter.__app_package}}.config import {{cookiecutter.__app_camel_case}}Config


def test_invalid_message(get_test_config: Callable[[str], {{cookiecutter.__app_camel_case}}Config]) -> None:
    """Test invalid message."""
    with pytest.raises(ValueError, match="AppConfDef: my_message cannot be empty"):
        get_test_config("config_app_message_invalid.toml")


def test_load_missing_config(tmp_path: Path) -> None:
    """Test loading a missing config file."""
    missing_config = Path(tmp_path) / "missing_config.toml"
    config = {{cookiecutter.__app_camel_case}}Config.load_config(missing_config)
    config.write_config(missing_config)
