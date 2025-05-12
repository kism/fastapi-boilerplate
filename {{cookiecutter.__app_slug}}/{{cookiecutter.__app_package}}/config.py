"""Config loading, setup, validating, writing."""

from pathlib import Path
from typing import List, Optional


import tomlkit

import tomlkit

from .logger import get_logger


# Logging should be all done at INFO level or higher as the log level hasn't been set yet
# Modules should all setup logging like this so the log messages include the modules name.
logger = get_logger(__name__)


from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# Default config dictionary, also works as a schema
# DEFAULT_CONFIG: dict[str, dict] = {
#     "app": {
#         "my_message": "Hello, World!",
#     },
#     "logging": {
#         "level": "INFO",
#         "path": "",
#     },
#     "flask": {  # This section is for Flask default config entries https://flask.palletsprojects.com/en/3.0.x/config/
#         "DEBUG": False,
#         "TESTING": False,
#     },
# }


class TargetDef(BaseModel):
    """Target definition for the application."""

    type: str = "local"
    rsync_host: str = ""
    path: Path = Path.cwd() / "output"


class SystemDef(BaseModel):
    local_dir: Path = Path.cwd() / "input_system_one"
    remote_dir: Path = Path.cwd() / "output_system_one"
    region_list_include: list[str] = []
    region_list_exclude: list[str] = []
    special_list_include: list[str] = []
    special_list_exclude: list[str] = []


class Settings(BaseSettings):
    """Settings loaded from a TOML file."""

    # Default values for our settings
    target: TargetDef = TargetDef()
    systems: List[SystemDef] = [SystemDef()]

    # Custom path for the config file
    config_path: Optional[Path] = None

    # Configure settings class
    model_config = SettingsConfigDict(
        env_prefix="APP_",  # environment variables with APP_ prefix will override settings
        env_nested_delimiter="__",  # APP_NESTED__NESTED_FIELD=value
        json_encoders={Path: str},
    )

    def __init__(self, **kwargs):
        config_path = kwargs.pop("config_path", None)
        # Initialize with default values first
        super().__init__(**kwargs)

        # If a config_path is provided, load and override settings from that file
        if config_path:
            self.config_path = Path(config_path)
            self._load_from_toml()
            self.write_config()

    def _load_from_toml(self):
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

        # Load and parse the TOML file
        try:
            with open(self.config_path, "rb") as f:
                config_data = tomlkit.load(f)

            # Update our settings from the loaded data
            for key, value in config_data.items():
                if key == "target" and isinstance(value, dict):
                    # Handle target settings
                    self.target = TargetDef(**value)
                elif key == "systems" and isinstance(value, list):
                    # Handle systems settings
                    self.systems = [SystemDef(**system) for system in value]
                elif hasattr(self, key):
                    setattr(self, key, value)

        except Exception as e:
            # In a real application, you might want better error handling
            print(f"Error loading config from {self.config_path}: {e}")

    def write_config(self):
        """Write the current settings to a TOML file."""
        if not self.config_path:
            raise ValueError("No config path specified.")

        # Convert settings to a dictionary
        print(f"Writing config to {self.config_path}")
        config_data_str = self.model_dump_json()

        import json

        config_data = json.loads(config_data_str)
        config_data.pop("config_path", None)

        # Write to the TOML file
        with open(self.config_path, "w") as f:
            tomlkit.dump(config_data, f)
