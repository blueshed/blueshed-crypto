# pylint: disable=W0223
"""our api handlers"""

import base64
import io
import logging
import os
from contextlib import contextmanager

import qrcode
import qrcode.image.svg
import tornado.escape
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from blueshed.gust import Routes

LOGGER = logging.getLogger(__name__)
QR_URL = os.getenv('QR_URL', 'https://blueshed-crypto.herokuapp.com')

routes = Routes()


@contextmanager
def fkey(path='key.key', passcode=None):
    """open key.key"""
    with open(path, 'rb') as file:
        key = file.read()
    if passcode:
        password = passcode.encode()  # Convert to type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=key,
            iterations=100000,
            backend=default_backend(),
        )
        key = base64.urlsafe_b64encode(
            kdf.derive(password)
        )  # Can only use kdf once
    crypto = Fernet(key)
    yield crypto


def encrypt(message, passcode=None):
    """returns an encrytped utf-8 string"""
    with fkey(passcode=passcode) as crypto:
        return crypto.encrypt(message.encode()).decode('utf-8')


def decrypt(message, passcode=None):
    """returns a decrypted utf-8 string"""
    with fkey(passcode=passcode) as crypto:
        return crypto.decrypt(message.encode()).decode('utf-8')


def qr_svg(value):
    """will return svg qr code image of value"""
    factory = qrcode.image.svg.SvgPathImage  # fragment
    passcode = tornado.escape.url_unescape(value)
    data = f'{QR_URL}?passcode={passcode}'
    img = qrcode.make(data, image_factory=factory)
    output = io.BytesIO()
    img._write(output)  # pylint: disable=W0212
    return output.getvalue()


@routes.post('/encrypt')
def do_encrypt(request):
    """handle the post request"""
    message = request.get_argument('message', '')
    passcode = request.get_argument('passcode', '')
    LOGGER.debug('encrypt: %r', message)
    request.set_header('Content-type', 'text/plain')
    return encrypt(message, passcode)


@routes.post('/decrypt')
def do_decrypt(request):
    """handle the post request"""
    message = request.get_argument('message', '')
    passcode = request.get_argument('passcode', '')
    LOGGER.debug('decrypt: %r', message)
    request.set_header('Content-type', 'text/plain')
    return decrypt(message, passcode)


@routes.get('/', template='index.html')
def do_get(request, message=None, passcode=None, error_message=None):
    """handle the get request"""
    passcode = request.get_argument('passcode', passcode)
    return {
        'message': message,
        'passcode': passcode,
        'error_message': error_message,
        'qr_svg': qr_svg,
    }


@routes.post('/', template='index.html')
def do_post(request):
    """handle the post request"""
    action = request.get_argument('submit', 'encrypt')
    message = request.get_argument('message', '')
    passcode = request.get_argument('passcode', '')
    error_message = None
    try:
        if action == 'encrypt':
            message = encrypt(message, passcode)
        else:
            message = decrypt(message, passcode)
    except InvalidToken:
        error_message = 'invalid passcode'
    return do_get(request, message, passcode, error_message=error_message)
