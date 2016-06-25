#coding=utf-8
import os
import json
import urllib2
import random

from smartqq import (
    on_all_message,
    on_group_message,
    on_private_message,
    on_from_uin_message
)
from smartqq import GroupMsg, PrivateMsg

class Chat(object):
    
    key = ""
    apiurl = "http://www.tuling123.com/openapi/api?"

    def init(self):
        pass

    def query(self, info):
        url = self.apiurl + 'key=' + self.key + '&' + 'info=' + info
        re = urllib2.urlopen(url).read()
        re_dict = json.loads(re)
        return re_dict['text']

def plugin_tuling(msg, bot, *args, **kwargs):

    msg_id = random.randint(1, 10000)
    response_list = [2488439125, 1705468594, 3931279346]

    # print("got from uin in repeat: %d" % msg.from_uin)
    if msg.from_uin not in response_list:
        return

    response = ""
    try:
        tulingbot = Chat()
        response = tulingbot.query(msg.content)
        print("response: %s" % response)
    except:
        print("Failed to query the tuling bot.")

    if not response: return

    if isinstance(msg, GroupMsg):
        bot.send_group_msg(response, msg.from_uin, msg_id)
    elif isinstance(msg, PrivateMsg):
        bot.send_friend_msg(response, msg.from_uin, msg_id)

if __name__ == "__main__":
    chat = Chat()
    chat.init()
    print chat.query("Hi!")
