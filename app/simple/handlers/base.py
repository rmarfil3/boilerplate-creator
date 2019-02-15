import os

import jinja2
import webapp2

from webapp2_extras import sessions

# setup template
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(
        os.path.dirname("frontend/static/")
    ),
    autoescape=True
)
JINJA_ENVIRONMENT.globals['uri_for'] = webapp2.uri_for


class BaseHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        webapp2.RequestHandler.__init__(self, request, response)
        self.session_store = sessions.get_store()

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session()

    def dispatch(self):
        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    def render_template(self, _template, _template_values={}):
        """Renders a template and writes the result to the response.

        :param _template: The location of the template
        :param _template_values: The template values
        """
        template = JINJA_ENVIRONMENT.get_template(_template)
        rv = template.render(_template_values)
        self.response.write(rv)
