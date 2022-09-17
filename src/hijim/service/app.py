# -*- coding: utf-8 -*-
from hijim.model.app import App


class AppService:

    @staticmethod
    async def app_create(*, name):
        app_model = App(name=name)
        await app_model.create()
