# -*- coding: utf-8 -*-
import json
from enum import Enum
from typing import List
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.hybrid import hybrid_property
from hijim.common.db import DbBase, TableBase, TableTombstoneMixin


class TaskStatus(Enum):
    CREATED = 0  # 创建完成
    IN_PROCESS = 1  # 运行中
    SUCCESS = 2  # 成功
    FAILED = 3  # 失败
    TIMEOUT = 4  # 超时


class Task(DbBase, TableBase, TableTombstoneMixin):

    __tablename__ = "task"

    name = Column(String(32), server_default='', comment='task name')
    description = Column(String(256), server_default='',
                         comment='task description')
    node_id = Column(Integer, comment='node which the task belong')
    app_id = Column(Integer)
    engine_name = Column(String(32), server_default='',
                         comment='the engine where the task run')
    _app_paras = Column(String(1024), server_default='',
                        comment='the para of the app')
    _status = Column('status', Integer,
                     server_default=f'{TaskStatus.CREATED.value}')

    @hybrid_property
    def status(self):
        return TaskStatus(self._status)

    @status.setter
    def status(self, status: TaskStatus) -> None:
        self._status = status.value

    @hybrid_property
    def app_paras(self) -> List:
        return json.loads(self._app_paras) if self._app_paras else []

    @app_paras.setter
    def app_paras(self, app_paras: List) -> None:
        self._app_paras = json.dumps(app_paras) if app_paras else ''
