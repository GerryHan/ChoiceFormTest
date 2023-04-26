# -*- coding = utf-8 -*-
# @Time: 2023/2/5 16:56
# @Author: Gerry
# @File: singLeton.py
# @Software: PyCharm
import threading


class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance
