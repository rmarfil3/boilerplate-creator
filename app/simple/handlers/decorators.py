import ast
import logging
import re

from google.appengine.ext import ndb
from models.user import User


def allow_only(allowed_user_types):
    """Restrict access to a certain handler.

    :param allowed_user_types: List of allowed user types
    """
    def decorate(fn):
        def wrap(self, *args, **kwargs):
            user_id = self.session.get("id")
            if user_id:
                user = ndb.Key(User, int(user_id)).get()

                if user.acl in allowed_user_types and user.status != "Blocked":
                    return fn(self, *args, **kwargs)
            self.redirect("/")
        return wrap
    return decorate
