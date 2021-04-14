# -*- coding: utf-8 -*-
from config import MCH_KEY_SERIAL_NO, MCHID, WECHAT_PUBLIC_KEY, MCH_PRIVATE_KEY, APPID, NOTIFY_URL

from wechatpayv3 import WeChatPay, WeChatPayType

wxpay = WeChatPay(wechatpay_type=WeChatPayType.MINIPROG,
                  mchid=MCHID,
                  mch_parivate_key=MCH_PRIVATE_KEY,
                  mch_key_serial_no=MCH_KEY_SERIAL_NO,
                  wechat_public_key=WECHAT_PUBLIC_KEY,
                  appid=APPID,
                  notify_url=NOTIFY_URL)


def certificate():
    code, message = wxpay.certificate()
    print('code: %s, message: %s' % (code, message))


def pay():
    code, message = wxpay.pay(description='demo-description',
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
    code, message = wxpay.refund(transaction_id='demo-transation-id',
                                 out_refund_no='demo-out-refund-no',
                                 amount={'refund': 100, 'total': 100, 'currency': 'CNY'})
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
    code, message = wxpay.download_bill(
        url='https://api.mch.weixin.qq.com/v3/billdownload/file?token=demo-token')
    print('code: %s, message: %s' % (code, message))


if __name__ == '__main__':
    # certificate()
    # pay()
    # query()
    # close()
    # refund()
    # query_refund()
    # trade_bill()
    # fundflow_bill()
    download_bill()
    pass
