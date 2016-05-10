from routes.BaseHandler import BaseHandler
from tornado.web import authenticated

class WebsiteEditorHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render("websiteeditor.html", title="Use website editor")
