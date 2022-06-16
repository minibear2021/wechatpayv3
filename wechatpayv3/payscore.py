# -*- coding: utf-8 -*-

from .type import RequestType
from .transaction import query_refund, refund


def payscore_direct_complete(self, out_order_no, openid, service_id, service_introduction, post_payments,
                             time_range, total_amount, post_discounts=None, location=None,
                             profit_sharing=False, goods_tag=None, attach=None, notify_url=None, appid=None):
    """创单结单合并
    :param out_order_no: 商户服务订单号，商户系统内部服务订单号（不是交易单号），要求此参数只能由数字、大小写字母_-|*组成，且在同一个商户号下唯一。示例值:'1234323JKHDFE1243252'
    :param openid: 用户标识，微信用户在商户对应appid下的唯一标识。示例值:'oUpF8uMuAJO_M2pxb1Q9zNjWeS6o'
    :param service_id: 服务ID。示例值:'500001'
    :param service_introduction: 服务信息，用于介绍本订单所提供的服务 ，当参数长度超过20个字符时，报错处理。示例值:'某某酒店'
    :param post_payments: 付费项目列表，最多包含100条付费项目。
    :param time_range: 服务时间范围。
    :param total_amount: 总金额，总金额 =（完结付费项目1…+完结付费项目n）-（完结商户优惠项目1…+完结商户优惠项目n）。示例值:50000
    :param post_discounts: 商户优惠，付费商户优惠列表，最多包含30条商户优惠。
    :param location: 服务位置，如果传入，用户侧则显示此参数。
    :param profit_sharing: 微信支付服务分账标记，默认为false，枚举值:False:不分账，True:分账。示例值:False
    :param goods_tag: 订单优惠标记。示例值:'goods_tag1'
    :param attach: 商户数据包。商户数据包可存放本订单所需信息，需要先urlencode后传入。当商户数据包总长度超出256字符时，报错处理。示例值:'Easdfowealsdkjfnlaksjdlfkwqoi&wl3l2sald'
    :param notify_url: 商户回调地址，商户接收扣款成功回调通知的地址，服务需要收款时此参数必填；服务无需收款时此参数不填。示例值:'https://api.test.com'
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    """
    params = {}
    if not (out_order_no and openid and service_id and service_introduction and post_payments and time_range and total_amount):
        raise Exception('ut_order_no or openid or service_id or service_introduction or post_payments or time_range or total_amount is not assigned.')
    params.update({'appid': appid or self._appid})
    params.update({'out_order_no': out_order_no})
    params.update({'openid': openid})
    params.update({'service_id': service_id})
    params.update({'service_introduction': service_introduction})
    params.update({'post_payments': post_payments})
    params.update({'time_range': time_range})
    params.update({'total_amount': total_amount})
    if post_discounts:
        params.update({'post_discounts': post_discounts})
    if location:
        params.update({'location': location})
    if profit_sharing:
        params.update({'profit_sharing': profit_sharing})
    if goods_tag:
        params.update({'goods_tag': goods_tag})
    if attach:
        params.update({'attach': attach})
    payment = False
    for item in post_payments:
        if item.get('amount') > 0:
            payment = True
            break
    if payment:
        if not (notify_url or self._notify_url):
            raise Exception('notify_url is not assigned.')
        params.update({'notify_url': notify_url or self._notify_url})
    path = '/payscore/serviceorder/direct-complete'
    return self._core.request(path, method=RequestType.POST, data=params)


def payscore_permission(self, service_id, authorization_code, notify_url=None, appid=None):
    """商户预授权
    :param service_id: 服务ID。示例值:'500001'
    :param authorization_code: 授权协议号，户系统内部授权协议号，要求此参数只能由数字、大小写字母_-*组成，且在同一个商户号下唯一。示例值:'1234323JKHDFE1243252'
    :param notify_url: 通知地址，商户接收授权回调通知的地址。示例值:'http://www.qq.com'
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    """
    params = {}
    if not (service_id and authorization_code):
        raise Exception('service_id or authorization_code is not assigned.')
    params.update({'appid': appid or self._appid})
    params.update({'service_id': service_id})
    params.update({'authorization_code': authorization_code})
    params.update({'notify_url': notify_url or self._notify_url})
    path = '/v3/payscore/permissions'
    return self._core.request(path, method=RequestType.POST, data=params)


