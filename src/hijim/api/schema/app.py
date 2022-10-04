# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class ReqAppCreate(Schema):
    name = fields.String(required=True)


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
