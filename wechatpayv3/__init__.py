# -*- coding: utf-8 -*-

from .type import SignType, WeChatPayType


class WeChatPay():
    def __init__(self,
                 wechatpay_type,
                 mchid,
                 private_key,
                 cert_serial_no,
                 appid,
                 apiv3_key,
                 notify_url=None,
                 cert_dir=None,
                 logger=None,
                 partner_mode=False,
                 proxy=None,
                 timeout=None,
                 public_key=None,
                 public_key_id=None):
        """
        :param wechatpay_type: 微信支付类型，示例值:WeChatPayType.MINIPROG
        :param mchid: 直连商户号，示例值:'1230000109'
        :param private_key: 商户证书私钥，示例值:'MIIEvwIBADANBgkqhkiG9w0BAQE...'
        :param cert_serial_no: 商户证书序列号，示例值:'444F4864EA9B34415...'
        :param appid: 应用ID，示例值:'wxd678efh567hg6787'
        :param apiv3_key: 商户APIv3密钥，示例值:'a12d3924fd499edac8a5efc...'
        :param notify_url: 通知地址，示例值:'https://www.weixin.qq.com/wxpay/pay.php'
        :param cert_dir: 平台证书存放目录，示例值:'/server/cert'
        :param logger: 日志记录器，示例值logging.getLoger('demo')
        :param partner_mode: 接入模式，默认False为直连商户模式，True为服务商模式
        :param proxy: 代理设置，示例值:{"https": "http://10.10.1.10:1080"}
        :param timeout: 超时时间，示例值：(10, 30), 10为建立连接的最大超时时间，30为读取响应的最大超时实践
        :param public_key: 微信支付平台公钥，示例值:'MIIEvwIBADANBgkqhkiG9w0BAQE...'
        :param public_key_id: 微信支付平台公钥id，示例值：'PUB_KEY_ID_444F4864EA9B34415...'
        """
        from .core import Core

        self._type = wechatpay_type
        self._mchid = mchid
        self._appid = appid
        self._notify_url = notify_url
        self._core = Core(mchid=self._mchid,
                          cert_serial_no=cert_serial_no,
                          private_key=private_key,
                          apiv3_key=apiv3_key,
                          cert_dir=cert_dir,
                          logger=logger,
                          proxy=proxy,
                          timeout=timeout,
                          public_key=public_key,
                          public_key_id=public_key_id)
        self._partner_mode = partner_mode

    def sign(self, data, sign_type=SignType.RSA_SHA256):
        """使用RSAwithSHA256或HMAC_256算法计算签名值供调起支付时使用
        :param data: 需要签名的参数清单
        :微信支付订单采用RSAwithSHA256算法时，示例值:['wx888','1414561699','5K8264ILTKCH16CQ2502S....','prepay_id=wx201410272009395522657....']
        :微信支付分订单采用HMAC_SHA256算法时，示例值:{'mch_id':'1230000109','service_id':'88888888000011','out_order_no':'1234323JKHDFE1243252'}
        """
        return self._core.sign(data, sign_type)

    def decrypt_callback(self, headers, body):
        """解密回调接口收到的信息，仅返回resource解密后的参数字符串，此接口为兼容旧版本而保留，建议调用callback()
        :param headers: 回调接口收到的headers
        :param body: 回调接口收到的body
        """
        return self._core.decrypt_callback(headers, body)

    def callback(self, headers, body):
        """解密回调接口收到的信息，返回所有传入的参数
        :param headers: 回调接口收到的headers
        :param body: 回调接口收到的body
        """
        return self._core.callback(headers, body)

    def decrypt(self, ciphtext):
        """解密微信支付平台返回的信息中的敏感字段
        :param ciphtext: 加密后的敏感字段，示例值:'Qe41VhP/sGdNeTHMQGlxCWiUyHu6XNO9GCYln2Luv4HhwJzZBfcL12sB+PgZcS5NhePBog30NgJ1xRaK+gbGDKwpg=='
        """
        return self._core.decrypt(ciphtext)

    from .apply4subject import (apply4subject_cancel, apply4subject_query,
                                apply4subject_state, apply4subject_submit)
    from .applyment import (applyment_query, applyment_settlement_modify,
                            applyment_settlement_query, applyment_submit)
    from .businesscircle import (business_parking_sync, business_point_status,
                                 points_notify, user_authorization)
    from .capital import (capital_branches, capital_cities,
                          capital_corporate_banks, capital_personal_banks,
                          capital_provinces, capital_search_bank_number)
    from .complaint import (complaint_complete, complaint_detail_query,
                            complaint_history_query, complaint_image_download,
                            complaint_image_upload, complaint_list_query,
                            complaint_notification_create,
                            complaint_notification_delete,
                            complaint_notification_query,
                            complaint_notification_update, complaint_response,
                            complaint_update_refund)
    from .fapiao import (fapiao_applications, fapiao_card_template,
                         fapiao_check_submch, fapiao_download_file,
                         fapiao_insert_cards, fapiao_merchant_base_info,
                         fapiao_merchant_config, fapiao_query,
                         fapiao_query_files, fapiao_reverse,
                         fapiao_set_merchant_config, fapiao_tax_codes,
                         fapiao_title, fapiao_title_url, fapiao_upload_file)
    from .goldplan import (goldplan_advertising_close,
                           goldplan_advertising_filter,
                           goldplan_advertising_open,
                           goldplan_custompage_change, goldplan_plan_change)
    from .marketing import (marketing_busifavor_callback_query,
                            marketing_busifavor_callback_update,
                            marketing_busifavor_coupon_associate,
                            marketing_busifavor_coupon_deactivate,
                            marketing_busifavor_coupon_detail,
                            marketing_busifavor_coupon_disassociate,
                            marketing_busifavor_coupon_return,
                            marketing_busifavor_coupon_use,
                            marketing_busifavor_couponcode_upload,
                            marketing_busifavor_stock_budget,
                            marketing_busifavor_stock_create,
                            marketing_busifavor_stock_modify,
                            marketing_busifavor_stock_query,
                            marketing_busifavor_subsidy_pay,
                            marketing_busifavor_subsidy_query,
                            marketing_busifavor_user_coupon,
                            marketing_card_send,
                            marketing_favor_callback_update,
                            marketing_favor_coupon_detail,
                            marketing_favor_refund_flow,
                            marketing_favor_stock_create,
                            marketing_favor_stock_detail,
                            marketing_favor_stock_item,
                            marketing_favor_stock_list,
                            marketing_favor_stock_merchant,
                            marketing_favor_stock_pause,
                            marketing_favor_stock_restart,
                            marketing_favor_stock_send,
                            marketing_favor_stock_start,
                            marketing_favor_use_flow,
                            marketing_favor_user_coupon,
                            marketing_image_upload,
                            marketing_partnership_build,
                            marketing_partnership_query,
                            marketing_paygift_activity_create,
                            marketing_paygift_activity_detail,
                            marketing_paygift_activity_list,
                            marketing_paygift_activity_terminate,
                            marketing_paygift_goods_list,
                            marketing_paygift_merchant_add,
                            marketing_paygift_merchant_delete,
                            marketing_paygift_merchants_list)
    from .media import image_upload, video_upload
    from .merchantrisk import (merchantrisk_callback_create,
                               merchantrisk_callback_delete,
                               merchantrisk_callback_query,
                               merchantrisk_callback_update)
    from .parking import (parking_enter, parking_order, parking_order_query,
                          parking_service_find)
    from .payscore import (payscore_cancel, payscore_complete, payscore_create,
                           payscore_direct_complete, payscore_merchant_bill,
                           payscore_modify, payscore_pay, payscore_permission,
                           payscore_permission_query,
                           payscore_permission_terminate, payscore_query,
                           payscore_refund, payscore_refund_query,
                           payscore_sync)
    from .profitsharing import (brand_profitsharing_add_receiver,
                                brand_profitsharing_amount_query,
                                brand_profitsharing_config_query,
                                brand_profitsharing_delete_receiver,
                                brand_profitsharing_order,
                                brand_profitsharing_order_query,
                                brand_profitsharing_return,
                                brand_profitsharing_return_query,
                                brand_profitsharing_unfreeze,
                                profitsharing_add_receiver,
                                profitsharing_amount_query, profitsharing_bill,
                                profitsharing_config_query,
                                profitsharing_delete_receiver,
                                profitsharing_order, profitsharing_order_query,
                                profitsharing_return,
                                profitsharing_return_query,
                                profitsharing_unfreeze)
    from .smartguide import (guides_assign, guides_query, guides_register,
                             guides_update)
    from .transaction import (abnormal_refund, close, codepay_reverse, combine_close,
                              combine_pay, combine_query, download_bill,
                              fundflow_bill, pay, query, query_refund, refund,
                              submch_fundflow_bill, trade_bill)
    from .transfer import (transfer_batch, transfer_bill_receipt,
                           transfer_detail_receipt, transfer_query_batchid,
                           transfer_query_bill_receipt,
                           transfer_query_detail_id,
                           transfer_query_out_batch_no,
                           transfer_query_out_detail_no,
                           transfer_query_receipt)
