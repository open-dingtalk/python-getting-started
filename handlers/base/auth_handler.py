import json

import models.user
from .base_handler import BaseHandler


class AuthHandler(BaseHandler):
    _COOKIE_NAME_KEY = "user_cookie_name"

    def get_current_user(self):
        """返回当前登录的用户信息
        该方法是TornadoWeb框架的一部分，通过该方法返回的登录用户信息可以在相关的RequestHandler中获取
        详见TornadoWeb文档
        """
        login_user = models.user.LoginUser()
        user_agent = self.request.headers.get("User-Agent")
        if user_agent and "dingtalk" in user_agent.lower():
            # 这里返回一个非空对象，以避免进入OAuth2免登流程，而是在前端页面中通过JSAPI实现免登。
            return login_user

        cookie_name = self.settings[self._COOKIE_NAME_KEY]
        user_cookie = self.get_secure_cookie(cookie_name)
        if not user_cookie:
            return None
        user = json.loads(user_cookie)

        login_user.from_map(user)
        return login_user
