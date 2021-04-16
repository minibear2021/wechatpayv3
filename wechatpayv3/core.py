# -*- coding: utf-8 -*-
from .utils import build_authorization, verify_response, certificate_serial_number
import requests
import json


class Core():
    def __init__(self, mchid, mch_key_serial_no, mch_private_key, wechat_certificate):
        self._mchid = mchid
        self._mch_key_serial_no = mch_key_serial_no
        self._mch_private_key = mch_private_key
        self._wechat_certificate = wechat_certificate
        self._gate_way = 'https://api.mch.weixin.qq.com'

    def get(self, path):
        headers = {}
        headers.update({'Content-Type': 'application/json'})
        headers.update({'Accept': 'application/json'})
        headers.update(
            {'User-Agent': 'wechatpay v3 python sdk(https://github.com/minibear2021/wechatpayv3)'})
        authorization = build_authorization(
            path, 'GET', self._mchid, self._mch_key_serial_no, self._mch_private_key)
        headers.update({'Authorization': authorization})
        response = requests.get(url=self._gate_way + path, headers=headers)
        if response.status_code in range(200, 300) and self._wechat_certificate:
            timestamp = response.headers.get('Wechatpay-Timestamp')
            nonce = response.headers.get('Wechatpay-Nonce')
            signature = response.headers.get('Wechatpay-Signature')
            body = response.text
            serial_no = response.headers.get('Wechatpay-Serial')
            if serial_no != certificate_serial_number(self._wechat_certificate):
                raise Exception(
                    "wechatpay certificate serial number does not match")
            if not verify_response(timestamp, nonce, body, signature, self._wechat_certificate):
                raise Exception("signature verification failed")
        return response.status_code, response.text

    def post(self, path, data=None):
        headers = {}
        headers.update({'Content-Type': 'application/json'})
        headers.update({'Accept': 'application/json'})
        headers.update(
            {'User-Agent': 'wechatpay v3 python sdk(https://github.com/minibear2021/wechatpayv3)'})
        authorization = build_authorization(
            path, 'POST', self._mchid, self._mch_key_serial_no, self._mch_private_key, data=json.dumps(data))
        headers.update({'Authorization': authorization})
        response = requests.post(self._gate_way + path,
                                 json=data,
                                 headers=headers)
        if response.status_code in range(200, 300) and self._wechat_certificate:
            timestamp = response.headers.get('Wechatpay-Timestamp')
            nonce = response.headers.get('Wechatpay-Nonce')
            signature = response.headers.get('Wechatpay-Signature')
            body = response.text
            serial_no = response.headers.get('Wechatpay-Serial')
            if serial_no != certificate_serial_number(self._wechat_certificate):
                raise Exception(
                    "wechatpay certificate serial number does not match")
            if not verify_response(timestamp, nonce, body, signature, self._wechat_certificate):
                raise Exception("signature verification failed")
        return response.status_code, response.text
