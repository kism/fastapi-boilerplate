"""Test versioning."""

import tomlkit

import {{cookiecutter.__app_package}}


def test_version():
    """Test version variable."""
    with open("pyproject.toml", "rb") as f:
        pyproject_toml = tomlkit.load(f)
    assert pyproject_toml["project"]["version"] == {{cookiecutter.__app_package}}.__version__
