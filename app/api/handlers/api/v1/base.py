import json

from base.handler import BaseHandler
from libraries.helpers import dict_functions


class ApiBaseHandler(BaseHandler):
    def render(self, status=200, code="SUCCESS", **extras):
        """Renders a response as JSON.

        :param code: Status code (default is 200)
        :param extras: Extra arguments
        """
        data = {
            "success": True,
            "status": status,
            "code": code
        }
        data = dict_functions.merge_dicts(data, extras)
        self.write(data)

    def render_error(self, exception):
        """Renders a error response as JSON.

        :param exception: The exception object (see `handlers/exceptions`)
        """
        data = {
            "success": False,
            "status": exception.status,
            "code": exception.code,
            "message": str(exception)
        }
        self.response.status = exception.status
        self.write(data)

    def write(self, data):
        """Renders a data as JSON.

        :param data: The data in dictionary
        """
        self.response.headers["Content-Type"] = "application/json"
        self.response.write(json.dumps(data))
