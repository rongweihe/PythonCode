# 5.16 增加或改变已打开文件的编码

## 问题

你想在不关闭一个已打开的文件前提下增加或改变它的Unicode编码。

## 解决方案

如果你想给一个以二进制模式打开的文件添加Unicode编码/解码方式， 可以使用 `io.TextIOWrapper()` 对象包装它。比如：

```python
import urllib.request
import io

u = urllib.request.urlopen('http://www.python.org')
f = io.TextIOWrapper(u, encoding='utf-8')
text = f.read()
```

如果你想修改一个已经打开的文本模式的文件的编码方式，可以先使用 `detach()` 方法移除掉已存在的文本编码层， 并使用新的编码方式代替。下面是一个在 `sys.stdout` 上修改编码方式的例子：

```python
>>> import sys
>>> sys.stdout.encoding
'UTF-8'
>>> sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='latin-1')
>>> sys.stdout.encoding
'latin-1'
>>>
```

这样做可能会中断你的终端，这里仅仅是为了演示而已。

## 讨论