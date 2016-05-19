from mongoengine import *

class User(Document):
    _id = StringField(required=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    start_up_name = StringField()
    start_up_description = StringField()
    start_up_tags = ListField()

    @property
    def full_name(self):
        return "%s, %s" % (self.last_name, self.first_name)
