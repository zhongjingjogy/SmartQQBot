#coding=utf-8
from random import randint

from smartqq import (
    on_all_message,
    on_group_message,
    on_private_message
)

from smartqq import GroupMsg, PrivateMsg

@on_all_message
def plugin_repeat(msg, bot, handler):

    msg_id = randint(1, 10000)
    response_list = [3931279346, ]
    print("got from uin in repeat: %d" % msg.from_uin)    
    if msg.from_uin not in response_list:
        return
    
    if isinstance(msg, GroupMsg):
        bot.send_group_msg(msg.content, msg.from_uin, msg_id)
    elif isinstance(msg, PrivateMsg):
        bot.send_friend_msg(msg.content, msg.from_uin, msg_id)
