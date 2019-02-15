from handlers.base import BaseHandler
from models.user import User


class IndexPage(BaseHandler):
    def get(self, *args, **kwargs):
        if self.session.get("id"):
            self.render_template("html/index.html", {
                "username": self.session.get("username"),
                "is_admin": self.session.get("user_type") == User.USER_TYPE_ADMIN
            })

        else:
            self.render_template("html/login.html")

    def post(self, *args, **kwargs):
        username = self.request.get("username")
        password = self.request.get("password")

        try:
            user = User.get_user(username, password)

            if user:
                self.session["id"] = user.key.id()
                self.session["username"] = user.username
                self.session["user_type"] = user.user_type

        except:
            pass

        self.redirect("/")
