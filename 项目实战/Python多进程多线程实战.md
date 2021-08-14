# 多进程

### 1、执行带有参数的任务+输出进程编号和父进程编号

```python
'''
Author: your name
Date: 2021-08-13 13:18:17
LastEditTime: 2021-08-13 13:24:24
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /spider/Python基础/多进程例子.py
'''
import multiprocessing
import time
import os

def sing(num,name):
    print("当前唱歌进程的编号",os.getpid(),os.getppid())
    for i in range(num):
        print(name)
        print("唱歌...")
        time.sleep(0.5)
        
def dance(num,name):
    print("当前跳舞进程的编号",os.getpid(),os.getppid())
    for i in range(num):
        print(name)
        print("跳舞...")
        time.sleep(0.5)
    
if __name__ == '__main__':
 		print("主进程pid",os.getpid())
    sing_process  = multiprocessing.Process(target=sing,args=(3,"hrw"))
    dance_process = multiprocessing.Process(target=dance,kwargs={"name":"hrw","num":3})

    sing_process.start()
    dance_process.start()
```

## 输出

```shell
主进程pid 89134
当前跳舞进程的编号 89138 89134
hrw
跳舞...
当前唱歌进程的编号 89137 89134
hrw
唱歌...
hrw
hrw
跳舞...
唱歌...
hrw
hrw
唱歌...
跳舞...
```

看输出，验证正确。

### 主进程和子进程区别

![](https://cdn.jsdelivr.net/gh/rongweihe/ImageHost01/gzh/multi01.png)

### 2、主进程退出会等待所有的子进程退出才退出

默认情况下，为了保护子进程能够正常执行，主进程会等待所有的子进程退出才退出。

那如果想要实现主进程退出之后子进程也退出，怎么做呢？

很简单，设置守护主进程。

```python
'''
Author: your name
Date: 2021-08-13 13:18:17
LastEditTime: 2021-08-14 15:29:38
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /spider/Python基础/设置守护主进程.py
'''
import multiprocessing
import time
import os

def sing():
    for i in range(10):
        print("唱歌...")
        time.sleep(0.5)
    
if __name__ == '__main__':
    print("主进程pid",os.getpid())
    sing_process  = multiprocessing.Process(target=sing)
    #设置守护主进程 主进程退出之后不在执行子进程
    sing_process.daemon = True
    sing_process.start()
    time.sleep(1)
    print("主进程完成...")
```

输出

```python
主进程pid 94797
唱歌...
唱歌...
主进程完成...
```

### 3、多进程实现数据拷贝

```python
'''
Author: your name
Date: 2021-08-13 13:18:17
LastEditTime: 2021-08-14 16:01:23
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /spider/Python基础/多进程实现数据拷贝.py
'''
import multiprocessing
import time
import os

def copy_file(file_name, source_dir, dest_dir):
    #1. 拼接文件路径 和 目标文件路径
    source_path = source_dir + "/" + file_name
    dest_path   = dest_dir   + "/" + file_name
    
    #2.打开源文件和目标文件
    with open(source_path,'rb') as source_file:
        with open(dest_path,'wb') as dest_file:
            #3. 循环读取源文件到目标路径
            #只要还能读到数据就一直读取 除非读不到数据了
            while True:
                data = source_file.read(1024)
                if data:
                    dest_file.write(data)
                else:
                    break
    
if __name__ == '__main__':
    #1. 定义源文件夹 和 目标文件夹
    source_dir = "/home/test1"
    dest_dir  =  "/home/test2"

    #2. 创建目标文件夹
    try:
        os.mkdir(dest_dir)
    except:
        print("目标文件夹已经存在")

    #3. 读取源文件夹列表
    file_list = os.listdir(source_dir)

    #4. 遍历文件列表进行拷贝
    for file_name in file_list:
        sub_process = multiprocessing.Process(target=copy_file,
                                            args=(file_name, source_dir, dest_dir))
        sub_process.start()
    print("主进程完成...")
```

# 多线程

- 多线程是 Python 程序中是实现多任务的一种方式。
- 线程是程序执行的最小单元。
- 同属一个进程的多个线程共享进程所有的全部资源。

**线程执行带有参数的任务**

- args：以元祖的方式给执行任务传参。
- Kwargs：以字典形式给执行任务传参。

**两种方式设置守护主线程**

```python
 sing_thread.setDaemon(True)	#调用函数设置守护主线程
 sing_thread  = threading.Thread(target=sing, daemon=True)	#创建子线程设置
```

**多线程之间执行是无序的，是 CPU 调度的。**

多线程实现数据的拷贝区别只在于修改一行代码：

```python
sub_thread = threading.Thread(target=copy_file,
                              args=(file_name, source_dir, dest_dir))
sub_thread.start()
```

**注意点：**

- 知识点一：当一个进程启动之后，会默认产生一个主线程，因为线程是程序执行流的最小单元，当设置多线程时，主线程会创建多个子线程，在 python 中，默认情况下（其实就是 setDaemon(False)），主线程执行完自己的任务以后，就退出了，此时子线程会继续执行自己的任务，直到自己的任务结束。
- 知识点二：当我们使用 setDaemon(True) 方法，设置子线程为守护线程时，主线程一旦执行结束，则全部线程全部被终止执行，可能出现的情况就是，子线程的任务还没有完全执行结束，就被迫停止。
- 知识点三：此时 join 的作用就凸显出来了，join 所完成的工作就是线程同步，即主线程任务结束之后，进入阻塞状态，一直等待其他的子线程执行结束之后，主线程在终止。