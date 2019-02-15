from google.appengine.ext import ndb

from models.user import User


class Post(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    user_key = ndb.KeyProperty(kind=User, required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
