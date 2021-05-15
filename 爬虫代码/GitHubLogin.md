

```python
# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import lxml.html
import json
import re
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

# 定义一个 Login 类，初始化一些变量
class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Host': 'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.feed_url = 'https://github.com/dashboard-feed'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session() # 维持一个会话，而且可以自动处理 Cookies
    
    # 用 Session 对象的 get() 方法访问 GitHub 的登录页面，然后用 XPath 解析出登录所需的 authenticity_token 信息并返回。
    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        # selector = etree.HTML(response.text) 2019版的GitHub已经不能用
        selector = pq(response.text)
        token = selector('input[name="authenticity_token"]').attr('value')
        # token = selector.xpath('//input[@name="authenticity_token"]')
        return token

    # 首先构造一个表单，复制各个字段，其中 email 和 password 是以变量的形式传递。然后再用 Session 对象的 post() 方法模拟登录即可。
    # 由于 requests 自动处理了重定向信息，我们登录成功后就可以直接跳转到首页，首页会显示所关注人的动态信息，
    # 得到响应之后我们用 dynamics() 方法来对其进行处理。接下来再用 Session 对象请求个人详情页，然后用 profile() 方法来处理个人详情页信息。
    def login(self, email, password):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': email,
            'password': password
        }

        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        response = self.session.get(self.feed_url, headers=self.headers)
        if response.status_code == 200:
            self.dynamics(response.text)
        
        response = self.session.get(self.login_url, headers=self.headers)
        if response.status_code == 200:
            self.profile(response.text)

    # 关注人的动态信息
    def dynamics(self, html):
        selector = pq(html)
        #dynamics = selector.xpath('//div[contains(@class, "news")]//div[contains(@class, "alert")]') 2019已失效
        dynamics = selector('div[class="d-flex flex-items-baseline"] div')
        print('*' * 10 + 'dynamics.text begin' + '*' * 10)
        print(dynamics.text())
        print('*' * 10 + 'dynamics.text end' + '*' * 10)

        print('*' * 10 + 'dynamics begin' + '*' * 10)
        for item in dynamics:
            etree.strip_elements(item, 'span')
            dynamic = ' '.join(item.xpath('.//text()')).replace('\n', ' ').strip()
            dynamic = re.sub(' +', '  ', dynamic)
            print(dynamic)
        print('*' * 10 + 'dynamics end' + '*' * 10)
    # 在 prifile() 方法里，我们提取了个人的昵称和绑定的邮箱，然后将其输出。
    def profile(self, html):
        print('*'*10+'profileing'+'*'*10)
        selector = etree.HTML(html)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')

        # soup = BeautifulSoup(selector.text,"lxml")
        # name = soup.find("input",id="user_profile_name")
        # email = soup.find("select",id="user_profile_email")
        # GitHub 后台应该也是改成了动态加载的方式，原先的做法已经提取不到 发现一个官方 api  https://api.github.com/users/rongweihe
        print(name, email)

if __name__ == "__main__":
    user = Login()
    user.login(email='rongweihe1995@gmail.com', password='Gitnyistacm325')
```

