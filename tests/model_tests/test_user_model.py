import unittest2 as unittest
from tornado.gen import coroutine
from tornado.testing import *

from mongoengine import *
from models.User import *

from utils.UserHelper import retrieve_user_with_email_id

class TestUserModel(AsyncTestCase):

    ## TODO move this into base parent class
    @coroutine
    def setUp(self):
        super(AsyncTestCase, self).setUp()
        self.io_loop = self.get_new_ioloop()
        self.io_loop.make_current()
        connect("min_bench")

        self.valid_test_email = "test@test.com"
        self.invalid_test_email = "not_a_valid_test_email@test.com"

    # Tests
    @gen_test
    def test_create_valid_test_user(self):
        user = yield self.create_test_user()
        self.assertEqual(user._id, self.valid_test_email)

    @gen_test
    def test_query_valid_test_user(self):
        user = yield retrieve_user_with_email_id(self.valid_test_email)
        self.assertIsNotNone(user)

    @gen_test
    def test_query_invalid_test_user(self):
        user = yield retrieve_user_with_email_id(self.invalid_test_email)
        self.assertFalse(user)


    ## TODO move this into base parent class
    def tearDown(self):
        yield self.destroy_test_user()

    # Helper Functions
    ## TODO move this into base parent class
    @coroutine
    def create_test_user(self):
        user = User(_id=self.valid_test_email, name="test", start_up_tags="education, business")
        user.save()
        return user

    @coroutine
    def destroy_test_user(self):
        user = yield retrieve_user_with_email_id(self.valid_test_email)
        user.delete()
