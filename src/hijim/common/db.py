# -*- coding: utf-8 -*-
import asyncio
import functools
from sqlalchemy import Column, DateTime, func, Integer, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from collections import defaultdict
from contextlib import asynccontextmanager
from hijim.common.utils import singleton, HijimConf

_hijim_conf = HijimConf()
DbBase = declarative_base()

engine = create_async_engine(_hijim_conf.DB['conn'])
_async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


@singleton
class SessionManager:

    def __init__(self):
        self.__task_local = defaultdict(list)

    @asynccontextmanager
    async def use(self):
        task_id = id(asyncio.current_task())
        session = _async_session()
        old_session_num = len(self.__task_local[task_id])
        try:
            async with session:
                async with session.begin():
                    self.__task_local[task_id].append(session)
                    yield
        finally:
            if task_id and len(self.__task_local[task_id]) > old_session_num:
                self.__task_local[task_id].pop()
            if not self.__task_local[task_id]:
                del self.__task_local[task_id]

    def get(self):
        task_id = id(asyncio.current_task())
        if self.__task_local[task_id]:
            return self.__task_local[task_id][-1]


def use_db_session(function):

    @functools.wraps(function)
    async def f(*args, **kwargs):
        async with SessionManager().use():
            ret = await function(*args, **kwargs)
        return ret

    return f


def with_db_session(function):

    @functools.wraps(function)
    async def f(*args, **kwargs):
        assert 'session' not in kwargs, '"session" keyword has been occupied'
        kwargs.update({'session': SessionManager().get()})
        ret = await function(*args, **kwargs)
        return ret
    return f


class TableBase:
    id = Column(Integer, primary_key=True)
    create_at = Column(DateTime, server_default=func.now())

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}

    @with_db_session
    async def create(self, *, session=None):
        session.add(self)
        await session.flush()

    @classmethod
    @with_db_session
    async def get_by_id(cls, _id, *, session=None):
        result = await session.execute(select(cls).filter(cls.id == _id))
        return result.scalars().first()

    @with_db_session
    async def delete(self, *, session=None):
        await session.delete(self)

    @classmethod
    @with_db_session
    async def get_list(cls, *, page=0, page_size=0, session=None):
        q = select(cls).order_by(cls.id.desc())
        if page and page_size:
            q = q.limit(page_size).offset(page_size * (page - 1))
        result = await session.execute(q)
        return result.scalars().all()


class TableTombstoneMixin:
    is_delete = Column(Boolean, server_default='0')
