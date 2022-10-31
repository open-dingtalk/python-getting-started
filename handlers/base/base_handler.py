# -*- coding: utf-8 -*-

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass
