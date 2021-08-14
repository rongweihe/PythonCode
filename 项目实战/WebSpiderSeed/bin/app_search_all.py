'''
Author: herongwei
Date: 2021-06-27 10:24:23
LastEditTime: 2021-06-27 10:33:38
LastEditors: Please set LastEditors
Description: 多进程启动
FilePath: /WebSpiderSeed/bin/app_search_all.py
'''
from lib.io_helper import IOHelper
import json
import multiprocessing
from multiprocessing import Manager

from lib.common_helper import CommonHelper
from lib.log_helper import LogHelper
from bin.fetch_worker import fetch_worker

class SeedFetcher(object):
    def __init__(self, config_file):
        self.config_file = config_file
        app_search_rule_text = IOHelper.read_all(self.config_file)
        app_search_rule = json.loads(app_search_rule_text)
        self.task_queue = Manager().Queue()
        for item in app_search_rule['web_url']:
            if item['status'] == 1:
                self.task_queue.put(item)
        self.thread_num = app_search_rule['thread_num']
        self.all_process = []

def run(self):
    self.all_process = [multiprocessing.Process(target=fetch_worker, args=(thead_index,self.task_queue)) for 
            thread_index in range(self.thread_num)]
    for p in self.all_process:
        p.start()
    for p in self.all_process:
        p.join()

def do_search():
    t1 = CommonHelper.get_time_millis()
    LogHelper.info("start_do_search_time:%s", t1)
    config_file = "./config/app_search_rule.json"
    seed_obj = SeedFetcher(config_file)
    seed_obj.run()
    t2 = CommonHelper.get_time_millis()
    LogHelper.info("end_do_search_time:%s cost_time:%s", t2, t2 - t1)