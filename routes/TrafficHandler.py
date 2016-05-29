from routes.BaseHandler import BaseHandler
from tornado.web import authenticated
from models.User import User

class TrafficHandler(BaseHandler):

    def get(self):
        if self.get_current_user() is None:
            email = 'test@test.com' 
        else:
            email = self.get_current_user()['email']
        user = User.objects.get(_id=email)
        print user.access_token
        self.render("traffic.html", access_token=user.access_token)
