from tornado.escape import json_encode, json_decode, url_escape
import tornado.ioloop
from tornado.auth import GoogleOAuth2Mixin
from tornado.gen import coroutine
from tornado.web import RequestHandler, Application, authenticated

####
## BaseHandler Definition
####
class BaseHandler(RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)

    def render(self, template_loc, **kwargs):
        kwargs["messages"] = self.settings["messages"]
        super(BaseHandler, self).render(template_loc, **kwargs)####
