# -*- coding: utf-8 -*-
import json
import functools
from marshmallow import Schema
from hijim.common.exceptions import ClientParaError


def schema_parse(query_data: Schema = None, json_data: Schema = None,
                 form_data: Schema = None, reply_data: Schema = None):

    def _load_query(handler, schema: Schema):
        data = {}
        for key, value in handler.request.query_arguments.items():
            if not key.endswith('[]'):
                data[key] = value[-1]
            else:
                data[key] = value
        return schema.load(data)

    def _load_form(handler, schema):
        data = {}
        for key, value in handler.request.body_arguments.items():
            if not key.endswith('[]'):
                data[key] = value[-1]
            else:
                data[key] = value
        return schema.load(data)

    def _load_json(handler, schema):
        content_type = handler.request.headers.get('Content-Type')
        if not content_type.startswith('application/json'):
            raise ClientParaError(detail='invalid content-type')
        try:
            data = json.loads(handler.request.body)
        except Exception:
            raise ClientParaError(detail='invalid content format')
        else:
            return schema.load(data)

    def wrapper(function):

        @functools.wraps(function)
        async def f(handler, *args, **kwargs):
            if query_data and isinstance(query_data, Schema):
                kwargs.update({'query_data': _load_query(handler, query_data)})
            if form_data and isinstance(form_data, Schema):
                kwargs.update({'form_data': _load_form(handler, form_data)})
            if json_data and isinstance(json_data, Schema):
                kwargs.update({'json_data': _load_json(handler, json_data)})
            ret = await function(handler, *args, **kwargs)
            handler.set_header('Content-Type',
                               'application/json; charset=UTF-8')
            if reply_data and isinstance(reply_data, Schema):
                data = reply_data.dump(ret['data'])
                return handler.finish(dict(code=ret.get('code', 0),
                                           msg=ret.get('msg', ''),
                                           data=data))
            if reply_data and isinstance(reply_data, bool):
                return handler.finish(dict(code=0, msg=''))
            return ret
        return f
    return wrapper
