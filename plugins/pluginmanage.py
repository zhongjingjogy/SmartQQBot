#coding: utf-8
import re
from random import randint
from smartqq import (
    on_all_message,
    on_group_message,
    on_private_message
)

cmd_list_plugin = re.compile(r"!list_plugin")
cmd_deactivate = re.compile(r"!deactivate \{(.*?)\}")
cmd_activate = re.compile(r"!activate \{(.*?)\}")

@on_private_message
def pluginmanage(msg, bot, handler):
    """
    Not implemented yet.
    """
    admin_uin = 2711321953
    msg_id = randint(1, 10000)

    print("in plugin manage")

    if msg.from_uin != admin_uin:
        return

    # print msg
    response = None
    # activate
    result = re.findall(cmd_activate, msg.content)
    if result:
        reponse = handler.add_to_activation(result[0])
        if response:
            # bot.send_friend_msg(",".join(response), msg.from_uin, msg_id)
            return

    # deactivate
    result = re.findall(cmd_deactivate, msg.content)
    if result:
        reponse = handler.del_handler(result[0])
        if response:
            # bot.send_friend_msg(",".join(response), msg.from_uin, msg_id)
            return

    # print("deactivate result : %s" % result)
    # list plugins
    result = re.findall(cmd_list_plugin, msg.content)
    # print("list result : %s" % result)
    if result:
        response = handler.list_handlers()
        if response:
            bot.send_friend_msg(",".join(response), msg.from_uin, msg_id)
            return
