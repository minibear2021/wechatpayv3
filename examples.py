# -*- coding: utf-8 -*-
from config import APIV3_KEY, APPID, CERT_SERIAL_NO, MCHID, NOTIFY_URL, PRIVATE_KEY, CERT_DIR
from wechatpayv3 import WeChatPay, WeChatPayType

wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.MINIPROG,
    mchid=MCHID,
    private_key=PRIVATE_KEY,
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
        payer={'openid': 'demo-openid'}
    )
    print('code: %s, message: %s' % (code, message))


def query():
    code, message = wxpay.query(
        transaction_id='demo-transation-id'
    )
    print('code: %s, message: %s' % (code, message))


def close():
    code, message = wxpay.close(
        out_trade_no='demo-out-trade-no'
    )
    print('code: %s, message: %s' % (code, message))


def refund():
    code, message = wxpay.refund(
        out_refund_no='demo-out-refund-no',
        amount={'refund': 100, 'total': 100, 'currency': 'CNY'},
        transaction_id='1217752501201407033233368018'
    )
    print('code: %s, message: %s' % (code, message))


def query_refund():
    code, message = wxpay.query_refund(
        out_refund_no='demo-out-refund-no'
    )
    print('code: %s, message: %s' % (code, message))


def trade_bill():
    code, message = wxpay.trade_bill(
        bill_date='2021-04-01'
    )
    print('code: %s, message: %s' % (code, message))


def fundflow_bill():
    code, message = wxpay.fundflow_bill(
        bill_date='2021-04-01'
    )
    print('code: %s, message: %s' % (code, message))


def download_bill():
    code, message = wxpay.download_bill(
        url='https://api.mch.weixin.qq.com/v3/billdownload/file?token=demo-token'
    )
    print('code: %s, message: %s' % (code, message))
    if code in range(200, 300) and isinstance(message, bytes):
        with open("demo.txt.gz", 'wb') as f:
            f.write(message)


def combine_pay():
    code, message = wxpay.combine_pay(
        combine_out_trade_no='demo_out_trade_no',
        sub_orders=[{'mchid': '1900000109',
                     'attach': '深圳分店',
                     'amount': {'total_amount': 100, 'currency': 'CNY'},
                     'out_trade_no': '20150806125346',
                     'description': '腾讯充值中心-QQ会员充值',
                     'settle_info': {'profit_sharing': False, 'subsidy_amount': 10}}],
        combine_payer_info={'openid': 'oUpF8uMuAJO_M2pxb1Q9zNjWeS6o'}
    )
    print('code: %s, message: %s' % (code, message))


def combine_query():
    code, message = wxpay.combine_query(
        combine_out_trade_no='demo_out_trade_no'
    )
    print('code: %s, message: %s' % (code, message))


def combine_close():
    code, message = wxpay.combine_close(
        combine_out_trade_no='demo_out_trade_no',
        sub_orders=[{'mchid': '1900000109', 'out_trade_no': '20150806125346'}]
    )
    print('code: %s, message: %s' % (code, message))


def sign():
    print(wxpay.sign(['wx888', '1414561699', '5K8264ILTKCH16CQ2502S....', 'prepay_id=wx201410272009395522657....']))


def decrypt():
    print(wxpay.decrypt(ciphtext='Qe41VhP/sGdNeTHMQGlxCWiUyHu6XNO9GCYln2Luv4HhwJzZBfcL12sB+PgZcS5NhePBog30NgJ1xRaK+gbGDKwpg=='))


def decrypt_callback(headers, body):
    print(wxpay.decrypt_callback(headers, body))


def points_notify():
    code, message = wxpay.points_notify(
        transaction_id='4200000533202000000000000000',
        openid='otPAN5xxxxxxxxrOEG6lUv_pzacc',
        earn_points=True,
        increased_points=100,
        points_update_time='2020-05-20T13:29:35.120+08:00'
    )
    print('code: %s, message: %s' % (code, message))


def user_authorization():
    code, message = wxpay.user_authorization(
        openid='otPAN5xxxxxxxxrOEG6lUv_pzacc'
    )
    print('code: %s, message: %s' % (code, message))


def guides_register():
    code, message = wxpay.guides_register(
        corpid='1234567890',
        store_id=1234,
        userid='rebert',
        name='rebert',
        mobile='13900000000',
        qr_code='https://open.work.weixin.qq.com/wwopen/userQRCode?vcode=xxx',
        avatar='http://wx.qlogo.cn/mmopen/ajNVdqHZLLA3WJ6DSZUfiakYe37PKnQhBIeOQBO4czqrnZDS79FH5Wm5m4X69TBicnHFlhiafvDwklOpZeXYQQ2icg/0',
        group_qrcode='http://p.qpic.cn/wwhead/nMl9ssowtibVGyrmvBiaibzDtp/0'
    )
    print('code: %s, message: %s' % (code, message))


def guides_assign():
    code, message = wxpay.guides_assign(
        guide_id='LLA3WJ6DSZUfiaZDS79FH5Wm5m4X69TBic',
        out_trade_no='20150806125346'
    )
    print('code: %s, message: %s' % (code, message))


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


def image_upload():
    code, message = wxpay.image_upload(
        filepath='./media/demo.png'
    )
    print('code: %s, message: %s' % (code, message))


def video_upload():
    code, message = wxpay.video_upload(
        filepath='./media/demo.mp4'
    )
    print('code: %s, message: %s' % (code, message))


def parking_service_find():
    code, message = wxpay.parking_service_find(
        plate_number='粤B888888',
        plate_color='BLUE',
        openid='oUpF8uMuAJOM2pxb1Q'
    )
    print('code: %s, message: %s' % (code, message))


