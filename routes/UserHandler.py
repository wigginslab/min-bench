from tornado.web import authenticated
from tornado.escape import json_decode
from tornado.gen import coroutine

from routes.BaseHandler import BaseHandler
from models.User import *
from models.UserForm import *
from utils.UserHelper import update_user, retrieve_user_with_email_id

class UserHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        current_user = self.get_current_user()
        user_id = current_user['email']
        user = yield retrieve_user_with_email_id(user_id)

        self.render("accountsetup.html", title="Edit Account Information", user=user)

    @authenticated
    @coroutine
    def post(self):
        form_data = self.sanitize_request_form_data(self.request.arguments)
        form = UserForm(data=form_data)
        form_data_is_valid = form.validate()

        if not form_data_is_valid:
            self.return_error_message(400, form.errors)
            return

        current_user = self.get_current_user()
        user_id = current_user['email']
        user = yield retrieve_user_with_email_id(user_id)

        if user is None:
            self.return_error_message(404, "Error: Could not find user with email {0}".format(user_id))
            return

        updated_user = yield update_user(user, form_data)

        if updated_user is None:
            self.return_error_message(500, "Error: Update for user with email {0} failed ".format(user_id))
            return

        self.set_status(200)

    def sanitize_request_form_data(self, form_data):
        if form_data is None:
            return {}

        sanitized_form_data = self.filter_dic_for_first_item(form_data)
        return sanitized_form_data

    def filter_dic_for_first_item(self, dic):
        new_dic = {}
        try:
            for k,v in dic.items():
                new_dic[k] = v[0]
        except:
            return {}

        return new_dic

    def return_error_message(self, status_code, message):
        self.set_status(status_code)
        self.write(message)
        self.finish()
