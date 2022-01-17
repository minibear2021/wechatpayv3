# -*- coding: utf-8 -*-

from .type import RequestType, WeChatPayType


def pay(self,
        description,
        out_trade_no,
        amount,
        payer=None,
        time_expire=None,
        attach=None,
        goods_tag=None,
        detail=None,
        scene_info=None,
        settle_info=None,
        notify_url=None,
        appid=None,
        mchid=None,
        sub_appid=None,
        sub_mchid=None):
    """统一下单
    :return code, message:
    :param description: 商品描述，示例值:'Image形象店-深圳腾大-QQ公仔'
    :param out_trade_no: 商户订单号，示例值:'1217752501201407033233368018'
    :param amount: 订单金额，示例值:{'total':100, 'currency':'CNY'}
    :param payer: 支付者，示例值:{'openid':'oHkLxtx0vUqe-18p_AXTZ1innxkCY'}
    :param time_expire: 交易结束时间，示例值:'2018-06-08T10:34:56+08:00'
    :param attach: 附加数据，示例值:'自定义数据'
    :param goods_tag: 订单优惠标记，示例值:'WXG'
    :param detail: 优惠功能，示例值:{'cost_price':608800, 'invoice_id':'微信123', 'goods_detail':[{'merchant_goods_id':'商品编码', 'wechatpay_goods_id':'1001', 'goods_name':'iPhoneX 256G', 'quantity':1, 'unit_price':828800}]}
    :param scene_info: 场景信息，示例值:{'payer_client_ip':'14.23.150.211', 'device_id':'013467007045764', 'store_info':{'id':'0001', 'name':'腾讯大厦分店', 'area_code':'440305', 'address':'广东省深圳市南山区科技中一道10000号'}}
    :param settle_info: 结算信息，示例值:{'profit_sharing':False}
    :param notify_url: 通知地址，示例值:'https://www.weixin.qq.com/wxpay/pay.php'
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    :param mchid: 微信支付商户号，可不填，默认传入初始化的mchid，示例值:'987654321'
    :param sub_appid: (服务商模式)子商户应用ID，示例值:'wxd678efh567hg6999'
    :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
    """
    params = {}
    if not (notify_url or self._notify_url):
        raise Exception('notify_url is not assigned.')
    params.update({'notify_url': notify_url or self._notify_url})
    if description:
        params.update({'description': description})
    else:
        raise Exception('description is not assigned.')
    if out_trade_no:
        params.update({'out_trade_no': out_trade_no})
    else:
        raise Exception('out_trade_no is not assigned.')
    if amount:
        params.update({'amount': amount})
    else:
        raise Exception('amount is not assigned.')
    if payer:
        params.update({'payer': payer})
    if scene_info:
        params.update({'scene_info': scene_info})
    if time_expire:
        params.update({'time_expire': time_expire})
    if attach:
        params.update({'attach': attach})
    if goods_tag:
        params.update({'goods_tag': goods_tag})
    if detail:
        params.update({'detail': detail})
    if settle_info:
        params.update({'settle_info': settle_info})
    if self._partner_mode:
        params.update({'sp_appid': appid or self._appid})
        params.update({'sp_mchid': mchid or self._mchid})
        if sub_mchid:
            params.update({'sub_mchid': sub_mchid})
        else:
            raise Exception('sub_mchid is not assigned.')
        if sub_appid:
            params.update({'sub_appid': sub_appid})
        if self._type in [WeChatPayType.JSAPI, WeChatPayType.MINIPROG]:
            if not payer:
                raise Exception('payer is not assigned')
            path = '/v3/pay/partner/transactions/jsapi'
        elif self._type == WeChatPayType.APP:
            path = '/v3/pay/partner/transactions/app'
        elif self._type == WeChatPayType.H5:
            if not scene_info:
                raise Exception('scene_info is not assigned.')
            path = '/v3/pay/partner/transactions/h5'
        elif self._type == WeChatPayType.NATIVE:
            path = '/v3/pay/partner/transactions/native'
    else:
        params.update({'appid': appid or self._appid})
        params.update({'mchid': mchid or self._mchid})
        if self._type in [WeChatPayType.JSAPI, WeChatPayType.MINIPROG]:
            if not payer:
                raise Exception('payer is not assigned')
            path = '/v3/pay/transactions/jsapi'
        elif self._type == WeChatPayType.APP:
            path = '/v3/pay/transactions/app'
        elif self._type == WeChatPayType.H5:
            if not scene_info:
                raise Exception('scene_info is not assigned.')
            path = '/v3/pay/transactions/h5'
        elif self._type == WeChatPayType.NATIVE:
            path = '/v3/pay/transactions/native'
    return self._core.request(path, method=RequestType.POST, data=params)


