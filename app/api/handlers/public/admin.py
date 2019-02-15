from handlers.base import BaseHandler
from models.user import User

from handlers.decorators import allow_only


class AdminPage(BaseHandler):
    @allow_only([User.USER_TYPE_ADMIN])
    def get(self, *args, **kwargs):
        self.render_template("html/admin.html", {
            "username": self.session.get("username")
        })
