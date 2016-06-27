#coding=utf-8
import threading
import time
from random import randint
import re
from tuling import tuling

def timer_weather(bot, *args, **kwargs):
    msg_id = randint(1, 10000)
    tulingbot = tuling(key="765021d90185a0c435eda69cbda836ca")
    bot.send_friend_msg(tulingbot.query("长沙天气"), 2055195329, msg_id)
    bot.send_group_msg(tulingbot.query("长沙天气"), 535551415, msg_id)
    time.sleep(1)
    bot.send_gruop_msg(tulingbot.query("上海天气"), 535551415, msg_id)
    time.sleep(1)
    bot.send_gruop_msg(tulingbot.query("岳阳天气"), 535551415, msg_id)
    return 6*60*60
