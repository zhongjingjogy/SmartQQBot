#coding: utf-8
import re
from random import randint

cmd_list_plugin = re.compile(r"!list_plugin")
cmd_deactivate = re.compile(r"!deactivate \{(.*?)\}")
cmd_activate = re.compile(r"!activate \{(.*?)\}")

def pluginmanage(msg, bot, handler):
    """
    Not implemented yet.
    """
    print(handler.list_handlers())
    msg_id = randint(1, 10000)

    # print msg
    response = None
    # activate
    result = re.findall(cmd_activate, msg.content)
    if result:
        reponse = handler.add_handler(result[0])

    # deactivate
    result = re.findall(cmd_deactivate, msg.content)
    if result:
        reponse = handler.del_handler(result[0])

    # list plugins
    result = re.findall(cmd_list_plugin, msg.content)
    if result:
        reponse = handler.list_handlers()

    if response:
        bot.reply_msg(msg, reponse)
