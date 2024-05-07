import importlib.resources

from tornado.options import parse_command_line
from blueshed.gust import Gust

from .api import routes


def make_app():
    static_path = importlib.resources.files(__package__) / 'static'
    template_path = importlib.resources.files(__package__) / '.'
    app = Gust(static_path=static_path, template_path=template_path)
    routes.install(app)
    return app


def main():
    make_app().run()


if __name__ == '__main__':
    parse_command_line()
    main()
