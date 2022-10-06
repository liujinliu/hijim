# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class ReqAppCreate(Schema):
    name = fields.String(required=True)
    file_ini = fields.String(required=True, data_key='fileIni')
    file_main = fields.String(required=True, data_key='fileMain')


class ResAppCreate(Schema):
    id = fields.Integer(required=True)


req_app_create = ReqAppCreate()
res_app_create = ResAppCreate()


class ResAppDetail(Schema):
    name = fields.String(required=True)
    author = fields.String(required=True)
    version = fields.String(required=True)
    description = fields.String(required=True)
    config = fields.Raw(dump_default=None)


res_app_detail = ResAppDetail()
