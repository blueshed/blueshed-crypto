""" test we can make it """
import logging
import unittest
import urllib

from tornado.testing import AsyncHTTPTestCase

from web import api_handlers
from web.app import make_app

api_handlers.LOGGER.setLevel(logging.DEBUG)


class TestHelloApp(AsyncHTTPTestCase):
    """ can we test our app """

    def get_app(self):
        """ get a testable app """
        return make_app()

    def test_homepage(self):
        """ can we get the home page """
        response = self.fetch('/')
        self.assertEqual(response.code, 200)

    def test_api(self):
        """ can we get the home page """
        message = 'hello world'

        body = urllib.parse.urlencode(
            {'message': message, 'passcode': 'hello'}
        )
        response = self.fetch('/encrypt', method='POST', body=body)
        self.assertEqual(response.code, 200)

        body = urllib.parse.urlencode(
            {'message': response.body, 'passcode': 'hello'}
        )
        response = self.fetch('/decrypt', method='POST', body=body)
        self.assertEqual(response.code, 200)

        self.assertEqual(response.body.decode('utf-8'), message)


if __name__ == '__main__':
    unittest.main()
