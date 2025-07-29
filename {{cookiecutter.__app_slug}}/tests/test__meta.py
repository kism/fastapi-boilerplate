from pathlib import Path

import tomlkit

import {{cookiecutter.__app_package}}


def test_version_pyproject() -> None:
    """Verify version in pyproject.toml matches package version."""
    pyproject_path = Path("pyproject.toml")
    with pyproject_path.open("rb") as f:
        pyproject_toml = tomlkit.load(f)
    assert pyproject_toml.get("project", {}).get("version") == {{cookiecutter.__app_package}}.version.__version__


def test_version_lock() -> None:
    """Verify version in uv.lock matches package version."""
    lock_path = Path("uv.lock")
    with lock_path.open() as f:
        uv_lock = tomlkit.load(f)

    found_version = False
    for package in uv_lock.get("package", []):
        if package["name"] == "{{cookiecutter.__app_package}}":
            assert package["version"] == {{cookiecutter.__app_package}}.version.__version__
            found_version = True
            break

    assert found_version, "{{cookiecutter.__app_package}} not found in uv.lock"
