# -*- coding: utf-8 -*-
import json
from enum import Enum

from .core import Core


class WeChatPay():
    def __init__(self,
                 wechatpay_type,
                 mchid,
                 mch_parivate_key,
                 mch_key_serial_no,
                 appid,
                 notify_url=None,
                 wechat_public_key=None):
        """
        :param wechatpay_type: 微信支付类型，示例值：WeChatPayType.MINIPROG
        :param mchid: 直连商户号，示例值：'1230000109'
        :param mch_private_key: 商户证书私钥，示例值：'MIIEvwIBADANBgkqhkiG9w0BAQE...'
        :param mch_key_serial_no: 商户证书序列号，示例值：'444F4864EA9B34415...'
        :param appid: 应用ID，示例值：'wxd678efh567hg6787'
        :param notify_url: 通知地址，示例值：'https://www.weixin.qq.com/wxpay/pay.php'
        :param wechat_public_key：微信支付平台证书公钥，示例值：'MIIEvwIBADANBgkqhkiG9w0BAQE...'
        """
        self._type = wechatpay_type
        self._mchid = mchid
        self._appid = appid
        self._notify_url = notify_url
        self._core = Core(mchid=self._mchid,
                          mch_key_serial_no=mch_key_serial_no,
                          mch_private_key=mch_parivate_key,
                          wechat_public_key=wechat_public_key)

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
            notify_url=None):
        """统一下单
        :return code, message:
        :param description: 商品描述，示例值：'Image形象店-深圳腾大-QQ公仔'
        :param out_trade_no: 商户订单号，示例值：'1217752501201407033233368018'
        :param amount: 订单金额，示例值：{'total':100, 'currency':'CNY'}
        :param payer: 支付者，示例值：{'openid':'oHkLxtx0vUqe-18p_AXTZ1innxkCY'}
        :param time_expire: 交易结束时间，示例值：'2018-06-08T10:34:56+08:00'
        :param attach: 附加数据，示例值：'自定义数据'
        :param goods_tag: 订单优惠标记，示例值：'WXG'
        :param detail: 优惠功能，示例值：{'cost_price':608800, 'invoice_id':'微信123', 'goods_detail':[{'merchant_goods_id':'商品编码', 'wechatpay_goods_id':'1001', 'goods_name':'iPhoneX 256G', 'quantity':1, 'unit_price':828800}]}
        :param scene_info: 场景信息，示例值：{'payer_client_ip':'14.23.150.211', 'device_id':'013467007045764', 'store_info':{'id':'0001', 'name':'腾讯大厦分店', 'area_code':'440305', 'address':'广东省深圳市南山区科技中一道10000号'}}
        :param settle_info: 结算信息，示例值：{'profit_sharing':false}
        :param notify_url: 通知地址，示例值：'https://www.weixin.qq.com/wxpay/pay.php'
        """
        params = {}
        params['appid'] = self._appid
        params['mchid'] = self._mchid
        params['notify_url'] = notify_url or self._notify_url
        if description:
            params.update({'description': description})
        else:
            raise WeChatPayException('description is not assigned.')
        if out_trade_no:
            params.update({'out_trade_no': out_trade_no})
        else:
            raise WeChatPayException('out_trade_no is not assigned.')
        if amount:
            params.update({'amount': amount})
        else:
            raise WeChatPayException('amount is not assigned.')
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
        if self._type in [WeChatPayType.JSAPI, WeChatPayType.MINIPROG]:
            if payer:
                params.update({'payer': payer})
            else:
                raise WeChatPayException('payer is not assigned')
            path = '/v3/pay/transactions/jsapi'
        elif self._type == WeChatPayType.APP:
            path = '/v3/pay/transactions/app'
        elif self._type == WeChatPayType.H5:
            if not scene_info:
                raise WeChatPayException('scene_info is not assigned.')
            path = '/v3/pay/transactions/h5'
        elif self._type == WeChatPayType.NATIVE:
            path = '/v3/pay/transactions/native'
        self._core.post(path, json=json.dumps(params))

    def close(self, out_trade_no):
        """关闭订单
        :param out_trade_no: 商户订单号，示例值：'1217752501201407033233368018'
        """
        if not out_trade_no:
            raise WeChatPayException('out_trade_no is not assigned.')
        path = '/v3/pay/transactions/out-trade-no/%s/close' % out_trade_no
        params = {}
        params['mchid'] = self._mchid
        params['out_trade_no'] = out_trade_no
        return self._core.post(path, json=json.dumps(params))

    def query(self, transaction_id=None, out_trade_no=None):
        """查询订单
        :param transaction_id: 微信支付订单号，示例值：1217752501201407033233368018
        :param out_trade_no: 商户订单号，示例值：1217752501201407033233368018
        """
        if not (transaction_id or out_trade_no):
            raise WeChatPayException('params is not assigned')
        params = {}
        params['mchid'] = self._mchid
        if transaction_id:
            path = '/v3/pay/transactions/id/%s' % transaction_id
            params['transaction_id'] = transaction_id
        else:
            path = '/v3/pay/transactions/out-trade-no/%s' % out_trade_no
            params['out_trade_no'] = out_trade_no
        return self._core.get(path, json=json.dumps(params))

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
        if out_refund_no:
            params.update({'out_refund_no': out_refund_no})
        else:
            raise WeChatPayException('out_refund_no is not assigned.')
        if amount:
            params.update({'amount': amount})
        else:
            raise WeChatPayException('amount is not assigned.')
        if transaction_id:
            params.update({'transation_id': transaction_id})
        if out_trade_no:
            params.update({'out_trade_no': out_trade_no})
        if reason:
            params.update({'reason': reason})
        if funds_account:
            params.update({'funds_account': funds_account})
        if goods_detail:
            params.update({'goods_detail': goods_detail})
        path = '/v3/refund/domestic/refunds'
        return self._core.post(path, json=json.dumps(params))

    def query_refund(self, out_refund_no):
        """查询单笔退款
        :param out_refund_no: 商户退款单号，示例值：'1217752501201407033233368018'
        """
        path = '/v3/refund/domestic/refunds/%s' % out_refund_no
        return self._core.get(path)

    def trade_bill(self, bill_date, bill_type='ALL', tar_type='GZIP'):
        """申请交易账单
        :param bill_date: 账单日期，示例值：'2019-06-11'
        :param bill_type: 账单类型, 默认值：'ALL'
        :param tar_type: 压缩类型，默认值：'GZIP'
        """
        path = '/v3/bill/tradebill?bill_date=%s&bill_type=%s&tar_type=%s' % (
            bill_date, bill_type, tar_type)
        return self._core.get(path)

    def fundflow_bill(self, bill_date, account_type='BASIC', tar_type='GZIP'):
        """申请资金账单
        :param bill_date: 账单日期，示例值：'2019-06-11'
        :param account_type: 资金账户类型, 默认值：'BASIC'，基本账户, 可选：'OPERATION'，运营账户；'FEES'，手续费账户
        :param tar_type: 压缩类型，默认值：'GZIP'
        """
        path = '/v3/bill/fundflowbill?bill_date=%s&account_type=%s&tar_type=%s' % (
            bill_date, account_type, tar_type)
        return self._core.get(path)

    def download_bill(self, url):
        """下载账单
        :param url: 账单下载地址，示例值：'https://api.mch.weixin.qq.com/v3/billdownload/file?token=xxx'
        """
        path = url[len(self._core._gate_way):] if url.startswith(
            self._core._gate_way) else url
        return self._core.get(path)

    def certificate(self):
        path = '/v3/certificates'
        return self._core.get(path)


class WeChatPayException(Exception):
    def __init__(self, reason):
        self._reason = reason

    def __str__(self):
        return self._reason


class WeChatPayType(Enum):
    JSAPI = 0
    APP = 1
    H5 = 2
    NATIVE = 3
    MINIPROG = 4
