import json

from .base_handler import BaseHandler


class AuthHandler(BaseHandler):
    _COOKIE_NAME_KEY = "user_cookie_name"
    def get_current_user(self):
        cookie_name = self.settings[self._COOKIE_NAME_KEY]
        user_cookie = self.get_secure_cookie(cookie_name)
        if not user_cookie:
            return None
        return json.loads(user_cookie)
