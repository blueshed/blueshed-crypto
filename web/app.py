import logging
import os
from distutils.util import strtobool
from pkg_resources import resource_filename
import tornado.ioloop
import tornado.log
import tornado.web
from .main_handler import MainHandler


def make_app():
    debug = strtobool(os.getenv("DEBUG", "False"))
    if debug:
        logging.info("running in debug mode")
    return tornado.web.Application(
        [(r"/", MainHandler)],
        debug=debug,
        static_path=resource_filename("web", "static"),
    )


def main():
    app = make_app()
    port = int(os.getenv("PORT", 8080))
    app.listen(port)
    logging.info("listening on port: %s", port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    main()
