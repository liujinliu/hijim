# -*- coding: utf-8 -*-
from sqlalchemy import Column, String
from hijim.common.db import DbBase, TableBase, TableTombstoneMixin


class App(DbBase, TableBase, TableTombstoneMixin):

    __tablename__ = "app"

    name = Column(String(32), server_default='')
    description = Column(String(512), server_default='')
    author = Column(String(32), server_default='')
    version = Column(String(16), server_default='')
