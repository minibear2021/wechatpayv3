# -*- coding: utf-8 -*-

import time
import uuid
from base64 import b64decode, b64encode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA256
from OpenSSL import crypto


def build_authorization(path,
                        method,
                        mchid,
                        serial_no,
                        mch_private_key,
                        data=None,
                        nonce_str=None):
    timeStamp = str(int(time.time()))
    nonce_str = nonce_str or ''.join(str(uuid.uuid4()).split('-')).upper()
    body = data if data else ''
    sign_str = method + '\n' + path + '\n' + \
        timeStamp + '\n' + nonce_str + '\n' + body + '\n'
    signature = sign(private_key=mch_private_key, sign_str=sign_str)
    authorization = 'WECHATPAY2-SHA256-RSA2048 mchid="%s",nonce_str="%s",signature="%s",timestamp="%s",serial_no="%s"' % (
        mchid, nonce_str, signature, timeStamp, serial_no)
    return authorization


def sign(private_key, sign_str):
    private_key = serialization.load_pem_private_key(data=format_private_key(
        private_key).encode('UTF-8'), password=None, backend=default_backend())
    message = sign_str.encode('UTF-8')
    signature = private_key.sign(message, PKCS1v15(), SHA256())
    sign = b64encode(signature).decode('UTF-8').replace('\n', '')
    return sign


def decrypt(nonce, ciphertext, associated_data, apiv3_key):
    key_bytes = apiv3_key.encode('UTF-8')
    nonce_bytes = nonce.encode('UTF-8')
    associated_data_bytes = associated_data.encode('UTF-8')
    data = b64decode(ciphertext)
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


def format_certificate(certificate):
    pem_start = '-----BEGIN CERTIFICATE-----\n'
    pem_end = '\n-----END CERTIFICATE-----'
    if not certificate.startswith(pem_start):
        certificate = pem_start + certificate
    if not certificate.endswith(pem_end):
        certificate = certificate + pem_end
    return certificate


def verify_response(timestamp, nonce, body, signature, certificate):
    sign_str = '%s\n%s\n%s\n' % (timestamp, nonce, body)
    public_key = dump_public_key(certificate)
    message = sign_str.encode('UTF-8')
    return public_key.verify(b64decode(signature), sign_str.encode('UTF-8'), PKCS1v15, SHA256)


def certificate_serial_number(certificate):
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, format_certificate(certificate))
    try:
        res = cert.get_signature_algorithm().decode('UTF-8')
        if res != 'sha256WithRSAEncryption':
            return None
        return hex(cert.get_serial_number()).upper()[2:]
    except:
        return None

def dump_public_key(certificate):
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, format_certificate(certificate))
    public_key = crypto.dump_publickey(crypto.FILETYPE_PEM, cert.get_pubkey()).decode("utf-8")
    return public_key
