from routes.BaseHandler import BaseHandler
from tornado.web import authenticated
from tornado.gen import coroutine

class VCMatcherHandler(BaseHandler):
    # TODO Get route should return
    # Top 10 investors from Market
    # https://angel.co/markets
    @authenticated
    @coroutine
    def get(self):
        self.render("vcmatcher.html", title="VC Matcher")


## TODO
## Helper function to create models from response
## def create_investor_models():
