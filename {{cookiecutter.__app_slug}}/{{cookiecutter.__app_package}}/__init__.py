"""Flask webapp {{cookiecutter.__app_package}}."""

from pprint import pformat

from pathlib import Path

from flask import Flask, render_template

from . import blueprint_one, config, logger

__version__ = "0.0.1"  # This is the version of the app, used in pyproject.toml, enforced in a test.


def create_app(test_config: dict | None = None, instance_path: str | None = None) -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True, instance_path=instance_path)  # Create Flask app object

    logger.setup_logger(in_loggers=[app.logger])  # Setup flask logger with defaults

    if test_config:  # For Python testing we will often pass in a config
        if not instance_path:
            app.logger.critical("When testing supply both test_config and instance_path!")
            raise AttributeError(instance_path)
        {{cookiecutter.__app_config_var}} = config.{{cookiecutter.__app_camel_case}}Config(config=test_config, instance_path=Path(app.instance_path))
    else:
        {{cookiecutter.__app_config_var}} = config.{{cookiecutter.__app_camel_case}}Config(instance_path=Path(app.instance_path))  # Loads app config from disk

    app.logger.debug("Instance path is: %s", app.instance_path)

    logger.setup_logger(log_level={{cookiecutter.__app_config_var}}.logging.level, log_path={{cookiecutter.__app_config_var}}.logging.path, in_loggers=[app.logger] )  # Setup logger with config

    # Flask config, at the root of the config object.
    app.config.from_mapping({{cookiecutter.__app_config_var}}.flask.dict())

    # Other sections handled by config.py
    app.config["app"] = {{cookiecutter.__app_config_var}}.app

    # Do some debug logging of config
    app_config_str = ">>>\nFlask config:"
    for key, value in app.config.items():
        app_config_str += f"\n  {key}: {pformat(value)}"

    app.logger.debug(app_config_str)

    # Now that we have loaded out configuration, we can import our blueprints
    # KISM-BOILERPLATE: This is a demo blueprint blueprint_one.py. Rename the file
    #  and vars to make your own http endpoints and pages. Use multiple blueprints if
    #  you have functionality you can categorise.
    app.register_blueprint(blueprint_one.bp)  # Register blueprint

    # For modules that need information from the app object we need to start them under `with app.app_context():`
    # Since in the blueprint_one module, we use `from flask import current_app` to get the app object to get the config
    with app.app_context():
        blueprint_one.start_blueprint_one()

    # Flask homepage, generally don't have this as a blueprint.
    @app.route("/")
    def home() -> str:
        """Flask home."""
        return render_template("home.html.j2", __app_nice_name=__name__)  # Return a webpage

    app.logger.info("Starting Web Server")
    app.logger.info("{{cookiecutter.__app_nice_name}} version: %s", __version__)

    return app
