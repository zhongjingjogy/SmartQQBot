# -*- coding: utf-8 -*-
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

logger = logging.getLogger("console logger")
init_logging(logger=logger)
