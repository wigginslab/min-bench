import unittest2 as unittest
from routes.TrafficHandler import *
from tornado.gen import coroutine
from tornado.testing import *
from mongoengine import *


class TrafficFetchTest(AsyncTestCase):
    @coroutine
    def setUp(self):
        super(AsyncTestCase, self).setUp()
        self.io_loop = self.get_new_ioloop()
        self.io_loop.make_current()
        connect("min-bench")

        self.valid_user_email = "test@test.com"
        yield self.create_test_user()

    @gen_test
    def test_http_fetch(self):
        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch("http://localhost:3036/traffic", self.handle_request)
        # Test contents of response
        self.assertIn("DateRangeSelector", response.body)

    @gen_test
    def test_http_fetch_1(self):
        client = AsyncHTTPClient(self.io_loop)
        response = yield client.fetch("http://localhost:3036/traffic", self.handle_request)
        # Test contents of response
        self.assertIn("propertySelector", response.body)

    def handle_request(self, response):
        if response.error:
            print("Error : {}".format(response.error))
            print("Body : {}".format(response.body))
        else:
            print("Success")


    def tearDown(self):
        yield self.destroy_test_user()

    @coroutine
    def create_test_user(self):
        user = User(_id="test@test.com", name="test")
        user.save()
        return user

    @coroutine
    def destroy_test_user(self):
        user = yield self.retrieve_user_with_id(self.valid_test_email)
        user.delete()

if __name__ == "__main__":
    unittest.main()
