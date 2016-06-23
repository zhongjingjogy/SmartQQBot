#coding=utf-8
from bot.messages import (
    GROUP_MSG,
    PRIVATE_MSG
)

def default_handle(msg, bot, handler):
    # print("process message with the default handler")
    pass

"""
message_decorate : set a filter for a plugin;
function_decorate : the decorator.
wrap_func : wrap the decorated function according to the message type.
"""
def message_decorate(msg_type):
    def function_decorate(func):
        def wrap_func(msg, bot, handler):
            if msg_type == "all":
                return func(msg, bot, handler)
            elif msg.type == msg_type:
                return func(msg, bot, handler)
            else:
                return default_handle(msg, bot, handler)
        return wrap_func
    return function_decorate

# wrap the message decorator into different filters.
on_all_message = message_decorate("all")
on_group_message = message_decorate(GROUP_MSG)
on_private_message = message_decorate(PRIVATE_MSG)
