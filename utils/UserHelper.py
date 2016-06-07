from tornado.gen import coroutine
from tornado.escape import json_decode
from tornado.web import RequestHandler

from models.User import *

def get_current_user():
    user_json = RequestHandler.get_secure_cookie("user")
    if not user_json: return None
    return json_decode(user_json)

@coroutine
def current_user_completed_onboarding(self):
    user_email = self.current_user['email']
    user = yield retrieve_user_with_email_id(user_email)
    raise Return(user.onboarding_complete)

@coroutine
def update_user(user, user_data):
    try:
        if user == None:
            return None

        for k,v in user_data.items():
            user[k] = v

        user['onboarding_complete'] = True

        user.save()
    except:
        return None

    return user

@coroutine
def retrieve_user_with_email_id(user_email):
    query = User.objects(_id=user_email)
    return query.first()

def retrieve_start_up_tags_from_user(user):
    tag_names = []
    for tag in user.start_up_tags.split(","):
        tag_names.append(tag)
    return tag_names
