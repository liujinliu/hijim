# -*- coding: utf-8 -*-

import sys
import os
from configparser import ConfigParser
from .utils import HijimConf, singleton
from .constant import HIJIM_ROOT_PATH
from .logging import PLOG


_hijim_conf = HijimConf()


@singleton
class HijimApp:

    def __init__(self):
        self.__workspace = None

    def init_workspace(self, workspace=None):
        if not workspace:
            conf = _hijim_conf.APP
            workspace = conf['workspace'] or os.path.join(HIJIM_ROOT_PATH,
                                                          'tests', 'workspace')
        PLOG.info(f'workspace is {workspace}')
        os.makedirs(workspace, exist_ok=True)
        self.__workspace = workspace
        if self.__workspace not in sys.path:
            sys.path.append(self.__workspace)

    @property
    def workspace(self):
        return self.__workspace

    def get_app_ini(self, app_name):
        config = ConfigParser()
        config.read(os.path.join(self.__workspace, app_name, 'app.ini'))
        return config
