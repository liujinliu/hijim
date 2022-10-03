# -*- coding: utf-8 -*-
import threading
from functools import partial
from hijim.common.base_work_engine import AbstractWorkEngine


class Engine(AbstractWorkEngine):

    def do_run(self, app, *args, **kwargs):
        mod = __import__(f'{app}.main', globals(), locals(), ['App'], 0)
        f = partial(mod.App().run, *args, **kwargs)
        t = threading.Thread(target=f)
        t.start()
