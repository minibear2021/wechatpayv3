# -*- coding: utf-8 -*-

import json
import time
import uuid
from base64 import b64decode, b64encode

from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP, PKCS1v15
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA1, SHA256
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.x509 import load_pem_x509_certificate


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


def rsa_verify(timestamp, nonce, body, signature, certificate):
    sign_str = '%s\n%s\n%s\n' % (timestamp, nonce, body)
    public_key = certificate.public_key()
    message = sign_str.encode('UTF-8')
    signature = b64decode(signature)
    try:
        public_key.verify(signature, message, PKCS1v15(), SHA256())
    except InvalidSignature:
        return False
    return True


def rsa_encrypt(text, certificate):
    data = text.encode('UTF-8')
    public_key = certificate.public_key()
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


def rotation_left(x, num):
    num %= 32
    left = (x << num) % (2 ** 32)
    right = (x >> (32 - num)) % (2 ** 32)
    result = left ^ right
    return result


def Int2Bin(x, k):
    x = str(bin(x)[2:])
    result = "0" * (k - len(x)) + x
    return result


class SM3:
    # copy from:
    # https://blog.csdn.net/weixin_43936250/article/details/105543266
    def __init__(self):
        self.IV = [0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600, 0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E]
        self.T = [0x79cc4519, 0x7a879d8a]
        self.maxu32 = 2 ** 32
        self.w1 = [0] * 68
        self.w2 = [0] * 64

    def ff(self, x, y, z, j):
        result = 0
        if j < 16:
            result = x ^ y ^ z
        elif j >= 16:
            result = (x & y) | (x & z) | (y & z)
        return result

    def gg(self, x, y, z, j):
        result = 0
        if j < 16:
            result = x ^ y ^ z
        elif j >= 16:
            result = (x & y) | (~x & z)
        return result

    def p(self, x, mode):
        result = 0
        if mode == 0:
            result = x ^ rotation_left(x, 9) ^ rotation_left(x, 17)
        elif mode == 1:
            result = x ^ rotation_left(x, 15) ^ rotation_left(x, 23)
        return result

    def sm3_fill(self, msg):
        length = len(msg)
        l = length * 8

        num = length // 64
        remain_byte = length % 64
        msg_remain_bin = ""
        msg_new_bytes = bytearray((num + 1) * 64)

        for i in range(length):
            msg_new_bytes[i] = msg[i]

        remain_bit = remain_byte * 8
        for i in range(remain_byte):
            msg_remain_bin += "{:08b}".format(msg[num * 64 + i])

        k = (448 - l - 1) % 512
        while k < 0:
            k += 512

        msg_remain_bin += "1" + "0" * k + Int2Bin(l, 64)

        for i in range(0, 64 - remain_byte):
            str = msg_remain_bin[i * 8 + remain_bit: (i + 1) * 8 + remain_bit]
            temp = length + i
            msg_new_bytes[temp] = int(str, 2)
        return msg_new_bytes

    def sm3_msg_extend(self, msg):
        for i in range(0, 16):
            self.w1[i] = int.from_bytes(msg[i * 4:(i + 1) * 4], byteorder="big")

        for i in range(16, 68):
            self.w1[i] = self.p(self.w1[i-16] ^ self.w1[i-9] ^ rotation_left(self.w1[i-3], 15), 1) ^ rotation_left(self.w1[i-13], 7) ^ self.w1[i-6]

        for i in range(64):
            self.w2[i] = self.w1[i] ^ self.w1[i+4]

    def sm3_compress(self, msg):
        self.sm3_msg_extend(msg)
        ss1 = 0

        A = self.IV[0]
        B = self.IV[1]
        C = self.IV[2]
        D = self.IV[3]
        E = self.IV[4]
        F = self.IV[5]
        G = self.IV[6]
        H = self.IV[7]

        for j in range(64):
            if j < 16:
                ss1 = rotation_left((rotation_left(A, 12) + E + rotation_left(self.T[0], j)) % self.maxu32, 7)
            elif j >= 16:
                ss1 = rotation_left((rotation_left(A, 12) + E + rotation_left(self.T[1], j)) % self.maxu32, 7)
            ss2 = ss1 ^ rotation_left(A, 12)
            tt1 = (self.ff(A, B, C, j) + D + ss2 + self.w2[j]) % self.maxu32
            tt2 = (self.gg(E, F, G, j) + H + ss1 + self.w1[j]) % self.maxu32
            D = C
            C = rotation_left(B, 9)
            B = A
            A = tt1
            H = G
            G = rotation_left(F, 19)
            F = E
            E = self.p(tt2, 0)

        self.IV[0] ^= A
        self.IV[1] ^= B
        self.IV[2] ^= C
        self.IV[3] ^= D
        self.IV[4] ^= E
        self.IV[5] ^= F
        self.IV[6] ^= G
        self.IV[7] ^= H

    def sm3_update(self, msg):
        msg_new = self.sm3_fill(msg)
        n = len(msg_new) // 64

        for i in range(0, n):
            self.sm3_compress(msg_new[i * 64:(i + 1) * 64])

    def sm3_final(self):
        digest_str = ""
        for i in range(len(self.IV)):
            digest_str += hex(self.IV[i])[2:]

        return digest_str.upper()

    def hashFile(self, filename):
        with open(filename, 'rb') as fp:
            contents = fp.read()
            self.sm3_update(bytearray(contents))
        return self.sm3_final()