def close(self, out_trade_no, mchid=None, sub_mchid=None):
    """关闭订单
    :param out_trade_no: 商户订单号，示例值:'1217752501201407033233368018'
    :param mchid: 微信支付商户号，可不传，默认传入初始化的mchid。示例值:'987654321'
    :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
    """
    if self._partner_mode:
        if out_trade_no:
            path = '/v3/pay/partner/transactions/out-trade-no/%s/close' % out_trade_no
        else:
            raise Exception('out_trade_no is not assigned.')
        if sub_mchid:
            params = {'sp_mchid': mchid or self._mchid, 'sub_mchid': sub_mchid}
        else:
            raise Exception('sub_mchid is not assigned.')
    else:
        if out_trade_no:
            path = '/v3/pay/transactions/out-trade-no/%s/close' % out_trade_no
        else:
            raise Exception('out_trade_no is not assigned.')
        params = {'mchid': mchid or self._mchid}
    return self._core.request(path, method=RequestType.POST, data=params)


def query(self, transaction_id=None, out_trade_no=None, mchid=None, sub_mchid=None):
    """查询订单
    :param transaction_id: 微信支付订单号，示例值:1217752501201407033233368018
    :param out_trade_no: 商户订单号，示例值:1217752501201407033233368018
    :param mchid: 微信支付商户号，可不传，默认传入初始化的mchid。示例值:'987654321'    
    :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
    """
    if self._partner_mode:
        if transaction_id:
            path = '/v3/pay/partner/transactions/id/%s' % transaction_id
        elif out_trade_no:
            path = '/v3/pay/partner/transactions/out-trade-no/%s' % out_trade_no
        else:
            raise Exception('transaction_id or out_trade_no is not assigned.')
        path = '%s?sp_mchid=%s&sub_mchid=%s' % (path, mchid or self._mchid, sub_mchid)
    else:
        if transaction_id:
            path = '/v3/pay/transactions/id/%s' % transaction_id
        elif out_trade_no:
            path = '/v3/pay/transactions/out-trade-no/%s' % out_trade_no
        else:
            raise Exception('transaction_id out_trade_no is not assigned.')
        path = '%s?mchid=%s' % (path, mchid or self._mchid)
    return self._core.request(path)


def refund(self,
           out_refund_no,
           amount,
           transaction_id=None,
           out_trade_no=None,
           reason=None,
           funds_account=None,
           goods_detail=None,
           notify_url=None,
           sub_mchid=None):
    """申请退款
    :param out_refund_no: 商户退款单号，示例值:'1217752501201407033233368018'
    :param amount: 金额信息，示例值:{'refund':888, 'total':888, 'currency':'CNY'}
    :param transaction_id: 微信支付订单号，示例值:'1217752501201407033233368018'
    :param out_trade_no: 商户订单号，示例值:'1217752501201407033233368018'
    :param reason: 退款原因，示例值:'商品已售完'
    :param funds_account: 退款资金来源，示例值:'AVAILABLE'
    :param goods_detail: 退款商品，示例值:{'merchant_goods_id':'1217752501201407033233368018', 'wechatpay_goods_id':'1001', 'goods_name':'iPhone6s 16G', 'unit_price':528800, 'refund_amount':528800, 'refund_quantity':1}
    :param notify_url: 通知地址，示例值:'https://www.weixin.qq.com/wxpay/pay.php'
    :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
    """
    params = {}
    if notify_url or self._notify_url:
        params.update({'notify_url': notify_url or self._notify_url})
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
    elif out_trade_no:
        params.update({'out_trade_no': out_trade_no})
    else:
        raise Exception('transaction_id is not assigned.')
    if reason:
        params.update({'reason': reason})
    if funds_account:
        params.update({'funds_account': funds_account})
    if goods_detail:
        params.update({'goods_detail': goods_detail})
    if self._partner_mode:
        if sub_mchid:
            params.update({'sub_mchid': sub_mchid})
        else:
            raise Exception('sub_mchid is not assigned.')
    path = '/v3/refund/domestic/refunds'
    return self._core.request(path, method=RequestType.POST, data=params)


