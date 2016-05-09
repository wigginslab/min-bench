from routes.BaseHandler import BaseHandler
from tornado.web import authenticated

class WebsiteCreatorHandler(BaseHandler):
    @authenticated
    def get(self):
        self.render("websitecreator.html",
                    title="Create a website through LeanWorkbench")

    def post(self):
        # TODO: validation for all arguments
        company_name = self.get_argument("companyname")
        company_short_desc = self.get_argument("companyshortdesc")
        website_template_type = self.get_argument("templatetype")

        database = self.settings["database"]
        user = self.get_current_user()
        database.websites.insert_one({ "owner" : user["email"],
                                       "company_name" : company_name,
                                       "template_type" : website_template_type })

        # caching
        self.settings["messages"].append(
            "Modified wesite '{0}'".format(company_name)
        )

        # TODO: redirect to already created website
        self.redirect("/websiteeditor")
