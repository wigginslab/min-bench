from tornado.gen import coroutine
from routes.BaseHandler import BaseHandler
from tornado.auth import GoogleOAuth2Mixin
from tornado.web import authenticated
from tornado.escape import json_encode

from models.User import *

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

            user_model = yield self.retrieve_user_with_email_id(user["email"])
            if not user_model:
                user = User(_id=user["email"],
                            name=user["name"],
                            access_token=access["access_token"])
                user.save()

            self.redirect("/main")
        else:
            yield self.authorize_redirect(
                redirect_uri=redirect_uri,
                client_id=self.settings["google_oauth"]["key"],
                scope=['profile', 'email', 'https://www.googleapis.com/auth/analytics', 'https://www.googleapis.com/auth/analytics.edit', 'https://www.googleapis.com/auth/analytics.readonly'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})

class AuthLogoutHandler(BaseHandler):
    @authenticated
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))
