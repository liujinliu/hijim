# -*- coding: utf-8 -*-
import os
import pathlib
import shutil
from collections import defaultdict
from hijim.model.app import App
from hijim.common.app import HijimApp
from hijim.common.utils import with_executor, HijimConf


class AppService:

    @classmethod
    @with_executor
    def __read_config_from_ini(cls, app_name):
        return HijimApp().get_app_ini(app_name=app_name)

    @classmethod
    @with_executor
    def __copy_app_files(cls, app_name, file_ini, file_main):
        workspace = HijimApp().workspace
        app_path = os.path.join(workspace, app_name)
        os.makedirs(app_path, exist_ok=True)
        tmp_path = HijimConf().tmp_path
        pathlib.Path(os.path.join(app_path, '__init__.py')).touch()
        shutil.move(os.path.join(tmp_path, file_ini),
                    os.path.join(app_path, 'app.ini'))
        shutil.move(os.path.join(tmp_path, file_main),
                    os.path.join(app_path, 'main.py'))

    @classmethod
    async def app_create(cls, *, name, file_ini, file_main):
        """
        Args:
            name: name of the app
        Returns:
        """
        await cls.__copy_app_files(name, file_ini, file_main)
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

    @classmethod
    async def app_list(cls, *, page=1, page_size=10):
        ret = await App.get_list(page=page, page_size=page_size)
        apps = [dict(name=x.name, author=x.author, version=x.version,
                     create_at=x.create_at)
                for x in ret]
        return dict(apps=apps)
