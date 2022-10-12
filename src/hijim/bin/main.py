# -*- coding: utf-8 -*-
import pkgutil
import asyncio
from tornado.web import Application as WebApplication
from tornado.options import parse_command_line, options
import hijim.model
from hijim.api.base import Route
import hijim.api
from importlib import import_module
from hijim.common.utils import HijimConf
from hijim.common.app import HijimApp
from hijim.common.logging import PLOG, init_logging
from hijim.bin.options import * # noqa
from hijim.common.engine_register import EngineRegister
from hijim.plugin.engine.simple_thread.main import (
    Engine as SimpleThreadEngine)
from hijim.common.constant import InnerEngineName


_hijim_app = HijimApp()
_engine_register = EngineRegister()
_hijim_conf = HijimConf()


async def init_db():
    from hijim.common.db import DbBase, engine
    for _, name, _ in pkgutil.iter_modules(hijim.model.__path__):
        PLOG.debug(f'loading model {name} ...')
        import_module(f'hijim.model.{name}', package=__package__)
    async with engine.begin() as conn:
        await conn.run_sync(DbBase.metadata.create_all)


def init_route():
    for _, name, _ in pkgutil.iter_modules(hijim.api.__path__):
        PLOG.debug(f'loading api {name} ...')
        import_module(f'hijim.api.{name}', package=__package__)


def inner_engine_reg():
    _engine_register.register(name=InnerEngineName.SIMPLE_THREAD.name,
                              engine=SimpleThreadEngine)


class HijimServer:

    def __init__(self):
        self.app = None

    def init_app(self):
        inner_engine_reg()
        init_route()
        settings = {
            'gzip': True,
            'autoreload': options.debug
        }
        self.app = WebApplication(handlers=Route.get_routes(), **settings)

    async def run(self):
        await init_db()
        self.app.listen(8000)
        await asyncio.Event().wait()

    def start(self):
        parse_command_line()
        init_logging()
        _hijim_conf.conf_init(options.hijim_conf)
        _hijim_app.init_workspace()
        self.init_app()
        asyncio.run(self.run())


start_server = HijimServer().start
