# -*- coding: utf-8 -*-
import asyncio
import functools
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from collections import defaultdict
from contextlib import asynccontextmanager
from hijim.conf.config import DB_CONF
from hijim.common.mixins import SingletonMixin


Base = declarative_base()

_engine = create_async_engine(DB_CONF['conn'], **DB_CONF['engine_setting'])
_async_session = sessionmaker(
    _engine, expire_on_commit=False, class_=AsyncSession
)


class SessionManager(SingletonMixin):

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


def use_db_session():

    def wrapper(function):

        @functools.wraps(function)
        async def f(*args, **kwargs):
            async with SessionManager().use():
                ret = await function(*args, **kwargs)
            return ret
        return f

    return wrapper


def with_db_session(function):

    @functools.wraps(function)
    async def f(*args, **kwargs):
        assert 'session' not in kwargs, '"session" keyword has been occupied'
        kwargs.update({'session': SessionManager().get()})
        ret = await function(*args, **kwargs)
        return ret
    return f
