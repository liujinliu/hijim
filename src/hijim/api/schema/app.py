# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class ReqAppCreate(Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
    file = fields.String(required=True)
    version = fields.String(required=True)
    author = fields.String(required=True)
    author_email = fields.String(required=True)


req_app_create = ReqAppCreate()
