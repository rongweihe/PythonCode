'''
Author: herongwei
Date: 2021-06-26 11:31:27
LastEditTime: 2021-06-26 11:47:06
LastEditors: Please set LastEditors
Description: 日志类
FilePath: /WebSpiderSeed/lib/log_helper.py
'''
#!/usr/bin/spython
# -*- coding: utf-8 -*-

import logging
from logging import handlers
import time
import os

'''
        # interval是时间间隔（wher=midnight时interval不生效），backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        默认DEUG级别，文件路径/logs/logfile.log，每天凌晨按天分割日志文件，保留100个日志文件，记录间隔默认1,when=H intervel=3表示3小时分割
'''

def configure_logging(level, filename, when, backupCount, interval, log_name):
    # 创建默认路径,设置默认参数
    if (not os.access('logs/', os.R_OK)):
        os.mkdir('logs')

    if level == None:
        when = logging.DEBUG
    if filename == None:
        filename = '/logs/logfile.log'
    if when == None:
        when = 'midnight'
    if backupCount == None:
        backupCount = 30
    if interval == None:
        interval = 1

    # add 'levelname_c' attribute to log resords
    orig_record_factory = logging.getLogRecordFactory()
    log_colors = {
        logging.DEBUG: "\033[1;34m",  # blue
        logging.INFO: "\033[1;32m",  # green
        logging.WARNING: "\033[1;35m",  # magenta
        logging.ERROR: "\033[1;31m",  # red
        logging.CRITICAL: "\033[1;41m",  # red reverted
    }

    def record_factory(*args, **kwargs):
        record = orig_record_factory(*args, **kwargs)
        record.levelname_c = "{}{}{}".format(
            log_colors[record.levelno], record.levelname, "\033[0m")
        return record

    logging.setLogRecordFactory(record_factory)

    formatter_c = logging.Formatter(
        "[%(asctime)s]-" + log_name + "-[%(thread)d]-[%(threadName)s]-%(levelname_c)s: %(message)s")
    format_str = logging.Formatter(
        '%(asctime)s - ' + log_name + ' - %(levelname)s: %(message)s')  # 设置日志格式

    stderr_handler = logging.StreamHandler()
    stderr_handler.setLevel(level)
    stderr_handler.setFormatter(formatter_c)
    time_handler = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backupCount,
                                                     interval=interval,
                                                     encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
    time_handler.setLevel(level)
    time_handler.setFormatter(format_str)  # 设置文件里写入的格式
    root_logger = logging.getLogger(filename)
    root_logger.setLevel(level)
    root_logger.addHandler(stderr_handler)  # 把对象加到logger里
    root_logger.addHandler(time_handler)  # 把对象加到logger里


_logger_main = logging.getLogger('logs/main.log')
configure_logging(logging.DEBUG, 'logs/main.log', 'D', 3, 1, "mainlog")
_logger_err = logging.getLogger('logs/err.log')
configure_logging(logging.ERROR, 'logs/err.log', 'D', 3, 1, "errlog")

import sys


def findcaller(func):
    def wrapper(*args):
        # 获取调用该函数的文件名、函数名及行号
        filename = sys._getframe(1).f_code.co_filename
        funcname = sys._getframe(1).f_code.co_name
        lineno = sys._getframe(1).f_lineno

        # 将原本的入参转变为列表，再把调用者的信息添加到入参列表中
        args = list(args)
        args.append(f'{os.path.basename(filename)}.{funcname}.{lineno}')
        func(*args)

    return wrapper


class LogHelper(object):
    _log_name = 'mainlog'

    @staticmethod
    def get_logger(log_name=""):
        if log_name == "errlog":
            return _logger_err
        return _logger_main

    @staticmethod
    @findcaller
    def debug(msg, *args, **kwargs):
        msg = LogHelper.__msg_formate(msg)
        _logger_main.debug(msg, *args, **kwargs)

    @staticmethod
    @findcaller
    def error(msg, *args, **kwargs):
        msg = LogHelper.__msg_formate(msg)

        _logger_main.error(msg, *args, **kwargs)
        _logger_err.error(msg, *args, **kwargs)

    @staticmethod
    @findcaller
    def info(msg, *args, **kwargs):
        msg = LogHelper.__msg_formate(msg)
        _logger_main.info(msg, *args, **kwargs)

    @staticmethod
    def __msg_formate(msg):
        return msg + " - %s "

#
# while True:
#     LogHelper.debug("debug  %s", 'aaaaaaaaa')
#     LogHelper.error("error  %s", 'aaaaaaeeeeeeeeeeaaa')
#     # logger.debug("debug  %s", 'aaaaaaaaa')
#     LogHelper.info("info ")
#     # logger.error("error 1111")
#     # logger2.error("error 2222")
#     # logger.critical("something unusual happened")
#     # logger.warning('war')
#     time.sleep(0.2)
