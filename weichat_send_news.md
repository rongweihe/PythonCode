``` python 
from __future__ import unicode_literals
from threading import Timer
from wxpy import *
import requests
import itchat
def get_news():
    url = "http://open.iciba.com/dsapi";
    r   = requests.get(url);
    contents = r.json()['content'];
    translation = r.json()['translation'];
    return contents,translation;
def send_news():
    try:
        # 登录你的微信号，会弹出网页二维码，扫描即可
        itchat.auto_login(hotReload=True);
        #获取对应的好友备注
        #改成你最心爱的人的名字
        my_friend = itchat.search_friends(name=u'彩虹宝宝');
        #获取对应名称的一串数字
        rainbowBB = my_friend[0]["UserName"];
        #获取金三词典的内容
        msg1 = str(get_news()[0]);
        content = str(get_news()[1][17:]);
        msg2 = str(content);
        msg3 = "来自你最爱的人";
        #发送消息
        itchat.send(msg1,toUserName=rainbowBB);
        itchat.send(msg2,toUserName=rainbowBB);
        itchat.send(msg3,toUserName=rainbowBB);
        # 每 86400 秒（1天）发送一次
        t = time(86400,send_news());
        t.start();
    except:
        msg4 = u"今天最爱的人出现啦";
        itchat.send(msg4,toUserName=rainbowBB);
        
if __name__ == "__main__":
    send_news()
```

##效果
![效果](https://i.loli.net/2019/02/17/5c692f140fd3f.jpg)
