# pylint: disable=W0223
""" our api handlers """
import logging

import tornado.web
from .main_handler import MainHandler

LOGGER = logging.getLogger(__name__)


class EncryptHandler(tornado.web.RequestHandler):
    """ encrypt message """

    def post(self):
        """ handle the post request """
        message = self.get_argument('message', '')
        passcode = self.get_argument('passcode', '')
        LOGGER.debug('encrypt: %r', message)
        self.set_header('Content-type', 'text/plain')
        self.write(MainHandler.encrypt(message, passcode))


class DecryptHandler(tornado.web.RequestHandler):
    """ decrypt message """

    def post(self):
        """ handle the post request """
        message = self.get_argument('message', '')
        passcode = self.get_argument('passcode', '')
        LOGGER.debug('decrypt: %r', message)
        self.set_header('Content-type', 'text/plain')
        self.write(MainHandler.decrypt(message, passcode))
