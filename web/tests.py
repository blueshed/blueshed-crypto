import os
import unittest
from tornado.testing import AsyncHTTPTestCase
from app import make_app


class TestHelloApp(AsyncHTTPTestCase):
    def get_app(self):
        return make_app()

    def test_homepage(self):
        response = self.fetch("/")
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b"Hello, world")


if __name__ == "__main__":
    unittest.main()
