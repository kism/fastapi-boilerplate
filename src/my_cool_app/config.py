"""Config loading, validating, writing."""

from pathlib import Path  # ruff: ignore[typing-only-standard-library-import] # Cannot be put in type checking block due to pydantic
from typing import Self

from pydantic import BaseModel, Field, model_validator

from .utils.logger import get_logger

# Logging should be all done at INFO level or higher as the log level hasn't been set yet
logger = get_logger(__name__)

CONFIG_FILE_NAME = "config.json"


class AppConf(BaseModel):
    """Application configuration definition."""

    my_message: str = "Hello, World!"

    @model_validator(mode="after")
    def my_message_not_empty(self) -> Self:
        """Validate the configuration."""
        if not self.my_message:
            msg = "AppConf: my_message cannot be empty"
            raise ValueError(msg)
        return self


class LoggingConf(BaseModel):
    """Logging configuration definition."""

    level: str = "INFO"
    path: Path | None = None


class Config(BaseModel):
    """Settings loaded from a JSON file in the instance directory."""

    app: AppConf = Field(default_factory=AppConf)
    logging: LoggingConf = Field(default_factory=LoggingConf)

    @classmethod
    def load(cls, instance_path: Path) -> Self:
        """Load the config from the instance directory, writing it back with any missing defaults filled in."""
        config_path = instance_path / CONFIG_FILE_NAME
        config = cls.model_validate_json(config_path.read_text()) if config_path.is_file() else cls()

        # ponytail: no backup of the old file, git/your backups can have that job
        instance_path.mkdir(parents=True, exist_ok=True)
        config_path.write_text(config.model_dump_json(indent=2) + "\n")
        logger.info("Config loaded from and written to: %s", config_path)

        return config
