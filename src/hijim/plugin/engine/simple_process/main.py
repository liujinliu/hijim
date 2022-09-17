# -*- coding: utf-8 -*-
import importlib
from multiprocessing import Pool
from hijim.common.base_work_engine import AbstractWorkEngine

_POOL = Pool(4)


class Engine(AbstractWorkEngine):

    def do_run(self, app, *args, **kwargs):
        mod = importlib(f'{app}.main.App')
        _POOL.apply_async(mod().run, *args, **kwargs)
