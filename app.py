#!/usr/bin/env python

"""
Main server script.
"""

import settings

from pymongo import MongoClient
import socket
from tornado.escape import json_encode, json_decode, url_escape
import tornado.ioloop
from tornado.auth import GoogleOAuth2Mixin
from tornado.gen import coroutine
from tornado.web import RequestHandler, Application, authenticated

class BaseHandler(RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)

class IndexHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect(u"/main")
        else:
            self.render("index.html", title="Minimalistic Lean Workbench")

class OnboardingHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render("onboarding.html", title="Minimalistic Lean Workbench")

# User authentication data:
# "users" collection schema: name, email
class AuthLoginHandler(BaseHandler, GoogleOAuth2Mixin):
    @coroutine
    def get(self):
        redirect_uri="http://{0}/auth/login".format(self.request.host)

        if self.get_argument('code', False):
            access = yield self.get_authenticated_user(
                redirect_uri=redirect_uri,
                code=self.get_argument('code'))
            user = yield self.oauth2_request(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                access_token=access["access_token"])
            self.set_secure_cookie("user", json_encode(user))

            database = self.settings["database"]
            if not database.users.find_one({ "_id" : user["email"] }):
                database.users.insert_one({ "_id" : user["email"],
                                            "name" : user["name"] })

            self.redirect("/main")
        else:
            yield self.authorize_redirect(
                redirect_uri=redirect_uri,
                client_id=self.settings["google_oauth"]["key"],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})

class AuthLogoutHandler(BaseHandler):
    @authenticated
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

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
        "database" : database
    }
    application = Application([
        (r"/", IndexHandler),
        (r"/auth/login/?", AuthLoginHandler),
        (r"/auth/logout/?", AuthLogoutHandler),
        (r"/main/?", OnboardingHandler),
    ], **settings_dict)

    application.listen(settings.PORT)
    tornado.ioloop.IOLoop.instance().start()
