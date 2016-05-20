import unittest2 as unittest
from models.User import *
from mongoengine import *
import tornado.ioloop
from tornado.gen import coroutine
from tornado.testing import *

class TestUserModel(AsyncTestCase):

    valid_test_email="test@test.com"
    invalid_test_email="not_a_valid_test_email@test.com"

    ## TODO move this into base parent class
    def setUp(self):
        super(AsyncTestCase, self).setUp()
        self.io_loop = self.get_new_ioloop()
        self.io_loop.make_current()
        connect("min-bench")

    # Tests
    @gen_test
    def test_create_valid_test_user(self):
        user = yield self.create_test_user()
        self.assertEqual(user._id, self.valid_test_email)

    @gen_test
    def test_query_valid_test_user(self):
        user = yield self.query_user_with_id(self.valid_test_email)
        self.assertIsNotNone(user)

    @gen_test
    def test_query_invalid_test_user(self):
        user = yield self.query_user_with_id(self.invalid_test_email)
        self.assertFalse(user)


    ## TODO move this into base parent class
    @coroutine
    def tearDown(self):
        yield self.destroy_test_user()

    # Helper Functions
    ## TODO move this into base parent class
    @coroutine
    def create_test_user(self):
        user = User(
            _id="test@test.com",
            name="test"
            )
        user.save()
        return user

    @coroutine
    def destroy_test_user(self):
        user = yield self.query_user_with_id(self.valid_test_email)
        user.delete()

    @coroutine
    def query_user_with_id(self, email_id):
        query = User.objects(_id=email_id)
        return query
