# -*- coding: utf-8 -*-
from collections import defaultdict
from hijim.model.app import App
from hijim.common.app import HijimApp
from hijim.common.utils import with_executor


class AppService:

    @classmethod
    @with_executor
    def __read_config_from_ini(cls, app_name):
        return HijimApp().get_app_ini(app_name=app_name)

    @classmethod
    async def app_create(cls, *, name):
        """
        Args:
            name: name of the app
        Returns:
        """
        config = await cls.__read_config_from_ini(app_name=name)
        app_model = App(name=name, author=config['info']['author'],
                        version=config['info']['version'],
                        description=config['info']['description'])
        await app_model.create()
        return dict(id=app_model.id)

    @classmethod
    async def app_detail(cls, *, app_id):
        app = await App.get_by_id(app_id)
        config = await cls.__read_config_from_ini(app_name=app.name)
        config_map = defaultdict(dict)
        for section in config:
            for k in config[section]:
                config_map[section][k] = config[section][k]
        return dict(name=app.name, author=app.author, version=app.version,
                    description=app.description, config=config_map)
