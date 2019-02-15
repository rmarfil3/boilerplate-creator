import json
import logging

from google.appengine.datastore.datastore_query import Cursor

import handlers.exceptions
from configs import api
from handlers.api.v1.base import ApiBaseHandler
from handlers.api.decorators import handle_errors, allow_only
from handlers.exceptions import model_exceptions
from models.user import User


class UsersApi(ApiBaseHandler):
    @handle_errors
    @allow_only(User.USER_TYPES)
    def get(self):
        param_cursor = self.request.get("cursor")
        users, cursor, more = User.custom_query().fetch_page(api.FETCH_PAGE_SIZE,
                                                             start_cursor=Cursor(urlsafe=param_cursor))
        self.render(users=[user.to_object() for user in users], cursor=cursor.urlsafe() if cursor else None, more=more)

    @handle_errors
    @allow_only(User.USER_TYPES)
    def post(self):
        try:
            user = User.add(**json.loads(self.request.body))
            self.render(user=user.to_object())
        except Exception, exc:
            logging.error(exc)
            self.render_error(handlers.exceptions.GenericError(str(exc)))

    # @allow_only(User.USER_TYPES)
    # def put(self, id):
    #     try:
    #         user = User.add(id=id, **json.loads(self.request.body))
    #         self.render(user=user.to_object())
    #     except voluptuous.MultipleInvalid, exc:
    #         self.render_error(model_exceptions.ValidationError(str(exc)))
    #     except Exception, exc:
    #         logging.error(exc)
    #         self.render_error(handlers.exceptions.GenericError(str(exc)))

    @handle_errors
    @allow_only(User.USER_TYPES)
    def delete(self, id):
        try:
            User.delete(id)
            self.render(status=204, code="DELETED")
        except model_exceptions.NDBEntityNotFoundError, exc:
            self.render_error(exc)
        except Exception, exc:
            logging.error(exc)
            self.render_error(handlers.exceptions.GenericError(str(exc)))