def query_refund(self, out_refund_no, sub_mchid=None):
    """查询单笔退款
    :param out_refund_no: 商户退款单号，示例值:'1217752501201407033233368018'
    :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'    
    """
    path = '/v3/refund/domestic/refunds/%s' % out_refund_no
    if self._partner_mode:
        if sub_mchid:
            path = '%s?sub_mchid=%s' % (path, sub_mchid)
        else:
            raise Exception('sub_mchid is not assigned.')
    return self._core.request(path)


def trade_bill(self, bill_date, bill_type='ALL', tar_type='GZIP', sub_mchid=None):
    """申请交易账单
    :param bill_date: 账单日期，示例值:'2019-06-11'
    :param bill_type: 账单类型, 默认值:'ALL'
    :param tar_type: 压缩类型，默认值:'GZIP'
    :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109' 
    """
    path = '/v3/bill/tradebill?bill_date=%s&bill_type=%s&tar_type=%s' % (bill_date, bill_type, tar_type)
    if self._partner_mode and sub_mchid:
        path = '%s&sub_mchid=%s' % (path, sub_mchid)
    return self._core.request(path)


def fundflow_bill(self, bill_date, account_type='BASIC', tar_type='GZIP'):
    """申请资金账单
    :param bill_date: 账单日期，示例值:'2019-06-11'
    :param account_type: 资金账户类型, 默认值:'BASIC'，基本账户, 可选:'OPERATION'，运营账户；'FEES'，手续费账户
    :param tar_type: 压缩类型，默认值:'GZIP'
    """
    path = '/v3/bill/fundflowbill?bill_date=%s&account_type=%s&tar_type=%s' % (bill_date, account_type, tar_type)
    return self._core.request(path)


def submch_fundflow_bill(self, sub_mchid, bill_date, account_type, algorithm='AEAD_AES_256_GCM', tar_type=None):
    """申请单个子商户资金账单
    :param sub_mchid: 子商户号，示例值:'19000000001'
    :param bill_date: 账单日期，格式YYYY-MM-DD，示例值:'2019-06-11'
    :param account_type: 资金账户类型，枚举值:'BASIC':基本账户，'OPERATION':运营账户，'FEES':手续费账户，示例值:'BASIC'
    :param algorithm: 加密算法，枚举值:'AEAD_AES_256_GCM':AEAD_AES_256_GCM加密算法
    :param tar_type: 压缩格式，枚举值:'GZIP':返回格式为.gzip的压缩包账单
    """
    params = {}
    if sub_mchid:
        params.update({'sub_mchid': sub_mchid})
    else:
        raise Exception('sub_mchid is not assigned.')
    if bill_date:
        params.update({'bill_date': bill_date})
    else:
        raise Exception('bill_date is not assigned.')
    if account_type:
        params.update({'account_type': account_type})
    else:
        raise Exception('account_type is not assigned.')
    if algorithm:
        params.update({'algorithm': algorithm})
    else:
        raise Exception('algorithm is not assigned.')
    if tar_type:
        params.update({'tar_type': tar_type})
    path = '/v3/bill/sub-merchant-fundflowbill'
    return self._core.request(path)


def download_bill(self, url):
    """下载账单
    :param url: 账单下载地址，示例值:'https://api.mch.weixin.qq.com/v3/billdownload/file?token=xxx'
    """
    path = url[len(self._core._gate_way):] if url.startswith(self._core._gate_way) else url
    return self._core.request(path, skip_verify=True)


