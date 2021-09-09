# -*- coding: utf-8 -*-

from .type import RequestType


def profitsharing_order(self, transaction_id, out_order_no, receivers, unfreeze_unsplit):
    """请求分账
    :param transaction_id: 微信支付订单号，示例值：'4208450740201411110007820472'
    :param out_order_no: 商户分账单号，只能是数字、大小写字母_-|*@，示例值：'P20150806125346'
    :param receivers: 分账接收方列表，最多可有50个分账接收方，示例值：{{'type':'MERCHANT_ID', 'account':'86693852', 'amount':888, 'description':'分给商户A'}}
    :param unfreeze_unsplit: 是否解冻剩余未分资金，示例值：True, False
    """
    params = {}
    if transaction_id:
        params.update({'transaction_id': transaction_id})
    else:
        raise Exception('transaction_id is not assigned')
    if out_order_no:
        params.update({'out_order_no': out_order_no})
    else:
        raise Exception('out_order_no is not assigned')
    if unfreeze_unsplit:
        params.update({'unfreeze_unsplit': unfreeze_unsplit})
    else:
        raise Exception('unfreeze_unsplit is not assigned')
    if receivers:
        params.update({'transaction_id': transaction_id})
    else:
        raise Exception('transaction_id is not assigned')
    path = '/v3/profitsharing/orders'
    return self._core.request(path, method=RequestType.POST, data=params)


def profitsharing_order_query(self, transaction_id, out_order_no):
    """查询分账结果
    :param transaction_id: 微信支付订单号，示例值：'4208450740201411110007820472'
    :param out_order_no: 商户分账单号，只能是数字、大小写字母_-|*@，示例值：'P20150806125346'
    """
    if not transaction_id:
        raise Exception('transaction_id is not assigned')
    if not out_order_no:
        raise Exception('out_order_no is not assigned')
    path = '/v3/profitsharing/orders/%s?transaction_id=%s' % (out_order_no, transaction_id)
    return self._core.request(path)


def profitsharing_return(self, order_id, out_order_no, out_return_no, return_mchid, amount, description):
    """请求分账回退
    :param order_id: 微信分账单号，与out_order_no参数二选一，示例值：'3008450740201411110007820472'
    :param out_order_no: 商户分账单号，只能是数字、大小写字母_-|*@，示例值：'P20150806125346'
    :param out_return_no: 商户回退单号，商户在自己后台生成的一个新的回退单号，在商户后台唯一，示例值：'R20190516001'
    :param return_mchid: 回退商户号，分账接口中的分账接收方商户号，示例值：'86693852'
    :param amount: 回退金额，单位为分，示例值：888
    :param description: 回退描述，分账回退的原因描述，示例值：'用户退款'
    """
    params = {}
    if not (order_id and out_order_no):
        raise Exception('order_id or out_order_no is not assigned')
    if order_id:
        params.update({'order_id': order_id})
    else:
        params.update({'out_order_no': out_order_no})
    if out_return_no:
        params.update({'out_return_no': out_return_no})
    else:
        raise Exception('out_return_no is not assigned')
    if return_mchid:
        params.update({'return_mchid': return_mchid})
    else:
        raise Exception('return_mchid is not assigned')
    if amount:
        params.update({'amount': amount})
    else:
        raise Exception('amount is not assigned')
    if description:
        params.update({'description': description})
    else:
        raise Exception('description is not assigned')
    path = '/v3/profitsharing/return-orders'
    return self._core.request(path, method=RequestType.POST, data=params)


def profitsharing_return_query(self, out_order_no, out_return_no):
    """查询分账回退结果
    :param out_order_no: 商户分账单号，只能是数字、大小写字母_-|*@，示例值：'P20150806125346'
    :param out_return_no: 商户回退单号，商户在自己后台生成的一个新的回退单号，在商户后台唯一，示例值：'R20190516001'
    """
    if not out_order_no:
        raise Exception('out_order_no is not assigned')
    if not out_return_no:
        raise Exception('out_return_no is not assigned')
    path = '/v3/profitsharing/return-orders/%s?&out_order_no=%s' % (out_return_no, out_order_no)
    return self._core.request(path)


