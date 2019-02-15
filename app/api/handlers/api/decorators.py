import logging

from google.appengine.ext import ndb
from handlers import exceptions
from handlers.exceptions import api_exceptions

from models.user import User


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


def allow_only(allowed_user_types):
    """Restrict access to a certain handler.

    :param allowed_user_types: List of allowed user types
    """
    def decorate(fn):
        def wrap(self, *args, **kwargs):
            user_id = self.session.get("id")
            if user_id:
                user = ndb.Key(User, int(user_id)).get()

                if user.user_type in allowed_user_types and not user.is_blocked:
                    return fn(self, *args, **kwargs)
            raise api_exceptions.ForbiddenAccess()
        return wrap
    return decorate