def combine_pay(self,
                combine_out_trade_no,
                sub_orders,
                scene_info=None,
                combine_payer_info=None,
                time_start=None,
                time_expire=None,
                combine_appid=None,
                combine_mchid=None,
                notify_url=None):
    """合单支付下单
    :param combine_out_trade_no: 合单商户订单号, 示例值:'P20150806125346'
    :param sub_orders: 子单信息，示例值:[{'mchid':'1900000109', 'attach':'深圳分店', 'amount':{'total_amount':100,'currency':'CNY'}, 'out_trade_no':'20150806125346', 'description':'腾讯充值中心-QQ会员充值', 'settle_info':{'profit_sharing':False, 'subsidy_amount':10}}]
    :param scene_info: 场景信息, 示例值:{'device_id':'POS1:123', 'payer_client_ip':'14.17.22.32'}
    :param combine_payer_info: 支付者, 示例值:{'openid':'oUpF8uMuAJO_M2pxb1Q9zNjWeS6o'}
    :param time_start: 交易起始时间，示例值:'2019-12-31T15:59:59+08:00'
    :param time_expire: 交易结束时间, 示例值:'2019-12-31T15:59:59+08:00'
    :param combine_appid: 合单商户appid, 示例值:'wxd678efh567hg6787'
    :param combine_mchid: 合单发起方商户号，示例值:'1900000109'
    :param notify_url: 通知地址, 示例值:'https://yourapp.com/notify'
    """
    params = {}
    params.update({'combine_appid': combine_appid or self._appid})
    params.update({'combine_mchid': combine_mchid or self._mchid})
    if not (notify_url or self._notify_url):
        raise Exception('notify_url is not assigned.')
    params.update({'notify_url': notify_url or self._notify_url})
    if combine_out_trade_no:
        params.update({'combine_out_trade_no': combine_out_trade_no})
    else:
        raise Exception('combine_out_trade_no is not assigned.')
    if sub_orders:
        params.update({'sub_orders': sub_orders})
    else:
        raise Exception('sub_orders is not assigned.')
    if scene_info:
        params.update({'scene_info': scene_info})
    if combine_payer_info:
        params.update({'combine_payer_info': combine_payer_info})
    if time_start:
        params.update({'time_start': time_start})
    if time_expire:
        params.update({'time_expire': time_expire})
    if self._type in [WeChatPayType.JSAPI, WeChatPayType.MINIPROG]:
        if not combine_payer_info:
            raise Exception('combine_payer_info is not assigned')
        path = '/v3/combine-transactions/jsapi'
    elif self._type == WeChatPayType.APP:
        path = '/v3/combine-transactions/app'
    elif self._type == WeChatPayType.H5:
        if not scene_info:
            raise Exception('scene_info is not assigned.')
        path = '/v3/combine-transactions/h5'
    elif self._type == WeChatPayType.NATIVE:
        path = '/v3/combine-transactions/native'
    return self._core.request(path, method=RequestType.POST, data=params)


def combine_query(self, combine_out_trade_no):
    """合单查询订单
    :param combine_out_trade_no: 合单商户订单号，示例值:P20150806125346
    """
    params = {}
    if not combine_out_trade_no:
        raise Exception('combine_out_trade_no is not assigned')
    else:
        params.update({'combine_out_trade_no': combine_out_trade_no})
    path = '/v3/combine-transactions/out-trade-no/%s' % combine_out_trade_no
    return self._core.request(path)


def combine_close(self, combine_out_trade_no, sub_orders, combine_appid=None):
    """合单关闭订单
    :param combine_out_trade_no: 合单商户订单号，示例值:'P20150806125346'
    :param sub_orders: 子单信息, 示例值:[{'mchid': '1900000109', 'out_trade_no': '20150806125346'}]
    :param combine_appid: 合单商户appid, 示例值:'wxd678efh567hg6787'
    """
    params = {}
    params.update({'combine_appid': combine_appid or self._appid})
    if not combine_out_trade_no:
        raise Exception('combine_out_trade_no is not assigned.')
    if not sub_orders:
        raise Exception('sub_orders is not assigned.')
    else:
        params.update({'sub_orders': sub_orders})
    path = '/v3/combine-transactions/out-trade-no/%s/close' % combine_out_trade_no
    return self._core.request(path, method=RequestType.POST, data=params)
