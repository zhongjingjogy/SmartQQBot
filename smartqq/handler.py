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
from bot.messages import MSG_TYPE_MAP

RAW_TYPE = "raw_message"

MSG_TYPES = MSG_TYPE_MAP.keys()
MSG_TYPES.append(RAW_TYPE)

Handler = namedtuple("Handler", ("func", "name"))
Task = namedtuple("Task", ("func", "name", "cls", "kwargs"))

class Worker(Thread):

    def __init__(
            self, queue, group=None,
            target=None, name=None, args=(),
            kwargs=None, verbose=None,
    ):
        """
        :type queue: Queue
        """
        super(Worker, self).__init__(
            group, target, name, args, kwargs, verbose
        )
        self.queue = queue
        self._stopped = False
        self.worker_timeout = 20
        self._stop_done = False

    def run(self):
        while True:
            if self._stopped:
                break
            task = self.queue.get()
            if task.func:
                try:
                    task.func(**task.kwargs)
                except Exception:
                    logger.exception(
                        "Error occurs when running task from plugin [%s]."
                        % task.name
                    )
            else:
                try:
                    task.cls.handle_msg(**task.kwargs)
                except Exception:
                    logger.exception(
                        "Error occurs when running task from plugin [%s]."
                        % task.name
                    )

        self._stop_done = True

    def stop(self):
        self._stopped = True


class Handler(object):
    def __init__(self, workers=5):

        # handler_queue
        self.handler_queue = Queue()
        self.workers = [Worker(self.handler_queue) for i in xrange(workers)]
        for worker in self.workers:
            worker.setDaemon(True)
            worker.start()

        # handler_funcs store the functions that handle messages
        self.handler_funcs = {}

        self.handler_api = {
            "list_handlers": self.list_handlers,
            "add_handler": self.add_handler,
            "del_handler": self.del_handler
        }

        self.activated_list = set()

    def add_to_activation(self, name):
        self.activated_list.add(name)

    def list_handlers(self):
        return self.activated_list

    def add_handler(self, name, handler):
        """
        :type name: str
        :type handler: callable
        The handler must be a function which handler two parameters: msg and bot.
        """
        name = str(name)
        if isinstance(handler, type):
            handler = handler()
        self.handler_funcs[name] = handler
        self.activated_list.add(name)

    def del_handler(self, name):
        """
        :type name: str
        Remove a certain handle function, if it exists.
        """
        name = str(name)
        if name in self.handler_funcs:
            self.handler_funcs.pop(name)
        if name in self.activated_list:
            self.activated_list.remove(name)
    def update_handler(self, name, handler):
        name = str(name)
        self.del_handler(name)
        self.add_handler(name, handler)

    def update_handlers(self, pluginmanager):
        """
        Update the handle functions according the activated_list.
        The activated_list would be modified by other modules.
        """
        # collect the handle functions that exist in the self.handler_funcs, which would be removed.
        self.activated_list = set([str(each) for each in self.activated_list])
        s = set(self.handler_funcs.keys()).difference(self.activated_list)
        if not s: return # the activated_list and the self.handler_funcs is the same, which require no further processing.
        for hname in s: self.del_handler(hname)
        # collect the handle function declared in the activated_list instead of self.handler_funcs
        # the handle function in this set would be query from the plugin manger and reload.
        s = set(self.activated_list).difference(self.handler_funcs.keys())
        for hname in s:
            if hname in pluginmanager.plugins:
                self.add_handler(hname, pluginmanager.plugins[hname])
            else:
                flag = pluginmanager.add_plugin(hname)
                if flag: self.add_handler(hname, pluginmanager.plugins[hname])
        # reset the current activated_list as the self.handler_funcs's keys().
        self.activated_list = set(self.handler_funcs.keys())

    def handle_msg_list(self, msg_list, bot):
        """
        :type msg_list: list or tuple
        """
        for msg in msg_list:
            self._handle_one(msg, bot)

    def _handle_one(self, msg, bot):
        """
        :type msg: smart_qq_bot.messages.QMessage
        """
        for (name, handler) in self.handler_funcs.items():
            if isinstance(handler, types.FunctionType):
                self.handler_queue.put(
                    Task(
                        func=handler,
                        name=name,
                        cls=None,
                        kwargs={"msg": msg, "bot": bot, "handler": self}
                    )
                )
            else:
                self.handler_queue.put(
                    Task(
                        func=None,
                        name=name,
                        cls=handler,
                        kwargs={"msg": msg, "bot": bot, "handler": self}
                    )
                )
