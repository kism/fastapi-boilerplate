"""Config loading, setup, validating, writing."""

import datetime
import json
from pathlib import Path
from typing import Self

import tomlkit
from pydantic import BaseModel, ConfigDict, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import get_logger

# Logging should be all done at INFO level or higher as the log level hasn't been set yet
# Modules should all setup logging like this so the log messages include the modules name.
logger = get_logger(__name__)


class FlaskConfDef(BaseModel):
    """Flask configuration definition."""

    model_config = ConfigDict(extra="allow") # Ok for config, will be dropped when saved

    DEBUG: bool = False
    TESTING: bool = False


class AppConfDef(BaseModel):
    """Application configuration definition."""

    model_config = ConfigDict(extra="allow") # Ok for config, will be dropped when saved

    my_message: str = "Hello, World!"

    @model_validator(mode="after")
    def my_message_not_empty(self) -> Self:
        """Validate the configuration."""
        if self.my_message == "":
            msg = "AppConfDef: my_message cannot be empty"
            raise ValueError(msg)
        return self


class LoggingConfDef(BaseModel):
    """Logging configuration definition."""

    model_config = ConfigDict(extra="allow") # Ok for config, will be dropped when saved

    level: str = "INFO"
    path: Path | str = ""


class {{cookiecutter.__app_camel_case}}Config(BaseSettings):
    """Settings loaded from a TOML file."""

    model_config = SettingsConfigDict(extra="allow") # Ok for config, will be dropped when saved

    # Default values for our settings
    app: AppConfDef = AppConfDef()
    flask: FlaskConfDef = FlaskConfDef()
    logging: LoggingConfDef = LoggingConfDef()
    top_level_field_for_a_laugh: str = "This is a top level field"

    def write_config(self, config_location: Path) -> None:
        """Write the current settings to a TOML file."""
        from . import PROGRAM_NAME, URL, __version__

        config_location.parent.mkdir(parents=True, exist_ok=True)

        config_data = json.loads(self.model_dump_json())  # This is how we make the object safe for tomlkit
        if not config_location.exists():
            logger.warning("Config file does not exist, creating it at %s", config_location)
            config_location.touch()
            existing_data = config_data
        else:
            with config_location.open("r") as f:
                existing_data = tomlkit.load(f)

        logger.info("Writing config to %s", config_location)

        new_file_content_str = f"# Configuration file for {PROGRAM_NAME} v{__version__} {URL}\n"
        new_file_content_str += tomlkit.dumps(config_data)

        if existing_data != config_data:  # The new object will be valid, so we back up the old one
            local_tz = datetime.datetime.now().astimezone().tzinfo
            time_str = datetime.datetime.now(tz=local_tz).strftime("%Y-%m-%d_%H%M%S")
            backup_file = config_location.parent / f"{config_location.stem}_{time_str}{config_location.suffix}.bak"
            logger.warning("Validation has changed the config file, backing up the old one to %s", backup_file)
            with backup_file.open("w") as f:
                f.write(tomlkit.dumps(existing_data))

        with config_location.open("w") as f:
            f.write(new_file_content_str)

    @classmethod
    def load_config(cls, config_path: Path) -> Self:
        """Load the configuration file."""
        if not config_path.exists():
            return cls()

        with config_path.open("r") as f:
            config = tomlkit.load(f)

        return cls(**config)
