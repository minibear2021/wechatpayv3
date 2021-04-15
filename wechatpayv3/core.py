# -*- coding: utf-8 -*-
from .utils import build_authorization
import requests


class Core():
    def __init__(self, mchid, mch_key_serial_no, mch_private_key, wechat_public_key):
        self._mchid = mchid
        self._mch_key_serial_no = mch_key_serial_no
        self._mch_private_key = mch_private_key
        self._wechat_public_key = wechat_public_key
        self._gate_way = 'https://api.mch.weixin.qq.com'

    def get(self, path):
        headers = {}
        headers.update({'Content-Type': 'application/json'})
        headers.update({'Accept': 'application/json'})
        headers.update({'User-Agent': 'wechatpay v3 python sdk v0.1'})
        headers.update({'Authorization': build_authorization(
            path, 'GET', self._mchid, self._mch_key_serial_no, self._mch_private_key)})
        response = requests.get(url=self._gate_way + path, headers=headers)
        return response.status_code, response.text

    def post(self, path, json=None):
        headers = {}
        headers.update({'Content-Type': 'application/json'})
        headers.update({'Accept': 'application/json'})
        headers.update({'User-Agent': 'wechatpay v3 python sdk v0.1'})
        headers.update({'Authorization': build_authorization(
            path, 'POST', self._mchid, self._mch_key_serial_no, self._mch_private_key, json)})
        response = requests.post(self._gate_way + path,
                                 json=json,
                                 headers=headers)
        return response.status_code, response.text
