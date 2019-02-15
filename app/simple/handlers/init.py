import logging

from handlers.base import BaseHandler
from models.user import User


class Init(BaseHandler):
    def get(self, *args, **kwargs):
        users = [
            {"username": "admin", "password": "admin", "user_type": User.USER_TYPE_ADMIN},
            {"username": "moderator", "password": "moderator", "user_type": User.USER_TYPE_MODERATOR},
            {"username": "user", "password": "user", "user_type": User.USER_TYPE_USER},
        ]

        for user in users:
            if not User.custom_query(User.username == user["username"]).get(keys_only=True):
                User.add(**user)
                self.response.write("Done adding {}\n".format(user["username"]))
            else:
                self.response.write("Already exists {}\n".format(user["username"]))
