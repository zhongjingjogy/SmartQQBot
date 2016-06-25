#coding=utf-8
from bot.messages import (
    GROUP_MSG,
    PRIVATE_MSG
)

def default_handle(*args, **kwargs):
    # print("process message with the default handler")
    pass

def message_filter(key, value=None):
    def function_decorate(func):
        def wrap_func(*args, **kwargs):
            if value == getattr(kwargs["msg"], key):
                return func(*args, **kwargs)
            else:
                return default_handle(*args, **kwargs)
        return wrap_func
    return function_decorate

on_group_message = message_filter("msg_type", GROUP_MSG)
on_private_message = message_filter("msg_type", PRIVATE_MSG)

def on_all_message(func):
    def wrap_func(*args, **kwargs):
        return func(*args, **kwargs)
    return wrap_func

def on_from_uin_message(value):
    def function_decorate(func):
        @message_filter("from_uin", value=value)
        def wrap_func(*args, **kwargs):
            return func(*args, **kwargs)
        return wrap_func
    return function_decorate
