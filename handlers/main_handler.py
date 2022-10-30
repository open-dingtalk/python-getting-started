# -*- coding: utf-8 -*-


import logging

from Tea.exceptions import TeaException
from alibabacloud_dingtalk.im_1_0 import models as dingtalkim__1__0_models
from alibabacloud_dingtalk.im_1_0.client import Client as dingtalkim_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
import tornado.web

from dingtalk.oauth import token_manager
import handlers.base


class MainHandler(handlers.base.AuthHandler):
    @tornado.web.authenticated
    async def get(self):
        # {"nick": "\u67ef\u6770", "unionId": "xbCad0RVEC8iE", "avatarUrl": "https://static-legacy.dingtalk.com/media/lADPDhJz2AydBOLNBOXNBOU_1253_1253.jpg", "openId": "qLCJ0jFaSloiE"}
        group_info = None

        if self.get_argument("openConversationId", False):
            cid = self.get_argument("openConversationId").replace(" ", "+")
            config = open_api_models.Config()
            config.protocol = "https"
            config.region_id = "central"
            client = dingtalkim_1_0Client(config)
            header = dingtalkim__1__0_models.GetSceneGroupInfoHeaders()
            token = await token_manager.get_token()
            header.x_acs_dingtalk_access_token = token.access_token

            request = dingtalkim__1__0_models.GetSceneGroupInfoRequest(
                open_conversation_id=cid,
                cool_app_code=self.settings["dingtalk_app"]["dt_cool_app_info_001"]["code"],
            )
            try:
                response = await client.get_scene_group_info_with_options_async(
                    request,
                    header,
                    util_models.RuntimeOptions())
                group_info = response.body
            except TeaException as err:
                if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                    logging.error("GetSceneGroupInfoRequest(), code=%s, msg=%s" % (err.code, err.message))
                    pass
        self.render("home.html", group_info=group_info)
