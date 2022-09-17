# -*- coding: utf-8 -*-
import pkgutil
import os
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

_HIJIM_ROOT = \
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__))))


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


class HijimServer:

    def __init__(self):
        self.app = None

    def init_app(self):
        init_route()
        settings = {
            'autoreload': False,
            'gzip': True,
        }
        self.app = WebApplication(handlers=Route.get_routes(), **settings)

    async def run(self):
        HijimApp().init_workspace()
        await init_db()
        self.app.listen(8000)
        await asyncio.Event().wait()

    def start(self):
        parse_command_line()
        init_logging()
        HijimConf().conf_init(options.hijim_conf)
        self.init_app()
        asyncio.run(self.run())


start_server = HijimServer().start