def payscore_permission_query(self, service_id, authorization_code=None, openid=None):
    """查询用户授权记录（授权协议号或openid）
    :param service_id: 服务ID。示例值:'500001'
    :param authorization_code: 授权协议号，户系统内部授权协议号，要求此参数只能由数字、大小写字母_-*组成，且在同一个商户号下唯一。示例值:'1234323JKHDFE1243252'
    :param openid: 用户标识，微信用户在商户对应appid下的唯一标识。示例值:'oUpF8uMuAJO_M2pxb1Q9zNjWeS6o'
    """
    if not service_id:
        raise Exception('service_id is not assigned.')
    if authorization_code:
        path = '/v3/payscore/permissions/authorization-code/%s?service_id=%s' % (authorization_code, service_id)
    elif openid:
        path = '/v3/payscore/permissions/openid/%s?appid=%s&service_id=%s' % (openid, self._appid, service_id)
    else:
        raise Exception('authorization_code or openid is not assigned.')
    return self._core.request(path)


def payscore_permission_terminate(self, service_id, reason, authorization_code=None, openid=None, appid=None):
    """解除用户授权记录（授权协议号或openid）
    :param service_id: 服务ID。示例值:'500001'
    :param reason: 撤销原因，解除授权原因。示例值:'撤销原因'
    :param authorization_code: 授权协议号，户系统内部授权协议号，要求此参数只能由数字、大小写字母_-*组成，且在同一个商户号下唯一。示例值:'1234323JKHDFE1243252'
    :param openid: 用户标识，微信用户在商户对应appid下的唯一标识。示例值:'oUpF8uMuAJO_M2pxb1Q9zNjWeS6o'
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    """
    params = {}
    if not (service_id and reason):
        raise Exception('service_id or reason is not assigned.')
    params.update({'service_id': service_id})
    params.update({'reason': reason})
    if authorization_code:
        path = 'v3/payscore/permissions/authorization-code/%s/terminate' % authorization_code
    elif openid:
        params.update({'appid': appid or self._appid})
        path = '/v3/payscore/permissions/openid/%s/terminate' % openid
    else:
        raise Exception('authorization_code or openid is not assigned.')
    return self._core.request(path, method=RequestType.POST, data=params)


def payscore_create(self, out_order_no, service_id, service_introduction, time_range,
                    risk_fund, attach=None, openid=None, post_payments=None, post_discounts=None,
                    location=None, need_user_confirm=True, notify_url=None, appid=None):
    """创建支付分订单
    :param out_order_no: 商户服务订单号，商户系统内部服务订单号（不是交易单号），要求此参数只能由数字、大小写字母_-|*组成，且在同一个商户号下唯一。示例值:'1234323JKHDFE1243252'
    :param service_id: 服务ID，该服务ID有本接口对应产品的权限。示例值:'500001'
    :param service_introduction: 服务信息，用于介绍本订单所提供的服务 ，当参数长度超过20个字符时，报错处理。示例值:'某某酒店'
    :param time_range: 服务时间范围。
    :param risk_fund: 订单风险金。
    :param attach: 商户数据包，商户数据包可存放本订单所需信息，需要先urlencode后传入。当商户数据包总长度超出256字符时，报错处理。示例值:'Easdfowealsdkjfnlaksjdlfkwqoi&wl3l2sald'
    :param openid: 用户标识，微信用户在商户对应appid下的唯一标识。免确认订单:必填，需确认订单:不填。示例值:'oUpF8uMuAJO_M2pxb1Q9zNjWeS6o'
    :param post_payments: 后付费项目，后付费项目列表，最多包含100条付费项目。如果传入，用户侧则显示此参数。
    :param post_discounts: 后付费商户优惠，后付费商户优惠列表，最多包含30条商户优惠。如果传入，用户侧则显示此参数。
    :param location: 服务位置信息，如果传入，用户侧则显示此参数。
    :param need_user_confirm: 是否需要用户确认，枚举值:False:免确认订单，True:需确认订单，默认值True。示例值:True
    :param notify_url: 通知地址，示例值:'https://www.weixin.qq.com/wxpay/pay.php'
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    """
    params = {}
    if out_order_no:
        params.update({'out_order_no': out_order_no})
    else:
        raise Exception('out_order_no is not assigned.')
    params.update({'appid': appid or self._appid})
    if service_id:
        params.update({'service_id': service_id})
    else:
        raise Exception('service_id is not assigned.')
    if service_introduction:
        params.update({'service_introduction': service_introduction})
    else:
        raise Exception('service_introduction is not assigned.')
    if time_range:
        params.update({'time_range': time_range})
    else:
        raise Exception('time_range is not assigned.')
    if risk_fund:
        params.update({'risk_fund': risk_fund})
    else:
        raise Exception('risk_fund is not assigned.')
    if attach:
        params.update({'attach': attach})
    if post_payments:
        params.update({'post_payments': post_payments})
    if post_discounts:
        params.update({'post_discounts': post_discounts})
    if location:
        params.update({'location': location})
    params.update({'need_user_confirm': need_user_confirm})
    if not need_user_confirm:
        if openid:
            params.update({'openid': openid})
        else:
            raise Exception('openid is not assigned.')
    params.update({'notify_url': notify_url or self._notify_url})
    path = '/v3/payscore/serviceorder'
    return self._core.request(path, method=RequestType.POST, data=params)


