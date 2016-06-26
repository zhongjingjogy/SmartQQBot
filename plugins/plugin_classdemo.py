#coding=utf-8
from random import randint
from baidutrans import BaiduFanyi
import json
from smartqq import (
    on_all_message,
    on_group_message,
    on_private_message,
    on_from_uin_message
)
from smartqq import GroupMsg, PrivateMsg

class plugin_classdemo(object):
    def __init__(self):
        pass
    def __setup__(self, *arg, **kwargs):
        pass
    def handle_msg(self, msg, bot, *arg, **kwargs):
        print("in plugin_classdemo activated...")
