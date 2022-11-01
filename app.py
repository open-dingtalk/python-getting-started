#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import asyncio
import logging
import os.path

import tornado.web

import dingtalk.oauth
import handlers
import handlers.base
import handlers.dingtalk
import settings

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def make_app():
    settings.update_from_env()
    oauth_setting = {
        "client_id": settings.app_settings["dt_app_info"]["app_key"],
        "client_secret": settings.app_settings["dt_app_info"]["app_secret"],
    }
    dingtalk.oauth.token_manager.set_oauth_setting(oauth_setting)
    dingtalk.oauth.token_manager.set_storage_service(dingtalk.oauth.StorageService())

    return tornado.web.Application([
        (r"/api/getUserInfo", handlers.dingtalk.JsapiUserInfoHandler),
        (r"/api/getUserInfoOAuth2", handlers.dingtalk.OAuth2UserInfoHandler),
        (r"/auth/login", handlers.dingtalk.DingTalkOAuth2LoginHandler),
        (r"/api/sendText", handlers.dingtalk.TextMessageHandler),
        (r"/api/sendMessageCard", handlers.dingtalk.MessageCardHandler),
        (r"/api/sendTopCard", handlers.dingtalk.TopBoxHandler),
        (r"/", handlers.MainHandler),
        (r"/index.html", handlers.MainHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(PROJECT_ROOT, "static")})
    ],
        login_url="/auth/login",
        template_path="./templates",
        cookie_secret=settings.app_settings["cookie_secret"],
        user_cookie_name="login_user",
        dingtalk_oauth=oauth_setting,
        dingtalk_app=settings.app_settings)


async def main():
    logging.basicConfig(format="%(asctime)s %(filename)s(%(lineno)s): %(levelname)-5s %(message)s", level=logging.INFO)
    port = 7001
    logging.info("listen port %d", port)

    app = make_app()
    app.listen(port)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
