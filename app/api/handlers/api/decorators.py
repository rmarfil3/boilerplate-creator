import logging

from handlers import exceptions
from handlers.exceptions import api_exceptions


def handle_errors(fn):
    """Renders errors in JSON format.

    :param fn: The function to be wrapped
    """
    def wrapper(self, *args, **kwargs):
        try:
            return fn(self, *args, **kwargs)
        except exceptions.Error, exc:
            logging.warning(exc)
            self.render_error(exc)
        except Exception, exc:
            logging.critical(exc)
            self.render_error(exceptions.GenericError())
    return wrapper
