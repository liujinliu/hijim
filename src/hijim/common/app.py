# -*- coding: utf-8 -*-

import sys
from .utils import HijimConf, singleton


@singleton
class HijimApp:

    def __init__(self):
        self.__workspace = None

    def init_workspace(self, workspace=None):
        if not workspace:
            conf = HijimConf().APP
            workspace = conf['workspace']
        if workspace not in sys.path:
            sys.path.append(workspace)
        self.__workspace = workspace

    @property
    def workspace(self):
        return self.__workspace

    def app_upload(self, app_name, file):
        """
        Args:
            app_name:
                the *file* will be extract to *workspace*, and the folder will
                be rename to *app_name*
            file:
                an compressed file, contains all the app files
        Returns:
        """
        pass
