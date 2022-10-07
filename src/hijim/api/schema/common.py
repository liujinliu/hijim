# -*- coding: utf-8 -*-
from marshmallow import fields, Schema


class PageSchemaMixin(Schema):
    page = fields.Integer(load_default=0)
    page_size = fields.Integer(load_default=0)