def payscore_query(self, service_id, out_order_no=None, query_id=None):
    """查询支付分订单
    :param service_id: 服务ID，该服务ID有本接口对应产品的权限。示例值:'500001'
    :param out_order_no: 商户服务订单号，商户系统内部服务订单号（不是交易单号），要求此参数只能由数字、大小写字母_-|*组成，且在同一个商户号下唯一。示例值:'1234323JKHDFE1243252'
    :param query_id: 回跳查询ID，微信侧回跳到商户前端时用于查单的单据查询id。商户单号与回跳查询id必填其中一个。不允许都填写或都不填写。示例值:'15646546545165651651'
    """
    if service_id:
        path = '/v3/payscore/serviceorder?service_id=%s&appid=%s' % (service_id, self._appid)
    else:
        raise Exception('service_id is not assigned.')
    if out_order_no:
        path = '%s&out_order_no=%s' % (path, out_order_no)
    elif query_id:
        path = '%s&query_id=%s' % (path, query_id)
    else:
        raise Exception('out_order_no or query_id is not assigned.')
    return self._core.request(path)


def payscore_cancel(self, out_order_no, service_id, reason, appid=None):
    """取消支付分订单
    :param out_order_no: 商户服务订单号，商户系统内部服务订单号（不是交易单号），要求此参数只能由数字、大小写字母_-|*组成，且在同一个商户号下唯一。示例值:'1234323JKHDFE1243252'
    :param service_id: 服务ID，该服务ID有本接口对应产品的权限。示例值:'500001'
    :param query_id: 回跳查询ID，微信侧回跳到商户前端时用于查单的单据查询id。商户单号与回跳查询id必填其中一个。不允许都填写或都不填写。示例值:'15646546545165651651'
    :param reason: 取消原因，最多30个字符，每个汉字/数字/英语都按1个字符计算超过长度报错处理。注:重录时需保证参数完全一致，包括取消原因。示例值:'用户投诉'
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    """
    params = {}
    if out_order_no:
        path = '/v3/payscore/serviceorder/%s/cancel' % out_order_no
    else:
        raise Exception('out_order_no is not assigned.')
    if service_id:
        params.update({'service_id': service_id})
    else:
        raise Exception('service_id is not assigned.')
    if reason:
        params.update({'reason': reason})
    else:
        raise Exception('reason is not assigned.')
    params.update({'appid': appid or self._appid})
    return self._core.request(path, method=RequestType.POST, data=params)


