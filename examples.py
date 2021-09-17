# -*- coding: utf-8 -*-
import json

from flask import Flask, jsonify, request

from wechatpayv3 import WeChatPay, WeChatPayType

# 微信支付商户号
MCHID = '1234567890'

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

# 初始化
wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.MINIPROG,
    mchid=MCHID,
    private_key=PRIVATE_KEY,
    cert_serial_no=CERT_SERIAL_NO,
    apiv3_key=APIV3_KEY,
    appid=APPID,
    notify_url=NOTIFY_URL,
    cert_dir=CERT_DIR)

app = Flask(__name__)


@app.route('/pay')
def pay():
    out_trade_no = 'demo-trade-no'
    description = 'demo-description'
    amount = 100
    openid = 'demo-openid'
    code, message = wxpay.pay(
        description=description,
        out_trade_no=out_trade_no,
        amount={'total': amount},
        payer={'openid': openid}
    )
    result = json.loads(message)
    if code in range(200, 300):
        prepay_id = result.get('prepay_id')
        timestamp = 'demo-timestamp'
        noncestr = 'demo-nocestr'
        package = 'prepay_id=' + prepay_id
        paysign = wxpay.sign([APPID, timestamp, noncestr, package])
        signtype = 'RSA'
        return jsonify({'code': 0, 'result': {
            'appId': APPID,
            'timeStamp': timestamp,
            'nonceStr': noncestr,
            'package': 'prepay_id=%s' % prepay_id,
            'signType': signtype,
            'paySign': paysign
        }})
    else:
        return jsonify({'code': -1, 'result': {'reason': result.get('code')}})


@app.route('/notify', methods=['POST'])
def notify():
    result = wxpay.decrypt_callback(request.headers, request.data)
    if result:
        resp = json.loads(result)
        appid = resp.get('appid')
        mchid = resp.get('mchid')
        out_trade_no = resp.get('out_trade_no')
        transaction_id = resp.get('transaction_id')
        trade_type = resp.get('trade_type')
        trade_state = resp.get('trade_state')
        trade_state_desc = resp.get('trade_state_desc')
        bank_type = resp.get('bank_type')
        attach = resp.get('attach')
        success_time = resp.get('success_time')
        payer = resp.get('payer')
        amount = resp.get('amount').get('total')
        #TODO: 根据返回参数进行必要的业务处理
        return 'SUCCESS'
    else:
        return 'FAILED'


if __name__ == '__main__':
    app.run()
