from routes.BaseHandler import BaseHandler

class LearnMoreHandler(BaseHandler):
    def get(self):
        self.render("learnmore.html", title="Learn more about LeanWorkbench")
