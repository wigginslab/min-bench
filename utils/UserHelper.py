from tornado.gen import coroutine
from models.User import User

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
