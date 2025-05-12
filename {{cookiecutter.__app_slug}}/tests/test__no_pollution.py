"""These are some tests to ensure that the flask app you have made won't accidentally pollute your tests.

Testing was hell for a couple of days, tests would pass when I just ran one test module, but fail when run all together.
After much frustration I realised that tests were interfering with each other since I was using real directories.
PyTest is multi threaded and thus multiple tests can (and will) be running at the same time.
Without tmp_path they will use each other's config/data.

Tests should always use the tmp_path fixture as an instance_path as it means they won't pollute each other.
And thus in the boilerplate I have some checks to ensure that your tests aren't possibly getting polluted.
"""

import pytest

from {{cookiecutter.__app_package}} import create_app


def test_instance_path_check(get_test_config):
    """TEST: When passed a dictionary as a config, the instance path must be specified."""
    with pytest.raises(AttributeError):
        create_app(test_config=get_test_config())


def test_config_validate_test_instance_path(get_test_config):
    """My boilerplate catches when you forget to use tmp_path in testing.

    This test exists because I spent so much time troubleshooting why some tests are using the default instance path.
    """
    import contextlib
    import os
    import random
    import shutil
    import string

    # Please always use tmp_path and never do this outside of this test.
    repo_instance_path = os.path.join(os.getcwd(), "instance")
    incorrect_instance_root = os.path.join(repo_instance_path, "_TEST")
    random_string = "".join(random.choice(string.ascii_uppercase) for _ in range(8))
    incorrect_instance_path = os.path.join(incorrect_instance_root, random_string)

    with contextlib.suppress(FileNotFoundError, FileExistsError):
        os.mkdir(repo_instance_path)
        shutil.rmtree(incorrect_instance_root)
        os.mkdir(incorrect_instance_root)
        os.mkdir(incorrect_instance_path)

    create_app(test_config=get_test_config(), instance_path=incorrect_instance_path)
    shutil.rmtree(incorrect_instance_root)
