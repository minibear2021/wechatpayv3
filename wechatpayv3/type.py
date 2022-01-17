# -*- coding: utf-8 -*-

from enum import Enum, unique


@unique
class RequestType(Enum):
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    PUT = 'PUT'
    DELETE = 'DELETE'


class WeChatPayType(Enum):
    JSAPI = 0
    APP = 1
    H5 = 2
    NATIVE = 3
    MINIPROG = 4


class SignType(Enum):
    RSA_SHA256 = 0
    HMAC_SHA256 = 1
    MD5 = 2
