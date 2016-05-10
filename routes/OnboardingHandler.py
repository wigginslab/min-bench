from routes.BaseHandler import BaseHandler
from tornado.web import authenticated

class OnboardingHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render("onboarding.html",
                    title="Minimalistic Lean Workbench")
        self.settings["messages"] = []
