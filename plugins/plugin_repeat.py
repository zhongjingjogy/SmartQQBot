#coding=utf-8
from random import randint

from smartqq import (
    on_all_message,
    on_group_message,
    on_private_message,
    on_from_uin_message
)
from smartqq import GroupMsg, PrivateMsg

syms = ["*", "&", "$", "@", "#", "+", "-", "!"]

# @on_from_uin_message(393127934)
def plugin_repeat(msg, bot, *args, **kwargs):

    msg_id = randint(1, 10000)
    response_list = [1705468594,]

    # print("got from uin in repeat: %d" % msg.from_uin)
    if msg.from_uin not in response_list:
        return

    if isinstance(msg, GroupMsg):
        bot.send_group_msg("%s (啊刀扣篮好营 好营)" % msg.content, msg.from_uin, msg_id)
    elif isinstance(msg, PrivateMsg):
        bot.send_friend_msg("%s %s" % (msg.content, "..."), msg.from_uin, msg_id)
