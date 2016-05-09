#!/usr/bin/env python

"""
Main server script.
"""

import settings

## Import Mongodb packages
from pymongo import MongoClient
import socket

## Import Tornado packages
from tornado.escape import json_encode, json_decode, url_escape
import tornado.ioloop
from tornado.auth import GoogleOAuth2Mixin
from tornado.gen import coroutine
from tornado.web import RequestHandler, Application, authenticated

## Import Route Handlers
from routes.BaseHandler import BaseHandler
from routes.IndexHandler import IndexHandler
from routes.OnboardingHandler import OnboardingHandler
from routes.LearnMoreHandler import LearnMoreHandler
from routes.WebsiteCreatorHandler import WebsiteCreatorHandler
from routes.WebsiteEditorHandler import WebsiteEditorHandler
from routes.AuthHandler import AuthLoginHandler, AuthLogoutHandler

## Main Configs
if __name__ == "__main__":
    client = MongoClient()
    database = client.min_bench

    settings_dict = {
        "static_path" : settings.STATIC_PATH,
        "template_path" : settings.TEMPLATE_PATH,
        "login_url" : "/auth/login/",
        "debug": settings.DEBUG,
        "cookie_secret": settings.COOKIE_SECRET,
        "google_oauth" : { "key" : settings.GAUTH_CLIENT_ID,
                           "secret" : settings.GAUTH_CLIENT_SECRET },
        "database" : database,
        "messages" : []
    }

    application = Application([
        (r"/", IndexHandler),
        (r"/auth/login/?", AuthLoginHandler),
        (r"/auth/logout/?", AuthLogoutHandler),
        (r"/main/?", OnboardingHandler),
        (r"/websitecreator/?", WebsiteCreatorHandler),
        (r"/websiteeditor/?", WebsiteEditorHandler),
        (r"/learn/?", LearnMoreHandler),
    ], **settings_dict)

    application.listen(settings.PORT)
    tornado.ioloop.IOLoop.instance().start()
