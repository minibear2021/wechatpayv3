# -*- coding: utf-8 -*-
import json
from enum import Enum

from .core import Core, RequestType


class WeChatPay():
    def __init__(self,
                 wechatpay_type,
                 mchid,
                 parivate_key,
                 cert_serial_no,
                 appid,
                 apiv3_key,
                 notify_url=None,
                 cert_dir=None):
        """
        :param wechatpay_type: 微信支付类型，示例值：WeChatPayType.MINIPROG
        :param mchid: 直连商户号，示例值：'1230000109'
        :param mch_private_key: 商户证书私钥，示例值：'MIIEvwIBADANBgkqhkiG9w0BAQE...'
        :param mch_key_serial_no: 商户证书序列号，示例值：'444F4864EA9B34415...'
        :param appid: 应用ID，示例值：'wxd678efh567hg6787'
        :param mch_apiv3_key: 商户APIv3密钥，示例值：'a12d3924fd499edac8a5efc...'
        :param notify_url: 通知地址，示例值：'https://www.weixin.qq.com/wxpay/pay.php'
        :param cert_dir: 平台证书存放目录，示例值：'/server/cert'
        """
        self._type = wechatpay_type
        self._mchid = mchid
        self._appid = appid
        self._notify_url = notify_url
        self._core = Core(mchid=self._mchid,
                          cert_serial_no=cert_serial_no,
                          private_key=parivate_key,
                          apiv3_key=apiv3_key,
                          cert_dir=cert_dir)

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
        :param settle_info: 结算信息，示例值：{'profit_sharing':False}
        :param notify_url: 通知地址，示例值：'https://www.weixin.qq.com/wxpay/pay.php'
        """
        params = {}
        params['appid'] = self._appid
        params['mchid'] = self._mchid
        params['notify_url'] = notify_url or self._notify_url
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

    def close(self, out_trade_no):
        """关闭订单
        :param out_trade_no: 商户订单号，示例值：'1217752501201407033233368018'
        """
        if not out_trade_no:
            raise Exception('out_trade_no is not assigned.')
        path = '/v3/pay/transactions/out-trade-no/%s/close' % out_trade_no
        params = {'mchid': self._mchid}
        return self._core.request(path, method=RequestType.POST, data=params)

    def query(self, transaction_id=None, out_trade_no=None):
        """查询订单
        :param transaction_id: 微信支付订单号，示例值：1217752501201407033233368018
        :param out_trade_no: 商户订单号，示例值：1217752501201407033233368018
        """
        if not (transaction_id or out_trade_no):
            raise Exception('params is not assigned')
        if transaction_id:
            path = '/v3/pay/transactions/id/%s' % transaction_id
        else:
            path = '/v3/pay/transactions/out-trade-no/%s' % out_trade_no
        path = '%s?mchid=%s' % (path, self._mchid)
        return self._core.request(path)

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

    def query_refund(self, out_refund_no):
        """查询单笔退款
        :param out_refund_no: 商户退款单号，示例值：'1217752501201407033233368018'
        """
        path = '/v3/refund/domestic/refunds/%s' % out_refund_no
        return self._core.request(path)

    def trade_bill(self, bill_date, bill_type='ALL', tar_type='GZIP'):
        """申请交易账单
        :param bill_date: 账单日期，示例值：'2019-06-11'
        :param bill_type: 账单类型, 默认值：'ALL'
        :param tar_type: 压缩类型，默认值：'GZIP'
        """
        path = '/v3/bill/tradebill?bill_date=%s&bill_type=%s&tar_type=%s' % (bill_date, bill_type, tar_type)
        return self._core.request(path)

    def fundflow_bill(self, bill_date, account_type='BASIC', tar_type='GZIP'):
        """申请资金账单
        :param bill_date: 账单日期，示例值：'2019-06-11'
        :param account_type: 资金账户类型, 默认值：'BASIC'，基本账户, 可选：'OPERATION'，运营账户；'FEES'，手续费账户
        :param tar_type: 压缩类型，默认值：'GZIP'
        """
        path = '/v3/bill/fundflowbill?bill_date=%s&account_type=%s&tar_type=%s' % (bill_date, account_type, tar_type)
        return self._core.request(path)

    def download_bill(self, url):
        """下载账单
        :param url: 账单下载地址，示例值：'https://api.mch.weixin.qq.com/v3/billdownload/file?token=xxx'
        """
        path = url[len(self._core._gate_way):] if url.startswith(self._core._gate_way) else url
        return self._core.request(path)

    # def certificates(self):
    #     """下载微信支付平台证书
    #     """
    #     return self._core.certificates

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
        :param combine_out_trade_no: 合单商户订单号, 示例值：'P20150806125346'
        :param sub_orders: 子单信息，示例值：[{'mchid':'1900000109', 'attach':'深圳分店', 'amount':{'total_amount':100,'currency':'CNY'}, 'out_trade_no':'20150806125346', 'description':'腾讯充值中心-QQ会员充值', 'settle_info':{'profit_sharing':False, 'subsidy_amount':10}}]
        :param scene_info: 场景信息, 示例值：{'device_id':'POS1:123', 'payer_client_ip':'14.17.22.32'}
        :param combine_payer_info: 支付者, 示例值：{'openid':'oUpF8uMuAJO_M2pxb1Q9zNjWeS6o'}
        :param time_start: 交易起始时间，示例值：'2019-12-31T15:59:59+08:00'
        :param time_expire: 交易结束时间, 示例值：'2019-12-31T15:59:59+08:00'
        :param combine_appid: 合单商户appid, 示例值：'wxd678efh567hg6787'
        :param combine_mchid: 合单发起方商户号，示例值：'1900000109'
        :param notify_url: 通知地址, 示例值：'https://yourapp.com/notify'
        """
        params = {}
        params['combine_appid'] = combine_appid or self._appid
        params['combine_mchid'] = combine_mchid or self._mchid
        params['notify_url'] = notify_url or self._notify_url
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
        :param combine_out_trade_no: 合单商户订单号，示例值：P20150806125346
        """
        params = {}
        if not combine_out_trade_no:
            raise Exception('param combine_out_trade_no is not assigned')
        else:
            params.update({'combine_out_trade_no': combine_out_trade_no})
        path = '/v3/combine-transactions/out-trade-no/%s' % combine_out_trade_no
        return self._core.request(path)

    def combine_close(self, combine_out_trade_no, sub_orders, combine_appid=None):
        """合单关闭订单
        :param combine_out_trade_no: 合单商户订单号，示例值：'P20150806125346'
        :param sub_orders: 子单信息, 示例值：[{'mchid': '1900000109', 'out_trade_no': '20150806125346'}]
        :param combine_appid: 合单商户appid, 示例值：'wxd678efh567hg6787'
        """
        params = {}
        params['combine_appid'] = combine_appid or self._appid

        if not combine_out_trade_no:
            raise Exception('combine_out_trade_no is not assigned.')
        if not sub_orders:
            raise Exception('sub_orders is not assigned.')
        else:
            params.update({'sub_orders': sub_orders})
        path = '/v3/combine-transactions/out-trade-no/%s/close' % combine_out_trade_no
        return self._core.request(path, method=RequestType.POST, data=params)

    def sign(self, data):
        """计算签名值paySign，供JSAPI、APP、NATIVE调起支付时使用
        :param data: 需要签名的参数清单，示例值：['wx888','1414561699','5K8264ILTKCH16CQ2502S....','prepay_id=wx201410272009395522657....']
        """
        sign_str = '\n'.join(data) + '\n'
        return self._core.sign(sign_str)

    def decrypt_callback(self, headers, body):
        """解密回调接口收到的信息
        """
        return self._core.decrypt_callback(headers, body)

    def points_notify(self, transaction_id, openid, earn_points, increased_points, points_update_time, no_points_remarks=None, total_points=None):
        """智慧商圈积分同步
        :param transaction_id: 微信订单号，示例值：'1217752501201407033233368018'
        :param appid: 小程序appid，示例值：'wx1234567890abcdef'
        :param openid: 用户标识，示例值：'oWmnN4xxxxxxxxxxe92NHIGf1xd8'
        :param earn_points: 是否获得积分，示例值：True
        :param increased_points: 订单新增积分值，示例值：100
        :param points_update_time: 积分更新时间，示例值：'2020-05-20T13:29:35.120+08:00'
        :param no_points_remarks: 未获得积分的备注信息，示例值：'商品不参与积分活动'
        :param total_points: 顾客积分总额，示例值：888888        
        """
        if self._type != WeChatPayType.MINIPROG:
            raise Exception('points notify only supports wechat mini prog')
        params = {}
        params.update({'appid': self._appid})
        if transaction_id:
            params.update({'transaction_id': transaction_id})
        else:
            raise Exception('transaction_id is not assigned.')
        if openid:
            params.update({'openid': openid})
        else:
            raise Exception('openid is not assigned.')
        if earn_points:
            params.update({'earn_points': earn_points})
        else:
            raise Exception('earn_points is not assigned.')
        if increased_points:
            params.update({'increased_points': increased_points})
        else:
            raise Exception('increased_points is not assigned')
        if points_update_time:
            params.update({'points_update_time': points_update_time})
        else:
            raise Exception('points_update_time is not assigned.')
        if no_points_remarks:
            params.update({'no_points_remarks': no_points_remarks})
        if total_points:
            params.update({'total_points': total_points})
        path = '/v3/businesscircle/points/notify'
        return self._core.request(path, method=RequestType.POST, data=params)

    def user_authorizations(self, openid):
        """智慧商圈积分授权查询
        :param openid: 用户标识，示例值：'oWmnN4xxxxxxxxxxe92NHIGf1xd8'
        """
        if self._type != WeChatPayType.MINIPROG:
            raise Exception('points notify only supports wechat mini prog')
        if not openid:
            raise Exception('openid is not assigned.')
        path = '/v3/businesscircle/user-authorizations/%s?appid=%s' % (openid, self._mchid)
        return self._core.request(path)


class WeChatPayType(Enum):
    JSAPI = 0
    APP = 1
    H5 = 2
    NATIVE = 3
    MINIPROG = 4
