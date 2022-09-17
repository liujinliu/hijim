# -*- coding: utf-8 -*-
import json
from sqlalchemy import Column, String
from sqlalchemy.ext.hybrid import hybrid_property
from hijim.common.db import DbBase, TableBase, TableTombstoneMixin


class App(DbBase, TableBase, TableTombstoneMixin):

    __tablename__ = "app"

    name = Column(String(32), server_default='')
    _config = Column('config', String(1024), server_default='')

    @hybrid_property
    def config(self):
        return json.loads(self._config) if self._config else {}
