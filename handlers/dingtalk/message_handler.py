# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import time
import uuid
import json

from Tea.exceptions import TeaException
from alibabacloud_dingtalk.robot_1_0.client import Client as dingtalkrobot_1_0Client
from alibabacloud_dingtalk.robot_1_0 import models as dingtalkrobot__1__0_models
from alibabacloud_dingtalk.im_1_0 import models as dingtalkim__1__0_models
from alibabacloud_dingtalk.im_1_0.client import Client as dingtalkim_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

import handlers.base
from dingtalk.oauth import token_manager


class MessageCardHandler(handlers.base.AuthHandler):
    async def post(self):
        payload = json.loads(str(self.request.body, "utf-8"))
        open_conversation_id = payload["openConversationId"]

        out_track_id = str(uuid.uuid4())
        headers = dingtalkim__1__0_models.SendInteractiveCardHeaders()
        token = await token_manager.get_token()
        headers.x_acs_dingtalk_access_token = token.access_token
        card_options = dingtalkim__1__0_models.SendInteractiveCardRequestCardOptions(
            support_forward=True
        )
        card_data_card_param_map = {
            "title": "开始下一个特性开发吧",
            "location": "钉钉应用开发平台",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # "2022-10-18 14:02:03",
        }
        card_data_card_media_id_param_map = {
        }
        card_data = dingtalkim__1__0_models.SendInteractiveCardRequestCardData(
            card_param_map=card_data_card_param_map,
            card_media_id_param_map=card_data_card_media_id_param_map,
        )
        request = dingtalkim__1__0_models.SendInteractiveCardRequest(
            card_template_id=self.settings["dingtalk_app"]["dt_interactive_cards"]["message_card_template_id_001"],
            open_conversation_id=open_conversation_id,
            out_track_id=out_track_id,
            robot_code=self.settings["dingtalk_app"]["dt_robot_info"]["code"],
            conversation_type=1,
            card_data=card_data,
            card_options=card_options,
            pull_strategy=False,
        )
        try:
            config = open_api_models.Config()
            config.protocol = "https"
            config.region_id = "central"
            client = dingtalkim_1_0Client(config)
            await client.send_interactive_card_with_options_async(
                request,
                headers,
                util_models.RuntimeOptions())
        except TeaException as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                logging.error("dingtalkim__1__0_models.SendInteractiveCardRequest failed, code=%s, message=%s",
                              err.code, err.message)
        self.write("ok")


class TopBoxHandler(handlers.base.AuthHandler):
    async def post(self):
        payload = json.loads(str(self.request.body, "utf-8"))
        open_conversation_id = payload["openConversationId"]
        out_track_id = str(uuid.uuid4())
        robot_code = self.settings["dingtalk_app"]["dt_robot_info"]["code"]

        private_data_value_key_card_media_id_param_map = {
            "key": "xxxx"
        }
        private_data_value_key_card_param_map = {
            "key": "wwhtxxxx"
        }
        private_data_value_key = dingtalkim__1__0_models.PrivateDataValue(
            card_param_map=private_data_value_key_card_param_map,
            card_media_id_param_map=private_data_value_key_card_media_id_param_map
        )
        private_data = {
            "privateDataValueKey": private_data_value_key
        }
        card_data_card_media_id_param_map = {
            "key": "sfrtxxxx"
        }
        card_data_card_param_map = {
            "progress": "30",
            "total": "10",
            "finished": "3",
            "unfinished": "7",
        }
        card_data = dingtalkim__1__0_models.InteractiveCardCreateInstanceRequestCardData(
            card_param_map=card_data_card_param_map,
            card_media_id_param_map=card_data_card_media_id_param_map
        )
        interactive_card_create_instance_request = dingtalkim__1__0_models.InteractiveCardCreateInstanceRequest(
            card_template_id=self.settings["dingtalk_app"]["dt_interactive_cards"]["top_card_template_id_001"],
            open_conversation_id=open_conversation_id,
            out_track_id=out_track_id,
            robot_code=robot_code,
            conversation_type=1,
            card_data=card_data,
            private_data=private_data,
        )
        headers = dingtalkim__1__0_models.SendInteractiveCardHeaders()
        token = await token_manager.get_token()
        headers.x_acs_dingtalk_access_token = token.access_token
        try:
            config = open_api_models.Config()
            config.protocol = "https"
            config.region_id = "central"
            client = dingtalkim_1_0Client(config)
            await client.interactive_card_create_instance_with_options_async(
                interactive_card_create_instance_request,
                headers,
                util_models.RuntimeOptions())
        except TeaException as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                logging.error("create instance error: code=%s, msg=%s", err.code, err.message)
                pass

        request = dingtalkim__1__0_models.TopboxOpenRequest(
            open_conversation_id=open_conversation_id,
            out_track_id=out_track_id,
            cool_app_code=self.settings["dingtalk_app"]["dt_cool_app_info_001"]["code"],
            expired_time=(int(time.time()) + 300) * 1000,
        )
        try:
            config = open_api_models.Config()
            config.protocol = "https"
            config.region_id = "central"
            client = dingtalkim_1_0Client(config)
            await client.topbox_open_with_options_async(
                request,
                headers,
                util_models.RuntimeOptions())
        except TeaException as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                logging.error("dingtalkim__1__0_models.TopboxOpenRequest failed, code=%s, msg=%s", err.code,
                              err.message)
                pass
        self.write("ok")


class TextMessageHandler(handlers.base.AuthHandler):
    async def post(self):
        token = await token_manager.get_token()
        robot_code = self.settings["dingtalk_app"]["dt_robot_info"]["code"]

        payload = json.loads(str(self.request.body, "utf-8"))
        open_conversation_id = payload["openConversationId"]
        content = json.dumps({"content": payload["txt"]})

        config = open_api_models.Config()
        config.protocol = "https"
        config.region_id = "central"
        client = dingtalkrobot_1_0Client(config)

        org_group_send_headers = dingtalkrobot__1__0_models.OrgGroupSendHeaders()

        org_group_send_headers.x_acs_dingtalk_access_token = token.access_token

        org_group_send_request = dingtalkrobot__1__0_models.OrgGroupSendRequest(
            msg_param=content,
            msg_key='sampleText',
            open_conversation_id=open_conversation_id,
            robot_code=robot_code,
            cool_app_code=self.settings["dingtalk_app"]["dt_cool_app_info_001"]["code"],
        )
        try:
            await client.org_group_send_with_options_async(org_group_send_request, org_group_send_headers,
                                                           util_models.RuntimeOptions())
        except TeaException as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                logging.error("dingtalkrobot__1__0_models.org_group_send_with_options_async failed, code=%s, msg=%s",
                              err.code, err.message)
        self.write({"result": "ok"})
