# Python代码多进程加速处理百万量级文件

【参考代码】

```python
'''
Author: herongwei
Date: 2021-07-29 16:24:36
LastEditTime: 2021-07-30 17:12:56
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /spider/vr_parse/novel.py
'''
# -*- coding:utf-8 -*-
import requests
from lxml import etree
import lxml.html
import json
import re
import os
import time
import sys
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ElementTree
import xmltojson
import threading

g = open('novel_ret.txt','wt',encoding='utf-8')

def timestamp_to_data(dt):
    time_local = time.localtime(int(dt))
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
    return timestamp

def get_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
    response = requests.get(url,headers=headers)
    status_code = response.status_code
    if status_code == 200:
        return response
    else:
        print("get_url_failed")
        return None

#开启10多进程加速
#根据每一行按 tab 分割
def test_novel(filpos,i):
    # 开启 100 进程加速
    # file_name = "vr"
    # if i < 10:
    #     file_name += "0"
    # file_name = filpos + file_name + str(i)
     with open(filpos+"novel"+str(i)+".txt") as f:
        for line in f:
            if line:
                try:
                    line = line.strip('\n')
                    line2 = line.split('\t')
                    name = line2[0].strip('').strip('\n').replace(' ','')
                    num1 = line2[1].strip('').strip('\n')
                    num2 = line2[2].strip('').strip('\n')
                    base_url = 'https://novel.xxx.com//api/dbook?query=' + name
                    print("base_url=",base_url)
                    response = get_url(base_url)
                    if response != None:
                        text = response.text
                        title = "NULL"
                        author = "NULL"
                        name_id = "NULL"
                        if text.find('<?xml') != -1:
                            text = text[text.find('<?xml'):]
                            json_str = xmltojson.parse(text)
                            #print("json_str=",json_str)
                            json_data = json.loads(json_str)
                            if json_data['DOCUMENT']['item']['key']:
                                title = json_data['DOCUMENT']['item']['key']
                                #print("title=",title)
                            if json_data['DOCUMENT']['item']['display']['author']:
                                author = json_data['DOCUMENT']['item']['display']['author']
                                #print("author=",author)
                            if json_data['DOCUMENT']['item']['display']['id']:
                                name_id = json_data['DOCUMENT']['item']['display']['id']
                                #print("name_id=",name_id)
                        if title and author and name_id:
                            print("title+author+name_id=",timestamp_to_data(time.time()),title,author,name_id)
                            g.write('%s\n'%(name + "#" + num1 + "#" + num2 + "#" + title + "#" + author + "#" + name_id))

                except Exception as e:
                    print(e)
                    pass
    
def thread_run(nums_thread):
    start_time = time.time()
    threads = []
    #调整多进程
    for i in range(0,nums_thread):
        t = threading.Thread(target=test_novel,args=("/xxx/",i+1))
        threads.append(t)
    for thr in threads:
        thr.start()
    thr.join()
    end_time = time.time()
    print("all_over=",end_time-start_time)

if __name__ == "__main__":
    nums_thread = 10
    thread_run(nums_thread)
```

【文件大小】

```c
[@root]# cat file.txt | wc -l
997576
```

【效果对比】

10 进程耗时：12892 秒 = 3.59 h

100 进程耗时：6198 秒 = 1.7 h

![](https://z3.ax1x.com/2021/07/30/WOcBUU.png)