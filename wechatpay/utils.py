# -*- coding: utf-8 -*-

import base64
import time
import uuid

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA256


def build_authorization(path,
                        method,
                        mchid,
                        serial_no,
                        mch_private_key,
                        body=None,
                        nonce_str=None):
    timeStamp = str(int(time.time()))
    nonce_str = nonce_str or ''.join(str(uuid.uuid4()).split('-')).upper()
    body = body if body else ''
    sign_str = method + '\n' + path + '\n' + \
        timeStamp + '\n' + nonce_str + '\n' + body + '\n'
    authorization = 'WECHATPAY2-SHA256-RSA2048 mchid="%s",serial_no="%s",nonce_str="%s",timestamp="%s",signature="%s"' % (
        mchid, serial_no, nonce_str, timeStamp, sign(mch_private_key=mch_private_key, sign_str=sign_str))
    return authorization


def sign(mch_private_key, sign_str):
    private_key = serialization.load_pem_private_key(data=format_private_key(
        mch_private_key).encode('UTF-8'), password=None, backend=default_backend())
    message = sign_str.encode('UTF-8')
    signature = private_key.sign(message, PKCS1v15(), SHA256())
    sign = base64.b64encode(signature).decode('UTF-8').replace('\n', '')
    return sign


def decrypt(nonce, ciphertext, associated_data, apiv3_key):
    key_bytes = apiv3_key.encode('UTF-8')
    nonce_bytes = nonce.encode('UTF-8')
    associated_data_bytes = associated_data.encode('UTF-8')
    data = base64.b64decode(ciphertext)
    aesgcm = AESGCM(key_bytes)
    return aesgcm.decrypt(nonce_bytes, data, associated_data_bytes).decode('UTF-8')


def format_private_key(private_key):
    pem_start = '-----BEGIN PRIVATE KEY-----\n'
    pem_end = '\n-----END PRIVATE KEY-----'
    if not private_key.startswith(pem_start):
        private_key = pem_start + private_key
    if not private_key.endswith(pem_end):
        private_key = private_key + pem_end
    return private_key


def format_public_key(public_key):
    pem_start = '-----BEGIN CERTIFICATE-----\n'
    pem_end = '\n-----END CERTIFICATE-----'
    if not public_key.startswith(pem_start):
        public_key = pem_start + public_key
    if not public_key.endswith(pem_end):
        public_key = public_key + pem_end
    return public_key
