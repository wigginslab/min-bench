from mongoengine import *
from tornado.gen import coroutine

class User(Document):
    _id = StringField(required=True, primaryKey=True)
    name = StringField(required=True)
    start_up_name = StringField()
    start_up_description = StringField()
    start_up_tags = StringField()
    onboarding_complete = BooleanField(default=False)
