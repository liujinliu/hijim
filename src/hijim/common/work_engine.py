# -*- coding: utf-8 -*-
import importlib
from .utils import HijimConf, singleton
from .base_work_engine import AbstractWorkEngine


@singleton
class HijimWorkEngine:

    def __init__(self):
        engine_name = HijimConf().WORK_ENGINE['name']
        self.__engine = importlib.import_module(engine_name)

    @property
    def engine(self) -> AbstractWorkEngine:
        return self.__engine.main.egine
