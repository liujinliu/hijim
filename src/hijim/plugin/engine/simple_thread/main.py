# -*- coding: utf-8 -*-
import threading
import queue
from functools import partial
from hijim.common.base_work_engine import AbstractWorkEngine
from hijim.common.utils import singleton
from hijim.common.logging import PLOG


@singleton
class Engine(AbstractWorkEngine):

    def __init__(self):
        self.__queue = queue.Queue()
        threading.Thread(target=self.__queue_processor, daemon=True).start()

    def __queue_processor(self):
        while True:
            f = self.__queue.get()
            try:
                f()
            except Exception as e:
                PLOG.warning(e, exc_info=True)
            finally:
                self.__queue.task_done()

    def do_run(self, app, *args, **kwargs):
        mod = __import__(f'{app}.main', globals(), locals(), ['App'], 0)
        self.__queue.put(partial(mod.App().run, *args, **kwargs))
