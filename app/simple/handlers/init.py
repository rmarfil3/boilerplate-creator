import logging

from handlers.base import BaseHandler
from models.user import User


class Init(BaseHandler):
    def get(self, *args, **kwargs):
        username = "admin"

        if not User.custom_query(User.username == username).get(keys_only=True):
            User.add(username=username, password="admin", user_type=User.USER_TYPE_ADMIN)
            logging.debug("Done adding admin")
