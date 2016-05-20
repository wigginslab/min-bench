from tornado.escape import json_encode, json_decode, url_escape
import tornado.ioloop
from tornado.auth import GoogleOAuth2Mixin
from tornado.gen import coroutine, Return
from tornado.web import RequestHandler, Application, authenticated

from models.User import *

class BaseHandler(RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)

    def render(self, template_loc, **kwargs):
        super(BaseHandler, self).render(template_loc, **kwargs)####

    @coroutine
    def current_user_completed_onboarding(self):
        user_email = self.current_user['email']
        user = yield self.retrieve_user_with_email_id(user_email)
        raise Return(user.onboarding_complete)

    @coroutine
    def retrieve_user_with_email_id(self, user_email):
        query = User.objects(_id=user_email)
        return query.first()
