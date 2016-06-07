from mongoengine import *

class Tag(Document):
    name = StringField(primaryKey=True, required=True)
    angel_list_id = IntField(required=True)
