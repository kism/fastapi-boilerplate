"""Tests the api endpoints."""

import logging
from http import HTTPStatus
from typing import TYPE_CHECKING

from fastapi.testclient import TestClient

from my_cool_app import create_app
from my_cool_app.config import AppConf, Config

if TYPE_CHECKING:
    from pathlib import Path

    import pytest


def test_hello(client: TestClient) -> None:
    """TEST: The default /hello/ response, this one uses the fixture in conftest.py."""
    response = client.get("/hello/")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["msg"] == "Hello, World!"


def test_hello_with_config(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """TEST: the hello endpoint with non-default config."""
    config = Config(app=AppConf(my_message="Hello, PyTest!"))
    client = TestClient(create_app(config=config, instance_path=tmp_path))

    with caplog.at_level(logging.DEBUG):
        response = client.get("/hello/")

    assert response.status_code == HTTPStatus.OK
    assert response.json()["msg"] == "Hello, PyTest!"
    assert "returning: Hello, PyTest!" in caplog.text


def test_hello_backwards(client: TestClient) -> None:
    """TEST: The default /hello_backwards/ response."""
    response = client.get("/hello_backwards/")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["msg"] == "!dlroW ,olleH"  # cspell:disable-line


def test_openapi_schema(client: TestClient) -> None:
    """TEST: The OpenAPI schema is served, it's what frontend/openapi.d.ts is generated from."""
    response = client.get("/openapi.json")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["paths"].keys() >= {"/hello/", "/hello_backwards/"}
