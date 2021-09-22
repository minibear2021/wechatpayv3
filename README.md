# 微信支付 API v3 Python SDK

[![PyPI version](https://badge.fury.io/py/wechatpayv3.svg)](https://badge.fury.io/py/wechatpayv3)
[![Download count](https://img.shields.io/pypi/dw/wechatpayv3)](https://img.shields.io/pypi/dw/wechatpayv3)

## 介绍

微信支付接口V3版python库。

欢迎微信支付开发者扫码进QQ群(群号：973102221)讨论：

![image](qq.png)

## 适用对象

**wechatpayv3**支持微信支付直连商户，接口说明详见 [官网](https://pay.weixin.qq.com/wiki/doc/apiv3/index.shtml)。

## 特性

1. 平台证书自动更新，无需开发者关注平台证书有效性，无需手动下载更新；
2. 支持本地缓存平台证书，初始化时指定平台证书保存目录即可；
3. 敏感信息直接传入明文参数，SDK内部自动加密，无需手动处理；
4. 回调通知自动验证回调消息，自动解密resource对象，并返回解密后的数据。

## 源码

[github](https://github.com/minibear2021/wechatpayv3)

[gitee](https://gitee.com/minibear2021/wechatpayv3)

## 安装

```
$ pip install wechatpayv3
```

## 使用方法

### 准备

参考微信官方文档准备好密钥, 证书文件和配置([证书/密钥/签名介绍](https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_0.shtml))

+ **商户 API 证书私钥：PRIVATE_KEY**。商户申请商户 API 证书时，会生成商户私钥，并保存在本地证书文件夹的文件 apiclient_key.pem 中。
> :warning: 不要把私钥文件暴露在公共场合，如上传到 Github，写在客户端代码等。
+ **商户API证书序列号：CERT_SERIAL_NO**。每个证书都有一个由 CA 颁发的唯一编号，即证书序列号。扩展阅读 [如何查看证书序列号](https://wechatpay-api.gitbook.io/wechatpay-api-v3/chang-jian-wen-ti/zheng-shu-xiang-guan#ru-he-cha-kan-zheng-shu-xu-lie-hao) 。
+ **微信支付 APIv3 密钥：APIV3_KEY**，是在回调通知和微信支付平台证书下载接口中，为加强数据安全，对关键信息 `AES-256-GCM` 加密时使用的对称加密密钥。

### 一个最小的后端

[examples.py](examples.py) 演示了一个带有支付接口和支付通知接口的后端。
首先，修改 **examplys.py** 里以下几项配置参数：

``` python
# 微信支付商户号
MCHID = '1230000109'

# 商户证书私钥
with open('path_to_key/apiclient_key.pem') as f:
    PRIVATE_KEY = f.read()

# 商户证书序列号
CERT_SERIAL_NO = '444F4864EA9B34415...'

# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
APIV3_KEY = 'MIIEvwIBADANBgkqhkiG9w0BAQE...'

# APPID
APPID = 'wxd678efh567hg6787'

# 回调地址，也可以在调用接口的时候覆盖
NOTIFY_URL = 'https://www.xxxx.com/notify'

# 微信支付平台证书缓存目录
CERT_DIR = './cert'

# 日志记录器，记录web请求和回调细节，便于调试排错
logging.basicConfig(filename=os.path.join(os.getcwd(), 'demo.log'), level=logging.DEBUG, filemode='a', format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger("demo")

```

检查一下参数无误，现在就可以用python解释器来运行：

```shell
$ python examples.py
 * Serving Flask app "examples" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

现在访问 http://127.0.0.1:5000/pay ，如果一切正常，你会看到下面一串json字符串：
```python
{"code":-1,"result":{"reason":"PARAM_ERROR"}}
```

因为我们还没有将实际业务系统的参数更新到/pay接口中，将代码中的参数更新为实际的业务参数后就可以获得类似下面的json字符串：
```python
{"code": 0, "result": {"appId": "wx2421b1c4370ec43b", "timeStamp": "1395712654", "nonceStr": "e61463f8efa94090b1f366cccfbbb444", "package": "prepay_id=up_wx21201855730335ac86f8c43d1889123400", "signType": "RSA", 'paySign': "oR9d8PuhnIc...KNqZLhLw4jq\/xDg=="}
```

到这一步统一下单的后端就完成了，前端只需要将上面的参数传到对应的调起支付接口中即可引导用户完成支付。

## 回调验证失败处理
开发者遇到的难点之一就是回调验证失败的问题，由于众多的python web框架对回调消息的处理不完全一致，如果出现回调验证失败，请务必确认传入的headers和body的值和类型。
通常框架传过来的headers类型是dict，而body类型是bytes。使用以下方法可直接获取到解密后的实际内容。

### flask框架

直接传入request.headers和request.data即可。
```python
result = wxpay.decrypt_callback(headers=request.headers, body=request.data)
```

### django框架

由于django框架特殊性，会将headers做一定的预处理，可以参考以下方式调用。
```python
headers = {}
headers.update({'Wechatpay-Signature': request.META.get('HTTP_WECHATPAY_SIGNATURE')})
headers.update({'Wechatpay-Timestamp': request.META.get('HTTP_WECHATPAY_TIMESTAMP')})
headers.update({'Wechatpay-Nonce': request.META.get('HTTP_WECHATPAY_NONCE')})
headers.update({'Wechatpay-Serial': request.META.get('HTTP_WECHATPAY_SERIAL')})
result = wxpay.decrypt_callback(headers=headers, body=request.body)
```

### tornado框架

直接传入request.headers和request.body即可。
```python
result = wxpay.decrypt_callback(headers=request.headers, body=request.body)
```

### 其他框架

参考以上处理方法，大原则就是保证传给decrypt_callback的参数值和收到的值一致，不要转换为dict，也不要转换为string。

## 接口清单

已适配的微信支付V3版API接口列表如下：

| 大类 | 小类 | 接口 | 接口函数 |
| --- | --- | --- | --- |
| 公用 | 公用 | 调起支付签名 | sign |
| 公用 | 公用 | 回调通知解密 | decrypt_callback |
| 公用 | 公用 | 敏感信息参数解密 | decrypt |
| 公用 | 公用 | *下载账单 | download_bill |
| 基础支付 | JSAPI、APP、H5、Native、小程序支付 | 统一下单 | pay |
| 基础支付 | JSAPI、APP、H5、Native、小程序支付 | 查询订单 | query |
| 基础支付 | JSAPI、APP、H5、Native、小程序支付 | 关闭订单 | close |
| 基础支付 | 合单支付 | 统一下单 | combine_pay |
| 基础支付 | 合单支付 | 查询订单 | combine_query |
| 基础支付 | 合单支付 | 关闭订单 | combine_close |
| 基础支付 | JSAPI、APP、H5、Native、小程序、合单支付 | 申请退款 | refund |
| 基础支付 | JSAPI、APP、H5、Native、小程序、合单支付 | 查询单笔退款 | refund_query |
| 基础支付 | JSAPI、APP、H5、Native、小程序、合单支付 | 申请交易账单 | trade_bill |
| 基础支付 | JSAPI、APP、H5、Native、小程序、合单支付 | 申请资金账单 | fundflow_bill |
| 经营能力 | 微信支付分（免确认模式） | 创单结单合并 | payscore_direct_complete |
| 经营能力 | 微信支付分（免确认预授权模式） | 商户预授权 | payscore_permission |
| 经营能力 | 微信支付分（免确认预授权模式） | 查询用户授权记录 | payscore_permission_query |
| 经营能力 | 微信支付分（免确认预授权模式） | 解除用户授权关系 | payscore_permission_terminate |
| 经营能力 | 微信支付分（公共API） | 创建支付分订单 | payscore_create |
| 经营能力 | 微信支付分（公共API） | 查询支付分订单 | payscore_query |
| 经营能力 | 微信支付分（公共API） | 取消支付分订单 | payscore_cancel |
| 经营能力 | 微信支付分（公共API） | 修改订单金额 | payscore_modify |
| 经营能力 | 微信支付分（公共API） | 完结支付分订单 | payscore_complete |
| 经营能力 | 微信支付分（公共API） | 商户发起催收扣款 | payscore_pay |
| 经营能力 | 微信支付分（公共API） | 同步服务订单信息 | payscore_sync |
| 经营能力 | 微信支付分（公共API） | 申请退款 | payscore_refund |
| 经营能力 | 微信支付分（公共API） | 查询单笔退款 | payscore_refund_query |
| 经营能力 | 支付即服务 | 服务人员注册 | guides_register |
| 经营能力 | 支付即服务 | 服务人员分配 | guides_assign |
| 经营能力 | 支付即服务 | 服务人员查询 | guides_query |
| 经营能力 | 支付即服务 | 服务人员信息更新 | guides_update |
| 行业方案 | 智慧商圈 | 商圈积分同步 | points_notify |
| 行业方案 | 智慧商圈 | 商圈积分授权查询 | user_authorization |
| 行业方案 | 微信支付分停车服务 | 查询车牌服务开通信息 | parking_service_find |
| 行业方案 | 微信支付分停车服务 | 创建停车入场 | parking_enter |
| 行业方案 | 微信支付分停车服务 | 扣费受理 | parking_order |
| 行业方案 | 微信支付分停车服务 | 查询订单 | parking_query |
| 营销工具 | 委托营销 | 建立合作关系 | marketing_partnership_build |
| 营销工具 | 委托营销 | 查询合作关系列表 | marketing_partnership_query |
| 营销工具 | 消费卡 | 发放消费卡 | marketing_card_send |
| 营销工具 | 支付有礼 | 创建全场满额送活动 | marketing_paygift_activity_create |
| 营销工具 | 支付有礼 | 查询活动详情接口 | marketing_paygift_activity_detail |
| 营销工具 | 支付有礼 | 查询活动发券商户号 | marketing_paygift_merchants_list |
| 营销工具 | 支付有礼 | 查询活动指定商品列表 | marketing_paygift_goods_list |
| 营销工具 | 支付有礼 | 终止活动 | marketing_paygift_activity_terminate |
| 营销工具 | 支付有礼 | 新增活动发券商户号 | marketing_paygift_merchant_add |
| 营销工具 | 支付有礼 | 获取支付有礼活动列表 | marketing_paygift_activity_list |
| 营销工具 | 支付有礼 | 删除活动发券商户号 | marketing_paygift_merchant_delete |
| 营销工具 | 图片上传 | 图片上传(营销专用) | marketing_image_upload |
| 资金应用 | 分账 | 请求分账 | profitsharing_order |
| 资金应用 | 分账 | 查询分账结果 | profitsharing_order_query |
| 资金应用 | 分账 | 请求分账回退 | profitsharing_return |
| 资金应用 | 分账 | 查询分账回退结果 | profitsharing_return_query |
| 资金应用 | 分账 | 解冻剩余资金 | profitsharing_unfreeze |
| 资金应用 | 分账 | 查询剩余待分金额 | profitsharing_amount_query |
| 资金应用 | 分账 | 添加分账接收方 | profitsharing_add_receiver |
| 资金应用 | 分账 | 删除分账接收方 | profitsharing_delete_receiver |
| 资金应用 | 分账 | 申请分账账单 | profitsharing_bill |
| 风险合规 | 消费者投诉2.0 | 查询投诉单列表 | complant_list_query |
| 风险合规 | 消费者投诉2.0 | 查询投诉单详情 | complant_detail_query |
| 风险合规 | 消费者投诉2.0 | 查询投诉协商历史 | complant_history_query |
| 风险合规 | 消费者投诉2.0 | 提交回复 | complant_response |
| 风险合规 | 消费者投诉2.0 | 反馈处理完成 | complant_complete |
| 风险合规 | 消费者投诉2.0 | 商户上传反馈图片 | complant_image_upload |
| 风险合规 | 消费者投诉2.0 | *图片下载 | complant_image_download |
| 其他能力 | 图片上传 | 图片上传 | image_upload |
| 其他能力 | 视频上传 | 视频上传 | video_upload |

### 接口函数参数

参数类型对照参考下表：

| 微信支付官方文档声明 | **wechatpayv3** SDK |
| --- | --- |
| string | str |
| int | int |
| object | dict: {} |
| array  | list: [] |
| boolean | bool: True, False |
| message | bytes |

### 接口函数返回值

每个接口均同步返回code和message，code为web请求得到的HTTP状态码，message为服务器返回的json字符串。
**特别要注意：
账单下载和图片下载两个接口的message为bytes类型，直接将message写入磁盘即可获得对应的目标文件。**


## 签名、验签、加密、解密的内部实现

一般应用开发者可以不用向下看了，有心了解这几项内部实现的可以参考一下。如果计划抽出来单独使用的，需要引入[cryptography](https://pypi.org/project/cryptography/)包。

### 构造签名信息

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


### 验证签名

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


### 回调信息解密

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


### 敏感信息加密

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


### 敏感信息解密

对应v3版微信支付api文档的[敏感信息加解密](https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay4_3.shtml)的解密部分。

```python
def rsa_decrypt(ciphertext, private_key):
    data = private_key.decrypt(ciphertext=b64decode(ciphertext), padding=OAEP(mgf=MGF1(algorithm=SHA1()), algorithm=SHA1()))
    result = data.decode('UTF-8')
    return result
```
