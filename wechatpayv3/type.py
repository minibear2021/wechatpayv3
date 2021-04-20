# -*- coding: utf-8 -*-

from enum import Enum

class WeChatPayType(Enum):
    JSAPI = 0
    APP = 1
    H5 = 2
    NATIVE = 3
    MINIPROG = 4

class RequestType(Enum):
    GET = 0
    POST = 1
