'''
Author: herongwei
Date: 2021-06-26 11:12:12
LastEditTime: 2021-06-26 11:16:42
LastEditors: Please set LastEditors
Description: 配置类
FilePath: /WebSpiderSeed/lib/config_helper.py
'''
#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lib.io_helper import IOHelper
import json

class ConfigHelper(object):
    config_path = '../env.json'
    _env = ''
    _module = ''
    from config.dev_config import DevConfig as _DevConfig
    from config.test_config import TestConfig as _TestConfig
    from config.online_config import OnlineConfig as _OnlineConfig

    config = {
        'dev': _DevConfig,
        'test': _TestConfig,
        'online': _OnlineConfig,
        'default': _DevConfig
    }

    @staticmethod
    def get_env():
        if ConfigHelper._env != '':
            return ConfigHelper._env
        # return 'local'
        if not IOHelper.exist(ConfigHelper.config_path):
            if IOHelper.exist('../../env.json'):
                ConfigHelper.config_path = '../../env.json'
            else:
                ConfigHelper.config_path = './env.json'
        if not IOHelper.exist(ConfigHelper.config_path):
            ConfigHelper._env = "dev"
        else:
            json_str = IOHelper.read_all(ConfigHelper.config_path)
            obj = json.loads(json_str)
            ConfigHelper._env = obj['env']
        return ConfigHelper._env

    @staticmethod
    def get_module():
        # return 'local'
        if not IOHelper.exist(ConfigHelper.config_path):
            if IOHelper.exist('../../env.json'):
                ConfigHelper.config_path = '../../env.json'
            else:
                ConfigHelper.config_path = './env.json'
        json_str = IOHelper.read_all(ConfigHelper.config_path)
        obj = json.loads(json_str)
        if ConfigHelper._module == '':
            ConfigHelper._module = obj.get('module', [])
        return ConfigHelper._module

    @staticmethod
    def get_config():
        return ConfigHelper.config[ConfigHelper.get_env()]
