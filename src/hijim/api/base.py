# -*- coding: utf-8 -*-
import logging
from tornado.web import RequestHandler
from traceback import format_tb
from marshmallow import ValidationError as SchemaValidationError
from hijim.common.exceptions import BaseError


LOG = logging.getLogger()
BASE_URI = '/api/v1/'


class Route:

    _ROUTES = []
    _ROUTE_URIS = []

    def __init__(self, uri):
        if uri in Route._ROUTE_URIS:
            raise BaseError(message=f'重复的URI定义({uri})')
        Route._ROUTE_URIS.append(uri)
        self.__uri = f'{BASE_URI}{uri}'

    def __call__(self, handler):
        Route._ROUTES.append((r'{}'.format(self.__uri), handler))
        return handler

    @classmethod
    def get_routes(cls):
        return cls._ROUTES


class BaseHandler(RequestHandler):

    def write_error(self, status_code: int, **kwargs) -> None:
        if 'exc_info' in kwargs:
            _, error, trace_back = kwargs['exc_info']
            if isinstance(error, BaseError):
                LOG.error(
                    'Exception: \n{}'.format("\t".join(format_tb(trace_back))))
                self.write(dict(code=error.code, msg=error.msg))
                self.set_status(error.http_status)
                return
            if isinstance(error, SchemaValidationError):
                LOG.error(
                    'Exception: \n{}'.format("\t".join(format_tb(trace_back))))
                self.write(dict(code=1001, msg=error.normalized_messages()))
                self.set_status(400)
                return
            super().write_error(status_code, **kwargs)
