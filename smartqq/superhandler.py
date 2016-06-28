# coding: utf-8
from collections import defaultdict, namedtuple
from Queue import Queue
from threading import Thread
import types

from bot.bot import QQBot
from bot.logger import logger
from bot.exceptions import (
    MsgProxyNotImplementError,
    InvalidHandlerType,
)
from bot.messages import PrivateMsg, GroupMsg
from bot.messages import MSG_TYPE_MAP
from handler import Handler
from model.dbhandler import DBHandler
RAW_TYPE = "raw_message"

MSG_TYPES = MSG_TYPE_MAP.keys()
MSG_TYPES.append(RAW_TYPE)

class GroupInfo(object):
    def __init__(self, name, gid, *args, **kwargs):
        self.name = name
        self.gid = gid

class SuperHandler(Handler):
    def __init__(self, dbhandle, workers=5):
        super(SuperHandler, self).__init__(workers=workers)
        self.group_list = {}
        self.dbhandler = DBHandler(dbhandle)
    def get_groupname_with_gid(self, from_uin):
        for each in self.group_list:
            if self.group_list[each].gid == from_uin:
                return each
        return None
    def update_message(self, msg):
        if not isinstance(msg, GroupMsg): msg
        flag = self.get_groupname_with_gid(msg.from_uin)
        if flag:
            msg.name = flag
        else:
            msg.name = "unknown"
        return msg
    def update_group_list(self, bot):
        groupinfos = bot.get_group_list_with_group_code()
        self.group_list = {}
        if not groupinfos: return
        for each in groupinfos:
            g = GroupInfo(**each)
            if g.name not in self.group_list:
                self.group_list[g.name] = g
    def handle_msg_list(self, msg_list, bot):
        """
        :type msg_list: list or tuple
        """
        for msg in msg_list:
            self.update_message(msg)
            self.dbhandler.insert_message(msg)
            self._handle_one(msg, bot)

if __name__ == "__main__":
    t = SuperHandler()
