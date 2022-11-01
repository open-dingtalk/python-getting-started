import json
import urllib.parse

from alibabacloud_dingtalk.oauth2_1_0.client import Client as dingtalkoauth2_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from Tea.exceptions import TeaException
import tornado.httpclient

from .oauth_models import DingtalkUserInfo


def create_client() -> dingtalkoauth2_1_0Client:
    config = open_api_models.Config()
    config.protocol = 'https'
    config.region_id = 'central'
    return dingtalkoauth2_1_0Client(config)


async def get_userinfo_by_authcode(access_token: str, code: str) -> DingtalkUserInfo:
    http = tornado.httpclient.AsyncHTTPClient()
    # 获取用户的ID信息
    body = json.dumps({
        "code": code,
    })
    url = ("https://oapi.dingtalk.com/topapi/v2/user/getuserinfo"
           + "?access_token=" + urllib.parse.quote_plus(access_token))
    response = await http.fetch(
        url,
        method="POST",
        headers={"Content-Type": "application/json"},
        body=body,
    )
    body = json.loads(response.body)
    error_code, error_message = body.get("errcode"), body.get("errmsg")
    if error_code and error_message:
        raise TeaException({
            "code": error_code,
            "message": error_message,
            "description": "request_id=%s" % body.get("request_id"),
        })
    result = body.get("result")
    user = DingtalkUserInfo()
    user.associated_unionid = result.get("associated_unionid")
    user.unionid = result.get("unionid")
    user.sys_level = result.get("sys_level")
    user.name = result.get("name")
    user.sys = result.get("sys")
    user.userid = result.get("userid")
    # 获取用户信息详情
    url = ("https://oapi.dingtalk.com/topapi/v2/user/get"
           + "?access_token=" + urllib.parse.quote_plus(access_token))
    body = json.dumps({
        "userid": user.userid,
    })
    response = await http.fetch(
        url,
        method="POST",
        headers={"Content-Type": "application/json"},
        body=body,
    )
    body = json.loads(response.body)
    error_code, error_message = body.get("errcode"), body.get("errmsg")
    if error_code and error_message:
        raise TeaException({
            "code": error_code,
            "message": error_message,
            "description": "request_id=%s" % body.get("request_id"),
        })
    result = body.get("result")
    user.avatar = result.get("avatar")
    return user
