'''
Author: herongwei
Date: 2021-06-26 11:19:03
LastEditTime: 2021-06-26 11:48:19
LastEditors: Please set LastEditors
Description: 通用操作帮助类
FilePath: /WebSpiderSeed/lib/common_helper.py
'''
#!/usr/bin/spython
# -*- coding: utf-8 -*-

import time
import hashlib
import socket
from functools import lru_cache
import math

class CommonHelper(object):
    @staticmethod
    def isNum(value):
        try:
            value + 1
        except TypeError:
            return False
        else:
            if math.isnan(value):
                return False
            return True

    @staticmethod
    @lru_cache(1)
    def get_hostname():
        return socket.gethostname()

    @staticmethod
    def get_time_millis():
        return int(round(time.time() * 1000))

    @staticmethod
    def get_time_str():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    @staticmethod
    def get_time_str_num():
        return time.strftime("%Y%m%d%H%M", time.localtime(time.time()))

    @staticmethod
    def encode(info):
        info = info.encode('utf-8')
        md5 = hashlib.md5(info)
        return md5.hexdigest()

    @staticmethod
    def dict_remove_item(dict_obj, key):
        if key in dict_obj:
            del dict_obj[key]

    @staticmethod
    def array_to_dict(arr, dict_key):
        dict_all = {}
        for item in arr:
            curr_key = item[dict_key]
            del item[dict_key]
            dict_all[curr_key] = item
        return dict_all

    @staticmethod
    def arr_remove_item(arr, item):
        if item in arr:
            arr.remove(item)

    @staticmethod
    def arr_append_item(arr, item):
        if item in arr:
            return
        arr.append(item)

    @staticmethod
    def enum(**enums):
        return type('Enum', (), enums)

    @staticmethod
    def sys_arg_to_dict(arr):
        dict_param = {}
        for i in range(0, len(arr), 2):
            dict_param[arr[i]] = arr[i + 1]
        return dict_param

# print(CommonHelper.get_hostname())
# print(CommonHelper.get_hostname())
# print(CommonHelper.encode('xuluhui:rgb-unlock:old-train-data:black-data:blacklist_attack_20180321_ls'))
# print(CommonHelper.encode('aaaa'))
# testenum = CommonHelper.enum(test1 = -1,test2 = 0,test3 = 1)
# print(testenum.test1)