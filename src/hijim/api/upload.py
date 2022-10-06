# -*- coding: utf-8 -*-
import os
from hijim.common.exceptions import FileUploadError
from hijim.common.utils import HijimConf
from hijim.common.utils import with_executor
from .base import BaseHandler, Route
from .utils import schema_parse


@Route('upload')
class FileUploadHandler(BaseHandler):

    @with_executor
    def __store_file(self, filename, content):
        with open(filename, 'wb') as f:
            f.write(content)

    @schema_parse(reply_data=True)
    async def post(self):
        file_metas = self.request.files.get('file', None)
        if not file_metas:
            raise FileUploadError(detail='no file meta')
        meta = file_metas[0]
        await self.__store_file(
            os.path.join(HijimConf().tmp_path, meta['filename']), meta['body'])
