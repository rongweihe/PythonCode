# Linux C/C++ 调用 Python 函数 demo

1、编写 Python 脚本，名称 py_add.py。

```python
def add(a=1,b=1):
    print('Function of python called!')
    print('a = ',a)
    print('b = ',b)
    print('a + b = ',a+b)
```

2、编写 C 代码。

```C
/*
 * @Author: herongwei
 * @Date: 2021-07-20 17:39:52
 * @LastEditTime: 2021-07-20 17:40:20
 * @LastEditors: Please set LastEditors
 * @Description: C 代码调用 Python demo 
 * @FilePath: /temp/hello.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <Python.h>

void clean(PyObject *obj) {
    if (obj) {
        Py_DECREF(obj);
    }
}

int main(int argc, char **argv) {
    //初始化 载入 Python 的扩展模块
    //判断初始化是否成功
    Py_Initialize();
    if (!Py_IsInitialized()) {
        printf("Python init failed");
        return -1;
    }
    //PyRun_SimpleString 为宏定义 执行一段 Python 代码
    //导入当前路径
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./')");

    PyObject *pName = NULL;
    PyObject *pModule = NULL;
    PyObject *pDict = NULL;
    PyObject *pFunc = NULL;
    PyObject *PArgs = NULL;

    //加载名为 py_add 的 Python 脚本
    pName = PyString_FromString("py_add");
    pModule = PyImport_Import(pName);
    if (!pModule) {
        printf("Load py_add failed");
        getchar();
        return -1;
    }

    pDict = PyModule_GetDict(pModule);
    if (!pDict) {
        printf("Load dict failed");
        return -1;
    }

    pFunc = PyDict_GetItemString(pDict, "add");
    if (!pFunc || !PyCallable_Check(pFunc)) {
        printf("Load fun failed");
        return -1;
    }

    //向 Python 传参是用元祖tuple形式传过去
    //因此我们实际上就是构造一个合适的Python元祖对象
    //用到 PyTuple_New, Py_BuildValue, PyTuple_SetItem 等几个函数
    PArgs = PyTuple_New(2);
    //PyObject* Py_BuildValue(char *format...)
    //把 C++ 的变量转换成一个 Python 对象 
    //当需要从 C++ 传递变量到 Python 代码中就需要用到这些函数
    //有点类似于 C 的 printf 但格式稍有不同 常用的格式有
    // s 表示字符串
    // i 表示整型
    // f 表示浮点数
    // O 表示一个浮点数
    PyTuple_SetItem(PArgs, 0, Py_BuildValue("i",234));
    PyTuple_SetItem(PArgs, 1, Py_BuildValue("i",345));

    //调用 Python 的 add 函数
    PyObject_CallObject(pFunc,PArgs);

    //清理 Python 对象
    clean(pName);
    clean(PArgs);
    clean(pModule);
    //关闭 Python 对象
    Py_Finalize();
    return 0;
}
```

3、编译

```shell
gcc -I /usr/include/python2.7/  hello.c -o hello -L /usr/lib/ -lpython2.7
```

备注：链接 Python 的库需在最后，否则可能会出现以下的错误提示：

`undefined reference to 'Py_Initialize'`

4、运行结果

[![WNNH6H.png](https://z3.ax1x.com/2021/07/20/WNNH6H.png)](https://imgtu.com/i/WNNH6H)

5、更多资料参考官方文档

https://docs.python.org/3/extending/index.html