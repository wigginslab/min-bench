from tornado.web import authenticated
from tornado.gen import coroutine

from routes.BaseHandler import BaseHandler
from utils.UserHelper import retrieve_user_with_email_id

from modules.vc_matcher_mb.VCMatcher import fetch_investors
from modules.vc_matcher_mb.utils.TagsHelper import retrieve_start_up_tags_from_user

class VCMatcherHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        current_user = self.get_current_user()
        user_email = current_user['email']
        user = yield retrieve_user_with_email_id(user_email)
        # TODO implement soft caching with TTL
        investors = fetch_investors(user);
        json_resp = {"investors": investors}
        self.write(json_resp)
