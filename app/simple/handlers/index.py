from handlers.base import BaseHandler


class IndexPage(BaseHandler):
    def get(self, *args, **kwargs):
        self.render_template("html/index.html")
