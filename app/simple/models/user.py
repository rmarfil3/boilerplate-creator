from hashlib import sha512

from google.appengine.ext import ndb

from config.default import SALT
from handlers.exceptions import Error


class User(ndb.Model):
    class UnauthenticatedAccess(Error):
        def __init__(self, message="No valid authentication details were provided. Access is denied."):
            self.status = 401
            self.code = "UNAUTHENTICATED_ACCESS"
            self.message = message

    class UnauthorizedAccess(Error):
        def __init__(self, message="You are not authorized. Access is denied."):
            self.status = 401
            self.code = "UNAUTHORIZED_ACCESS"
            self.message = message

    class AccountBlocked(Error):
        def __init__(self, message="Your account has been blocked."):
            self.status = 401
            self.code = "ACCOUNT_BLOCKED"
            self.message = message

    class UsernameAlreadyTaken(Error):
        def __init__(self, message="Username has already been registered."):
            self.status = 409
            self.code = "USERNAME_ALREADY_TAKEN"
            self.message = message

    USER_TYPE_ADMIN = "admin"
    USER_TYPE_MODERATOR = "moderator"
    USER_TYPE_USER = "user"
    USER_TYPES = [
        USER_TYPE_ADMIN,
        USER_TYPE_MODERATOR,
        USER_TYPE_USER
    ]

    # Basic info
    username = ndb.StringProperty()
    password = ndb.StringProperty()  # SHA512
    user_type = ndb.StringProperty(choices=USER_TYPES, default=USER_TYPE_USER)

    # Login
    is_blocked = ndb.BooleanProperty(default=False)
    deleted = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)

    @classmethod
    def custom_query(cls, *args, **kwargs):
        return cls.query(cls.deleted == False, *args, **kwargs)

    def _pre_put_hook(self):
        self.username = self.username.lower()

    @classmethod
    def hash_password(cls, password):
        return sha512(SALT + password).hexdigest()

    @classmethod
    def get_user(cls, username, password):
        username = username.lower()

        user = User.custom_query(User.username == username, User.password == cls.hash_password(password)).get()
        if not user:
            raise User.UnauthenticatedAccess()

        if user.is_blocked:
            raise User.AccountBlocked()

        return user

    @classmethod
    def add(cls, *args, **kwargs):
        username = kwargs.get("username", "").lower()

        if username and User.custom_query(User.username == username).get(keys_only=True):
            raise User.UsernameAlreadyTaken()

        user = User()

        for key, value in kwargs.iteritems():
            if key == "password":
                value = cls.hash_password(value)
            setattr(user, key, value)
        user.put()
        return user

    def delete(self):
        self.deleted = True
        self.put()
