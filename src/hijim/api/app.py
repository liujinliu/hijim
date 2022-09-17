# -*- coding: utf-8 -*-

from hijim.service.app import AppService
from hijim.common.db import use_db_session
from .base import BaseHandler, Route
from .schema.app import (
    req_app_create, res_app_create, res_app_detail)
from .utils import schema_parse


@Route('app')
class AppHandler(BaseHandler):
    """AppHandler is the api interface for app management"""

    @use_db_session
    async def __do_post(self, json_data):
        return await AppService.app_create(**json_data)

    @schema_parse(json_data=req_app_create, reply_data=res_app_create)
    async def post(self, *, json_data):
        """
        This interface serve the request of app create
        Args:
            json_data:
                the parameters for app create, here is an example::
                    {
                        name: "demo_app"
                    }
        Returns:
            N/A
        """
        ret = await self.__do_post(json_data)
        return dict(data=ret)


@Route('app/(?P<app_id>.*)')
class AppDetailHandler(BaseHandler):

    @use_db_session
    async def __do_get(self, app_id):
        return await AppService.app_detail(app_id=app_id)

    @schema_parse(reply_data=res_app_detail)
    async def get(self, app_id):
        ret = await self.__do_get(app_id)
        return dict(data=ret)
