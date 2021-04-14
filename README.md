# wechatpay-api-v3
[![PyPI version](https://badge.fury.io/py/wechatpay-api-v3.svg)](https://badge.fury.io/py/wechatpay-api-v3)

## 介绍

**wechatpay-api-v3** 
微信支付接口V3版python库.

## 安装

```
$ pip install wechatpay-api-v3
```

## 使用方法
### 准备
参考微信官方文档准备好密钥, 证书文件和配置([证书/密钥/签名介绍](https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_0.shtml))

### 初始化
``` python
from wechatpay-api-v3 import WeChatPay, WeChatPayType

MCHID = '1230000109'

MCH_PRIVATE_KEY = 'MIIEvwIBADANBgkqhkiG9w0BAQE...'
MCH_KEY_SERIAL_NO = '444F4864EA9B34415...'
WECHAT_PUBLIC_KEY = 'MIIEvwIBADANBgkqhkiG9w0BAQE...'
APPID = 'wxd678efh567hg6787'
NOTIFY_URL = 'https://www.weixin.qq.com/wxpay/pay.php'

wxpay = WeChatPay(wechatpay_type=WeChatPayType.MINIPROG,
                  mchid=MCHID,
                  mch_parivate_key=MCH_PRIVATE_KEY,
                  mch_key_serial_no=MCH_KEY_SERIAL_NO,
                  wechat_public_key=WECHAT_PUBLIC_KEY,
                  appid=APPID,
                  notify_url=NOTIFY_URL)
```

### 接口
参考examples.py


