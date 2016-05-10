from tornado.gen import coroutine
from routes.BaseHandler import BaseHandler
from tornado.auth import GoogleOAuth2Mixin
from tornado.web import authenticated
from tornado.escape import json_encode


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
