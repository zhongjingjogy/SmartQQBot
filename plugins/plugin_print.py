#coding=utf-8
from random import randint

from smartqq import (
    on_all_message,
    on_group_message,
    on_private_message,
    on_from_uin_message
)
from smartqq import GroupMsg, PrivateMsg

def plugin_print(msg, bot, *args, **kwargs):
    print msg
    print("plugin print activated")
