"""test we can make it"""

import logging
import urllib.parse

import pytest
from blueshed.crypto import api
from blueshed.crypto.main import make_app

api.LOGGER.setLevel(logging.DEBUG)


@pytest.fixture
def app():
    """get a testable app"""
    return make_app()


async def test_homepage(http_server_client):
    """can we get the home page"""
    response = await http_server_client.fetch('/')
    assert response.code == 200


async def test_api(http_server_client):
    """can we get the home page"""
    message = 'hello world'

    body = urllib.parse.urlencode({'message': message, 'passcode': 'hello'})
    response = await http_server_client.fetch(
        '/encrypt', method='POST', body=body
    )
    assert response.code == 200

    body = urllib.parse.urlencode(
        {'message': response.body, 'passcode': 'hello'}
    )
    response = await http_server_client.fetch(
        '/decrypt', method='POST', body=body
    )
    assert response.code == 200
    assert response.body.decode('utf-8') == message

    body = urllib.parse.urlencode(
        {'message': response.body, 'passcode': 'hello', 'action': 'decrypt'}
    )
    response = await http_server_client.fetch('/', method='POST', body=body)
    assert response.code == 200
