#!/usr/bin/env python

import os

import tornado.ioloop
from tornado.web import RequestHandler, Application, asynchronous

class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html", title="Minimalistic Lean Workbench")

if __name__ == "__main__":
    dirname = os.path.dirname(__file__)
    settings = {
        "static_path" : os.path.join(dirname, "static"),
        "template_path" : os.path.join(dirname, "templates")
    }
    application = Application([
        (r"/", IndexHandler)
    ], **settings)

    application.listen(3036)
    tornado.ioloop.IOLoop.instance().start()
