# wechatpayv3
[![PyPI version](https://badge.fury.io/py/wechatpayv3.svg)](https://badge.fury.io/py/wechatpayv3)
[![Download count](https://img.shields.io/pypi/dw/wechatpayv3)](https://img.shields.io/pypi/dw/wechatpayv3)
## 介绍


微信支付接口V3版python库。

## 适用对象

**wechatpayv3**支持微信支付直连商户，接口说明详见 [官网](https://pay.weixin.qq.com/wiki/doc/apiv3/index.shtml)。

## 特性

1. 平台证书自动更新，无需开发者关注平台证书有效性，无需手动下载更新；
2. 支持本地缓存平台证书，初始化时指定平台证书保存目录即可。

## 适配进度

微信支付V3版API接口

其中：

#### 基础支付
    JSAPI支付 已适配
    APP支付 已适配
    H5支付 已适配
    Native支付 已适配
    小程序支付 已适配
    合单支付 已适配
    付款码支付 待官网更新
    刷脸支付 无需适配

#### 行业方案
    智慧商圈 已适配

## 源码

[github](https://github.com/minibear2021/wechatpayv3)

[gitee](https://gitee.com/minibear2021/wechatpayv3)

## 安装

```
$ pip install wechatpayv3
```

## 使用方法
### 参数类型
官网接口文档中指明的参数类型和**wechatpayv3**中接口需要传入的参数类型对应如下：
| 文档声明 | **wechatpayv3** |
| --- | --- |
| string | string |
| int | int |
| object | dict: {} |
| array  | list: [] |
| boolean | bool: True, False |
### 准备
参考微信官方文档准备好密钥, 证书文件和配置([证书/密钥/签名介绍](https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_0.shtml))

### 初始化
``` python
from wechatpayv3 import WeChatPay, WeChatPayType

# 微信支付商户号
MCHID = '1230000109'
# 商户证书私钥
PRIVATE_KEY = 'MIIEvwIBADANBgkqhkiG9w0BAQE...'
# 商户证书序列号
CERT_SERIAL_NO = '444F4864EA9B34415...'
# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
APIV3_KEY = 'MIIEvwIBADANBgkqhkiG9w0BAQE...'
# APPID
APPID = 'wxd678efh567hg6787'
# 回调地址，也可以在调用接口的时候覆盖
NOTIFY_URL = 'https://www.weixin.qq.com/wxpay/pay.php'

wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.MINIPROG,
    mchid=MCHID,
    parivate_key=PRIVATE_KEY,
    cert_serial_no=CERT_SERIAL_NO,
    apiv3_key=APIV3_KEY,
    appid=APPID,
    notify_url=NOTIFY_URL)
```

### 接口

``` python

# 统一下单
def pay():
    code, message = wxpay.pay(
        description='demo-description',
        out_trade_no='demo-trade-no',
        amount={'total': 100},
        payer={'openid': 'demo-openid'})
    print('code: %s, message: %s' % (code, message))

# 订单查询
def query():
    code, message = wxpay.query(transaction_id='demo-transation-id')
    print('code: %s, message: %s' % (code, message))

# 关闭订单
def close():
    code, message = wxpay.close(out_trade_no='demo-out-trade-no')
    print('code: %s, message: %s' % (code, message))

# 申请退款
def refund():
    code, message=wxpay.refund(
        out_refund_no='demo-out-refund-no',
        amount={'refund': 100, 'total': 100, 'currency': 'CNY'},
        transaction_id='1217752501201407033233368018')
    print('code: %s, message: %s' % (code, message))

# 退款查询
def query_refund():
    code, message = wxpay.query_refund(out_refund_no='demo-out-refund-no')
    print('code: %s, message: %s' % (code, message))

# 申请交易账单
def trade_bill():
    code, message = wxpay.trade_bill(bill_date='2021-04-01')
    print('code: %s, message: %s' % (code, message))

# 申请资金流水账单
def fundflow_bill():
    code, message = wxpay.fundflow_bill(bill_date='2021-04-01')
    print('code: %s, message: %s' % (code, message))

# 下载账单
def download_bill():
    code, message = wxpay.download_bill(url='https://api.mch.weixin.qq.com/v3/billdownload/file?token=demo-token')
    print('code: %s, message: %s' % (code, message))

# 合单支付下单
def combine_pay():
    code, message = wxpay.combine_pay(
        combine_out_trade_no='demo_out_trade_no',
        sub_orders=[{'mchid':'1900000109',
                     'attach':'深圳分店',
                     'amount':{'total_amount':100,'currency':'CNY'},
                     'out_trade_no':'20150806125346',
                     'description':'腾讯充值中心-QQ会员充值',
                     'settle_info':{'profit_sharing':False, 'subsidy_amount':10}}])
    print('code: %s, message: %s' % (code, message))

# 合单订单查询
def combine_query():
    code, message = wxpay.combine_query(combine_out_trade_no='demo_out_trade_no')
    print('code: %s, message: %s' % (code, message))

# 合单订单关闭
def combine_close():
    code, message = wxpay.combine_close(
        combine_out_trade_no='demo_out_trade_no', 
        sub_orders=[{'mchid': '1900000109', 'out_trade_no': '20150806125346'}])
    print('code: %s, message: %s' % (code, message))

# 计算签名供调起支付时拼凑参数使用
# 注意事项：注意参数顺序，某个参数为空时不能省略，以空字符串''占位
def sign():
    print(wxpay.sign(['wx888','1414561699','5K8264ILTKCH16CQ2502S....','prepay_id=wx201410272009395522657....']))

# 验证并解密回调消息，把回调接口收到的headers和body传入
def decrypt_callback(headers, body):
    print(wxpay.decrypt_callback(headers, body))

# 智慧商圈积分同步
def points_notify():
    code, message = wxpay.points_notify(
        transaction_id='4200000533202000000000000000',
        openid='otPAN5xxxxxxxxrOEG6lUv_pzacc',
        earn_points=True,
        increased_points=100,
        points_update_time='2020-05-20T13:29:35.120+08:00')
    print('code: %s, message: %s' % (code, message))

```

