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
class FriendInfo(object):
    def __init__(self, account, nick, uin, *args, **kwargs):
        self.account = account
        self.nickname = nick
        self.uin = uin

class SuperHandler(Handler):
    def __init__(self, dbhandle, workers=5):
        super(SuperHandler, self).__init__(workers=workers)
        self.group_list = {}
        self.friend_list = {} # account, uin, nickname
        self.dbhandler = DBHandler(dbhandle)
    def get_friendname_with_uid(self, from_uin):
        for each in self.friend_list:
            if from_uin == self.friend_list[each].account:
                return self.friend_list[each]
        return None
    def get_groupname_with_gid(self, from_uin):
        for each in self.group_list:
            if self.group_list[each].gid == from_uin:
                return each
        return None
    def update_message(self, msg, bot):
        if isinstance(msg, GroupMsg):
            flag = self.get_groupname_with_gid(msg.from_uin)
            res = False#self.get_friendname_with_uid(msg.send_uin)
            if flag:
                msg.name = flag
            else:
                msg.name = "unknown"
            if res:
                msg.nickname = res.nickname
                msg.send_account = res.account
            else:
                friend_list = []# bot.get_friend_info(msg.send_uin)
                if friend_list:
                    friend = FriendInfo(**friend_list)
                    self.dbhandler.insert_friend(friend_list)
                    msg.nickname = friend.nickname
                    msg.send_account = friend.account
                    self.friend_list[friend.account] = friend
            return msg
        elif isinstance(msg, PrivateMsg):
            res = self.get_friendname_with_uid(msg.from_uin)
            if res:
                msg.nickname = res.nickname
                msg.account = res.account
            else:
                friend_list = bot.get_friend_info(msg.from_uin)
                if friend_list:
                    friend = FriendInfo(**friend_list)
                    self.dbhandler.insert_friend(friend_list)
                    msg.nickname = friend.nickname
                    msg.account = friend.account
                    self.friend_list[friend.account] = friend
            return msg
        else:
            return msg
    def update_group_list(self, bot):
        return
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
            self.update_message(msg, bot)
            self.dbhandler.insert_message(msg)
            self._handle_one(msg, bot)

if __name__ == "__main__":
    t = SuperHandler()
