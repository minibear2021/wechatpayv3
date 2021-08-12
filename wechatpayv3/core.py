# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime

import requests

from .type import RequestType
from .utils import build_authorization, aes_decrypt, load_certificate, rsa_sign, rsa_verify, rsa_encrypt, rsa_decrypt


class Core():
    def __init__(self, mchid, cert_serial_no, private_key, apiv3_key, cert_dir=None):
        self._mchid = mchid
        self._cert_serial_no = cert_serial_no
        self._private_key = private_key
        self._apiv3_key = apiv3_key
        self._gate_way = 'https://api.mch.weixin.qq.com'
        self._certificates = []
        self._cert_dir = cert_dir + '/' if cert_dir else None
        self._load_local_certificates()

    def _update_certificates(self):
        path = '/v3/certificates'
        code, message = self.request(path, skip_verify=False if self._certificates else True)
        if code != 200:
            return
        self._certificates.clear()
        data = json.loads(message).get('data')
        for value in data:
            serial_no = value.get('serial_no')
            effective_time = value.get('effective_time')
            expire_time = value.get('expire_time')
            encrypt_certificate = value.get('encrypt_certificate')
            algorithm = nonce = associated_data = ciphertext = None
            if encrypt_certificate:
                algorithm = encrypt_certificate.get('algorithm')
                nonce = encrypt_certificate.get('nonce')
                associated_data = encrypt_certificate.get('associated_data')
                ciphertext = encrypt_certificate.get('ciphertext')
            if not (serial_no and effective_time and expire_time and algorithm and nonce and associated_data and ciphertext):
                continue
            cert_str = aes_decrypt(
                nonce=nonce,
                ciphertext=ciphertext,
                associated_data=associated_data,
                apiv3_key=self._apiv3_key)
            certificate = load_certificate(cert_str)
            if not certificate:
                continue
            now = datetime.utcnow()
            if now < certificate.not_valid_before or now > certificate.not_valid_after:
                continue
            self._certificates.append(certificate)
            if not self._cert_dir:
                continue
            if not os.path.exists(self._cert_dir):
                os.makedirs(self._cert_dir)
            if not os.path.exists(self._cert_dir + serial_no + '.pem'):
                f = open(self._cert_dir + serial_no + '.pem', 'w')
                f.write(cert_str)
                f.close()

    def _verify_signature(self, headers, body):
        signature = headers.get('Wechatpay-Signature')
        timestamp = headers.get('Wechatpay-Timestamp')
        nonce = headers.get('Wechatpay-Nonce')
        serial_no = headers.get('Wechatpay-Serial')
        cert_found = False
        for cert in self._certificates:
            if int('0x' + serial_no, 16) == cert.serial_number:
                cert_found = True
                certificate = cert
                break
        if not cert_found:
            self._update_certificates()
            for cert in self._certificates:
                if int('0x' + serial_no, 16) == cert.serial_number:
                    cert_found = True
                    certificate = cert
                    break
            if not cert_found:
                return False
        if not rsa_verify(timestamp, nonce, body, signature, certificate):
            return False
        return True

    def request(self, path, method=RequestType.GET, data=None, skip_verify=False, sign_data=None, files=None, cipher_data=False):
        headers = {}
        if files:
            headers.update({'Content-Type': 'multipart/form-data;boundary=boundary'})
        else:
            headers.update({'Content-Type': 'application/json'})
        headers.update({'Accept': 'application/json'})
        headers.update({'User-Agent': 'wechatpay v3 python sdk(https://github.com/minibear2021/wechatpayv3)'})
        if cipher_data:
            headers.update({'Wechatpay-Serial': hex(self._last_certificate().serial_number)[2:].upper()})
        authorization = build_authorization(
            path,
            'GET' if method == RequestType.GET else 'POST' if method == RequestType.POST else 'PATCH',
            self._mchid,
            self._cert_serial_no,
            self._private_key,
            data=sign_data if sign_data else data)
        headers.update({'Authorization': authorization})
        if method == RequestType.GET:
            response = requests.get(url=self._gate_way + path, headers=headers)
        elif method == RequestType.POST:
            response = requests.post(url=self._gate_way + path, json=data if not files else None, data=data if files else None, headers=headers, files=files)
        else:
            response = requests.patch(url=self._gate_way + path, json=data, headers=headers)
        if response.status_code in range(200, 300) and not skip_verify:
            if not self._verify_signature(response.headers, response.text):
                raise Exception('failed to verify the signature')
        return response.status_code, response.text

    def sign(self, sign_str):
        return rsa_sign(self._private_key, sign_str)

    def decrypt_callback(self, headers, body):
        if not self._verify_signature(headers, body):
            return None
        data = json.loads(body)
        resource_type = data.get('resource_type')
        if resource_type != 'encrypt-resource':
            return None
        resource = data.get('resource')
        if not resource:
            return None
        algorithm = resource.get('algorithm')
        if algorithm != 'AEAD_AES_256_GCM':
            return None
        nonce = resource.get('nonce')
        ciphertext = resource.get('ciphertext')
        associated_data = resource.get('associated_data')
        if not (nonce and ciphertext):
            return None
        if not associated_data:
            associated_data = ''
        result = aes_decrypt(
            nonce=nonce,
            ciphertext=ciphertext,
            associated_data=associated_data,
            apiv3_key=self._apiv3_key)
        return result

    def _load_local_certificates(self):
        if not (self._cert_dir and os.path.exists(self._cert_dir)):
            return
        for file_name in os.listdir(self._cert_dir):
            if not file_name.lower().endswith('.pem'):
                continue
            f = open(self._cert_dir + file_name, encoding="utf-8")
            certificate = load_certificate(f.read())
            f.close()
            now = datetime.utcnow()
            if certificate and now >= certificate.not_valid_before and now <= certificate.not_valid_after:
                self._certificates.append(certificate)

    def decrypt(self, ciphtext):
        return rsa_decrypt(ciphertext=ciphtext, private_key=self._private_key)

    def encrypt(self, text):
        return rsa_encrypt(text=text, certificate=self._last_certificate())
    
    def _last_certificate(self):
        if not self._certificates:
            self._update_certificates()
        certificate = self._certificates[0]
        for cert in self._certificates:
            if certificate.not_valid_after < cert.not_valid_after:
                certificate = cert
        return certificate