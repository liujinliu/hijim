# -*- coding: utf-8 -*-
import threading


class SingletonMixin:

    _LOCK = threading.Lock()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._LOCK:
                cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