def parking_enter():
    code, message = wxpay.parking_enter(
        out_parking_no='1231243',
        plate_number='粤B888888',
        plate_color='BLUE',
        start_time='2017-08-26T10:43:39+08:00',
        parking_name='欢乐海岸停车场',
        free_duration=3600
    )
    print('code: %s, message: %s' % (code, message))


def parking_order():
    code, message = wxpay.parking_order(
        description='停车场扣费',
        out_trade_no='20150806125346',
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


def parking_order_query():
    code, message = wxpay.parking_order_query(
        out_trade_no='20150806125346'
    )
    print('code: %s, message: %s' % (code, message))


def marking_image_upload():
    code, message = wxpay.marketing_image_upload(
        filepath='./media/demo.png'
    )
    print('code: %s, message: %s' % (code, message))


def profitsharing_order():
    code, message = wxpay.profitsharing_order(
        transaction_id='4208450740201411110007820472',
        out_order_no='P20150806125346',
        receivers={{'type': 'MERCHANT_ID', 'account': '86693852', 'amount': 888, 'description': '分给商户A'}},
        unfreeze_unsplit=True
    )
    print('code: %s, message: %s' % (code, message))


def profitsharing_order_query():
    code, message = wxpay.profitsharing_order_query(
        transaction_id='4208450740201411110007820472',
        out_order_no='P20150806125346'
    )
    print('code: %s, message: %s' % (code, message))


def profitsharing_return():
    code, message = wxpay.profitsharing_return(
        order_id='3008450740201411110007820472',
        out_return_no='R20190516001',
        return_mchid='86693852',
        amount=888,
        description='用户退款')
    print('code: %s, message: %s' % (code, message))


def profitsharing_return_query():
    code, message = wxpay.profitsharing_return_query(
        out_order_no='P20150806125346',
        out_return_no='R20190516001'
    )
    print('code: %s, message: %s' % (code, message))


def profitsharing_unfreeze():
    code, message = wxpay.profitsharing_unfreeze(
        transaction_id='4208450740201411110007820472',
        out_order_no='P20150806125346',
        description='解冻全部剩余资金'
    )
    print('code: %s, message: %s' % (code, message))


def profitsharing_amount_query():
    code, message = wxpay.profitsharing_amount_query(
        transaction_id='4208450740201411110007820472'
    )
    print('code: %s, message: %s' % (code, message))


def profitsharing_add_receiver():
    code, message = wxpay.profitsharing_add_receiver(
        account_type='MERCHANT_ID',
        account='86693852',
        relation_type='CUSTOM',
        name='腾讯充值中心',
        custom_relation='代理商'
    )
    print('code: %s, message: %s' % (code, message))


def profitsharing_delete_receiver():
    code, message = wxpay.profitsharing_delete_receiver(
        account_type='MERCHANT_ID',
        account='86693852'
    )
    print('code: %s, message: %s' % (code, message))


def profitsharing_bill():
    code, message = wxpay.profitsharing_bill(
        bill_date='2021-04-01'
    )
    print('code: %s, message: %s' % (code, message))


def complant_list_query():
    code, message = wxpay.complant_list_query(
        begin_date='2019-01-01'
    )
    print('code: %s, message: %s' % (code, message))


def complant_detail_query():
    code, message = wxpay.complant_detail_query(
        complaint_id='200201820200101080076610000'
    )
    print('code: %s, message: %s' % (code, message))


def complant_history_query():
    code, message = wxpay.complant_history_query(
        complaint_id='200201820200101080076610000'
    )
    print('code: %s, message: %s' % (code, message))


def complant_notification_create():
    code, message = wxpay.complant_notification_create(
        url='https://www.xxx.com/notify'
    )
    print('code: %s, message: %s' % (code, message))


def complant_notification_query():
    code, message = wxpay.complant_notification_query()
    print('code: %s, message: %s' % (code, message))


def complant_notification_update():
    code, message = wxpay.complant_notification_update(
        url='https://www.xxx.com/notify'
    )
    print('code: %s, message: %s' % (code, message))


def complant_notification_delete():
    code, message = wxpay.complant_notification_delete()
    print('code: %s, message: %s' % (code, message))


def complant_response():
    code, message = wxpay.complant_response(
        complaint_id='200201820200101080076610000',
        response_content='已与用户沟通解决'
    )
    print('code: %s, message: %s' % (code, message))


def complant_complete():
    code, message = wxpay.complant_complete(
        complaint_id='200201820200101080076610000'
    )
    print('code: %s, message: %s' % (code, message))


def complant_image_upload():
    code, message = wxpay.complant_image_upload(
        filepath='./media/demo.png'
    )
    print('code: %s, message: %s' % (code, message))


def complant_image_download():
    code, message = wxpay.complant_image_download(
        media_url='https://api.mch.weixin.qq.com/v3/merchant-service/images/xxxxx'
    )
    print('code: %s, message: %s' % (code, message))
    if code in range(200, 300) and isinstance(message, bytes):
        with open("demo.bmp", 'wb') as f:
            f.write(message)


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
    decrypt()
    points_notify()
    user_authorization()
    guides_register()
    guides_assign()
    guides_query()
    guides_update()
    image_upload()
    video_upload()
    parking_service_find()
    parking_enter()
    parking_order()
    parking_order_query()
    marking_image_upload()
    profitsharing_order()
    profitsharing_order_query()
    profitsharing_return()
    profitsharing_return_query()
    profitsharing_unfreeze()
    profitsharing_amount_query()
    profitsharing_add_receiver()
    profitsharing_delete_receiver()
    profitsharing_bill()
    complant_list_query()
    complant_detail_query()
    complant_history_query()
    complant_notification_create()
    complant_notification_query()
    complant_notification_update()
    complant_notification_delete()
    complant_response()
    complant_complete()
    complant_image_upload()
    complant_image_download()
    pass
