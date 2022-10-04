# -*- coding: utf-8 -*-
import requests
import json
from hijim.common.base_app import AbstractApp


class App(AbstractApp):

    def __init__(self):
        self.__actions = {
            'ACTION0': self.__show_value,
            'ACTION1': self.__show_value
        }

    def __show_value(self, value):
        print(value)

    def __run_by_action(self, action, value):
        self.__actions[action](value)

    def do_run(self, paras_list) -> dict:
        if not paras_list:
            return
        for paras in paras_list:
            action, value = paras.split('::', 1)
            self.__run_by_action(action, value)
