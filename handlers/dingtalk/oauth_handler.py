# -*- coding: utf-8 -*-

import json
import logging
import urllib.parse
from typing import cast

import tornado.web
import tornado.escape
from alibabacloud_tea_util.client import Client as UtilClient
from Tea.exceptions import TeaException

import dingtalk.oauth
import dingtalk.oauth_client
import dingtalk.oauth_models
import handlers.base
import models.user


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
            login_user = models.user.LoginUser()
            login_user.name = user.get("nick")
            login_user.avatar = user.get("avatarUrl")
            login_user.unionid = user.get("unionId")
            self.set_secure_cookie(cookie_name, json.dumps(login_user.to_map()))
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


class JsapiUserInfoHandler(handlers.base.BaseHandler):
    """
    获取用户信息的接口一（共两个）：
    在钉钉端内，通过JSAPI拿到AuthCode后，通过AuthCode获取用户信息
    """
    _COOKIE_NAME_KEY = "user_cookie_name"

    async def get(self):
        logging.info("url: %s", self.request.full_url())
        code = self.get_argument("requestAuthCode")
        token = await dingtalk.oauth.token_manager.get_token()
        userinfo = None
        # 获取用户ID和Name
        try:
            userinfo = await dingtalk.oauth_client.get_userinfo_by_authcode(
                access_token=token.access_token,
                code=code,
            )
        except TeaException as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                logging.error("get_user_token_async failed, code=%s, message=%s", err.code, err.message)
        # 获取用户头像等更详细信息

        # 设置登录态cookie并返回用户信息
        login_user = models.user.LoginUser()
        login_user.name = userinfo.name
        login_user.avatar = userinfo.avatar
        login_user.unionid = userinfo.unionid
        handler = cast(tornado.web.RequestHandler, self)
        cookie_name = handler.settings[self._COOKIE_NAME_KEY]
        self.set_secure_cookie(cookie_name, json.dumps(login_user.to_map()))
        self.write({
            "data": login_user.to_map(),
        })


class OAuth2UserInfoHandler(handlers.base.AuthHandler):
    """
    获取用户信息的接口二（共两个）：
    在钉钉端外（浏览器场景），通过Oauth2拿到AuthCode后，通过AuthCode获取用户信息
    备注：已经通过TornadoWeb框架的OAuth2能力完成免登集成，此处直接返回用户信息即可
    """

    @tornado.web.authenticated
    async def get(self):
        self.write({
            "data": self.current_user.to_map(),
        })
