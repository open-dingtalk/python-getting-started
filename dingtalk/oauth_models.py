from alibabacloud_dingtalk.oauth2_1_0.models import GetUserTokenRequest
from alibabacloud_dingtalk.oauth2_1_0.models import GetSsoUserInfoRequest
from alibabacloud_dingtalk.oauth2_1_0.models import GetSsoUserInfoHeaders


class DingtalkUserInfo:
    """
    see: https://open.dingtalk.com/document/orgapp-server/obtain-the-userid-of-a-user-by-using-the-log-free
    """

    def __init__(self):
        self.associated_unionid = None
        self.unionid = None
        self.device_id = None
        self.sys_level = None
        self.name = None
        self.sys = None
        self.userid = None
        self.avatar = None

    def __str__(self):
        return f"DingtalkUserInfo(name={self.name}, userid={self.userid})"
