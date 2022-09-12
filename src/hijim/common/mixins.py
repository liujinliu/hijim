# -*- coding: utf-8 -*-
import threading


class SingletonMixin:

    __LOCK = threading.Lock()
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            with cls.__LOCK:
                cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance
