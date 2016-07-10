#coding=utf-8
import argparse
import json
import os
from smartqq import start_qq, list_messages, create_db, logger
import logging

def init_logging(logger, log_level=logging.DEBUG):
    assert isinstance(logger, logging.Logger)

    log_format = '[%(levelname)s] %(asctime)s  %(filename)s line %(lineno)d: %(message)s'
    date_fmt = '%a, %d %b %Y %H:%M:%S'
    formatter = logging.Formatter(log_format, date_fmt)
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def load_pluginconfig(configjson):
    config = None
    if configjson is not None:
        if os.path.isfile(configjson):
            with open(configjson, "r") as f:
                config = json.load(f)
        else:
            print("unable to load the configuration file for plugins, default settings will be used.")
    return config

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-gui",
        action="store_true",
        default=False,
        help="Whether display QRCode with tk and PIL."
    )
    parser.add_argument(
        "--new-user",
        action="store_true",
        default=False,
        help="Logout old user first(by clean the cookie file.)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Switch to DEBUG mode for better view of requests and responses."
    )
    parser.add_argument(
        "--plugin",
        default="config.json",
        help="Specify the json file for the setting of the plugins."
    )
    parser.add_argument(
        "--cookie",
        default="cookie.data",
        help="Specify the storage path for cookie."
    )
    parser.add_argument(
        "--vpath",
        default="./v.jpg",
        help="Specify the storage path for login bar code."
    )
    parser.add_argument(
        "--list",
        action="store_true",
        default=False,
        help="List the recored qq messages."
    )
    parser.add_argument(
        "--create",
        action="store_true",
        default=False,
        help="List the recored qq messages."
    )

    options = parser.parse_args()
    configjson = load_pluginconfig(options.plugin)
    try:
        configjson = load_pluginconfig(options.plugin)
        print("got json: %s" % configjson)
    except:
        print("using default setting")
        configjson = {
            "dbhandler": "sqlite:///message-record.db",
            "plugin_root": "./plugins",
            "plugins": [
                "pluginmanage",
                "plugindemo"
            ]
        }
    if options.debug:
        init_logging(logger)

    if options.list:
        list_messages()
    elif options.create:
        create_db(configjson["dbhandler"])
    else:
        try:
            start_qq(
                plugin_setting=configjson,
                no_gui=options.no_gui,
                new_user=options.new_user,
                debug=options.debug,
                dbhandler=configjson["dbhandler"],
                cookie_file=options.cookie,
                vpath=options.vpath
            )
        except KeyboardInterrupt:
            exit(0)

if __name__ == "__main__":
    main()
