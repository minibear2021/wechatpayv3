# -*- coding: utf-8 -*-

import json
import time
import uuid
from base64 import b64decode, b64encode

from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP, PKCS1v15
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA1, SHA256, SM3, Hash
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.x509 import load_pem_x509_certificate
from cryptography import __version__ as cryptography_version


def build_authorization(path,
                        method,
                        mchid,
                        serial_no,
                        private_key,
                        data=None,
                        nonce_str=None):
    timeStamp = str(int(time.time()))
    nonce_str = nonce_str or ''.join(str(uuid.uuid4()).split('-')).upper()
    body = data if isinstance(data, str) else json.dumps(data) if data else ''
    sign_str = '%s\n%s\n%s\n%s\n%s\n' % (method, path, timeStamp, nonce_str, body)
    signature = rsa_sign(private_key=private_key, sign_str=sign_str)
    authorization = 'WECHATPAY2-SHA256-RSA2048 mchid="%s",nonce_str="%s",signature="%s",timestamp="%s",serial_no="%s"' % (mchid, nonce_str, signature, timeStamp, serial_no)
    return authorization


def rsa_sign(private_key, sign_str):
    message = sign_str.encode('UTF-8')
    signature = private_key.sign(data=message, padding=PKCS1v15(), algorithm=SHA256())
    sign = b64encode(signature).decode('UTF-8').replace('\n', '')
    return sign


def aes_decrypt(nonce, ciphertext, associated_data, apiv3_key):
    key_bytes = apiv3_key.encode('UTF-8')
    nonce_bytes = nonce.encode('UTF-8')
    associated_data_bytes = associated_data.encode('UTF-8')
    data = b64decode(ciphertext)
    aesgcm = AESGCM(key=key_bytes)
    try:
        result = aesgcm.decrypt(nonce=nonce_bytes, data=data, associated_data=associated_data_bytes).decode('UTF-8')
    except InvalidTag:
        result = None
    return result


def format_private_key(private_key_str):
    pem_start = '-----BEGIN PRIVATE KEY-----\n'
    pem_end = '\n-----END PRIVATE KEY-----'
    if not private_key_str.startswith(pem_start):
        private_key_str = pem_start + private_key_str
    if not private_key_str.endswith(pem_end):
        private_key_str = private_key_str + pem_end
    return private_key_str


def format_public_key(public_key_str):
    pem_start = '-----BEGIN PUBLIC KEY-----\n'
    pem_end = '\n-----END PUBLIC KEY-----'
    if not public_key_str.startswith(pem_start):
        public_key_str = pem_start + public_key_str
    if not public_key_str.endswith(pem_end):
        public_key_str = public_key_str + pem_end
    return public_key_str


def load_certificate(certificate_str):
    try:
        return load_pem_x509_certificate(data=certificate_str.encode('UTF-8'), backend=default_backend())
    except:
        return None


def load_private_key(private_key_str):
    try:
        return load_pem_private_key(data=format_private_key(private_key_str).encode('UTF-8'), password=None, backend=default_backend())
    except:
        raise Exception('failed to load private key.')


def load_public_key(public_key_str):
    try:
        return load_pem_public_key(data=format_public_key(public_key_str).encode('UTF-8'), backend=default_backend())
    except:
        raise Exception('failed to load public key.')


def rsa_verify(timestamp, nonce, body, signature, public_key):
    sign_str = '%s\n%s\n%s\n' % (timestamp, nonce, body)
    message = sign_str.encode('UTF-8')
    try:
        signature = b64decode(signature)
    except:
        return False
    try:
        public_key.verify(signature, message, PKCS1v15(), SHA256())
    except InvalidSignature:
        return False
    return True


def rsa_encrypt(text, public_key):
    data = text.encode('UTF-8')
    cipherbyte = public_key.encrypt(
        plaintext=data,
        padding=OAEP(mgf=MGF1(algorithm=SHA1()), algorithm=SHA1(), label=None)
    )
    return b64encode(cipherbyte).decode('UTF-8')


def rsa_decrypt(ciphertext, private_key):
    data = private_key.decrypt(
        ciphertext=b64decode(ciphertext),
        padding=OAEP(mgf=MGF1(algorithm=SHA1()), algorithm=SHA1(), label=None)
    )
    result = data.decode('UTF-8')
    return result


def hmac_sign(key, sign_str):
    hmac = HMAC(key.encode('UTF-8'), SHA256())
    hmac.update(sign_str.encode('UTF-8'))
    sign = hmac.finalize().hex().upper()
    return sign


def sha256(data):
    hash = Hash(SHA256())
    hash.update(data)
    return hash.finalize().hex()


def sm3(data):
    hash = Hash(SM3())
    hash.update(data)
    return hash.finalize().hex()
