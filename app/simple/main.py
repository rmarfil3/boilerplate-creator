#!/usr/bin/env python
# -- coding: utf-8 --
import webapp2
from webapp2_extras import routes

# public
from handlers.index import IndexPage
from handlers.init import Init

app = webapp2.WSGIApplication([
    routes.DomainRoute(r"<:.*>", [
        webapp2.Route("/init", handler=Init, name="www-init"),
        webapp2.Route("<:.*>", handler=IndexPage, name="www-index")
    ])
], debug=True)
