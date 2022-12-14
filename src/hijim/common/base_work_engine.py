# -*- coding: utf-8 -*-
import logging
from abc import ABC, abstractmethod

LOG = logging.getLogger()


class AbstractWorkEngine(ABC):
    """This is the interface of work engine, hijim can register any
    third party module that implemented this interface. Because write async
    code is not easy, so this class is remained on sync currently. And There is
    one IMPORTANT thing should be mentioned, that this module should not
    depend on hijim. Cause one day this module should be move out as an
    independent module"""

    @abstractmethod
    def do_run(self, app, *, task_id, paras_list):
        """
        Each engine should implement this method to do the real job.

        Args:
            app: The app, and the entry class is *<app-name>*.main.App
            task_id: will be used for the app to send result to hijim
            paras_list:

        Returns:
        """
        pass

    def run(self, app, *, task_id, paras_list: dict = None):
        """
        This the entry for the work engine

        Args:
            task_id: the id for record the result
            app: app name that passed to the task execute engine
            paras_list: the paras pass to the app

        Returns:
        """
        self.do_run(app, task_id=task_id, paras_list=paras_list)
