# -*- coding: utf-8 -*-
from hijim.model.app import App


class AppService:

    @staticmethod
    async def app_create(*, name, version, author, author_email, description,
                         file):
        app_model = App(name=name, version=version, author=author, file=file,
                        author_email=author_email, description=description)
        await app_model.create()
