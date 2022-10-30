# -*- coding: utf-8 -*-

import os

app_settings = {
    "cookie_secret": "",
    "dt_app_info": {
        "app_key": "your-app-key",
        "app_secret": "your-app-secret",
    },
    "dt_robot_info": {
        "code": "your-robot-code",
    },
    "dt_cool_app_info_001": {
        "code": "your-cool-app-code",
    },
    "dt_interactive_cards": {
        "message_card_template_id_001": "your-message-card-template-id",
        "top_card_template_id_001": "your-top-card-template-id",
    },
}

def update_from_env():
    app_settings["cookie_secret"] = os.getenv(
        "APP_COOKIE_SECRET",
        app_settings["cookie_secret"]
    )
    app_settings["dt_app_info"]["app_key"] = os.getenv(
        "APP_KEY",
        app_settings["dt_app_info"]["app_key"]
    )
    app_settings["dt_app_info"]["app_secret"] = os.getenv(
        "APP_SECRET",
        app_settings["dt_app_info"]["app_secret"]
    )
    app_settings["dt_robot_info"]["code"] = os.getenv(
        "APP_ROBOT_CODE",
        app_settings["dt_robot_info"]["code"]
    )
    app_settings["dt_cool_app_info_001"]["code"] = os.getenv(
        "APP_COOLAPP_CODE_001",
        app_settings["dt_cool_app_info_001"]["code"]
    )
    app_settings["dt_interactive_cards"]["message_card_template_id_001"] = os.getenv(
        "APP_MESSAGE_TEMPLATE_001",
        app_settings["dt_interactive_cards"]["message_card_template_id_001"]
    )
    app_settings["dt_interactive_cards"]["top_card_template_id_001"] = os.getenv(
        "APP_TOP_TEMPLATE_001",
        app_settings["dt_interactive_cards"]["top_card_template_id_001"]
    )
