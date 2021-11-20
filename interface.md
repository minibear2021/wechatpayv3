# 接口示例

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
    if code in range(200, 300) and isinstance(message, bytes):
        with open("demo.txt.gz", 'wb') as f:
            f.write(message)

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

# 解密部分接口返回的敏感信息，详见官方文档说明：
# https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay4_3.shtml
def decrypt():
    print(wxpay.decrypt(ciphtext='Qe41VhP/sGdNeTHMQGlxCWiUyHu6XNO9GCYln2Luv4HhwJzZBfcL12sB+PgZcS5NhePBog30NgJ1xRaK+gbGDKwpg=='))

# 验证并解密回调消息，把回调接口收到的headers和body传入，详见官方文档说明：
# https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay4_2.shtml
# 这里以flask框架为例，其他web框架如果遇到InvalidSignature，请确认传入的body和收到的一致，没有做额外的预处理
def callback(headers=request.headers, body=request.data):
    print(wxpay.callback(headers, body))

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

# 请求分账
def profitsharing_order():
    code, message = wxpay.profitsharing_order(
        transaction_id='4208450740201411110007820472',
        out_order_no='P20150806125346',
        receivers={{'type': 'MERCHANT_ID', 'account': '86693852', 'amount': 888, 'description': '分给商户A'}},
        unfreeze_unsplit=True
    )
    print('code: %s, message: %s' % (code, message))

# 查询分账结果
def profitsharing_order_query():
    code, message = wxpay.profitsharing_order_query(
        transaction_id='4208450740201411110007820472',
        out_order_no='P20150806125346'
    )
    print('code: %s, message: %s' % (code, message))

# 请求分账回退
def profitsharing_return():
    code, message = wxpay.profitsharing_return(
        order_id='3008450740201411110007820472',
        out_return_no='R20190516001',
        return_mchid='86693852',
        amount=888,
        description='用户退款')
    print('code: %s, message: %s' % (code, message))

# 查询分账回退结果
def profitsharing_return_query():
    code, message = wxpay.profitsharing_return_query(
        out_order_no='P20150806125346',
        out_return_no='R20190516001'
    )
    print('code: %s, message: %s' % (code, message))

# 解冻剩余资金
def profitsharing_unfreeze():
    code, message = wxpay.profitsharing_unfreeze(
        transaction_id='4208450740201411110007820472',
        out_order_no='P20150806125346',
        description='解冻全部剩余资金'
    )
    print('code: %s, message: %s' % (code, message))

# 查询剩余待分金额
def profitsharing_amount_query():
    code, message = wxpay.profitsharing_amount_query(
        transaction_id='4208450740201411110007820472'
    )
    print('code: %s, message: %s' % (code, message))

# 添加分账接收方
def profitsharing_add_receiver():
    code, message = wxpay.profitsharing_add_receiver(
        account_type='MERCHANT_ID',
        account='86693852',
        relation_type='CUSTOM',
        name='腾讯充值中心',
        custom_relation='代理商'
    )
    print('code: %s, message: %s' % (code, message))

# 删除分账接收方
def profitsharing_delete_receiver():
    code, message = wxpay.profitsharing_delete_receiver(
        account_type='MERCHANT_ID',
        account='86693852'
    )
    print('code: %s, message: %s' % (code, message))

# 申请分账账单
def profitsharing_bill():
    code, message = wxpay.profitsharing_bill(
        bill_date='2021-04-01'
    )
    print('code: %s, message: %s' % (code, message))

# 查询投诉单列表
def complant_list_query():
    code, message = wxpay.complant_list_query(
        begin_date='2019-01-01'
    )
    print('code: %s, message: %s' % (code, message))

# 查询投诉单详情
def complant_detail_query():
    code, message = wxpay.complant_detail_query(
        complaint_id='200201820200101080076610000'
    )
    print('code: %s, message: %s' % (code, message))

# 查询投诉协商历史
def complant_history_query():
    code, message = wxpay.complant_history_query(
        complaint_id='200201820200101080076610000'
    )
    print('code: %s, message: %s' % (code, message))

# 创建投诉通知回调地址
def complant_notification_create():
    code, message = wxpay.complant_notification_create(
        url='https://www.xxx.com/notify'
    )
    print('code: %s, message: %s' % (code, message))

# 查询投诉通知回调地址
def complant_notification_query():
    code, message = wxpay.complant_notification_query()
    print('code: %s, message: %s' % (code, message))

# 更新投诉通知回调地址
def complant_notification_update():
    code, message = wxpay.complant_notification_update(
        url='https://www.xxx.com/notify'
    )
    print('code: %s, message: %s' % (code, message))

# 删除投诉通知回调地址
def complant_notification_delete():
    code, message = wxpay.complant_notification_delete()
    print('code: %s, message: %s' % (code, message))

# 提交投诉回复
def complant_response():
    code, message = wxpay.complant_response(
        complaint_id='200201820200101080076610000',
        response_content='已与用户沟通解决'
    )
    print('code: %s, message: %s' % (code, message))

# 反馈投诉处理完成
def complant_complete():
    code, message = wxpay.complant_complete(
        complaint_id='200201820200101080076610000'
    )
    print('code: %s, message: %s' % (code, message))

# 商户上传投诉反馈图片
def complant_image_upload():
    code, message = wxpay.complant_image_upload(
        filepath='./media/demo.png'
    )
    print('code: %s, message: %s' % (code, message))

# 下载客户投诉图片
def complant_image_download():
    code, message = wxpay.complant_image_download(
        media_url='https://api.mch.weixin.qq.com/v3/merchant-service/images/xxxxx'
    )
    print('code: %s, message: %s' % (code, message))
    if code in range(200, 300) and isinstance(message, bytes):
        with open("demo.bmp", 'wb') as f:
            f.write(message)
```
