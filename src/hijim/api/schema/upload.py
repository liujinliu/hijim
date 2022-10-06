# -*- coding: utf-8 -*-
from marshmallow import fields, Schema


class ResFileUpload(Schema):
    tmp_file_name = fields.String(required=True, data_key='tmpFileName')


res_file_upload = ResFileUpload()
