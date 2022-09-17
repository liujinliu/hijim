# -*- coding: utf-8 -*-

from tornado.options import define

define('debug', default=False, type=bool, group='app',
       help='开启调试模式')
define('hijim-conf', default='', type=str, group='app',
       help='服务配置ini文件路径')
