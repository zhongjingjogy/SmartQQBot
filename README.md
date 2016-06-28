#smartqqbot

友情提示
-------
项目来至：[Yinzo/SmartQQBot](https://github.com/Yinzo/SmartQQBot),这里主要是重构了一下项目结构和插件机制，感谢该项目的作者和贡献者。正在重做原项目的插件，要是能够实现到原项目的程度，会申请一下pull request到原项目中。。。

Features
--------

* 插件热载入
* 将类作为插件导入
* orm记录聊天记录
* 计时功能
* 更多特性请走上访传送门了解原来项目。

安装及使用
-------
* 安装到系统库(生产环境慎用,建议virtualenv创建相应环境)
```
python setup.py install
```
* 使用时，新建config.json和plugins文件夹。
    * 在config.json中配置数据库路径，插件根目录以及插件名称；
    * 在plugins中放置作为插件脚本的python文件,记得添加\_\_init\_\_.py文件；
    * 插件脚本中的处理函数需要和脚本名称同名,也要和config.json中声明的plugins相一致.
* 第一次启动时需要创建记录聊天记录数据库。命令行执行smartqq --create，该操作会读取config.json的数据设置，然后创建相应的数据库。
* 聊天记录查看请命令行执行smartqq --list.(发现一个管理sqlite数据库的好软件,http://sqlitebrowser.org/).

使用说明
------------

* 可以通过运行main.py来启动QQ，这时不需要把这个库安装到系统库；
```
python main.py --create/--list
python main.py --plugin config.json
python main.py --plugin config.json --no-gui
```
* config.json 中设置相关的配置信息,包括保存消息的数据库的位置，插件目录以及插件目录下的插件模块；
```
{
    "dbhandler": "sqlite:///message-record.db",
    "plugin_root": "./plugins",
    "plugins": [
        "pluginmanage",
        "plugindemo",
        "plugin_repeat"
    ],
    "timers": [
        "timer_weather"    
    ]
}
```
* 插件模块目前只支持导入模块中与模块名相同的函数,如下例plugindemo.py中plugindemo函数会被导入。
* 目前默认传递给插件函数的参数有三个，分别是msg, bot和handler。目前handler还有实质性的作用，设计用于让插件能够获取的管理模块。自定义插件时请注意参数个数至少为三个，如果只需要用到bot和msg的话请添加\*arg, \*\*kwargs在函数参数列表中。
* 发送消息的功能，请参考bot.py中的函数，主要是发送群消息和好友消息两个函数。

可用插件
-------
* 插件管理,pluginmanager
* 复读机,plugin_repeat
* 图灵机器人,plugin_tuling(需要自行申请key,加到代码里面就行了).

热载入插件说明
-------------
* 基本的思路是在第一次导入插件是检测插件对应文件的修改时间，然后在每次处理消息以后查询插件当前的修改时间，并与记录值对比。如果当前修改时间较新，那么插件模块将会被reload，存储的消息处理函数也会被更新。
* 支持运行时添加插件，请确保pluginmanage插件已经打开并且设置正确的admin_uin。在plugins文件夹中正确部署插件脚本后，利用admin_uin对应的用户向被运行的QQ发送!activate {plugin_name}。

自定义插件说明
-------------
需要修改两个地方：
* 在config.json的plugins中注册插件名称。
* 在plugins文件夹中新建与插件同名的python文件。
以下是一个简单复读插件的实现过程，插件名为plugin_repeat。
* 创建config.json,注册插件；
```
{
    "dbhandler": "sqlite:///message-record.db",
    "plugin_root": "./plugins",
    "plugins": [
        "plugin_repeat"
    ]
}
```
* plugin_root对应当前文件夹下的一个plugins文件夹，在其中创建plugin_repeat.py。
```
#coding=utf-8
# >plugin_repeat.py<

from random import randint
from smartqq import (
    on_all_message,
    on_group_message,
    on_private_message,
    on_from_uin_message
)
@on_private_message
def plugindemo(msg, bot, *args, **kwargs):
    msg_id = randint(1, 10000)
    response_list = [3931279346, 1705468594]

    print("got from uin in repeat: %d" % msg.from_uin)
    if msg.from_uin not in response_list:
        return

    if isinstance(msg, GroupMsg):
        bot.send_group_msg("%s ..." % msg.content, msg.from_uin, msg_id)
    elif isinstance(msg, PrivateMsg):
        bot.send_friend_msg("%s ..." % msg.content, msg.from_uin, msg_id)
```

定时插件说明
------------
插件定义方式与一般插件类似,声明插件请在config.json中的timers字段增加.
* 目前只运行用户定义函数,即在plugin_root对应的文件夹中定义插件,并在其中定义要定时执行的函数.
* 默认触发时间为2秒,如果需要更改,请在执行函数中添加返回值(单位秒).
* 第一次触发为导入计时插件两秒后.

定义插件类处理消息
-----------------
定义方式与函数定义方式类似.
* 类名必须与插件名一致
* 必须包含handle_msg这个类成员函数,并且定义为
类插件的作用
* 可以记录消息,而不用依赖与全局变量;
* 可以自定义复杂行为.
```
#coding=utf-8
from random import randint
from baidutrans import BaiduFanyi
import json
from smartqq import (
    on_all_message,
    on_group_message,
    on_private_message,
    on_from_uin_message
)
from smartqq import GroupMsg, PrivateMsg

class plugin_classdemo(object):
    def __init__(self):
        pass
    def __setup__(self, *arg, **kwargs):
        pass
    def handle_msg(self, msg, bot, *arg, **kwargs):
        print("in plugin_classdemo activated...")
```

插件消息过滤
--------
在插件中可以自定义比较复杂的过滤规则，但是一般的过滤基本是根据消息类型和发送者等信息来进行。在smartqq中提供了一些预定义的修饰函数来进行简单的过滤。
* 只处理群消息，@on_group_message
* 只处理私有信息，@on_private_message
* 只处理特定from_uin的消息，@on_from_uin_message(from_uin)

常见问题
-------
* windows下PIL模块不能正在显示二维码，此时需要在启动选项中加入--no-gui来后台下载二维码。

TODO
----
