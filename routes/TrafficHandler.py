from routes.BaseHandler import BaseHandler
from tornado.web import authenticated
from models.User import User

class TrafficHandler(BaseHandler):
    def get(self):
        user = User.objects.get(_id=self.get_current_user()['email'])
        self.render("traffic.html", access_token=user.access_token)