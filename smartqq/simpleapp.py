# -*- coding: utf-8 -*-
import argparse
import logging
import os
import socket
import sys

from bot.bot import QQBot
from bot.logger import logger
from bot.messages import mk_msg
from bot.exceptions import ServerResponseEmpty
from handler import Handler
from superhandler import SuperHandler
from plugin_manager import PluginManager
from model.dbhandler import DBHandler
from plugin_timer import PluginTimer

def start_qq(
        no_gui=False, new_user=False, debug=False,
        vpath="./v.jpg",
        smart_qq_refer="http://d1.web2.qq.com/proxy.html?v=20030916001&callback=1&id=2",
        cookie_file="cookie.data",
        plugin_setting={
            "plugin_root": "./plugins",
            "plugins": [
                "pluginmanage",
                "test1"
            ],
            "timers": [
                "timer_weather"
            ]
        },
        dbhandler='sqlite:///message-record.db',
    ):
    bot = QQBot(vpath, smart_qq_refer, cookie_file)

    # update the modules and enbale utf-8 decoding.
    reload(sys)
    sys.setdefaultencoding("utf-8")

    # set the mode for logger.
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # login
    bot.login(no_gui)

    # initialze the handler
    handler = SuperHandler(dbhandle=dbhandler, workers=5)
    handler.update_group_list(bot)
    logger.info("Update group list...")

    # dbhandler = DBHandler()
    # initialize the plugin manager
    plmanager = PluginManager(plugin_setting["plugin_root"])
    timermanager = PluginManager(plugin_setting["plugin_root"])
    # load the plugins
    for plugin_name in plugin_setting["plugins"]:
        # plmanager.add_plugin(plugin_name)
        try:
            plmanager.add_plugin(plugin_name)
        except Exception, e:
            print(e)
            logger.error("Failed to load plugin: %s" % plugin_name)
    for timer_name in plugin_setting["timers"]:
        try:
            timermanager.add_plugin(timer_name)
        except Exception, e:
            print(e)
            logger.error("Failed to load plugin: %s" % plugin_name)
    # register the plugins to the message handlers
    for (name, plugin) in plmanager.plugins.items():
        handler.add_handler(name, plugin)

    timers = {}
    for (name, plugin) in timermanager.plugins.items():
        t = PluginTimer(plugin, args=(bot, ), sleep=2)
        t.start()
        timers[name] = t

    logger.info("plugin available: %s" % plmanager.plugins.keys())
    # main loop, query new messages and handle them.
    while True:
        # query the plugins to be updated.
        try:
            tobeupdated = plmanager.update_plugin()
            if tobeupdated:
                logger.info("changes are detected...try to update: [%s]" % ",".join(tobeupdated))
            for each in tobeupdated:
                logger.info("update plugin: %s" % each)
                handler.update_handler(each, plmanager.plugins[each])
        except Exception, e:
            logger.error("Fail to update the plugins.")

        try:
            tobeupdated = timermanager.update_plugin()
            if tobeupdated:
                logger.info("changes are detected in timers...try to update: [%s]" % ",".join(tobeupdated))
            for each in tobeupdated:
                logger.info("update plugin: %s" % each)
                timers[each].stop()
                timers[each] = PluginTimer(timermanager.plugins[each], args=(bot, ), sleep=10)
                timers[each].start()
        except Exception, e:
            logger.error("Fail to update the plugins.")

        # update the activation list in the handler.
        try:
            handler.update_handlers(plmanager)
            # logger.info("update handlers....")
        except Exception, e:
            print(e)
            logger.info("Unable to update the handlers' list")

        try:
            # query new messages from the smart qq bot.
            msg_list = bot.check_msg()

            updated_msg = []
            if msg_list is not None:
                updated_msg = handler.handle_msg_list(
                    [mk_msg(msg) for msg in msg_list], bot
                )
            # if msg_list:
            #     # logging.debug("recording messages...")
            #     for each in updated_msg:
            #         dbhandler.insert_message(mk_msg(each))
            # logger.info("checking messages...")
        except ServerResponseEmpty:
            continue
        except (socket.timeout, IOError):
            logger.warning("Message pooling timeout, retrying...")
        except Exception:
            logger.exception("Exception occurs when checking msg.")

if __name__ == "__main__":
    start_qq()
