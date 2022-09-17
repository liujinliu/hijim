# -*- coding: utf-8 -*-

from marshmallow import Schema, fields


class ReqAppCreate(Schema):
    name = fields.String(required=True)


req_app_create = ReqAppCreate()
