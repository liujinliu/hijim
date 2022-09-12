# -*- coding: utf-8 -*-
import os


def __env_int(k, default):
    if k in os.environ:
        return int(os.environ[k])
    return default


def __env_str(k, default):
    return os.environ.get(k, default)


def __env_bool(k, default):
    if k in os.environ:
        return os.environ[k].upper() in ['TRUE', 'T', 'Y', 'YES']
    return default


DB_CONF = {
    'conn': __env_str('DB_CONN', 'sqlite+aiosqlite:///unitestdb'),
    'engine_setting': {
        'echo': __env_bool('DB_ECHO', False),
        'echo_pool': __env_bool('DB_ECHO_POOL', False),
        'pool_recycle': __env_int('DB_POOL_RECYCLE', 7*60*60),
        'pool_size': __env_int('DB_POOL_SIZE', 20),
        'max_overflow': __env_int('DB_POOL_OVERFLOW', 20)
    }
}