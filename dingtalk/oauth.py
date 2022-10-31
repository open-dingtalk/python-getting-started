#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import time
from typing import Any
from typing import Dict
from typing import Optional
from typing import cast
import json

from tornado.web import RequestHandler
import tornado.auth
import tornado.httpclient
import tornado.httputil


class AccessTokenModel(object):
    _REFRESH_INTERVAL_SECONDS = 5 * 60

    def __init__(self):
        self.access_token = None
        self.grant_time = None
        self.expire_time = None

    def update(self, access_token, expire_in):
        self.access_token = access_token
        self.grant_time = int(time.time())
        self.expire_time = self.grant_time + expire_in

    def is_valid(self):
        now = int(time.time())
        if (self.access_token
                and self.expire_time
                and self.grant_time
                and self.expire_time > now
                and self.grant_time + self._REFRESH_INTERVAL_SECONDS > now):
            return True
        return False


class StorageService(object):
    def __init__(self):
        self._token = None

    def save_token(self, token: AccessTokenModel):
        self._token = token

    def load_token(self) -> AccessTokenModel:
        return self._token


class DingTalkTokenManager(object):
    _OAUTH_ACCESS_TOKEN_URL = "https://api.dingtalk.com/v1.0/oauth2/accessToken"

    def __init__(self):
        self._oauth_setting = None
        self._storage_service = StorageService()

    def set_oauth_setting(self, oauth_setting):
        self._oauth_setting = oauth_setting

    def set_storage_service(self, storage_service):
        self._storage_service = storage_service

    async def get_token(self) -> AccessTokenModel:
        token = self._storage_service.load_token()
        if token and token.is_valid():
            return token

        http = tornado.httpclient.AsyncHTTPClient()
        body = json.dumps({
            "appKey": self._oauth_setting["client_id"],
            "appSecret": self._oauth_setting["client_secret"],
        })
        response = await http.fetch(
            self._OAUTH_ACCESS_TOKEN_URL,
            method="POST",
            headers={"Content-Type": "application/json"},
            body=body,
        )
        token_obj = json.loads(response.body)
        token = AccessTokenModel()
        token.update(token_obj["accessToken"], token_obj["expireIn"])
        self._storage_service.save_token(token)
        return token


token_manager = DingTalkTokenManager()


class DingTalkOAuth2Mixin(tornado.auth.OAuth2Mixin):
    _OAUTH_ACCESS_TOKEN_URL = "https://api.dingtalk.com/v1.0/oauth2/userAccessToken"
    _DINGTALK_APP_KEY = "dingtalk_app"

    def get_dingtalk_app_settings(self) -> Dict[str, str]:
        handler = cast(RequestHandler, self)
        return handler.settings[self._DINGTALK_APP_KEY]

    async def get_authenticated_user(
            self,
            redirect_uri: str,
            code: str,
            extra_fields: Optional[Dict[str, Any]] = None,
    ):
        app_settings = self.get_dingtalk_app_settings()
        token = await token_manager.get_token()

        body = json.dumps(dict(
            clientId=app_settings["dt_app_info"]["app_key"],
            clientSecret=app_settings["dt_app_info"]["app_secret"],
            code=code,
            grantType="authorization_code"
        ))
        http = self.get_auth_http_client()
        user_token = None
        try:
            response = await http.fetch(
                self._OAUTH_ACCESS_TOKEN_URL,
                method="POST",
                headers={"Content-Type": "application/json", "x-acs-dingtalk-access-token": token.access_token},
                body=body,
            )
            user_token = json.loads(response.body)
        except tornado.httpclient.HTTPError as e:
            logging.error("http fetch error, %s", e)
            return None
        user = None
        try:
            response = await http.fetch(
                "https://api.dingtalk.com/v1.0/contact/users/me",
                method="GET",
                headers={"Content-Type": "application/json", "x-acs-dingtalk-access-token": user_token["accessToken"]},
            )
            user = json.loads(response.body)
        except tornado.httpclient.HTTPError as e:
            logging.error("http fetch error, %s", e)
            return None
        return user

    def get_auth_http_client(self) -> tornado.httpclient.AsyncHTTPClient:
        return tornado.httpclient.AsyncHTTPClient()
