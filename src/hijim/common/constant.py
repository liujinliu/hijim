# -*- coding: utf-8 -*-
import os
from enum import Enum

HIJIM_ROOT_PATH = \
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__))))


class InnerEngineName(Enum):
    SIMPLE_THREAD = 0
