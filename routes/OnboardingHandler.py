from routes.BaseHandler import BaseHandler
from tornado.web import authenticated

from tornado.gen import coroutine

class OnboardingHandler(BaseHandler):
    @authenticated
    @coroutine
    def get(self):
        show_onboarding = yield self.current_user_completed_onboarding()
        if show_onboarding:
            self.render("onboarding.html", title="Minimalistic Lean Workbench")
        else:
            self.render("accountsetup.html", title="Finish Account Setup", user={})
