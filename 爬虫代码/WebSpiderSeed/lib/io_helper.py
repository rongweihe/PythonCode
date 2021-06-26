'''
Author: herongwei
Date: 2021-06-26 11:20:16
LastEditTime: 2021-06-26 11:26:27
LastEditors: Please set LastEditors
Description: IO 文件操作/帮助类
FilePath: /WebSpiderSeed/lib/io_helper.py
'''
#!/usr/bin/spython
# -*- coding: utf-8 -*-
import os

class IOHelper(object):
    @staticmethod
    def exist(path):
        return os.path.exist(path)

    @staticmethod
    def read_all(path):
        file_obj = open(path)
        try:
            file_context = file_obj.read()
        finally:
            file_obj.close()
        return file_context
    
    @staticmethod
    def write_all(path, data):
        IOHelper.delfile(path)
        with open(path, 'w') as file_object:
            file_object.write(data)

    @staticmethod
    def write_line(path, data_arr):
        with open(path, 'a+') as file_object:
            for line in data_arr:
                file_object.write(line)
                file_object.write("\n")

    @staticmethod
    def delfile(path):
        if os.path.exists(path):  # 如果文件存在
            os.remove(path)

    
    
