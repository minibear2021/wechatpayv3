# -*- coding: utf-8 -*-

from enum import Enum


class RequestType(Enum):
    GET = 0
    POST = 1
    PATCH = 2


class WeChatPayType(Enum):
    JSAPI = 0
    APP = 1
    H5 = 2
    NATIVE = 3
    MINIPROG = 4
