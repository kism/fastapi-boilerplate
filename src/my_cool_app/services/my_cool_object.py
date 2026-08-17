"""Demo object."""

from typing import TYPE_CHECKING

from my_cool_app.utils.logger import get_logger

if TYPE_CHECKING:
    from my_cool_app.config import AppConf

logger = get_logger(__name__)


# KISM-BOILERPLATE: Demo object, doesn't do much
class MyCoolObject:
    """Demo object."""

    def __init__(self, app_conf: AppConf) -> None:
        """Init MyCoolObject."""
        logger.debug("Creating MyCoolObject with config: %s", app_conf)
        self._my_message = app_conf.my_message

    def get_my_message(self) -> str:
        """Return the message."""
        logger.trace("Getting message")
        return self._my_message

    def get_my_message_backwards(self) -> str:
        """Return the message backwards."""
        return self._my_message[::-1]
