# -*- coding: utf-8 -*-
import atexit
import threading
from functools import partial
from multiprocessing.pool import Pool
from hijim.common.base_work_engine import AbstractWorkEngine

_POOL = Pool(4)


class Engine(AbstractWorkEngine):

    def do_run(self, app, *args):
        mod = __import__(f'{app}.main', globals(), locals(), ['App'], 0)
        f = partial(mod.App().run, *args)
        t = threading.Thread(target=f)
        t.start()

    @staticmethod
    @atexit.register
    def __close_engine():
        _POOL.close()
