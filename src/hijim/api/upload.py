# -*- coding: utf-8 -*-
import os
import uuid
from hijim.common.exceptions import FileUploadError
from hijim.common.utils import HijimConf
from hijim.common.utils import with_executor
from .base import BaseHandler, Route
from .utils import schema_parse
from .schema.upload import res_file_upload


_hijim_conf = HijimConf()


@Route('upload')
class FileUploadHandler(BaseHandler):

    @with_executor
    def __store_file(self, filename, content):
        with open(filename, 'wb') as f:
            f.write(content)

    @schema_parse(reply_data=res_file_upload)
    async def post(self):
        file_metas = self.request.files.get('file', None)
        if not file_metas:
            raise FileUploadError(detail='no file meta')
        meta = file_metas[0]
        filename = uuid.uuid4().hex
        await self.__store_file(
            os.path.join(_hijim_conf.tmp_path, filename), meta['body'])
        return dict(data=dict(tmp_file_name=filename))
