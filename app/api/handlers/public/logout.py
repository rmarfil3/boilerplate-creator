from handlers.public.base import BaseHandler
from models.user import User


class Logout(BaseHandler):
    def get(self, *args, **kwargs):
        self.session["id"] = ""
        self.session["username"] = ""
        self.session["user_type"] = ""

        self.redirect("/")
