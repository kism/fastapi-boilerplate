"""Config loading, setup, validating, writing."""

import json
from pathlib import Path

from typing import Optional

import tomlkit
from pydantic import BaseModel
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

    # Custom path for the config file
    config_path: Path | None = None

    # Configure settings class
    model_config = SettingsConfigDict(
        env_prefix="APP_",  # environment variables with APP_ prefix will override settings
        env_nested_delimiter="__",  # APP_NESTED__NESTED_FIELD=value
        json_encoders={Path: str},
    )

    def __init__(self, instance_path: Path) -> None:
        """Initialize settings and load from a TOML file if provided.

        Args:
            config_path (str): Path to the TOML configuration file.
        """
        # Initialize with default values first
        super().__init__()

        self.config_path = Path(instance_path / "config.toml")
        self._load_from_toml()
        self.write_config()

    def _load_from_toml(self) -> None:
        """Load settings from the TOML file specified in config_path."""
        if not self.config_path or not self.config_path.exists():
            # Try default locations if no specific path was provided or the path doesn't exist
            default_paths = [
                Path.cwd() / "config.toml",  # Current working directory
                Path(__file__).parent.parent / "config.toml",  # Project root
            ]

            for path in default_paths:
                if path.exists():
                    self.config_path = path
                    break
            else:
                # No config file found, keep using default values
                return

            with self.config_path.open("r") as f:
                config_data = tomlkit.load(f)

            # Update our settings from the loaded data
            for key, value in config_data.items():
                if key == "flask" and isinstance(value, dict):
                    self.target = FlaskConfDef(**value)
                elif key == "app" and isinstance(value, dict):
                    self.systems = [AppConfDef(**value)]
                elif key == "logging" and isinstance(value, dict):
                    self.logging = LoggingConfDef(**value)
                elif hasattr(self, key):
                    setattr(self, key, value)

    def write_config(self) -> None:
        """Write the current settings to a TOML file."""
        if not self.config_path:
            msg = "No config path specified."
            raise ValueError(msg)

        # Convert settings to a dictionary
        logger.info("Writing config to %s", self.config_path)
        config_data_str = self.model_dump_json()

        config_data = json.loads(config_data_str)
        config_data.pop("config_path", None)

        # Write to the TOML file
        if not self.config_path.parent.exists():
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, "w") as f:
            tomlkit.dump(config_data, f)
