import pytest


def test_invalid_message(get_test_config):
    """Test invalid message."""
    with pytest.raises(ValueError, match="AppConfDef: my_message cannot be empty"):
        get_test_config("config_app_message_invalid.toml")
