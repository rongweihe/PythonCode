'''
Author: herongwei
Date: 2021-06-26 11:32:42
LastEditTime: 2021-06-26 11:45:12
LastEditors: Please set LastEditors
Description: 请求帮助类
FilePath: /WebSpiderSeed/lib/req_helper.py
'''
import requests
import json
import time
from comlib.common_helper import CommonHelper
from comlib.log_helper import LogHelper
from retrying import retry
from comlib.config_helper import ConfigHelper
import traceback

class ReqHelper(object):
    #模拟 pc_ua 和 安卓_ua
    g_pc_ua = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.1.4322; CIBA'
    g_wap_ua = 'Mozilla/5.0 (Linux; U; Android 4.4.4; Nexus 5 Build/KTU84P) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
    headers = {'Content-Type': 'application/json;charset=utf8'}
    get_headers = {}
    s = requests.session()
    http_proxies = ConfigHelper.get_config().PROXIES

    @staticmethod
    def get_url(url):
        # url = ReqHelper.url_base + url
        # print('url:' + url)
        return url

    @staticmethod
    @retry(stop_max_attempt_number=3, wait_incrementing_increment=1200)
    def post_json(url, data):
        t1 = CommonHelper.get_time_millis()
        response = ReqHelper.s.post(ReqHelper.get_url(url), data=json.dumps(data))
        t2 = CommonHelper.get_time_millis()
        return response.json()

    @staticmethod
    @retry(stop_max_attempt_number=3, wait_incrementing_increment=1200)
    #获取网页
    def __get_html(url, ua=None,use_proxy=0):
        if not ua:
            ua = ReqHelper.g_pc_ua
        headers = {'user-agent': ua}
        t1 = CommonHelper.get_time_millis()
        # http_proxies
        if use_proxy == 0:
            response = ReqHelper.s.get(url, headers=headers, timeout=30, verify=False)
        else:
            http_proxies = ConfigHelper.get_config().PROXIES
            response = ReqHelper.s.get(url, headers=headers, timeout=30, verify=False, proxies=http_proxies)
        # print()
        response.encoding = response.apparent_encoding
        # print(response.text)
        t2 = CommonHelper.get_time_millis()
        LogHelper.debug("req url %s cost_time: %s", url, t2 - t1)
        # print('cost time %s ms' % (t2 - t1))
        if response.status_code != 200:
            err_info = 'req %s status_code %s' % (url, response.status_code)
            LogHelper.error(err_info)
            raise Exception(err_info)
        return response.text

    @staticmethod
    def get_html(url, ua=None,use_proxy=0):
        try:
            text = ReqHelper.__get_html(url, ua,use_proxy)
            return text
        except Exception as e:
            LogHelper.error("get_html url:%s err:%s trace_back:%s", url, e, traceback.format_exc())
            return None