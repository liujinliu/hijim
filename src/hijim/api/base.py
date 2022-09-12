# -*- coding: utf-8 -*-
import logging
from tornado.web import RequestHandler
from traceback import format_tb
from marshmallow import ValidationError as SchemaValidationError
from hijim.common.exceptions import BaseError


LOG = logging.getLogger()


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

