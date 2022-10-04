# -*- coding: utf-8 -*-

from sqlalchemy import Column, String
from hijim.common.db import DbBase, TableBase, TableTombstoneMixin


class Node(DbBase, TableBase, TableTombstoneMixin):

    __tablename__ = "node"

    name = Column(String(32), server_default='')
    description = Column(String(256), server_default='')
