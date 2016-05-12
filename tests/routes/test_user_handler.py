import unittest2 as unittest
from routes.UserHandler import *
from routes.BaseHandler import BaseHandler
from pymongo import MongoClient
import settings

class TestUserHandler(unittest.TestCase):
    def setUp(self):
        client = MongoClient()
        database = client.min_bench

        self.settings = {"database": database }
        self.valid_user_email = "test@gmail.com"
        self.non_existent_user_email = "not_a_user@gmail.com"

        createTestUser(self, "test@gmail.com", "testy")

    def test_user_exists(self):
        user = retrieve_user(self, self.valid_user_email)
        self.assertIsNotNone(user)

    def test_user_does_not_exist(self):
        user = retrieve_user(self, self.non_existent_user_email)
        self.assertIsNone(user)

    def test_valid_user_can_update(self):
        self.test_user_exists()

        new_user_data = {"name": "dan"}
        new_user_data_dto = build_user_dto(new_user_data)
        self.assertIsNotNone(new_user_data_dto)

        update_result = update_user_with_email_id(self, "test@gmail.com", new_user_data_dto)
        self.assertIs(update_successful(update_result), True)

    def test_non_existent_user_cannot_update(self):
        self.test_user_does_not_exist()

        new_user_data = {"name": "dan"}
        new_user_data_dto = build_user_dto(new_user_data)
        self.assertIsNotNone(new_user_data_dto)

        update_result = update_user_with_email_id(self, "not_a_user@gmail.com", new_user_data_dto)
        self.assertIs(update_successful(update_result), False)

    def tearDown(self):
        destroyTestUser(self, "test@gmail.com")

## Testing Utility Functions
def createTestUser(self, email, name):
    database = self.settings["database"]
    database.users.insert_one({ "_id" : email, "name" : name })

def destroyTestUser(self, email):
    database = self.settings["database"]
    database.users.delete_one({ "_id" : email})

def retrieve_user(self, name):
    test_user = retrieve_user_with_email_id(self, name)
    return test_user

if __name__ == "__main__":
    unittest.main()
