"""Config loading, setup, validating, writing."""

import json
from pathlib import Path
from typing import Self

import tomlkit
from pydantic import BaseModel, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import get_logger

# Logging should be all done at INFO level or higher as the log level hasn't been set yet
# Modules should all setup logging like this so the log messages include the modules name.
logger = get_logger(__name__)


class FlaskConfDef(BaseModel):
    """Flask configuration definition."""

    DEBUG: bool = False
    TESTING: bool = False


class AppConfDef(BaseModel):
    """Application configuration definition."""

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

    level: str = "INFO"
    path: Path | str = ""


class {{cookiecutter.__app_camel_case}}Config(BaseSettings):
    """Settings loaded from a TOML file."""

    # Default values for our settings
    app: AppConfDef = AppConfDef()
    flask: FlaskConfDef = FlaskConfDef()
    logging: LoggingConfDef = LoggingConfDef()
    top_level_field_for_a_laugh: str = "This is a top level field"

    # Custom path for the config file
    config_path: Path = Path()

    # Configure settings class
    model_config = SettingsConfigDict(
        env_prefix="APP_",  # environment variables with APP_ prefix will override settings
        env_nested_delimiter="__",  # APP_NESTED__NESTED_FIELD=value
        json_encoders={Path: str},
    )

    def __init__(self, instance_path: Path) -> None:
        """Initialize settings and load from a TOML file if provided.

        Args:
            instance_path (str): Path to load config.toml
        """
        # Initialize with default values first
        super().__init__()

        self.config_path = Path(instance_path / "config.toml")
        self._load_from_toml()
        self.write_config()

    def _load_from_toml(self) -> None:
        """Load settings from the TOML file specified in config_path."""
        if self.config_path.is_file():
            with self.config_path.open("r") as f:
                config_data = tomlkit.load(f)

            # Update our settings from the loaded data
            for key, value in config_data.items():
                if key == "flask" and isinstance(value, dict):
                    self.flask = FlaskConfDef(**value)
                elif key == "app" and isinstance(value, dict):
                    self.app = AppConfDef(**value)
                elif key == "logging" and isinstance(value, dict):
                    self.logging = LoggingConfDef(**value)
                elif hasattr(self, key):
                    setattr(self, key, value)

    def write_config(self) -> None:
        """Write the current settings to a TOML file."""
        logger.info("Writing config to %s", self.config_path)
        config_data = json.loads(self.model_dump_json())  # This is how we make the object safe for tomlkit
        config_data.pop("config_path", None)  # Remove config_path from the data to be written

        # Write to the TOML file
        if not self.config_path.parent.exists():
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with self.config_path.open("w") as f:
            tomlkit.dump(config_data, f)
