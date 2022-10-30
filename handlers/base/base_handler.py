# -*- coding: utf-8 -*-

import logging

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass
