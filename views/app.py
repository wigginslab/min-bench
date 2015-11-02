#!/usr/bin/env python

import settings

import tornado.escape
import tornado.ioloop
from tornado.web import RequestHandler, Application, asynchronous, authenticated, addslash

class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class IndexHandler(BaseHandler):
    #@authenticated
    def get(self):
        # username = tornado.escape.xhtml_escape(self.current_user)
        # self.render("index.html", username=username, title="Minimalistic Lean Workbench")
        self.render("index.html", title="Minimalistic Lean Workbench")

class AuthLoginHandler(BaseHandler):
    @addslash
    def get(self):
        try:
            errormessage = self.get_argument("error")
        except:
            errormessage = ""
        self.render("login.html", errormessage = errormessage)

    def check_permission(self, password, username):
        if username == "admin" and password == "admin":
            return True
        return False

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        auth = self.check_permission(password, username)
        if auth:
            self.set_current_user(username)
            self.redirect(self.get_argument("next", u"/"))
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect")
            self.redirect(u"/auth/login/" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

class AuthLogoutHandler(BaseHandler):
    @addslash
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

if __name__ == "__main__":
    settings_dict = {
        "static_path" : settings.STATIC_PATH,
        "template_path" : settings.TEMPLATE_PATH,
        "login_url" : "/auth/login/",
        "debug": settings.DEBUG,
        "cookie_secret": settings.COOKIE_SECRET
    }
    application = Application([
        (r"/", IndexHandler),
        (r"/auth/login/", AuthLoginHandler),
        (r"/auth/logout/", AuthLogoutHandler)
    ], **settings_dict)

    application.listen(3036)
    tornado.ioloop.IOLoop.instance().start()
