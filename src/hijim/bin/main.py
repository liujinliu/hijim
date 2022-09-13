# -*- coding: utf-8 -*-
import logging
import pkgutil
import asyncio
from tornado.web import Application as WebApplication
import hijim.model
from hijim.api.base import Route
import hijim.api
from importlib import import_module
from hijim.common.db import DbBase, engine


LOG = logging.getLogger()


async def init_db():
    for _, name, _ in pkgutil.iter_modules(hijim.model.__path__):
        LOG.debug(f'loading model {name} ...')
        import_module(f'hijim.model.{name}', package=__package__)
    async with engine.begin() as conn:
        await conn.run_sync(DbBase.metadata.create_all)


def init_route():
    for _, name, _ in pkgutil.iter_modules(hijim.api.__path__):
        LOG.debug(f'loading api {name} ...')
        import_module(f'hijim.api.{name}', package=__package__)


class HijimServer:

    def init_app(self):
        # asyncio.run(init_db())
        init_route()
        settings = {
            'autoreload': False,
            'gzip': True,
        }
        self.app = WebApplication(handlers=Route.get_routes(), **settings)

    async def run(self):
        self.app.listen(8000)
        await asyncio.Event().wait()

    def start(self):
        self.init_app()
        asyncio.run(self.run())


start_server = HijimServer().start
