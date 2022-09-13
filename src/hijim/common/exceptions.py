# -*- coding: utf-8 -*-
import warnings
from enum import Enum


class _ErrorCode(Enum):
    CLIENT_PARA_ERROR = 400001


class _MetaError(type):

    __error_codes = []

    def __new__(cls, name, bases, attr):
        new_class = super().__new__(cls, name, bases, attr)
        class_name = attr['__qualname__']
        code = getattr(new_class, 'code', None)
        if code in cls.__error_codes:
            warnings.warn(f'{class_name} error code is already been used!!')
        else:
            cls.__error_codes.append(code)
        return new_class


class BaseError(Exception, metaclass=_MetaError):

    code = 500
    message = '内部错误'
    http_status = 500

    def __init__(self, message=None, **kwargs):
        self.msg = (message or self.message).format(**kwargs)
        super().__init__(**kwargs)


class ClientParaError(BaseError):
    code = _ErrorCode.CLIENT_PARA_ERROR.value
    http_status = 403
    message = 'client param error({detail})'
