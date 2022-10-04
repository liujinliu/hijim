# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from sqlalchemy.ext.hybrid import hybrid_property
from hijim.common.db import DbBase, TableBase, TableTombstoneMixin


class Pipeline(DbBase, TableBase, TableTombstoneMixin):

    __tablename__ = "pipeline"

    name = Column(String(32), server_default='')
    description = Column(String(256), server_default='')
    _nodes = Column('nodes', String(1024), server_default='')

    @hybrid_property
    def nodes(self):
        if self._nodes:
            return [int(x.strip()) for x in self._nodes.split(',')]
        return []

    @nodes.setter
    def status(self, nodes) -> None:
        if not nodes:
            self._nodes = ''
        else:
            self._nodes = ','.join([f'{x}' for x in nodes])