def payscore_modify(self, out_order_no, service_id, post_payments, total_amount, reason, post_discounts=None, appid=None):
    """修改订单金额
    :param out_order_no: 商户服务订单号，商户系统内部服务订单号（不是交易单号），要求此参数只能由数字、大小写字母_-|*组成，且在同一个商户号下唯一。示例值:'1234323JKHDFE1243252'
    :param service_id: 服务ID，该服务ID有本接口对应产品的权限。示例值:'500001'
    :param post_payments: 后付费项目，后付费项目列表，最多包含100条付费项目。
    :param total_amount: 总金额，单位为分，不能超过完结订单时候的总金额，只能为整数，详见支付金额。示例值:50000
    :param reason: 取消原因，最多30个字符，每个汉字/数字/英语都按1个字符计算超过长度报错处理。注:重录时需保证参数完全一致，包括取消原因。示例值:'用户投诉'
    :param post_discounts: 后付费商户优惠，后付费商户优惠列表，最多包含30条商户优惠。如果传入，用户侧则显示此参数。
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    """
    params = {}
    if out_order_no:
        path = '/v3/payscore/serviceorder/%s/modify' % out_order_no
    else:
        raise Exception('out_order_no is not assigned.')
    if service_id:
        params.update({'service_id': service_id})
    else:
        raise Exception('service_id is not assigned.')
    if post_payments:
        params.update({'post_payments': post_payments})
    else:
        raise Exception('post_payments is not assigned.')
    if total_amount:
        params.update({'total_amount': total_amount})
    else:
        raise Exception('total_amount is not assigned.')
    if reason:
        params.update({'reason': reason})
    else:
        raise Exception('reason is not assigned.')
    if post_discounts:
        params.update({'post_discounts': post_discounts})
    params.update({'appid': appid or self._appid})
    return self._core.request(path, method=RequestType.POST, data=params)


def payscore_complete(self, out_order_no, service_id, post_payments, total_amount, post_discounts=None,
                      time_range=None, location=None, profit_sharing=False, goods_tag=None, appid=None):
    """完结支付分订单
    :param out_order_no: 商户服务订单号，商户系统内部服务订单号（不是交易单号），要求此参数只能由数字、大小写字母_-|*组成，且在同一个商户号下唯一。示例值:'1234323JKHDFE1243252'
    :param service_id: 服务ID，该服务ID有本接口对应产品的权限。示例值:'500001'
    :param post_payments: 后付费项目，后付费项目列表，最多包含100条付费项目。如果传入，用户侧则显示此参数。
    :param total_amount: 总金额，数字，必须≥0（单位:分），只能为整数。示例值:100
    :param post_discounts: 后付费商户优惠，后付费商户优惠列表，最多包含30条商户优惠。如果传入，用户侧则显示此参数。
    :param time_range: 服务时间范围。
    :param location: 服务位置信息，如果传入，用户侧则显示此参数。
    :param profit_sharing: 微信支付服务分账标记，完结订单分账接口标记。False:不分账，True:分账，默认:False，示例值:False
    :param goods_tag: 订单优惠标记，订单优惠标记，代金券或立减金优惠的参数，示例值:'goods_tag'
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    """
    params = {}
    if out_order_no:
        path = '/v3/payscore/serviceorder/%s/complete' % out_order_no
    else:
        raise Exception('out_order_no is not assigned.')
    if service_id:
        params.update({'service_id': service_id})
    else:
        raise Exception('service_id is not assigned.')
    if post_payments:
        params.update({'post_payments': post_payments})
    else:
        raise Exception('post_payments is not assigned.')
    if type(total_amount) is int and total_amount >= 0:
        params.update({'total_amount': total_amount})
    else:
        raise Exception('total_amount is not assigned.')
    if post_discounts:
        params.update({'post_discounts': post_discounts})
    if time_range:
        params.update({'time_range': time_range})
    if location:
        params.update({'location': location})
    if goods_tag:
        params.update({'goods_tag': goods_tag})
    params.update({'profit_sharing': profit_sharing})
    params.update({'appid': appid or self._appid})
    return self._core.request(path, method=RequestType.POST, data=params)


def payscore_pay(self, out_order_no, service_id, appid=None):
    """商户发起催收扣款
    :param out_order_no: 商户服务订单号，商户系统内部服务订单号（不是交易单号），要求此参数只能由数字、大小写字母_-|*组成，且在同一个商户号下唯一。示例值:'1234323JKHDFE1243252'
    :param service_id: 服务ID，该服务ID有本接口对应产品的权限。示例值:'500001'
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    """
    params = {}
    if out_order_no:
        path = '/v3/payscore/serviceorder/%s/pay' % out_order_no
    else:
        raise Exception('out_order_no is not assigned.')
    if service_id:
        params.update({'service_id': service_id})
    else:
        raise Exception('service_id is not assigned.')
    params.update({'appid': appid or self._appid})
    return self._core.request(path, method=RequestType.POST, data=params)


