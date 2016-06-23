# -*- coding: utf-8 -*-
import os
import sys
import json

class PluginManager(object):
    """
    Parameters
    ----------
    prefix : str
        The location of the plugins.
    plugins : dict
        A storage of the handle functions.
    mtimes : dict
        A storage of the modified time of the plugins.
    """
    def __init__(self, prefix=""):

        self.plugins = {}
        self.mtimes = {}

        self.prefix = prefix
        # add prefix to the system path
        sys.path.append(self.prefix)

    def add_plugin(self, plugin_name):
        """
        Load a plugin with the module name.
        """
        if not os.path.isfile(self.prefix + "/" + plugin_name + ".py"):
            return
        try:
            module = __import__(plugin_name)
            self.plugins[plugin_name] = getattr(module, plugin_name)
            self.check_plugin(plugin_name)
        except ImportError:
            print("import error, fail to import %s" % plugin)

    def del_plugin(self, plugin_name):
        """
        Remove a plugin from the plugin list.
        """
        if plugin_name in self.plugins:
            self.plugins.pop(plugin_name)

    def update_plugin(self):
        """
        Reload the plugins whose source files have been changed.
        A list that records the changed plugin would be return.
        """
        tobeupdated = []
        for each in self.plugins:
            if self.check_plugin(each):
                # reload the module from the sys modules.
                module = sys.modules[each]
                # rewrite the handle function,
                self.plugins[each] = getattr(module, each)
                tobeupdated.append(each)
        return tobeupdated

    def check_plugin(self, mod_name):
        """
        Check if source file of a plugin is changed.
        """
        # call the module from the sys modules
        mod = sys.modules[mod_name]
        # make sure that the module exists.
        if not (mod and hasattr(mod, '__file__') and mod.__file__):
            return
        # make sure the module is reachable.
        try:
            # retrieve the modified time of the source file.
            mtime = os.stat(mod.__file__).st_mtime
        except (OSError, IOError):
            return
        # add modified time to the records of the modified time, if it never exists.
        if mod_name not in self.mtimes:
            self.mtimes[mod_name] = mtime
        # camparing the current and recorded modified time, reload a module
        # if the current modified time is the latest.
        elif self.mtimes[mod_name] < mtime:
            try:
                reload(mod)
                self.mtimes[mod_name] = mtime
                return True
            except ImportError:
                print("reload error : fail to reload %s" % mod)

if __name__ == "__main__":
    manager = PluginManager("./plugins")
    manager.add_plugin("test1")
    manager.add_plugin("test2")
    for each in manager.plugins:
        print(manager.plugins[each])
        manager.plugins[each](1, 2)
    import time
    time.sleep(10)
    manager.update_plugin()
    for each in manager.plugins:
        print(manager.plugins[each])
        manager.plugins[each](1, 2)
