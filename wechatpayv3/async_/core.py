# -*- coding: utf-8 -*-

import json
from datetime import datetime, timezone

import httpx
import aiofiles
try:
    from aiofiles import os as aiofiles_os
except ImportError:
    import aiofiles.os as aiofiles_os

from .type import RequestType, SignType
from .utils import (aes_decrypt, build_authorization, hmac_sign, load_public_key,
                    load_certificate, load_private_key, rsa_decrypt,
                    rsa_encrypt, rsa_sign, rsa_verify, cryptography_version)


class AsyncCore:
    def __init__(self, mchid, cert_serial_no, private_key, apiv3_key, cert_dir=None, logger=None, proxy=None, timeout=None, public_key=None, public_key_id=None):
        self._proxy = proxy
        self._mchid = mchid
        self._cert_serial_no = cert_serial_no
        self._private_key = load_private_key(private_key)
        self._apiv3_key = apiv3_key
        self._gate_way = 'https://api.mch.weixin.qq.com'
        self._certificates = []
        self._cert_dir = cert_dir + '/' if cert_dir else None
        self._logger = logger
        self._timeout = timeout
        self._public_key = load_public_key(public_key)
        self._public_key_id = public_key_id
        if (public_key is None) != (public_key_id is None):
            raise Exception('public_key_id or public_key is not assigned.')
        self._client = None
        if not self._public_key:
            # Will be initialized in async context
            pass

    async def __aenter__(self):
        """Async context manager entry"""
        self._client = httpx.AsyncClient(
            proxy=self._proxy,
            timeout=httpx.Timeout(
                timeout=self._timeout[1] if isinstance(self._timeout, tuple) else self._timeout,
                connect=self._timeout[0] if isinstance(self._timeout, tuple) else 10.0
            ) if self._timeout else httpx.Timeout(30.0)
        )
        if not self._public_key:
            await self._init_certificates()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self._client:
            await self._client.aclose()
        return False

    async def _update_certificates(self):
        path = '/v3/certificates'
        self._certificates.clear()
        code, message = await self.request(path, skip_verify=True)
        if code != 200:
            return
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
            if (int(cryptography_version.split(".")[0]) < 42):
                now = datetime.utcnow()
                if now < certificate.not_valid_before or now > certificate.not_valid_after:
                    continue
            else:
                now = datetime.now(timezone.utc)
                if now < certificate.not_valid_before_utc or now > certificate.not_valid_after_utc:
                    continue
            self._certificates.append(certificate)
            if not self._cert_dir:
                continue
            if not await aiofiles_os.path.exists(self._cert_dir):
                await aiofiles_os.makedirs(self._cert_dir)
            if not await aiofiles_os.path.exists(self._cert_dir + serial_no + '.pem'):
                async with aiofiles.open(self._cert_dir + serial_no + '.pem', 'w') as f:
                    await f.write(cert_str)

    def _verify_signature(self, headers, body):
        signature_mark = 'Wechatpay-Signature'
        timestamp_mark = 'Wechatpay-Timestamp'
        nonce_mark = 'Wechatpay-Nonce'
        serial_mark = 'Wechatpay-Serial'
        signature_type_mark = 'Wechatpay-Signature-Type'        
        if headers.get('HTTP_WECHATPAY_SIGNATURE'): # 兼容django
            signature_mark = 'HTTP_WECHATPAY_SIGNATURE'
            timestamp_mark = 'HTTP_WECHATPAY_TIMESTAMP'
            nonce_mark = 'HTTP_WECHATPAY_NONCE'
            serial_mark = 'HTTP_WECHATPAY_SERIAL'
            signature_type_mark = 'HTTP_WECHATPAY_SIGNATURE_TYPE'
        if headers.get('wechatpay-signature'): # 兼容fastapi
            signature_mark = 'wechatpay-signature'
            timestamp_mark = 'wechatpay-timestamp'
            nonce_mark = 'wechatpay-nonce'
            serial_mark = 'wechatpay-serial'
            signature_type_mark = 'wechatpay-signature-type'            
        signature = headers.get(signature_mark, '')
        timestamp = headers.get(timestamp_mark, '')
        nonce = headers.get(nonce_mark, '')
        serial_no = headers.get(serial_mark, '')
        signature_type = headers.get(signature_type_mark, '')
        if signature_type != 'WECHATPAY2-SHA256-RSA2048':
            raise Exception(f'wechatpayv3 does not support this algorithm: {signature_type}')
        if serial_no == self._public_key_id:
            public_key = self._public_key
        else:
            cert_found = False
            for cert in self._certificates:
                if int('0x' + serial_no, 16) == cert.serial_number:
                    cert_found = True
                    certificate = cert
                    break
            if not cert_found:
                # In sync context, we can't update certificates
                # Certificates should be loaded via async context
                return False
            public_key = certificate.public_key()
        if not rsa_verify(timestamp, nonce, body, signature, public_key):
            return False
        return True

    async def _verify_signature_async(self, headers, body):
        """Async version of signature verification for use in async contexts"""
        signature_mark = 'Wechatpay-Signature'
        timestamp_mark = 'Wechatpay-Timestamp'
        nonce_mark = 'Wechatpay-Nonce'
        serial_mark = 'Wechatpay-Serial'
        signature_type_mark = 'Wechatpay-Signature-Type'        
        if headers.get('HTTP_WECHATPAY_SIGNATURE'): # 兼容django
            signature_mark = 'HTTP_WECHATPAY_SIGNATURE'
            timestamp_mark = 'HTTP_WECHATPAY_TIMESTAMP'
            nonce_mark = 'HTTP_WECHATPAY_NONCE'
            serial_mark = 'HTTP_WECHATPAY_SERIAL'
            signature_type_mark = 'HTTP_WECHATPAY_SIGNATURE_TYPE'
        if headers.get('wechatpay-signature'): # 兼容fastapi
            signature_mark = 'wechatpay-signature'
            timestamp_mark = 'wechatpay-timestamp'
            nonce_mark = 'wechatpay-nonce'
            serial_mark = 'wechatpay-serial'
            signature_type_mark = 'wechatpay-signature-type'            
        signature = headers.get(signature_mark, '')
        timestamp = headers.get(timestamp_mark, '')
        nonce = headers.get(nonce_mark, '')
        serial_no = headers.get(serial_mark, '')
        signature_type = headers.get(signature_type_mark, '')
        if signature_type != 'WECHATPAY2-SHA256-RSA2048':
            raise Exception(f'wechatpayv3 does not support this algorithm: {signature_type}')
        if serial_no == self._public_key_id:
            public_key = self._public_key
        else:
            cert_found = False
            for cert in self._certificates:
                if int('0x' + serial_no, 16) == cert.serial_number:
                    cert_found = True
                    certificate = cert
                    break
            if not cert_found:
                await self._update_certificates()
                for cert in self._certificates:
                    if int('0x' + serial_no, 16) == cert.serial_number:
                        cert_found = True
                        certificate = cert
                        break
                if not cert_found:
                    return False
            public_key = certificate.public_key()
        if not rsa_verify(timestamp, nonce, body, signature, public_key):
            return False
        return True

    async def request(self, path, method=RequestType.GET, data=None, skip_verify=False, sign_data=None, files=None, cipher_data=False, headers={}):
        if files:
            headers.update({'Content-Type': 'multipart/form-data'})
        else:
            headers.update({'Content-Type': 'application/json'})
        headers.update({'Accept': 'application/json'})
        headers.update({'User-Agent': 'wechatpay python sdk v1.3.11(https://github.com/minibear2021/wechatpayv3)'})
        if self._public_key_id or cipher_data:
            wechatpay_serial = self._public_key_id if self._public_key_id else hex(self._last_certificate().serial_number)[2:].upper()            
            headers.update({'Wechatpay-Serial': wechatpay_serial})
        authorization = build_authorization(
            path,
            method.value,
            self._mchid,
            self._cert_serial_no,
            self._private_key,
            data=sign_data if sign_data else data)
        headers.update({'Authorization': authorization})
        if self._logger:
            self._logger.debug('Request url: %s' % self._gate_way + path)
            self._logger.debug('Request type: %s' % method.value)
            self._logger.debug('Request headers: %s' % headers)
            self._logger.debug('Request params: %s' % data)
        if method == RequestType.GET:
            response = await self._client.get(url=self._gate_way + path, headers=headers)
        elif method == RequestType.POST:
            if files:
                response = await self._client.post(url=self._gate_way + path, data=data, headers=headers, files=files)
            else:
                response = await self._client.post(url=self._gate_way + path, json=data, headers=headers)
        elif method == RequestType.PATCH:
            response = await self._client.patch(url=self._gate_way + path, json=data, headers=headers)
        elif method == RequestType.PUT:
            response = await self._client.put(url=self._gate_way + path, json=data, headers=headers)
        elif method == RequestType.DELETE:
            response = await self._client.delete(url=self._gate_way + path, headers=headers)
        else:
            raise Exception('wechatpayv3 does no support this request type.')
        if self._logger:
            self._logger.debug('Response status code: %s' % response.status_code)
            self._logger.debug('Response headers: %s' % response.headers)
            self._logger.debug('Response content: %s' % response.text)
        if response.status_code in range(200, 300) and not skip_verify:
            if not await self._verify_signature_async(response.headers, response.text):
                raise Exception('failed to verify the signature')
        return response.status_code, response.text if 'application/json' in response.headers.get('Content-Type', '') else response.content

    def sign(self, data, sign_type=SignType.RSA_SHA256):
        if sign_type == SignType.RSA_SHA256:
            sign_str = '\n'.join(data) + '\n'
            return rsa_sign(self._private_key, sign_str)
        elif sign_type == SignType.HMAC_SHA256:
            key_list = sorted(data.keys())
            sign_str = ''
            for k in key_list:
                v = data[k]
                sign_str += str(k) + '=' + str(v) + '&'
            sign_str += 'key=' + self._apiv3_key
            return hmac_sign(self._apiv3_key, sign_str)
        else:
            raise ValueError('unexpected value of sign_type.')

    def decrypt_callback(self, headers, body):
        if isinstance(body, bytes):
            body = body.decode('UTF-8')
        if self._logger:
            self._logger.debug('Callback headers: %s' % headers)
            self._logger.debug('Callback body: %s' % body)
        if not self._verify_signature(headers, body):
            if self._logger:
                self._logger.debug('Failed to verify signature')
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
            raise Exception(f'wechatpayv3 does not support this algorithm: {algorithm}')
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
        if self._logger:
            self._logger.debug('Callback result: %s' % result)
            if not result:
                self._logger.debug('Please double check your apiv3 key')
        return result

    def callback(self, headers, body):
        if isinstance(body, bytes):
            body = body.decode('UTF-8')
        result = self.decrypt_callback(headers=headers, body=body)
        if result:
            data = json.loads(body)
            data.update({'resource': json.loads(result)})
            return data
        else:
            return result

    async def _init_certificates(self):
        if self._cert_dir and await aiofiles_os.path.exists(self._cert_dir):
            for file_name in await aiofiles_os.listdir(self._cert_dir):
                if not file_name.lower().endswith('.pem'):
                    continue
                async with aiofiles.open(self._cert_dir + file_name, encoding="utf-8") as f:
                    certificate = load_certificate(await f.read())
                if (int(cryptography_version.split(".")[0]) < 42):
                    now = datetime.utcnow()
                    if certificate and now >= certificate.not_valid_before and now <= certificate.not_valid_after:
                        self._certificates.append(certificate)
                else:
                    now = datetime.now(timezone.utc)
                    if certificate and now >= certificate.not_valid_before_utc and now <= certificate.not_valid_after_utc:
                        self._certificates.append(certificate)
        if not self._certificates:
            await self._update_certificates()
        if not self._certificates:
            raise Exception('No wechatpay platform certificate, please double check your init params.')

    def decrypt(self, ciphtext):
        return rsa_decrypt(ciphertext=ciphtext, private_key=self._private_key)

    def encrypt(self, text):
        if self._public_key_id:
            public_key = self._public_key
        else:
            public_key = self._last_certificate().public_key()
        return rsa_encrypt(text=text, public_key=public_key)

    def _last_certificate(self):
        if not self._certificates:
            raise Exception('No certificates available. Please ensure AsyncCore is used within async context.')
        certificate = self._certificates[0]
        for cert in self._certificates:
            if certificate.not_valid_after < cert.not_valid_after:
                certificate = cert
        return certificate
