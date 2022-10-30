## 依赖

该指南假设你已经做好了一下准备工作：
1. 免费的应用开发者账号，可以直接用已有的钉钉账号。
2. 本地开放环境安装好Python 3.10版本，可以参考 Python 官网上各个平台的安装指南，[OS X](http://docs.python-guide.org/en/latest/starting/install3/osx/)、[Windows](http://docs.python-guide.org/en/latest/starting/install3/win/)以及 [Linux](http://docs.python-guide.org/en/latest/starting/install3/linux/)。
3. 可选安装[Git](https://git-scm.com/)，用于获取官方提供的示例代码，以便于快速启动开发。
4. 可选安装[Docker](https://www.docker.com/)，用于容器化构建和部署。

## 快速指南

可以参考以下步骤，在本地快速运行

1. 获取代码：`git clone git@gitlab.alibaba-inc.com:dingtalk-getting-started/python-getting-started.git`
2. 参考下一章节的配置描述，设置配置项
3. 安装依赖：`pip3 install -r requirements.txt`
4. 启动服务：`python3 app.py`

## 配置

开发者可以选择以下两种方式之一来设置该示例应用的配置项：

1. （推荐）符合云原生原则，通过环境变量设置，可灵活部署。该示例中已经提供了 Dockerfile，在不修改代码/配置情况下构建的镜像在启动时会自动读取环境变量中配置项；
2. 通过示例的配置文件创建 `cp settings.example.py settings.py`，然后修改 `settings.py` 文件；

| 环境变量 | 配置文件中的配置项 | 解释说明 |
|-----------|-------------------|----------|
| APP_COOKIE_SECRET | cookie_secret | 字符串，必填，非空值，建议填入长度16字节以上的任意随机字符串，用于生成加密的前端用户登录态 Cookie |
| APP_KEY | dt_app_info.app_key | 字符串，必填，钉钉开发者后台中创建企业内部应用后平台生成的AppKey |
| APP_SECRET | dt_app_info.app_secret | 字符串，必填，钉钉开发者后台中创建企业内部应用后平台生成的AppSecret，与上面的AppKey成对出现 |
| APP_ROBOT_CODE | dt_robot_info.code | 字符串，选填（在发消息流程中必填），钉钉开发者后台中创建机器人生成的RobotCode |
| APP_COOLAPP_CODE_001 | dt_cool_app_info_001.code | 字符串，选填（开发酷应用场景必填），在钉钉开发者后台创建酷应用后由平台生成。钉钉同一个应用下可以创建多个酷应用扩展 |
| APP_MESSAGE_TEMPLATE_001 | dt_interactive_cards.message_card_template_id_001 | 字符串，选填（发送酷应用聊天消息卡片场景中必填），在钉钉开发者后台的卡片搭建中生成**消息卡片**。钉钉同一个应用下可以创建多个消息卡片 |
| APP_TOP_TEMPLATE_001 | dt_interactive_cards.top_card_template_id_001 |  字符串，选填（发送酷应用聊天消息卡片场景中必填），在钉钉开发者后台的卡片搭建中生成**吊顶卡片**。钉钉同一个应用下可以创建多个吊顶卡片 |

## 规范

项目结构：https://docs.python-guide.org/writing/structure/
