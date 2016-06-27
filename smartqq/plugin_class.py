#coding=utf-8
from random import randint
from smartqq import (
    on_all_message,
    on_group_message,
    on_private_message,
    on_from_uin_message
)
from smartqq import GroupMsg, PrivateMsg

class ClassPluginBase(object):
    def __init__(self):
        self.admin = None
        self.on_msg_type = set()
        self.on_from_uin = set()
        self.passwd = None
    def set_admin(self, admin):
        self.admin = admin
    def set_passwd(self, passwd):
        self.passwd = passwd
    def add_msgtype(self, msgtype):
        self.on_msg_type.add(msgtype)
    def add_fromuin(self, from_uin):
        self.on_from_uin.add(from_uin)
    def is_admin(self, uin):
        return uin == self.admin
    def is_onmsgtype(self, msgtype):
        return msgtype in self.on_msg_type
    def is_onfromuin(self, from_uin):
        return from_uin in self.on_from_uin
    def is_passwd(self, passwd):
        return passwd == self.passwd
    def handle_msg(self, msg, bot, *args, **kwargs):
        pass

if __name__ == "__main__":
    a = ClassPluginBase()
