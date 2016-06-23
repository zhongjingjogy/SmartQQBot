#smartqqbot

友情提示
-------
项目来至：[Yinzo/SmartQQBot](https://github.com/Yinzo/SmartQQBot),这里主要是重构了一下项目结构和插件机制，感谢该项目的作者和贡献者。正在重做原项目的插件，要是能够实现到原项目的程度，会申请一下pull request到原项目中。。。

Features
--------

* 插件热载入
* orm记录聊天记录
* 更多特性请走上访传送门了解原来项目。

安装及使用说明
-------
1. 安装到系统库中，python setup.py install。
2. 使用时，新建config.json和plugins文件夹。然后根据上面的示例配置数据库路径，插件根目录以及插件名称；在plugins中要有__init__.py文件；在plugins里面新建python文件，并在文件中编写同名的处理消息的函数。
3. 创建记录聊天记录数据库请使用smartqq --create，该操作会读取config.json的数据设置，然后创建相应的数据库。

Quick Start
------------

* 可以通过运行main.py来启动QQ；
```
python main.py --plugin config.json
```
* config.json 中设置相关的配置信息,包括保存消息的数据库的位置，插件目录以及插件目录下的插件模块；
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
* 插件模块目前只支持导入模块中与模块名相同的函数,如下例plugindemo.py中plugindemo函数会被导入。
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
* 和插件同名的函数需要接受三个参数，分别是msg, bot和handler。目前handler还有实质性的作用，设计用于让插件能够获取的管理模块。
* 发送消息的功能，请参考bot.py中的函数，主要是发送群消息和好友消息两个函数。

常见问题
-------
* windows下PIL模块不能正在显示二维码，此时需要在启动选项中加入--no-gui来后台下载二维码。

TODO
----
* 设计插件的基类，实现从插件模块文件中导入类并产生类对象来处理消息。
