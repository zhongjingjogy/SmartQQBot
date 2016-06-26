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
from smartqq import GroupMsg, PrivateMsg, ClassPluginBase

class plugin_classdemo(ClassPluginBase):
    def __init__(self):
        super(plugin_classdemo, self).__init__()
        self.__setup__()
    def __setup__(self, *arg, **kwargs):
        self.set_admin(2055195329)
        print("admin is set as %d" % self.admin)
    def handle_msg(self, msg, bot, *arg, **kwargs):
        if msg.from_uin != self.admin:
            return
        print(msg)
        print(type(msg.content))
        print("in plugin_classdemo activated...")
