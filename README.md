# wechatpayv3

[![PyPI version](https://badge.fury.io/py/wechatpayv3.svg)](https://badge.fury.io/py/wechatpayv3)
[![Download count](https://img.shields.io/pypi/dw/wechatpayv3)](https://img.shields.io/pypi/dw/wechatpayv3)

## 介绍

微信支付接口V3版python库。

欢迎微信支付开发者扫码进QQ群讨论：

![image](qq.png)

## 适用对象

**wechatpayv3**支持微信支付直连商户，接口说明详见 [官网](https://pay.weixin.qq.com/wiki/doc/apiv3/index.shtml)。

## 特性

1. 平台证书自动更新，无需开发者关注平台证书有效性，无需手动下载更新；
2. 支持本地缓存平台证书，初始化时指定平台证书保存目录即可；
3. 敏感信息直接传入明文参数，SDK内部自动加密，无需手动处理。

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
    微信支付分停车服务 已适配

#### 营销工具

    图片上传(营销专用) 已适配

#### 经营能力

    支付即服务 已适配

#### 其他能力

    图片上传 已适配
    视频上传 已适配

#### 需要的接口还没有适配怎么办？

由于**wechatpayv3**包内核心的core.py已经封装了请求签名和消息验证过程，开发者无需关心web请求细节，直接根据官方文档参考以下基础支付的[申请退款](https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter3_1_9.shtml)接口代码自行适配，测试OK的话，欢迎提交代码。
必填的参数建议加上空值检查，可选的参数默认传入None。参数类型对照参考下表：

| 文档声明 | **wechatpayv3** |
| --- | --- |
| string | string |
| int | int |
| object | dict: {} |
| array  | list: [] |
| boolean | bool: True, False |

```python
def refund(self,
           out_refund_no,
           amount,
           transaction_id=None,
           out_trade_no=None,
           reason=None,
           funds_account=None,
           goods_detail=None,
           notify_url=None):
    """申请退款
    :param out_refund_no: 商户退款单号，示例值：'1217752501201407033233368018'
    :param amount: 金额信息，示例值：{'refund':888, 'total':888, 'currency':'CNY'}
    :param transaction_id: 微信支付订单号，示例值：'1217752501201407033233368018'
    :param out_trade_no: 商户订单号，示例值：'1217752501201407033233368018'
    :param reason: 退款原因，示例值：'商品已售完'
    :param funds_account: 退款资金来源，示例值：'AVAILABLE'
    :param goods_detail: 退款商品，示例值：{'merchant_goods_id':'1217752501201407033233368018', 'wechatpay_goods_id':'1001', 'goods_name':'iPhone6s 16G', 'unit_price':528800, 'refund_amount':528800, 'refund_quantity':1}
    :param notify_url: 通知地址，示例值：'https://www.weixin.qq.com/wxpay/pay.php'
    """
    params = {}
    params['notify_url'] = notify_url or self._notify_url
    # 
    if out_refund_no:
        params.update({'out_refund_no': out_refund_no})
    else:
        raise Exception('out_refund_no is not assigned.')
    if amount:
        params.update({'amount': amount})
    else:
        raise Exception('amount is not assigned.')
    if transaction_id:
        params.update({'transaction_id': transaction_id})
    if out_trade_no:
        params.update({'out_trade_no': out_trade_no})
    if reason:
        params.update({'reason': reason})
    if funds_account:
        params.update({'funds_account': funds_account})
    if goods_detail:
        params.update({'goods_detail': goods_detail})
    path = '/v3/refund/domestic/refunds'
    return self._core.request(path, method=RequestType.POST, data=params)
```

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

### 初始化

``` python
from wechatpayv3 import WeChatPay, WeChatPayType

# 微信支付商户号
MCHID = '1230000109'
# 商户证书私钥
PRIVATE_KEY = open('path_to_key/apiclient_key.pem').read()
# 商户证书序列号
CERT_SERIAL_NO = '444F4864EA9B34415...'
# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
APIV3_KEY = 'MIIEvwIBADANBgkqhkiG9w0BAQE...'
# APPID
APPID = 'wxd678efh567hg6787'
# 回调地址，也可以在调用接口的时候覆盖
NOTIFY_URL = 'https://www.weixin.qq.com/wxpay/pay.php'
# 微信支付平台证书缓存目录
CERT_DIR = './cert'

wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.MINIPROG,
    mchid=MCHID,
    private_key=PRIVATE_KEY,
    cert_serial_no=CERT_SERIAL_NO,
    apiv3_key=APIV3_KEY,
    appid=APPID,
    notify_url=NOTIFY_URL,
    cert_dir=CERT_DIR)
```

### 接口

``` python

# 统一下单
def pay():
    code, message = wxpay.pay(
        description='demo-description',
        out_trade_no='demo-trade-no',
        amount={'total': 100},
        payer={'openid': 'demo-openid'}
    )
    print('code: %s, message: %s' % (code, message))

# 订单查询
def query():
    code, message = wxpay.query(
        transaction_id='demo-transation-id'
    )
    print('code: %s, message: %s' % (code, message))

# 关闭订单
def close():
    code, message = wxpay.close(
        out_trade_no='demo-out-trade-no'
    )
    print('code: %s, message: %s' % (code, message))

# 申请退款
def refund():
    code, message=wxpay.refund(
        out_refund_no='demo-out-refund-no',
        amount={'refund': 100, 'total': 100, 'currency': 'CNY'},
        transaction_id='1217752501201407033233368018'
    )
    print('code: %s, message: %s' % (code, message))

# 退款查询
def query_refund():
    code, message = wxpay.query_refund(
        out_refund_no='demo-out-refund-no'
    )
    print('code: %s, message: %s' % (code, message))

# 申请交易账单
def trade_bill():
    code, message = wxpay.trade_bill(
        bill_date='2021-04-01'
    )
    print('code: %s, message: %s' % (code, message))

# 申请资金流水账单
def fundflow_bill():
    code, message = wxpay.fundflow_bill(
        bill_date='2021-04-01'
    )
    print('code: %s, message: %s' % (code, message))

# 下载账单
def download_bill():
    code, message = wxpay.download_bill(
        url='https://api.mch.weixin.qq.com/v3/billdownload/file?token=demo-token'
    )
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
                     'settle_info':{'profit_sharing':False, 'subsidy_amount':10}}]
    )
    print('code: %s, message: %s' % (code, message))

# 合单订单查询
def combine_query():
    code, message = wxpay.combine_query(
        combine_out_trade_no='demo_out_trade_no'
    )
    print('code: %s, message: %s' % (code, message))

# 合单订单关闭
def combine_close():
    code, message = wxpay.combine_close(
        combine_out_trade_no='demo_out_trade_no', 
        sub_orders=[{'mchid': '1900000109', 'out_trade_no': '20150806125346'}]
    )
    print('code: %s, message: %s' % (code, message))

# 计算签名供调起支付时拼凑参数使用
# 注意事项：注意参数顺序，某个参数为空时不能省略，以空字符串''占位
def sign():
    print(wxpay.sign(['wx888','1414561699','5K8264ILTKCH16CQ2502S....','prepay_id=wx201410272009395522657....']))

# 验证并解密回调消息，把回调接口收到的headers和body传入
def decrypt_callback(headers, body):
    print(wxpay.decrypt_callback(headers, body))

# 智慧商圈积分通知
def points_notify():
    code, message = wxpay.points_notify(
        transaction_id='4200000533202000000000000000',
        openid='otPAN5xxxxxxxxrOEG6lUv_pzacc',
        earn_points=True,
        increased_points=100,
        points_update_time='2020-05-20T13:29:35.120+08:00'
    )
    print('code: %s, message: %s' % (code, message))

# 智慧商圈积分授权查询
def user_authorization():
    code, message = wxpay.user_authorizations(
        openid='otPAN5xxxxxxxxrOEG6lUv_pzacc'
    )
    print('code: %s, message: %s' % (code, message))

# 支付即服务人员注册
def guides_register():
    code, message = wxpay.guides_register(
        corpid='1234567890',
        store_id=1234,
        userid='rebert',
        name='robert',
        mobile='13900000000',
        qr_code='https://open.work.weixin.qq.com/wwopen/userQRCode?vcode=xxx',
        avatar='http://wx.qlogo.cn/mmopen/ajNVdqHZLLA3WJ6DSZUfiakYe37PKnQhBIeOQBO4czqrnZDS79FH5Wm5m4X69TBicnHFlhiafvDwklOpZeXYQQ2icg/0',
        group_qrcode='http://p.qpic.cn/wwhead/nMl9ssowtibVGyrmvBiaibzDtp/0'
    )
    print('code: %s, message: %s' % (code, message))

# 支付即服务人员分配
def guides_assign():
    code, message = wxpay.guides_assign(
        guide_id='LLA3WJ6DSZUfiaZDS79FH5Wm5m4X69TBic',
        out_trade_no='20150806125346'
    )
    print('code: %s, message: %s' % (code, message))

# 支付即服务人员查询
def guides_query():
    code, message = wxpay.guides_query(
        store_id=1234,
        userid='robert',
        mobile='13900000000',
        work_id='robert',
        limit=5,
        offset=0
    )
    print('code: %s, message: %s' % (code, message))

# 支付即服务人员信息更新
def guides_update():
    code, message = wxpay.guides_update(
        guide_id='LLA3WJ6DSZUfiaZDS79FH5Wm5m4X69TBic',
        name='robert',
        mobile='13900000000',
        qr_code='https://open.work.weixin.qq.com/wwopen/userQRCode?vcode=xxx',
        avatar='http://wx.qlogo.cn/mmopen/ajNVdqHZLLA3WJ6DSZUfiakYe37PKnQhBIeOQBO4czqrnZDS79FH5Wm5m4X69TBicnHFlhiafvDwklOpZeXYQQ2icg/0',
        group_qrcode='http://p.qpic.cn/wwhead/nMl9ssowtibVGyrmvBiaibzDtp/0'
    )
    print('code: %s, message: %s' % (code, message))

# 图片上传
def image_upload():
    code, message = wxpay.image_upload(
        filepath='./media/demo.png'
    )
    print('code: %s, message: %s' % (code, message))

# 视频上传
def video_upload():
    code, message = wxpay.video_upload(
        filepath='./media/demo.mp4'
    )
    print('code: %s, message: %s' % (code, message))

# 查询车牌服务开通信息
def parking_service_find():
    code, message = wxpay.parking_service_find(
        plate_number='粤B888888',
        plate_color='BLUE',
        openid='oUpF8uMuAJOM2pxb1Q'
    )
    print('code: %s, message: %s' % (code, message))

# 创建停车入场
def parking_enter():
    code, message = wxpay.parking_enter(
        out_parking_no='1231243',
        plate_number='粤B888888',
        plate_color='BLUE',
        notify_url='https://yoursite.com/wxpay.html',
        start_time='2017-08-26T10:43:39+08:00',
        parking_name='欢乐海岸停车场',
        free_duration=3600
    )
    print('code: %s, message: %s' % (code, message))

# 停车扣费受理
def parking_order():
    code, message = wxpay.parking_order(
        description='停车场扣费',
        out_trade_no='20150806125346',
        notify_url='https://yoursite.com/wxpay.html',
        total=888,
        parking_id='5K8264ILTKCH16CQ250',
        plate_number='粤B888888',
        plate_color='BLUE',
        start_time='2017-08-26T10:43:39+08:00',
        end_time='2017-08-26T10:43:39+08:00',
        parking_name='欢乐海岸停车场',
        charging_duration=3600,
        device_id='12313'
    )
    print('code: %s, message: %s' % (code, message))

# 查询停车扣费订单
def parking_order_query():
    code, message = wxpay.parking_order_query(
        out_trade_no='20150806125346'
    )
    print('code: %s, message: %s' % (code, message))

# 图片上传(营销专用)
def marking_image_upload():
    code, message = wxpay.marketing_image_upload(
        filepath='./media/demo.png'
    )
    print('code: %s, message: %s' % (code, message))
```