def payscore_sync(self, out_order_no, service_id, scene_type='Order_Paid', detail={'paid_time': None}, appid=None):
    """同步服务订单信息
    :param out_order_no: 商户服务订单号，商户系统内部服务订单号（不是交易单号），要求此参数只能由数字、大小写字母_-|*组成，且在同一个商户号下唯一。示例值:'1234323JKHDFE1243252'
    :param service_id: 服务ID，该服务ID有本接口对应产品的权限。示例值:'500001'
    :param scene_type: 场景类型，场景类型为“Order_Paid”，表示“订单收款成功” 。示例值:'Order_Paid'
    :param detail: 内容信息详情，场景类型为Order_Paid时，为必填项。其中	paid_time表示收款成功时间，示例值:'20091225091210'
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    """
    params = {}
    if out_order_no:
        path = '/v3/payscore/serviceorder/%s/sync' % out_order_no
    else:
        raise Exception('out_order_no is not assigned.')
    if service_id:
        params.update({'service_id': service_id})
    else:
        raise Exception('service_id is not assigned.')
    if scene_type:
        params.update({'type': scene_type})
    else:
        raise Exception('scene_type is not assigned.')
    if detail:
        params.update({'detail': detail})
    else:
        raise Exception('detail is not assigned.')
    params.update({'appid': appid or self._appid})
    return self._core.request(path, method=RequestType.POST, data=params)


def payscore_refund(self, transaction_id, out_refund_no, amount, reason=None,
                    funds_account=None, goods_detail=None, notify_url=None):
    """申请退款
    :param transaction_id: 微信支付订单号，示例值:'1217752501201407033233368018'
    :param out_refund_no: 商户退款单号，示例值:'1217752501201407033233368018'
    :param amount: 金额信息，示例值:{'refund':888, 'total':888, 'currency':'CNY'}
    :param reason: 退款原因，示例值:'商品已售完'
    :param funds_account: 退款资金来源，示例值:'AVAILABLE'
    :param goods_detail: 退款商品，示例值:{'merchant_goods_id':'1217752501201407033233368018', 'wechatpay_goods_id':'1001', 'goods_name':'iPhone6s 16G', 'unit_price':528800, 'refund_amount':528800, 'refund_quantity':1}
    :param notify_url: 通知地址，示例值:'https://www.weixin.qq.com/wxpay/pay.php'
    """
    return refund(self, out_refund_no=out_refund_no, amount=amount, transaction_id=transaction_id, reason=reason,
                  funds_account=funds_account, goods_detail=goods_detail, notify_url=notify_url)


def payscore_refund_query(self, out_refund_no):
    """查询单笔退款
    :param out_refund_no: 商户退款单号，示例值:'1217752501201407033233368018'
    """
    return query_refund(self, out_refund_no=out_refund_no)


def payscore_merchant_bill(self, bill_date, service_id, tar_type='GZIP', encryption_algorithm='AEAD_AES_256_GCM'):
    """商户申请获取对账单
    :param bill_date: 账单日期，格式'YYYY-MM-DD'，仅支持下载近三个月的账单。示例值:'2021-01-01'
    :param service_id: 支付分服务ID。示例值:'2002000000000558128851361561536'
    :param tar_type: 账单的压缩类型，'GZIP':文件压缩方式为gzip，返回.gzip格式的压缩文件。示例值:'GZIP'
    :param encryption_algorithm: 加密算法，对返回账单原文加密的算法'AEAD_AES_256_GCM'，账单使用AEAD_AES_256_GCM加密算法进行加密。示例值:'AEAD_AES_256_GCM'
    """
    if bill_date:
        path = '/v3/payscore/merchant-bill?bill_date=%s' % bill_date
    else:
        raise Exception('bill_date is not assigned.')
    if service_id:
        path = '%s&service_id=%s' % (path, service_id)
    else:
        raise Exception('service_id is not assigned.')
    path = '%s&tar_type=%s' % (path, tar_type if tar_type else 'GZIP')
    path = '%s&encryption_algorithm=%s' % (path, encryption_algorithm if encryption_algorithm else 'AEAD_AES_256_GCM')
    return self._core.request(path)
