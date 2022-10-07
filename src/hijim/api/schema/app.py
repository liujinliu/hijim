# -*- coding: utf-8 -*-

from marshmallow import Schema, fields
from .common import PageSchemaMixin


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


class ReqAppList(PageSchemaMixin):
    pass


class _AppItem(Schema):
    name = fields.String(required=True)
    author = fields.String(required=True)
    version = fields.String(required=True)
    create_at = fields.Date(data_key='createAt')


class ResAppList(Schema):
    apps = fields.Nested(_AppItem, many=True)


req_app_list = ReqAppList()
res_app_list = ResAppList()
