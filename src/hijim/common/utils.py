# -*- coding: utf-8 -*-
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser
import threading
import functools


def singleton(cls):
    instances = {}
    instance_lock = threading.Lock()

    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            with instance_lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


_executor_pool = ThreadPoolExecutor(4)


def with_executor(function):

    @functools.wraps(function)
    async def inner(*args, **kwargs):
        func = functools.partial(function, *args, **kwargs)
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(_executor_pool, func)
    return inner


@singleton
class HijimConf:

    def __init__(self, conf_file=None):
        if not conf_file:
            conf_path = os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            conf_file = os.path.join(conf_path, 'hijim.ini')
        self.config = ConfigParser()
        self.config.read(conf_file)

    def __getattr__(self, item):
        return self.config[item]
