# 签名、验签、加密、解密的内部实现

## 构造签名信息

对应v3版微信支付api文档的[签名生成](https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay4_0.shtml)部分。

```python
def build_authorization(path,
                        method,
                        mchid,
                        serial_no,
                        mch_private_key,
                        data=None,
                        nonce_str=None):
    timeStamp = str(int(time.time()))
    nonce_str = nonce_str or ''.join(str(uuid.uuid4()).split('-')).upper()
    body = json.dumps(data) if data else ''
    sign_str = '%s\n%s\n%s\n%s\n%s\n' % (method, path, timeStamp, nonce_str, body)
    signature = rsa_sign(private_key=mch_private_key, sign_str=sign_str)
    authorization = 'WECHATPAY2-SHA256-RSA2048 mchid="%s",nonce_str="%s",signature="%s",timestamp="%s",serial_no="%s"' % (mchid, nonce_str, signature, timeStamp, serial_no)
    return authorization
```


## 验证签名

对应v3版微信支付api文档的[签名验证](https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay4_1.shtml)部分。

```python
def rsa_verify(timestamp, nonce, body, signature, certificate):
    sign_str = '%s\n%s\n%s\n' % (timestamp, nonce, body)
    public_key = certificate.public_key()
    message = sign_str.encode('UTF-8')
    signature = b64decode(signature)
    try:
        public_key.verify(signature, sign_str.encode('UTF-8'), PKCS1v15(), SHA256())
    except InvalidSignature:
        return False
    return True
```


## 回调信息解密

对应v3版微信支付api文档的[证书和回调报文解密](https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay4_2.shtml)部分。

```python
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
```


## 敏感信息加密

对应v3版微信支付api文档的[敏感信息加解密](https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay4_3.shtml)的加密部分。

```python
def rsa_encrypt(text, certificate):
    data = text.encode('UTF-8')
    public_key = certificate.public_key()
    cipherbyte = public_key.encrypt(
        plaintext=data,
        padding=OAEP(mgf=MGF1(algorithm=SHA1()), algorithm=SHA1(), label=None)
    )
    return b64encode(cipherbyte).decode('UTF-8')
```


## 敏感信息解密

对应v3版微信支付api文档的[敏感信息加解密](https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay4_3.shtml)的解密部分。

```python
def rsa_decrypt(ciphertext, private_key):
    data = private_key.decrypt(ciphertext=b64decode(ciphertext), padding=OAEP(mgf=MGF1(algorithm=SHA1()), algorithm=SHA1()))
    result = data.decode('UTF-8')
    return result
```


## 注意事项

以上涉及到的几项签名如果计划抽出来单独使用，需要引入[cryptography](https://pypi.org/project/cryptography/)包。