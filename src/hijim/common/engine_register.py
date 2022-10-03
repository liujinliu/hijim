# -*- coding: utf-8 -*-
from hijim.common.utils import singleton
from hijim.common.base_work_engine import AbstractWorkEngine
from hijim.common.exceptions import EngineRegError


@singleton
class EngineRegister:

    def __init__(self):
        self.__engines = dict()

    def register(self, *, name, engine: AbstractWorkEngine):
        if name in self.__engines:
            raise EngineRegError(detail=f'engine {name} already registered')
        self.__engines[name] = engine

    def get_engine(self, name):
        return self.__engines.get(name, None)
