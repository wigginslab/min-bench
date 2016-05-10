from routes.BaseHandler import BaseHandler

class IndexHandler(BaseHandler):
    def get(self):
        if self.current_user:
            self.redirect("/main")
        else:
            self.render("index.html", title="Minimalistic Lean Workbench")
