from routes.BaseHandler import BaseHandler
from tornado.web import authenticated
from tornado.escape import json_decode

class UserHandler(BaseHandler):

    # TODO should we eventually make a user model?
    USER_MODEL_KEYS = [
        "_id",
        "name",
        "startup_name",
        "startup_tag_line",
        "startup_tags"
    ]

    #@authenticated
    def post(self):
        req_body = get_req_body(self)
        req_user_data = build_user_dto(req_body)
        user_id = req_user_data['_id']
        user = retrieve_user_with_email_id(self, user_id)

        if user:
            update_result = update_user_with_email_id(self, user_id, req_user_data)
            if update_successful(update_result):
                self.set_status(200)
            else:
                return_error_message(self, 500, "Error: Update for user with email {0} failed ".format(user_id))
        else:
            return_error_message(self, 404, "Error: Could not find user with email {0}".format(user_id))


def get_req_body(self):
    req_json_body = self.request.body
    req_body = json_decode(req_json_body)
    return req_body

def build_user_dto(user_data):
    user_dto = filter_req_data_for_user_data(user_data)
    #TODO Do we want to do any validation here?
    return user_dto

def filter_req_data_for_user_data(req_data):
    user_dto = {}

    for key in req_data.keys():
        if key in UserHandler.USER_MODEL_KEYS:
            user_dto[key] = req_data[key]

    return user_dto

def retrieve_user_with_email_id(self, user_email):
    database = self.settings["database"]
    user_json_data = database.users.find_one({ "_id" : user_email })
    return user_json_data

def update_user_with_email_id(self, user_email, user_data):
    database = self.settings["database"]
    result = database.users.update_one({
        "_id": user_email },
        {"$set": user_data })

    return result

def update_successful(update_result):
    if update_result.raw_result['updatedExisting'] == True:
        return True

    return False

def return_error_message(self, status_code, message):
    self.set_status(status_code)
    self.write(message)
