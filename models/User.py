from mongoengine import *
from tornado.gen import coroutine
from modules.vc_matcher_mb.utils.AngelList import fetch_tag_data_from_angel_list
from models.Tag import *

class User(Document):
    _id = StringField(required=True, primaryKey=True)
    name = StringField(required=True)
    start_up_name = StringField()
    start_up_description = StringField()
    start_up_tags = StringField(required=True)
    onboarding_complete = BooleanField(default=False)

    @coroutine
    def clean(self):
        tagNames = self.start_up_tags.split(",")
        tagsToLookUp = []

        for tagName in tagNames:
            tag = Tag.objects(name=tagName)
            if len(tag) == 0:
                tagsToLookUp.append(tagName)

        for tagName in tagsToLookUp:
            fetch_tag_data_from_angel_list(tagName);
