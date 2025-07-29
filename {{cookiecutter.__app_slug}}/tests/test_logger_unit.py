"""Logger unit tests."""

import logging
from collections.abc import Generator
from pathlib import Path

import pytest
from pydantic import BaseModel, ConfigDict
from pytest_mock import MockerFixture

from {{cookiecutter.__app_package}}.flask_helpers import Flask{{cookiecutter.__app_camel_case}}
from {{cookiecutter.__app_package}}.logger import CustomLogger, _add_file_handler, _set_log_level, setup_logger


class BaseLoggingConfig(BaseModel):
    """Configuration for logging tests."""

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
    )

    log_level: str
    log_path: Path | str
    in_loggers: list[logging.Logger | CustomLogger]
    include_root_logger: bool = False

@pytest.fixture
def logger() -> Generator[logging.Logger]:
    """Logger to use in unit tests, including cleanup."""
    logger = logging.getLogger("TEST_LOGGER")

    assert len(logger.handlers) == 0  # Check the logger has no handlers

    yield logger

    # Reset the test object since it will persist.
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()


def test_logging_permissions_error(logger: CustomLogger, tmp_path: Path, mocker: MockerFixture) -> None:
    """Test logging, mock a permission error."""
    mock_open_func = mocker.mock_open(read_data="")
    mock_open_func.side_effect = PermissionError("Permission denied")

    mocker.patch("builtins.open", mock_open_func)

    # TEST: That a permissions error is raised when open() results in a permissions error.
    with pytest.raises(PermissionError):
        _add_file_handler(logger, tmp_path)


def test_config_logging_to_dir(logger: logging.Logger, tmp_path: Path) -> None:
    """TEST: Correct exception is caught when you try log to a folder."""


    with pytest.raises(IsADirectoryError):
        _add_file_handler(logger, tmp_path)


def test_handler_console_added(logger: logging.Logger, app: Flask{{cookiecutter.__app_camel_case}}) -> None:
    """Test logging console handler."""
    logging_conf = BaseLoggingConfig(
        log_level="INFO",
        log_path="",
        in_loggers=[logger],
        include_root_logger=False,
    )

    setup_logger(**logging_conf.model_dump())
    assert len(logger.handlers) == 1

    # TEST: Still only one handler
    setup_logger(**logging_conf.model_dump())
    assert len(logger.handlers) == 1


def test_handler_file_added(logger: logging.Logger, tmp_path: Path, app: Flask{{cookiecutter.__app_camel_case}}) -> None:
    """Test logging file handler."""
    logging_conf = BaseLoggingConfig(
        log_level="INFO",
        log_path="",
        in_loggers=[logger],
        include_root_logger=False,
    )

    setup_logger(**logging_conf.model_dump())
    assert len(logger.handlers) == 2  # noqa: PLR2004 A console and a file handler are expected

    # TEST: Still two handlers
    setup_logger(**logging_conf.model_dump())
    assert len(logger.handlers) == 2  # noqa: PLR2004 A console and a file handler are expected


@pytest.mark.parametrize(
    ("log_level_in", "log_level_expected"),
    [
        (50, 50),
        ("INFO", 20),
        ("WARNING", 30),
        ("INVALID", 20),
    ],
)
def test_set_log_level(log_level_in: str | int, log_level_expected: int, logger: logging.Logger) -> None:
    """Test if _set_log_level results in correct log_level."""

    _set_log_level(logger, log_level_in)
    assert logger.getEffectiveLevel() == log_level_expected


def test_no_loggers_supplied() -> None:
    """Test if no loggers supplied, root logger is used."""
    # This is just for coverage
    setup_logger(include_root_logger=False)
