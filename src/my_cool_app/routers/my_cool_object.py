"""Router for the demo object."""

from typing import TYPE_CHECKING

from fastapi import APIRouter, Request
from pydantic import BaseModel

from my_cool_app.utils.logger import get_logger

if TYPE_CHECKING:
    from my_cool_app.services import MyCoolObject

logger = get_logger(__name__)  # Logger named my_cool_app.routers.my_cool_object, config inherited from the root logger

router = APIRouter(tags=["my_cool_object"])


class MessageResponse(BaseModel):
    """Response model, FastAPI turns this into the json response and the OpenAPI docs."""

    msg: str


def _get_my_cool_object(request: Request) -> MyCoolObject:
    """Get the app's MyCoolObject, set in create_app()."""
    return request.app.state.my_cool_object


# KISM-BOILERPLATE: Demo api endpoint, enough to show a basic javascript interaction.
@router.get("/hello/")
def get_hello(request: Request) -> MessageResponse:
    """Hello GET Method."""
    msg = _get_my_cool_object(request).get_my_message()
    logger.debug("GET request to /hello/, returning: %s", msg)
    return MessageResponse(msg=msg)


@router.get("/hello_backwards/")
def get_hello_backwards(request: Request) -> MessageResponse:
    """Hello backwards GET Method."""
    msg = _get_my_cool_object(request).get_my_message_backwards()
    logger.debug("GET request to /hello_backwards/, returning: %s", msg)
    return MessageResponse(msg=msg)
