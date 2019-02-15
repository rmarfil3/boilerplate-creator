#!/usr/bin/env python
# -- coding: utf-8 --
import webapp2
from webapp2_extras import routes

# public
from handlers.init import Init
from handlers.index import IndexPage
from handlers.admin import AdminPage
from handlers.logout import Logout

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
        # webapp2.Route("<:.*>", handler=IndexPage, name="www-index")
    ])
], debug=True, config=config)
