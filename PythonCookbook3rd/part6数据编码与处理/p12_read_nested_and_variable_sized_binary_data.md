# 6.12 读取嵌套和可变长二进制数据

## 问题

你需要读取包含嵌套或者可变长记录集合的复杂二进制格式的数据。这些数据可能包含图片、视频、电子地图文件等。

## 解决方案

`struct` 模块可被用来编码/解码几乎所有类型的二进制的数据结构。为了解释清楚这种数据，假设你用下面的Python数据结构 来表示一个组成一系列多边形的点的集合：

```python
polys = [
    [ (1.0, 2.5), (3.5, 4.0), (2.5, 1.5) ],
    [ (7.0, 1.2), (5.1, 3.0), (0.5, 7.5), (0.8, 9.0) ],
    [ (3.4, 6.3), (1.2, 0.5), (4.6, 9.2) ],
]
```

现在假设这个数据被编码到一个以下列头部开始的二进制文件中去了：

```json
+------+--------+------------------------------------+
|Byte  | Type   |  Description                       |
+======+========+====================================+
|0     | int    |  文件代码（0x1234，小端）          |
+------+--------+------------------------------------+
|4     | double |  x 的最小值（小端）                |
+------+--------+------------------------------------+
|12    | double |  y 的最小值（小端）                |
+------+--------+------------------------------------+
|20    | double |  x 的最大值（小端）                |
+------+--------+------------------------------------+
|28    | double |  y 的最大值（小端）                |
+------+--------+------------------------------------+
|36    | int    |  三角形数量（小端）                |
+------+--------+------------------------------------+
```

紧跟着头部是一系列的多边形记录，编码格式如下：

```json
+------+--------+-------------------------------------------+
|Byte  | Type   |  Description                              |
+======+========+===========================================+
|0     | int    |  记录长度（N字节）                        |
+------+--------+-------------------------------------------+
|4-N   | Points |  (X,Y) 坐标，以浮点数表示                 |
+------+--------+-------------------------------------------+
```

为了写这样的文件，你可以使用如下的Python代码：

```python
import struct
import itertools

def write_polys(filename, polys):
    # Determine bounding box
    flattened = list(itertools.chain(*polys))
    min_x = min(x for x, y in flattened)
    max_x = max(x for x, y in flattened)
    min_y = min(y for x, y in flattened)
    max_y = max(y for x, y in flattened)
    with open(filename, 'wb') as f:
        f.write(struct.pack('<iddddi', 0x1234,
                            min_x, min_y,
                            max_x, max_y,
                            len(polys)))
        for poly in polys:
            size = len(poly) * struct.calcsize('<dd')
            f.write(struct.pack('<i', size + 4))
            for pt in poly:
                f.write(struct.pack('<dd', *pt))
```

将数据读取回来的时候，可以利用函数 `struct.unpack()` ，代码很相似，基本就是上面写操作的逆序。如下：

```python
def read_polys(filename):
    with open(filename, 'rb') as f:
        # Read the header
        header = f.read(40)
        file_code, min_x, min_y, max_x, max_y, num_polys = \
            struct.unpack('<iddddi', header)
        polys = []
        for n in range(num_polys):
            pbytes, = struct.unpack('<i', f.read(4))
            poly = []
            for m in range(pbytes // 16):
                pt = struct.unpack('<dd', f.read(16))
                poly.append(pt)
            polys.append(poly)
    return polys
```

尽管这个代码可以工作，但是里面混杂了很多读取、解包数据结构和其他细节的代码。如果用这样的代码来处理真实的数据文件， 那未免也太繁杂了点。因此很显然应该有另一种解决方法可以简化这些步骤，让程序员只关注自最重要的事情。

在本小节接下来的部分，我会逐步演示一个更加优秀的解析字节数据的方案。 目标是可以给程序员提供一个高级的文件格式化方法，并简化读取和解包数据的细节。但是我要先提醒你， 本小节接下来的部分代码应该是整本书中最复杂最高级的例子，使用了大量的面向对象编程和元编程技术。 一定要仔细的阅读我们的讨论部分，另外也要参考下其他章节内容。