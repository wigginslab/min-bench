import unittest2 as unittest
from routes.BaseHandler import *
from routes.UserHandler import *
from models.User import *
from tornado.gen import coroutine
from tornado.testing import *
from mongoengine import *

class TestUserHandler(AsyncTestCase):
    @coroutine
    def setUp(self):
        super(AsyncTestCase, self).setUp()
        self.io_loop = self.get_new_ioloop()
        self.io_loop.make_current()
        connect("min-bench")

        self.valid_user_email = "test@test.com"
        self.non_existent_user_email = "not_a_user@gmail.com"
        yield self.create_test_user()

    @gen_test
    def test_user_exists(self):
        user = yield self.retrieve_user(self.valid_user_email)
        self.assertTrue(user)

    @gen_test
    def test_user_does_not_exist(self):
        user = yield self.retrieve_user(self.non_existent_user_email)
        self.assertFalse(user)

    @gen_test
    def test_valid_user_can_update(self):
        test_user = yield self.retrieve_user(self.valid_user_email)
        new_user_data = {"_id": "test@test.com", "name": "new_test_name"}
        user = yield update_user_with_email_id(self, test_user, new_user_data)
        self.assertIs(user.name, "new_test_name")

    @gen_test
    def test_user_update_is_invalid(self):
        test_user = yield self.retrieve_user(self.valid_user_email)
        new_user_data = {"_id": "test@test.com", "name": 111}
        user = yield update_user_with_email_id(self, test_user, new_user_data)
        self.assertIsNone(user)

    @gen_test
    def test_non_existent_user_cannot_update(self):
        test_user = yield self.retrieve_user(self.non_existent_user_email)
        new_user_data = {"_id": "test@test.com", "name": "new_test_name"}
        user = yield update_user_with_email_id(self, test_user, new_user_data)
        self.assertIsNone(user)

    def tearDown(self):
        yield self.destroy_test_user()

    @coroutine
    def create_test_user(self):
        user = User(
            _id="test@test.com",
            name="test")
        user.save()
        return user

    @coroutine
    def destroy_test_user(self):
        user = yield self.query_user_with_id(self.valid_test_email)
        user.delete()

    @coroutine
    def retrieve_user(self, user_email):
        query = User.objects(_id=user_email)
        return query.first()

if __name__ == "__main__":
    unittest.main()
