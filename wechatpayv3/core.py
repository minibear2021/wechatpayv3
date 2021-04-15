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
        if response.status_code in [200, 202, 204]:
            timestamp = response.headers.get('Wechatpay-Timestamp')
            nonce = response.headers.get('Wechatpay-Nonce')
            signature = response.headers.get('Wechatpay-Signature')
            body = response.content
            serial_no = response.headers.get('Wechatpay-Serial')
            if serial_no != certificate_serial_number(self._wechat_certificate):
                return -1, '{"message": "微信支付平台证书序号不一致"}'
            if not verify_response(timestamp, nonce, body, signature, self._wechat_certificate):
                return -1, '{"message": "应答签名验证失败"}'
        return response.status_code, response.content

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
        if response.status_code in [200, 202, 204]:
            timestamp = response.headers.get('Wechatpay-Timestamp')
            nonce = response.headers.get('Wechatpay-Nonce')
            signature = response.headers.get('Wechatpay-Signature')
            body = response.content
            serial_no = response.headers.get('Wechatpay-Serial')
            if serial_no != certificate_serial_number(self._wechat_certificate):
                return -1, '{"message": "微信支付平台证书序号不一致"}'
            if not verify_response(timestamp, nonce, body, signature, self._wechat_certificate):
                return -1, '{"message": "应答签名验证失败"}'
        return response.status_code, response.content
