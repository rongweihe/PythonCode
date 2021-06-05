# 2.1 使用多个界定符分割字符串

## 问题

你需要将一个字符串分割为多个字段，但是分隔符(还有周围的空格)并不是固定的。

## 解决方案

`string` 对象的 `split()` 方法只适应于非常简单的字符串分割情形， 它并不允许有多个分隔符或者是分隔符周围不确定的空格。 当你需要更加灵活的切割字符串的时候，最好使用 `re.split()` 方法：

```python
>>> line = 'asdf fjdk; afed, fjek,asdf, foo'
>>> import re
>>> re.split(r'[;,\s]\s*', line)
['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
```

Ps：空格字符分割是以 \s 来分割的

```python
>>> import re
>>> line = 'aaa bbb ccc;ddd   eee,fff'
>>> line
'aaa bbb ccc;ddd   eee,fff'
```

单字符切割

```python
>>> re.split(r';',line)
['aaa bbb ccc', 'ddd\teee,fff']
```

两个字符以上切割需要放在 [ ] 中

```python
>>> re.split(r'[;,]',line)
['aaa bbb ccc', 'ddd\teee', 'fff']
```

所有空白字符切割

```python
>>> re.split(r'[;,\s]',line)
['aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff']
```

使用括号捕获分组，默认保留分割符

```python
>>> re.split(r'([;])',line)
['aaa bbb ccc', ';', 'ddd\teee,fff']
```

不想保留分隔符，以（?:...）的形式指定

```python
>>> re.split(r'(?:[;])',line)
['aaa bbb ccc', 'ddd\teee,fff']
```