"""Demo object."""

from .config import AppConfDef
from .logger import get_logger

logger = get_logger(__name__)


# KISM-BOILERPLATE: Demo object, doesn't do much
class MyCoolObject:
    """Demo object."""

    def __init__(self, {{cookiecutter.__app_config_var}}: AppConfDef) -> None:
        """Init MyCoolObject."""
        logger.debug("Creating MyCoolObject")
        logger.debug({{cookiecutter.__app_config_var}})
        self._my_message = {{cookiecutter.__app_config_var}}.my_message  # Already validated

    def get_my_message_backwards(self) -> str:
        """Return the string backwards."""
        return self._my_message[::-1]
