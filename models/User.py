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
        start_up_tags = self.start_up_tags
        print(start_up_tags)
        tag_names = self.start_up_tags.split(",")
        print(tag_names)
        tags_to_look_up = []

        for tag_name in tag_names:
            tag_name = tag_name.strip()
            tag_name = tag_name.strip()
            tag = Tag.objects(name=tag_name)
            if len(tag) == 0:
                tags_to_look_up.append(tag_name)

        try:
            for tag_name in tags_to_look_up:
                print("tag_name")
                fetch_tag_data_from_angel_list(tag_name);
        except ValueError as err:
            raise ValidationError(err)
