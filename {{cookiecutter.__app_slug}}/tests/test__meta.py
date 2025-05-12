"""Test versioning."""

from pathlib import Path

import tomlkit

import {{cookiecutter.__app_package}}


def test_version():
    """Test version variable."""
    with Path("pyproject.toml").open("rb") as f:
        pyproject_toml = tomlkit.load(f)
    assert pyproject_toml["project"]["version"] == {{cookiecutter.__app_package}}.__version__
