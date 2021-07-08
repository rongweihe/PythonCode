'''
Author: your name
Date: 2021-06-27 17:13:00
LastEditTime: 2021-06-27 17:52:26
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /WebSpiderSeed/ok.py
'''

def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)
    # Invoke the callback with the result
    callback(result)

from queue import Queue
from functools import wraps

class Async:
    def __init__(self, func, args):
        self.func = func
        self.args = args

def inlined_async(func):
    def wrapper(*args):
        f = func(args)
        result_queue = Queue()
        result_queue.put(None)
        while True:
            result = result_queue.get()
            try:
                a = f.send(result)
                apply_async(a.func, a.args, callback=result_queue.put)
            except StopIteration:
                break
    return wrapper

def sample():
    n = 0
    # Closure function
    def func():
        print('n=',n)
    # Accessor methods for n
    def get_n():
        return n
    def set_n(new_n):
        nonlocal n
        n = new_n

    func.get_n = get_n
    func.set_n = set_n

    return func

if __name__ == '__main__':
    f  = sample()
    f()#n= 0
    f.set_n(100)
    f()#n= 100
    f.get_n()
    f()#n= 100
