#smartqqbot

Features
--------

* 插件热载入
* orm记录聊天记录

Quick Start
------------

1. setup.py 还没有写好，目前是通过运行main.py来启动QQ；
    ```
    python main.py --plugin config.json
    ```
2. config.json 中设置相关的配置信息,包括保存消息的数据库的位置，插件目录以及插件目录下的插件模块；
    ```
    {
        "dbhandler": "sqlite:///message-record.db",
        "plugin_root": "./plugins",
        "plugins": [
            "pluginmanage",
            "plugindemo"
        ]
    }
    ```
3. 插件模块目前只支持导入模块中与模块名相同的函数,如下例plugindemo.py中plugindemo函数会被导入。
    ```
    #coding: utf-8
    from random import randint
    import sys
    sys.path.append("../")
    from smartqq import (
        on_all_message,
        on_group_message,
        on_private_message
    )
    @on_private_message
    def plugindemo(msg, bot, handler):
        # print __file__
        # print("process message with %s" % "test1")
        # print("new test1.....")
        msg_id = randint(1, 10000)
        print type(msg.from_uin)
        print("activating the test1")
        print msg
        bot.send_friend_msg("yep, this is message from a smartqq bot, %d" % msg_id, 2895548428, msg_id)
        # if msg.from_uin == "3335494540":
        # bot.send_group_msg("recieved a message from group %s, the content is: %s" % (msg.from_uin, msg.content), 3335494540, msg_id)
        # print("modified test1")
        # print("add modified")
        # print("finish process message with %s" % "test1")
        pass
        ```
4. 和插件同名的函数需要接受三个参数，分别是msg, bot和handler。目前handler还有实质性的作用，设计用于让插件能够获取的管理模块。
5. 发送消息的功能，请参考bot.py中的函数，主要是发送群消息和好友消息两个函数。

TODO
----
* 设计插件的基类，实现从插件模块文件中导入类并产生类对象来处理消息。
