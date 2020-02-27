""" an example function and exposing it through __all__ """
import base64
import io
import logging
import tornado.web
import tornado.escape
from contextlib import contextmanager
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import qrcode
import qrcode.image.svg


@contextmanager
def fkey(path="key.key", passcode=None):
    with open("key.key", "rb") as file:
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
        key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
    crypto = Fernet(key)
    yield crypto


class MainHandler(tornado.web.RequestHandler):
    """ Handles get and post requests """

    def qr_svg(self, value):
        """ will return qr_svg of value """
        factory = qrcode.image.svg.SvgPathImage  # fragment
        passcode = tornado.escape.url_unescape(value)
        data = f"https://blueshed-crypto.herokuapp.com?passcode={passcode}"
        img = qrcode.make(data, image_factory=factory)
        output = io.BytesIO()
        img._write(output)
        return output.getvalue()

    def get_template_namespace(self):
        """ expose qr_svg to template """
        result = super().get_template_namespace()
        result["qr_svg"] = self.qr_svg
        return result

    def get(self, message=None, passcode=None, error_message=None):
        """ handle the get request """
        passcode = self.get_argument("passcode", passcode)
        self.render(
            "index.html",
            message=message,
            passcode=passcode,
            error_message=error_message,
        )

    def post(self):
        """ handle the post request """
        action = self.get_argument("submit", "encrypt")
        message = self.get_argument("message", "")
        passcode = self.get_argument("passcode", "")
        error_message = None
        try:
            if action == "encrypt":
                message = self.encrypt(message, passcode)
            else:
                message = self.decrypt(message, passcode)
        except InvalidToken as ex:
            error_message = "invalid passcode"
        self.get(message, passcode, error_message=error_message)

    @classmethod
    def encrypt(cls, message, passcode=None):
        """ returns an encrytped utf-8 string """
        with fkey(passcode=passcode) as crypto:
            return crypto.encrypt(message.encode()).decode("utf-8")

    @classmethod
    def decrypt(cls, message, passcode=None):
        """ returns a decrypted utf-8 string """
        with fkey(passcode=passcode) as crypto:
            return crypto.decrypt(message.encode()).decode("utf-8")
