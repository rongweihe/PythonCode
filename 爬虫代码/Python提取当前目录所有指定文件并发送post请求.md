## 功能

遍历当前目录所有指定文件并提取内容，发送 post 请求。

对于文件名的匹配，你可能会考虑使用 `glob` 或 `fnmatch` 模块。比如：

```python
import glob
pyfiles = glob.glob('somedir/*.py')

from fnmatch import fnmatch
pyfiles = [name for name in os.listdir('somedir')
            if fnmatch(name, '*.py')]
```

```python
# -*- coding: UTF-8 -*-
import base64
import codecs
import json
import logging
import os
import os.path
import requests
import sys
import zlib
import traceback
from fnmatch import fnmatch
pyfiles = [name for name in os.listdir('/search/odin/herongwei/app_parse/post_data/')
                    if fnmatch(name, '*.json')]
# usage: python recovery.py user_id date favorite_file
url = 'http://xxx'

def post_data():
    for file_name in pyfiles:
        print("file_name=",file_name)
        with open(file_name, 'r', encoding="utf-8") as json_file:
            json_obj = json.load(json_file)
            resp = requests.post(url=url, json=json_obj)
            if resp.status_code != 200:
                print("mi_post_err=",resp.status_code)
            result = resp.json()
            print("mi_post_result=",result)

if __name__ == "__main__":
    try:
        #test_file()
        post_data()
    except Exception as e:
        print("parse_mi_error=",e)
        traceback.print_exc()
```

