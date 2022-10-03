# -*- coding: utf-8 -*-
import logging
import os
import requests
from abc import ABC, abstractmethod

LOG = logging.getLogger()


class AbstractApp(ABC):
    """
    This is the interface of app, each app should register several
    **keyword** to hijim.
    When write a new app, you should use the app-name as the fold-name,
    and always name the entry file as *main.py*
    TODO define how to register **keyword** to hijim.
    """

    _HIJIM_ENDPOINT = os.environ.get(
        'HIJIM_ENDPOINT', 'http://127.0.0.1:8000')

    @abstractmethod
    def do_run(self, paras_list) -> dict:
        """
        Args:
            paras_list:
                each para item is a string with the pattern
                *keyword::paras*
                how to parse the para depends on the app self
        Returns:
            return with no exception will be treated as success, basically it
            should return a *dict*
        """

    def __record_the_result(self, run_id, result: dict):
        """
        call the RestFul of hijim to record the result on run_id
        Returns:
        """
        requests.post(f'{self._HIJIM_ENDPOINT}/api/v1/unit-result',
                      json=dict(runId=run_id, result=result))

    def run(self, run_id, paras_list) -> None:
        try:
            res = self.do_run(paras_list)
        except Exception as e:
            LOG.error(e, exc_info=True)
            res = dict(error=1, data=str(e))
        self.__record_the_result(run_id, result=res)
