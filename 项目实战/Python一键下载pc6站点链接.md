# 一键爬取pc6站点应用APP链接

网页： http://www.pc6.com/android/588_1.html 

参考代码

```python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import requests
from lxml import etree
import lxml.html
import json
import urllib
import re
from bs4 import BeautifulSoup
import xmltojson
import utils
from pprint import pprint
import random
import time
import requests
from lxml import etree
import lxml.html
import json
import re
import traceback

#提取小米网站当个页面的APP信息种子 并保存到文件里
#author:by@herongwei

class appParse:
    def __init__(self,appname):
        self.appname = appname
        self.base_url = "http://www.pc6.com"
        self.category_url = "http://www.pc6.com/android/588_"
    def get_domain_urls(self, category_url, base_url):
        response = requests.get(category_url)
        text = response.text
        html = etree.HTML(text)
        detail_urls = html.xpath("//dl[@id='listCont']//dd/p/a[last()-1]/@href")
        if not detail_urls:
            raise Exception("url does not exist")
        print("html2=", detail_urls)
        url_set = set([])
        all_url = []
        for i in detail_urls:
            if '/az/' in i:
                i = base_url + i
                if i not in url_set:
                    url_set.add(i)
                    all_url.append(i)
        return all_url
    def save_list(self,all_url, url_set):
        file_path= self.appname + ".txt"
        with open(file_path,"a",encoding="utf-8") as f:
            for url in all_url:
                if url not in url_set:
                    url_set.add(url)
                    f.write(json.dumps(url,ensure_ascii=False,indent=3))
                    f.write("\n")
        print("保存成功")

    def run(self):
        url_set = set([])
        for i in range(1,235):
            category_url = self.category_url + str(i) + ".html"
            print("category_url=", category_url)
            base_url = self.base_url
            all_url = self.get_domain_urls(category_url, base_url)
            self.save_list(all_url, url_set)

if __name__ == "__main__":
    try:
        app=appParse("pc6")
        app.run() 
    except Exception as e:
        print("crawl_pc6_error=",e)
        traceback.print_exc()
```

爬取结果：

![](https://cdn.jsdelivr.net/gh/rongweihe/ImageHost01/images/pc6.png)