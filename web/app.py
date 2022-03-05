""" Out web app """
import logging
import os
from distutils.util import strtobool

import tornado.ioloop
import tornado.log
import tornado.web
from tornado.options import options, define, parse_command_line
from pkg_resources import resource_filename

from .main_handler import MainHandler
from .api_handlers import EncryptHandler, DecryptHandler

LOGGER = logging.getLogger(__name__)

define('debug', type=bool, default=False, help='run in debug mode')


def make_app():
    """ make tornado application """
    debug = strtobool(os.getenv('DEBUG', str(options.debug)))
    if debug:
        logging.info('running in debug mode')
    return tornado.web.Application(
        [
            (r'/encrypt', EncryptHandler),
            (r'/decrypt', DecryptHandler),
            (r'/', MainHandler),
        ],
        debug=debug,
        static_path=resource_filename('web', 'static'),
    )


def main():
    """ make and run tornado application """
    app = make_app()
    port = int(os.getenv('PORT', '8080'))
    app.listen(port)
    LOGGER.info('listening on port: %s', port)
    loop = tornado.ioloop.IOLoop.current()
    try:
        loop.start()
    except KeyboardInterrupt:
        LOGGER.info('shutting down.')
        loop.stop()


if __name__ == '__main__':
    parse_command_line()
    main()
