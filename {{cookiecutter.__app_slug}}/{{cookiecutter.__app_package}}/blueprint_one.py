"""Blueprint one's object..."""

from http import HTTPStatus

from flask import Blueprint, Response, jsonify

from .blueprint_one_object import MyCoolObject
from .flask_helpers import get_current_app
from .logger import get_logger

# Modules should all setup logging like this so the log messages include the modules name.
# If you were to list all loggers with something like...
# `loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]`
# Before creating this object, you would not see a logger with this modules name ({{cookiecutter.__app_package}}.this_module_name)
logger = get_logger(__name__)  # Create a logger: {{cookiecutter.__app_package}}.this_module_name, inherit config from root logger

# Register this module (__name__) as available to the blueprints of {{cookiecutter.__app_package}}, I think https://flask.palletsprojects.com/en/3.0.x/blueprints/
bp = Blueprint("{{cookiecutter.__app_package}}", __name__)

my_cool_object: MyCoolObject | None = None
current_app = get_current_app()


# KISM-BOILERPLATE:
# So regarding current_app, have a read of https://flask.palletsprojects.com/en/3.0.x/appcontext/
# This function is a bit of a silly example, but often you need to do things to initialise the module.
# You can't use the current_app object outside of a function since it behaves a bit weird, even if
#   you import the module under `with app.app_context():`
# So we call this to set globals in this module.
# You don't need to use this to set every variable as current_app will work fine in any function.
def start_blueprint_one() -> None:
    """Method to 'configure' this module. Needs to be called under `with app.app_context():` from __init__.py."""
    global my_cool_object  # noqa: PLW0603 Necessary evil as far as I can tell, could move to all objects but eh...
    my_cool_object = MyCoolObject(current_app.{{cookiecutter.__app_config_var}}.app)  # Create the object with the config from the app object


# KISM-BOILERPLATE: This is the demo api endpoint, enough to show a basic javascript interaction.
@bp.route("/hello/", methods=["GET"])
def get_hello() -> Response:
    """Hello GET Method."""
    message = {"msg": current_app.{{cookiecutter.__app_config_var}}.app.my_message}  # We don't use the object here, but we could.

    logger.debug(
        "GET request to /hello/, returning: %s as json, due to config: %s",
        message,
        current_app.{{cookiecutter.__app_config_var}}.app,
    )

    response = jsonify(message)
    response.status_code =  HTTPStatus.OK
    return response # Return json, not a webpage.


# KISM-BOILERPLATE: This is the demo api endpoint, enough to demonstrate object loading.
@bp.route("/hello_backwards/", methods=["GET"])
def get_hello_backwards() -> Response:
    """Hello GET Method."""
    assert my_cool_object is not None  # noqa: S101 Appease mypy

    message = {"msg": my_cool_object.get_my_message_backwards()}

    logger.debug(
        "GET request to /hello_backwards/, returning: %s",
        message,
    )

    response = jsonify(message)
    response.status_code =  HTTPStatus.OK

    return response  # Return json, not a webpage.
