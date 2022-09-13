# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Text
from hijim.common.db import DbBase, TableBase, TableTombstoneMixin


class App(DbBase, TableBase, TableTombstoneMixin):

    __tablename__ = "app"

    name = Column(String(32), server_default='')
    version = Column(String(32), server_default='')
    author = Column(String(32), server_default='')
    author_email = Column(String(64), server_default='')
    description = Column(Text, server_default='')
    file = Column(String(128), server_default='')





