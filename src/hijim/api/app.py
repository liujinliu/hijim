# -*- coding: utf-8 -*-

from hijim.service.app import AppService
from hijim.common.db import use_db_session
from .base import BaseHandler, Route
from .schema.app import req_app_create
from .utils import schema_parse


@Route('app')
class AppHandler(BaseHandler):
    """AppHandler is the api interface of for app management"""

    @use_db_session
    async def __do_post(self, json_data):
        return await AppService.app_create(**json_data)

    @schema_parse(json_data=req_app_create, reply_data=True)
    async def post(self, *, json_data):
        """
        This interface serve the request of app create
        Args:
            json_data: the parameters for app create

        Returns:
            N/A
        """
        await self.__do_post(json_data)
