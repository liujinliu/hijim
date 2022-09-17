# -*- coding: utf-8 -*-
import os
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
