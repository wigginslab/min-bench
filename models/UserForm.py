from wtforms import Form, BooleanField, StringField, TextAreaField, validators

class UserForm(Form):
    name = StringField('name', [validators.required(), validators.length(min=1, max=25)])
    start_up_name = StringField('start_up_name', [validators.required(), validators.length(min=1, max=25)])
    start_up_description = TextAreaField('start_up_description', [validators.required(), validators.length(min=1, max=500)])
    start_up_tags = TextAreaField('start_up_tags', [validators.required(),validators.length(min=1, max=500)])
