"""Logger unit tests."""

import logging

import pytest

import {{cookiecutter.__app_package}}.logger


@pytest.fixture
def logger():
    """Logger to use in unit tests, including cleanup."""
    logger = logging.getLogger("TEST_LOGGER")

    assert len(logger.handlers) == 0  # Check the logger has no handlers

    yield logger

    # Reset the test object since it will persist.
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()


def test_logging_permissions_error(logger, tmp_path, mocker):
    """Test logging, mock a permission error."""
    from {{cookiecutter.__app_package}}.logger import _add_file_handler

    mock_open_func = mocker.mock_open(read_data="")
    mock_open_func.side_effect = PermissionError("Permission denied")

    mocker.patch("builtins.open", mock_open_func)

    # TEST: That a permissions error is raised when open() results in a permissions error.
    with pytest.raises(PermissionError):
        _add_file_handler(logger, str(tmp_path))


def test_config_logging_to_dir(logger, tmp_path):
    """TEST: Correct exception is caught when you try log to a folder."""
    from {{cookiecutter.__app_package}}.logger import _add_file_handler

    with pytest.raises(IsADirectoryError):
        _add_file_handler(logger, tmp_path)


def test_handler_console_added(logger, app):
    """Test logging console handler."""
    logging_conf = {"log_level": "INFO", "log_path": "", "in_loggers": [logger]}

    # TEST: Only one handler (console), should exist when no logging path provided
    {{cookiecutter.__app_package}}.logger.setup_logger(**logging_conf)
    assert len(logger.handlers) == 1

    # TEST: If a console handler exists, another one shouldn't be created
    {{cookiecutter.__app_package}}.logger.setup_logger(**logging_conf)
    assert len(logger.handlers) == 1


def test_handler_file_added(logger, tmp_path, app):
    """Test logging file handler."""
    logging_conf = {"log_level": "INFO", "log_path": tmp_path / "test.log", "in_loggers": [logger]}

    # TEST: Two handlers when logging to file expected
    {{cookiecutter.__app_package}}.logger.setup_logger(**logging_conf)
    assert len(logger.handlers) == 2  # noqa: PLR2004 A console and a file handler are expected

    # TEST: Two handlers when logging to file expected, another one shouldn't be created
    {{cookiecutter.__app_package}}.logger.setup_logger(**logging_conf)
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
def test_set_log_level(log_level_in: str | int, log_level_expected: int, logger):
    """Test if _set_log_level results in correct log_level."""
    from {{cookiecutter.__app_package}}.logger import _set_log_level

    # TEST: Logger ends up with correct values
    _set_log_level(logger, log_level_in)
    assert logger.getEffectiveLevel() == log_level_expected
