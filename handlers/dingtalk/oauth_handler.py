# -*- coding: utf-8 -*-

import json
import urllib.parse
from typing import cast

import tornado.web
import tornado.escape

import dingtalk.oauth


class DingTalkOAuth2LoginHandler(tornado.web.RequestHandler,
                                 dingtalk.oauth.DingTalkOAuth2Mixin):
    _COOKIE_NAME_KEY = "user_cookie_name"

    async def get(self):
        auth_url = (
            urllib.parse.urljoin(self.request.full_url(), "/auth/login?next=")
            + tornado.escape.url_escape(self.get_argument("next", "/"))
        )
        if self.get_argument("authCode", False):
            code = self.get_argument("authCode")
            user = await self.get_authenticated_user(
                redirect_uri=auth_url,
                code=code)
            if not user:
                return

            handler = cast(tornado.web.RequestHandler, self)
            cookie_name = handler.settings[self._COOKIE_NAME_KEY]
            self.set_secure_cookie(cookie_name, json.dumps(user))
            self.redirect(self.get_argument("next", "/"))
            return
        else:
            self._OAUTH_AUTHORIZE_URL = "https://login.dingtalk.com/oauth2/auth"
            self.authorize_redirect(
                auth_url,
                client_id=self.settings["dingtalk_app"]["dt_app_info"]["app_key"],
                scope="openid",
                response_type="code",
                extra_params={"state": "mystage", "prompt": "consent"})
