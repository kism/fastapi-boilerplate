"""Demo object."""


# KISM-BOILERPLATE: Demo object, doesn't do much
class MyCoolObject:
    """Demo object."""

    def __init__(self, {{cookiecutter.__app_config_var}}: dict) -> None:
        """Init config for the NGINX Allowlist Writer."""
        # Monitor Writing
        print({{cookiecutter.__app_config_var}})

        self._my_message = {{cookiecutter.__app_config_var}}.my_message

    def get_my_message_backwards(self) -> str:
        """Return the string backwards."""
        return self._my_message[::-1]
