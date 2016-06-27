#coding=utf-8
import threading
import time

class PluginTimer(threading.Thread):
    def __init__(self, func, args=(), sleep=10):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.sleep = sleep
        self.enabled = True
        self.setDaemon(True)
    def stop(self):
        self.enabled = False
    def run(self):
        while self.enabled:
            res = self.func(*self.args)
            # apply(self.func, self.args)
            try:
                print("got sleep time: %s" % res)
                if res: time.sleep(res)
            except:
                time.sleep(self.sleep)
