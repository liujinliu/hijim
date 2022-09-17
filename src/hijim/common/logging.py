# -*- coding: UTF-8 -*-
from tornado.options import define, options
import logging
import logging.config

define('logging-config', default=None, type=str, group='app',
       help='日志配置文件路径')

PLOG = logging.getLogger('app')  # 程序日志
ZLOG = logging.getLogger('biz')  # 业务日志

DEFAULT_LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': ('%(asctime)s %(filename)s[line:%(lineno)d] '
                       '%(levelname)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'app': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'biz': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        }
    },
}


def init_logging():
    level = 'DEBUG' if options.debug else options.logging.upper()
    logging.config.dictConfig(DEFAULT_LOGGING_CONFIG)
    if options.logging_config:
        logging.config.fileConfig(options.logging_config,
                                  disable_existing_loggers=False)
    logging.getLogger().setLevel(getattr(logging, level))
