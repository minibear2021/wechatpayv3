# -*- coding: utf-8 -*-
from config import APIV3_KEY, APPID, CERT_SERIAL_NO, MCHID, NOTIFY_URL, PRIVATE_KEY, CERT_DIR
from wechatpayv3 import WeChatPay, WeChatPayType

wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.MINIPROG,
    mchid=MCHID,
    parivate_key=PRIVATE_KEY,
    cert_serial_no=CERT_SERIAL_NO,
    apiv3_key=APIV3_KEY,
    appid=APPID,
    notify_url=NOTIFY_URL,
    cert_dir=CERT_DIR)


def pay():
    code, message = wxpay.pay(
        description='demo-description',
        out_trade_no='demo-trade-no',
        amount={'total': 100},
        payer={'openid': 'demo-openid'})
    print('code: %s, message: %s' % (code, message))


def query():
    code, message = wxpay.query(transaction_id='demo-transation-id')
    print('code: %s, message: %s' % (code, message))


def close():
    code, message = wxpay.close(out_trade_no='demo-out-trade-no')
    print('code: %s, message: %s' % (code, message))


def refund():
    code, message = wxpay.refund(
        out_refund_no='demo-out-refund-no',
        amount={'refund': 100, 'total': 100, 'currency': 'CNY'},
        transaction_id='1217752501201407033233368018')
    print('code: %s, message: %s' % (code, message))


def query_refund():
    code, message = wxpay.query_refund(out_refund_no='demo-out-refund-no')
    print('code: %s, message: %s' % (code, message))


def trade_bill():
    code, message = wxpay.trade_bill(bill_date='2021-04-01')
    print('code: %s, message: %s' % (code, message))


def fundflow_bill():
    code, message = wxpay.fundflow_bill(bill_date='2021-04-01')
    print('code: %s, message: %s' % (code, message))


def download_bill():
    code, message = wxpay.download_bill(url='https://api.mch.weixin.qq.com/v3/billdownload/file?token=demo-token')
    print('code: %s, message: %s' % (code, message))


def combine_pay():
    code, message = wxpay.combine_pay(
        combine_out_trade_no='demo_out_trade_no',
        sub_orders=[{'mchid': '1900000109',
                     'attach': '深圳分店',
                     'amount': {'total_amount': 100, 'currency': 'CNY'},
                     'out_trade_no': '20150806125346',
                     'description': '腾讯充值中心-QQ会员充值',
                     'settle_info': {'profit_sharing': False, 'subsidy_amount': 10}}],
        combine_payer_info={'openid': 'oUpF8uMuAJO_M2pxb1Q9zNjWeS6o'})
    print('code: %s, message: %s' % (code, message))


def combine_query():
    code, message = wxpay.combine_query(combine_out_trade_no='demo_out_trade_no')
    print('code: %s, message: %s' % (code, message))


def combine_close():
    code, message = wxpay.combine_close(
        combine_out_trade_no='demo_out_trade_no',
        sub_orders=[{'mchid': '1900000109', 'out_trade_no': '20150806125346'}])
    print('code: %s, message: %s' % (code, message))


def sign():
    print(wxpay.sign(['wx888', '1414561699', '5K8264ILTKCH16CQ2502S....', 'prepay_id=wx201410272009395522657....']))


def decrypt_callback(headers, body):
    print(wxpay.decrypt_callback(headers, body))


def points_notify():
    code, message = wxpay.points_notify(
        transaction_id='4200000533202000000000000000',
        openid='otPAN5xxxxxxxxrOEG6lUv_pzacc',
        earn_points=True,
        increased_points=100,
        points_update_time='2020-05-20T13:29:35.120+08:00')
    print('code: %s, message: %s' % (code, message))


def user_authorization():
    code, message = wxpay.user_authorization(openid='otPAN5xxxxxxxxrOEG6lUv_pzacc')
    print('code: %s, message: %s' % (code, message))


def guides_register():
    code, message = wxpay.guides_register(
        corpid='1234567890',
        store_id=1234,
        userid='rebert',
        name='pVd1HJ6v/69bDnuC4EL5Kz4jBHLiCa8MRtelw/wDa4SzfeespQO/0kjiwfqdfg==',
        mobile='pVd1HJ6v/69bDnuC4EL5Kz4jBHLiCa8MRtelw/wDa4SzfeespQO/0kjiwfqdfg==',
        qr_code='https://open.work.weixin.qq.com/wwopen/userQRCode?vcode=xxx',
        avatar='http://wx.qlogo.cn/mmopen/ajNVdqHZLLA3WJ6DSZUfiakYe37PKnQhBIeOQBO4czqrnZDS79FH5Wm5m4X69TBicnHFlhiafvDwklOpZeXYQQ2icg/0',
        group_qrcode='http://p.qpic.cn/wwhead/nMl9ssowtibVGyrmvBiaibzDtp/0')
    print('code: %s, message: %s' % (code, message))


def guides_assign():
    code, message = wxpay.guides_assign(
        guide_id='LLA3WJ6DSZUfiaZDS79FH5Wm5m4X69TBic',
        out_trade_no='20150806125346')
    print('code: %s, message: %s' % (code, message))


def guides_query():
    code, message = wxpay.guides_query(
        store_id=1234,
        userid='robert',
        mobile='RXjWsWlqTZ0Y8Q+piBCS5ACusK6nz7mKQeypi9fKjAggRfvNFPf/bNxPvork4mMVgZkA==',
        work_id='robert',
        limit=5,
        offset=0)
    print('code: %s, message: %s' % (code, message))

def guides_update():
    code, message = wxpay.guides_update(
        guide_id='LLA3WJ6DSZUfiaZDS79FH5Wm5m4X69TBic',
        name='pVd1HJ6v/69bDnuC4EL5Kz4jBHLiCa8MRtelw/wDa4SzfeespQO/0kjiwfqdfg==',
        mobile='pVd1HJ6v/69bDnuC4EL5Kz4jBHLiCa8MRtelw/wDa4SzfeespQO/0kjiwfqdfg==',
        qr_code='https://open.work.weixin.qq.com/wwopen/userQRCode?vcode=xxx',
        avatar='http://wx.qlogo.cn/mmopen/ajNVdqHZLLA3WJ6DSZUfiakYe37PKnQhBIeOQBO4czqrnZDS79FH5Wm5m4X69TBicnHFlhiafvDwklOpZeXYQQ2icg/0',
        group_qrcode='http://p.qpic.cn/wwhead/nMl9ssowtibVGyrmvBiaibzDtp/0')
    print('code: %s, message: %s' % (code, message))


if __name__ == '__main__':
    pay()
    query()
    close()
    refund()
    query_refund()
    trade_bill()
    fundflow_bill()
    download_bill()
    combine_pay()
    combine_query()
    combine_close()
    sign()
    points_notify()
    user_authorization()
    guides_register()
    guides_assign()
    guides_query()
    guides_update()
    pass
