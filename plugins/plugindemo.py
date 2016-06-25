#coding=utf-8
from random import randint

from smartqq import (
    on_all_message,
    on_group_message,
    on_private_message,
    on_from_uin_message
)

@on_from_uin_message(100)
def plugindemo(msg, bot, handler):
    # print __file__
    # print("process message with %s" % "test1")
    # print("new test1.....")
    msg_id = randint(1, 10000)
    print type(msg.from_uin)
    # print("activating the test1")
    print msg
    # bot.send_friend_msg("yep, this is message from a smartqq bot, %d" % msg_id, 2895548428, msg_id)
    # if msg.from_uin == "3335494540":
    # bot.send_group_msg("recieved a message from group %s, the content is: %s" % (msg.from_uin, msg.content), 3335494540, msg_id)
    # print("modified test1")
    # print("add modified")
    # print("finish process message with %s" % "test1")
    pass
