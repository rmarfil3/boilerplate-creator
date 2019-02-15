#!/usr/bin/env python
# -- coding: utf-8 --
import webapp2
from webapp2_extras import routes

# public
from handlers.public.init import Init
from handlers.public.index import IndexPage
from handlers.public.admin import AdminPage
from handlers.public.logout import Logout

# api
from handlers.api.v1.users import UsersApi

config = {
    'webapp2_extras.sessions': {
        'secret_key': '#$sdgfdsre&^)^(":?><',
    },
}

app = webapp2.WSGIApplication([
    routes.DomainRoute(r"<:.*>", [
        webapp2.Route("/init", handler=Init, name="www-init"),
        webapp2.Route("/admin", handler=AdminPage, name="www-init"),
        webapp2.Route("/logout", handler=Logout, name="www-logout"),
        webapp2.Route("/", handler=IndexPage, name="www-index"),
        # webapp2.Route("<:.*>", handler=IndexPage, name="www-index")
    ])
], debug=True, config=config)

api = webapp2.WSGIApplication([
    routes.DomainRoute(r"<:.*>", [
        routes.PathPrefixRoute("/api", [
            routes.PathPrefixRoute("/v1", [
                webapp2.Route("/users", handler=UsersApi, name="api-users")
            ])
        ])
    ])
], debug=True, config=config)
