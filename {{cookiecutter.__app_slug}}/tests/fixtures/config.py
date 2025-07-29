import shutil
from collections.abc import Callable
from pathlib import Path

import pytest

from {{cookiecutter.__app_package}}.config import {{cookiecutter.__app_camel_case}}Config
from tests.constants import TEST_CONFIGS_LOCATION


@pytest.fixture
def get_test_config(tmp_path: Path, place_test_config: Callable[[str, Path], None]) -> Callable[[str], {{cookiecutter.__app_camel_case}}Config]:
    """Function returns a function, which is how it needs to be."""

    def _get_test_config(config_name) -> {{cookiecutter.__app_camel_case}}Config:
        place_test_config(config_name, tmp_path)
        return {{cookiecutter.__app_camel_case}}Config.load_config(Path(tmp_path) / "config.toml")

    return _get_test_config


@pytest.fixture
def place_test_config() -> Callable[[str, Path], None]:
    """Fixture that places a config in the tmp_path.

    Returns: a function to place a config in the tmp_path.
    """

    def _place_test_config(config_name: str, path: str) -> None:
        """Place config in tmp_path by name."""
        filepath = TEST_CONFIGS_LOCATION / config_name
        config_path = Path(path) / "config.toml"
        shutil.copyfile(filepath, config_path)

    return _place_test_config
