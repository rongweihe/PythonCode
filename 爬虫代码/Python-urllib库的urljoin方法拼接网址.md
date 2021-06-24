## 用 urllib 的 urljoin() 拼接两个网址（很强大）

对于 urljoin()，第一个参数是基础母站的 url，第二个是需要拼接成绝对路径的 url。

即使后者完全没有前者的内容，也可以。

```python
Python 3.5.3 (v3.5.3:1880cb95a742, Jan 16 2017, 08:49:46) 

[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin

Type "help", "copyright", "credits" or "license" for more information.

>>> from urllib import parse
>>> url1 = "http://www.youtube.com/user/khanacademy"
>>> url2 = "/user/khanacademy"
>>> parse.urljoin(url1,url2)
'http://www.youtube.com/user/khanacademy'
>>> url1 = "http://www.youtube.com/"
>>> parse.urljoin(url1,url2)
'http://www.youtube.com/user/khanacademy'
```

如果 url2，是一个完整的 url，则以后者的为准，所以，不管 url2 是不是短连接，都可以放进去拼接。

```python
>>> url2 = "http://www.youtube.com/user/khanacademy"
>>> parse.urljoin(url1,url2)
'http://www.youtube.com/user/khanacademy'
>>> url2 = "http://d.com/user/khanacademy"
>>> parse.urljoin(url1,url2)
'http://d.com/user/khanacademy'
```

 