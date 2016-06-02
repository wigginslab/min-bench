import unittest2 as unittest
from routes.BaseHandler import *
from routes.TrafficHandler import *
from models.User import *
from tornado.gen import coroutine
from tornado.testing import *
from mongoengine import *
import settings
from app import *

class TestTrafficHandler(AsyncHTTPTestCase):

    def get_app(self):

        client = MongoClient()
        database = client.min_bench
        connect("min-bench")

        settings_dict = {
            "static_path": settings.STATIC_PATH,
            "template_path": settings.TEMPLATE_PATH,
            "login_url": "/auth/login/",
            "debug": settings.DEBUG,
            "cookie_secret": settings.COOKIE_SECRET,
            "google_oauth": {"key": settings.GAUTH_CLIENT_ID,
                             "secret": settings.GAUTH_CLIENT_SECRET},
            "database": database,
            "messages": []
        }

        application = Application([
            (r"/", IndexHandler),
            (r"/auth/login/?", AuthLoginHandler),
            (r"/auth/logout/?", AuthLogoutHandler),
            (r"/learn/?", LearnMoreHandler),
            (r"/traffic/?", TrafficHandler),
            (r"/main/?", OnboardingHandler),
            (r"/edit/?", UserHandler),
            (r"/websitecreator/?", WebsiteCreatorHandler),
            (r"/websiteeditor/?", WebsiteEditorHandler)
        ], **settings_dict)

        return application

    @gen_test
    def test_http_fetch(self):
        response = yield self.fetch("/traffic")
        self.assertIn("chart-container", response.body)

if __name__ == "__main__":
    unittest.main()
