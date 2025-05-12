"""Flask helpers for {{cookiecutter.__app_camel_case}}."""
from pathlib import Path
from typing import Any, cast

from flask import Flask, current_app

from .config import {{cookiecutter.__app_camel_case}}Config


class Flask{{cookiecutter.__app_camel_case}}(Flask):
    """Extend flask to add out config object to the app object."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Extend flask to add out config object to the app object."""
        super().__init__(*args, **kwargs)
        self.{{cookiecutter.__app_config_var}} = {{cookiecutter.__app_camel_case}}Config(instance_path=Path(self.instance_path))


def get_current_app() -> Flask{{cookiecutter.__app_camel_case}}:
    """Get the current app object."""
    return cast("Flask{{cookiecutter.__app_camel_case}}", current_app)
