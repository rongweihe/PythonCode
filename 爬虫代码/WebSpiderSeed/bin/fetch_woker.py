'''
Author: herongwei
Date: 2021-06-27 09:54:36
LastEditTime: 2021-06-27 10:20:22
LastEditors: Please set LastEditors
Description: 核心工作类
FilePath: /WebSpiderSeed/bin/fetch_woker.py
'''
#!/usr/bin/spython
# -*- coding: utf-8 -*-

from comlib.io_helper import IOHelper
import json
import traceback
import multiprocessing
from multiprocessing import Manager
from comlib.req_helper import ReqHelper
from lxml import etree
from urllib.parse import urljoin
import time
from lib.common_helper import CommonHelper
from lib.log_helper import LogHelper
from lib.config_helper import ConfigHelper

def do_get_all_category_urls(seed_url_item, seed_url, curr_ua, data, process_index):
    try:
        web_name = data['web_name']
        use_proxy = data.get('use_proxy', 0)
        seed_url_category_urls = []
        if seed_url_item["type"] == "category_multi_page":
            if seed_url_item["xpath_str_get_category"] == "is_full_category_url":
                seed_url_category_urls.append(seed_url)#当前页就是全部页
            elif seed_url_item['xpath_str_get_category'] == 'is_fix_category_url':
                seed_url_category_urls.append(seed_url)
                seed_url_category_urls.extend(seed_url_item['fix_category_urls'])
                seed_url_category_urls = list(set(seed_url_category_urls))
            else:
                seed_url_html = ReqHelper.get_html(seed_url, curr_ua, use_proxy)
                if seed_url_html:
                    selector = etree.HTML(seed_url_html)
                    temp_category_urls = selector.xpath(seed_url_item['xpath_str_get_category'])
                    for key in temp_category_urls:
                        seed_url_category_urls.append(urljoin(seed_url, key))
        LogHelper.info("ing_do_search_%s time:%s thread_index:%s category_urls:%s", web_name,
                       CommonHelper.get_time_millis(), process_index, seed_url_category_urls)
    except Exception as e:
        LogHelper.error("do_get_all_category_urls url:%s err:%s trace_back:%s", seed_url, e, traceback.format_exc())

    return seed_url_category_urls

