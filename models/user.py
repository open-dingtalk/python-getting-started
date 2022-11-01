class LoginUser:
    """当前登录用户的属性信息
    包括用户的姓名、头像等信息。区别于钉钉等平台返回的用户信息，原因是该工程的交互与钉钉等平台解耦合
    """
    def __init__(self):
        # 当前登录用户的名称，尽量取用户的真实姓名而不是昵称
        # 备注：非企业用户，也即个人用户场景中，缺乏真实姓名信息时候以昵称代替
        self.name = None
        # 用户头像URL，可能为空（用户未上传头像的场景）
        self.avatar = None
        # 用户在当前钉钉开放平台账号范围内的唯一标识，
        # 详见文档：https://open.dingtalk.com/document/org/basic-concepts
        self.unionid = None

    def to_map(self):
        """返回map信息，方便将该对象转为json"""
        return {
            "name": self.name,
            "avatar": self.avatar,
            "unionid": self.unionid,
        }

    def from_map(self, user):
        self.name = user.get("name") or ""
        self.avatar = user.get("avatar") or ""
        self.unionid = user.get("unionid") or ""
