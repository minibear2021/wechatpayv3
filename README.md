# wechatpayv3
[![PyPI version](https://badge.fury.io/py/wechatpayv3.svg)](https://badge.fury.io/py/wechatpayv3)

## 介绍

**wechatpayv3** 
微信支付接口V3版python库.

## 安装

```
$ pip install wechatpayv3
```

## 使用方法
### 准备
参考微信官方文档准备好密钥, 证书文件和配置([证书/密钥/签名介绍](https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_0.shtml))

### 初始化
``` python
from wechatpayv3 import WeChatPay, WeChatPayType

MCHID = '1230000109'
MCH_PRIVATE_KEY = 'MIIEvwIBADANBgkqhkiG9w0BAQE...'
MCH_KEY_SERIAL_NO = '444F4864EA9B34415...'
WECHAT_PUBLIC_KEY = 'MIIEvwIBADANBgkqhkiG9w0BAQE...'
APPID = 'wxd678efh567hg6787'
NOTIFY_URL = 'https://www.weixin.qq.com/wxpay/pay.php'

wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.MINIPROG,
    mchid=MCHID,
    mch_parivate_key=MCH_PRIVATE_KEY,
    mch_key_serial_no=MCH_KEY_SERIAL_NO,
    wechat_public_key=WECHAT_PUBLIC_KEY,
    appid=APPID,
    notify_url=NOTIFY_URL)
```

### 接口

``` python
# 下载证书
def certificate():
    code, message = wxpay.certificate()
    print('code: %s, message: %s' % (code, message))

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
    code, message = wxpay.refund(
        transaction_id='demo-transation-id',
        out_refund_no='demo-out-refund-no',
        amount={'refund': 100, 'total': 100, 'currency': 'CNY'})
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
    code, message = wxpay.download_bill(
        url='https://api.mch.weixin.qq.com/v3/billdownload/file?token=demo-token')
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
```