def profitsharing_unfreeze(self, transaction_id, out_order_no, description):
    """解冻剩余资金
    :param transaction_id: 微信支付订单号，示例值：'4208450740201411110007820472'
    :param out_order_no: 商户分账单号，只能是数字、大小写字母_-|*@，示例值：'P20150806125346'
    :param description: 分账描述，分账的原因描述，分账账单中需要体现，示例值：'解冻全部剩余资金'
    """
    params = {}
    if transaction_id:
        params.update({'transaction_id': transaction_id})
    else:
        raise Exception('transaction_id is not assigned')
    if out_order_no:
        params.update({'out_order_no': out_order_no})
    else:
        raise Exception('out_order_no is not assigned')
    if description:
        params.update({'description': description})
    else:
        raise Exception('description is not assigned')
    path = '/v3/profitsharing/orders/unfreeze'
    return self._core.request(path, method=RequestType.POST, data=params)


def profitsharing_amount_query(self, transaction_id):
    """查询剩余待分金额
    :param transaction_id: 微信支付订单号，示例值：'4208450740201411110007820472'
    """
    if not transaction_id:
        raise Exception('transaction_id is not assigned')
    path = '/v3/profitsharing/transactions/%s/amounts' % transaction_id
    return self._core.request(path)


def profitsharing_add_receiver(self, account_type, account, relation_type, name=None, custom_relation=None):
    """添加分账接收方
    :param account_type: 分账接收方类型，枚举值：'MERCHANT_ID'：商户ID，'PERSONAL_OPENID'：个人openid
    :param account: 分账接收方账号，类型是'MERCHANT_ID'时，是商户号，类型是'PERSONAL_OPENID'时，是个人openid，示例值：'86693852'
    :param relation_type:与分账方的关系类型，枚举值：'STORE'：门店，'STAFF'：员工，'STORE_OWNER'：店主，
                            'PARTNER'：合作伙伴，'HEADQUARTER'：总部，'BRAND'：品牌方，'DISTRIBUTOR'：分销商，
                            'USER'：用户，'SUPPLIER'： 供应商，'CUSTOM'：自定义，示例值：'STORE'
    :param name: 分账个人接收方姓名，分账接收方类型是'MERCHANT_ID'时，是商户全称（必传），当商户是小微商户或个体户时，是开户人姓名，
                            分账接收方类型是'PERSONAL_OPENID'时，是个人姓名
    :param custom_relation: 自定义的分账关系，子商户与接收方具体的关系，本字段最多10个字。当字段'relation_type'的值为'CUSTOM'时，本字段必填;
                            当字段'relation_type'的值不为'CUSTOM'时，本字段无需填写。示例值：'代理商'                            
    """
    params = {}
    if account_type:
        params.update({'type': account_type})
    else:
        raise Exception('account_type is not assigned')
    if account:
        params.update({'account': account})
    else:
        raise Exception('account is not assigned')
    if relation_type:
        params.update({'relation_type': relation_type})
    else:
        raise Exception('relation_type is not assigned')
    if name:
        params.update({'name': self._core.encrypt(name)})
    if relation_type == 'CUSTOM':
        if custom_relation:
            params.update({'custom_relation': custom_relation})
        else:
            raise Exception('custom_relation is not assigned')
    path = '/v3/profitsharing/receivers/add'
    return self._core.request(path, method=RequestType.POST, data=params, cipher_data=True if name else False)


def profitsharing_delete_receiver(self, account_type, account):
    """删除分账接收方
    :param account_type: 分账接收方类型，枚举值：'MERCHANT_ID'：商户ID，'PERSONAL_OPENID'：个人openid
    :param account: 分账接收方账号，类型是'MERCHANT_ID'时，是商户号，类型是'PERSONAL_OPENID'时，是个人openid，示例值：'86693852'
    """
    params = {}
    if account_type:
        params.update({'type': account_type})
    else:
        raise Exception('account_type is not assigned')
    if account:
        params.update({'account': account})
    else:
        raise Exception('account is not assigned')
    path = '/v3/profitsharing/receivers/delete'
    return self._core.request(path, method=RequestType.POST, data=params)


def profitsharing_bill(self, bill_date, tar_type='GZIP'):
    """申请分账账单
    :param bill_date: 账单日期，格式'YYYY-MM-DD'，仅支持三个月内的账单下载申请。示例值：'2019-06-11'
    :param tar_type: 压缩类型，默认值：'GZIP'
    """
    path = '/v3/profitsharing/bills?bill_date=%s&tar_type=%s' % (bill_date, tar_type)
    return self._core.request(path)
