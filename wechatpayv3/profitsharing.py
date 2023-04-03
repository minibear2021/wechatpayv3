# -*- coding: utf-8 -*-

from .type import RequestType


def profitsharing_order(self, transaction_id, out_order_no, receivers, unfreeze_unsplit,
                        appid=None, sub_appid=None, sub_mchid=None):
    """请求分账
    :param transaction_id: 微信支付订单号，示例值:'4208450740201411110007820472'
    :param out_order_no: 商户分账单号，只能是数字、大小写字母_-|*@，示例值:'P20150806125346'
    :param receivers: 分账接收方列表，最多可有50个分账接收方，示例值:[{'type':'MERCHANT_ID', 'account':'86693852', 'amount':888, 'description':'分给商户A'}]
    :param unfreeze_unsplit: 是否解冻剩余未分资金，示例值:True, False
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    :param sub_appid: (服务商模式)子商户应用ID，示例值:'wxd678efh567hg6999'
    :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
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
    if isinstance(unfreeze_unsplit, bool):
        params.update({'unfreeze_unsplit': unfreeze_unsplit})
    else:
        raise Exception('unfreeze_unsplit is not assigned')
    if isinstance(receivers, list):
        params.update({'receivers': receivers})
    else:
        raise Exception('receivers is not assigned')
    cipher_data = False
    for receiver in params.get('receivers'):
        if receiver.get('name'):
            receiver['name'] = self._core.encrypt(receiver.get('name'))
            cipher_data = True
    params.update({'appid': appid or self._appid})
    if self._partner_mode:
        if sub_appid:
            params.update({'sub_appid': sub_appid})
        if sub_mchid:
            params.update({'sub_mchid': sub_mchid})
        else:
            raise Exception('sub_mchid is not assigned.')
    path = '/v3/profitsharing/orders'
    return self._core.request(path, method=RequestType.POST, data=params, cipher_data=cipher_data)


def profitsharing_order_query(self, transaction_id, out_order_no, sub_mchid=None):
    """查询分账结果
    :param transaction_id: 微信支付订单号，示例值:'4208450740201411110007820472'
    :param out_order_no: 商户分账单号，只能是数字、大小写字母_-|*@，示例值:'P20150806125346'
    :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
    """
    if transaction_id and out_order_no:
        path = '/v3/profitsharing/orders/%s?transaction_id=%s' % (out_order_no, transaction_id)
    else:
        raise Exception('transaction_id or out_order_no is not assigned.')
    if self._partner_mode:
        if sub_mchid:
            path = '%s&sub_mchid=%s' % (path, sub_mchid)
        else:
            raise Exception('sub_mchid is not assigned.')
    return self._core.request(path)


def profitsharing_return(self, out_return_no, return_mchid, amount, description,
                         order_id=None, out_order_no=None, sub_mchid=None):
    """请求分账回退
    :param out_return_no: 商户回退单号，商户在自己后台生成的一个新的回退单号，在商户后台唯一，示例值:'R20190516001'
    :param return_mchid: 回退商户号，分账接口中的分账接收方商户号，示例值:'86693852'
    :param amount: 回退金额，单位为分，示例值:888
    :param description: 回退描述，分账回退的原因描述，示例值:'用户退款'
    :param order_id: 微信分账单号，与out_order_no参数二选一，示例值:'3008450740201411110007820472'
    :param out_order_no: 商户分账单号，只能是数字、大小写字母_-|*@，示例值:'P20150806125346'
    :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
    """
    params = {}
    if order_id:
        params.update({'order_id': order_id})
    elif out_order_no:
        params.update({'out_order_no': out_order_no})
    else:
        raise Exception('order_id or out_order_no is not assigned.')
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
    if self._partner_mode:
        if sub_mchid:
            params.update({'sub_mchid': sub_mchid})
        else:
            raise Exception('sub_mchid is not assigned.')
    path = '/v3/profitsharing/return-orders'
    return self._core.request(path, method=RequestType.POST, data=params)


def profitsharing_return_query(self, out_order_no, out_return_no, sub_mchid=None):
    """查询分账回退结果
    :param out_order_no: 商户分账单号，只能是数字、大小写字母_-|*@，示例值:'P20150806125346'
    :param out_return_no: 商户回退单号，商户在自己后台生成的一个新的回退单号，在商户后台唯一，示例值:'R20190516001'
    :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
    """
    if out_order_no and out_return_no:
        path = '/v3/profitsharing/return-orders/%s?&out_order_no=%s' % (out_return_no, out_order_no)
    else:
        raise Exception('out_order_no or out_return_no is not assigned')
    if self._partner_mode:
        if sub_mchid:
            path = '%s&sub_mchid=%s' % (path, sub_mchid)
        else:
            raise Exception('sub_mchid is not assigned.')
    return self._core.request(path)


def profitsharing_unfreeze(self, transaction_id, out_order_no, description, sub_mchid=None):
    """解冻剩余资金
    :param transaction_id: 微信支付订单号，示例值:'4208450740201411110007820472'
    :param out_order_no: 商户分账单号，只能是数字、大小写字母_-|*@，示例值:'P20150806125346'
    :param description: 分账描述，分账的原因描述，分账账单中需要体现，示例值:'解冻全部剩余资金'
    :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
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
    if self._partner_mode:
        if sub_mchid:
            params.update({'sub_mchid': sub_mchid})
        else:
            raise Exception('sub_mchid is not assigned.')
    path = '/v3/profitsharing/orders/unfreeze'
    return self._core.request(path, method=RequestType.POST, data=params)


def profitsharing_amount_query(self, transaction_id):
    """查询剩余待分金额
    :param transaction_id: 微信支付订单号，示例值:'4208450740201411110007820472'
    """
    if transaction_id:
        path = '/v3/profitsharing/transactions/%s/amounts' % transaction_id
    else:
        raise Exception('transaction_id is not assigned')
    return self._core.request(path)


def profitsharing_config_query(self, sub_mchid):
    """查询最大分账比例
    :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
    """
    if sub_mchid:
        path = '/v3/profitsharing/merchant-configs/%s' % sub_mchid
    else:
        raise Exception('sub_mchid is not assigned')
    return self._core.request(path)


def profitsharing_add_receiver(self, account_type, account, relation_type, name=None,
                               custom_relation=None, appid=None, sub_appid=None, sub_mchid=None):
    """添加分账接收方
    :param account_type: 分账接收方类型，枚举值:'MERCHANT_ID':商户ID，'PERSONAL_OPENID':个人openid
    :param account: 分账接收方账号，类型是'MERCHANT_ID'时，是商户号，类型是'PERSONAL_OPENID'时，是个人openid，示例值:'86693852'
    :param relation_type:与分账方的关系类型，枚举值:'STORE':门店，'STAFF':员工，'STORE_OWNER':店主，
                            'PARTNER':合作伙伴，'HEADQUARTER':总部，'BRAND':品牌方，'DISTRIBUTOR':分销商，
                            'USER':用户，'SUPPLIER': 供应商，'CUSTOM':自定义，示例值:'STORE'
    :param name: 分账个人接收方姓名，分账接收方类型是'MERCHANT_ID'时，是商户全称（必传），当商户是小微商户或个体户时，是开户人姓名，
                            分账接收方类型是'PERSONAL_OPENID'时，是个人姓名
    :param custom_relation: 自定义的分账关系，子商户与接收方具体的关系，本字段最多10个字。当字段'relation_type'的值为'CUSTOM'时，本字段必填;
                            当字段'relation_type'的值不为'CUSTOM'时，本字段无需填写。示例值:'代理商'
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    :param sub_appid: (服务商模式)子商户应用ID，示例值:'wxd678efh567hg6999'
    :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
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
    cipher_data = False
    if name:
        params.update({'name': self._core.encrypt(name)})
        cipher_data = True
    if relation_type == 'CUSTOM':
        if custom_relation:
            params.update({'custom_relation': custom_relation})
        else:
            raise Exception('custom_relation is not assigned')
    params.update({'appid': appid or self._appid})
    if self._partner_mode:
        if sub_appid:
            params.update({'sub_appid': sub_appid})
        if sub_mchid:
            params.update({'sub_mchid': sub_mchid})
        else:
            raise Exception('sub_mchid is not assigned.')
    path = '/v3/profitsharing/receivers/add'
    return self._core.request(path, method=RequestType.POST, data=params, cipher_data=cipher_data)


def profitsharing_delete_receiver(self, account_type, account, appid=None, sub_appid=None, sub_mchid=None):
    """删除分账接收方
    :param account_type: 分账接收方类型，枚举值:'MERCHANT_ID':商户ID，'PERSONAL_OPENID':个人openid
    :param account: 分账接收方账号，类型是'MERCHANT_ID'时，是商户号，类型是'PERSONAL_OPENID'时，是个人openid，示例值:'86693852'
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    :param sub_appid: (服务商模式)子商户应用ID，示例值:'wxd678efh567hg6999'
    :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
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
    params.update({'appid': appid or self._appid})
    if self._partner_mode:
        if sub_appid:
            params.update({'sub_appid': sub_appid})
        if sub_mchid:
            params.update({'sub_mchid': sub_mchid})
        else:
            raise Exception('sub_mchid is not assigned.')
    path = '/v3/profitsharing/receivers/delete'
    return self._core.request(path, method=RequestType.POST, data=params)


def profitsharing_bill(self, bill_date, tar_type='GZIP', sub_mchid=None):
    """申请分账账单
    :param bill_date: 账单日期，格式'YYYY-MM-DD'，仅支持三个月内的账单下载申请。示例值:'2019-06-11'
    :param tar_type: 压缩类型，默认值:'GZIP'
    :param sub_mchid: (服务商模式)子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
    """
    path = '/v3/profitsharing/bills?bill_date=%s&tar_type=%s' % (bill_date, tar_type)
    if self._partner_mode and sub_mchid:
        path = '%s&sub_mchid=%s' % (path, sub_mchid)
    return self._core.request(path)


def brand_profitsharing_order(self, brand_mchid, sub_mchid, transaction_id, out_order_no, receivers,
                              finish, appid=None, sub_appid=None):
    """连锁品牌请求分账
    :param brand_mchid: 品牌主商户号，示例值:'1900000108'
    :param sub_mchid: 子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
    :param transaction_id: 微信支付订单号，示例值:'4208450740201411110007820472'
    :param out_order_no: 商户分账单号，只能是数字、大小写字母_-|*@，示例值:'P20150806125346'
    :param receivers: 分账接收方列表，最多可有50个分账接收方，示例值:{{'type':'MERCHANT_ID', 'account':'86693852', 'amount':888, 'description':'分给商户A'}}
    :param finish: 是否完成分账，示例值:True, False
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    :param sub_appid: 子商户应用ID，示例值:'wxd678efh567hg6999'
    """
    params = {}
    if brand_mchid:
        params.update({'brand_mchid': brand_mchid})
    else:
        raise Exception('brand_mchid is not assigned')
    if sub_mchid:
        params.update({'sub_mchid': sub_mchid})
    else:
        raise Exception('sub_mchid is not assigned.')
    if transaction_id:
        params.update({'transaction_id': transaction_id})
    else:
        raise Exception('transaction_id is not assigned')
    if out_order_no:
        params.update({'out_order_no': out_order_no})
    else:
        raise Exception('out_order_no is not assigned')
    if receivers:
        params.update({'receivers': receivers})
    else:
        raise Exception('receivers is not assigned')
    if isinstance(finish, bool):
        params.update({'finish': finish})
    else:
        raise Exception('finish is not assigned')
    params.update({'appid': appid or self._appid})
    if sub_appid:
        params.update({'sub_appid': sub_appid})
    path = '/v3/brand/profitsharing/orders'
    return self._core.request(path, method=RequestType.POST, data=params)


def brand_profitsharing_order_query(self, transaction_id, out_order_no, sub_mchid):
    """查询连锁品牌分账结果
    :param transaction_id: 微信支付订单号，示例值:'4208450740201411110007820472'
    :param out_order_no: 商户分账单号，只能是数字、大小写字母_-|*@，示例值:'P20150806125346'
    :param sub_mchid: 子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
    """
    if sub_mchid:
        path = '/v3/brand/profitsharing/orders?sub_mchid=%s' % sub_mchid
    else:
        raise Exception('sub_mchid is not assigned.')
    if transaction_id and out_order_no:
        path = '%s&transaction_id=%s&out_order_no=%s' % (path, transaction_id, out_order_no)
    else:
        raise Exception('transaction_id or out_order_no is not assigned.')
    return self._core.request(path)


def brand_profitsharing_return(self, sub_mchid, out_return_no, return_mchid, amount,
                               description, order_id=None, out_order_no=None,):
    """请求连锁品牌分账回退
    :param sub_mchid: 子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
    :param out_return_no: 商户回退单号，商户在自己后台生成的一个新的回退单号，在商户后台唯一，示例值:'R20190516001'
    :param return_mchid: 回退商户号，分账接口中的分账接收方商户号，示例值:'86693852'
    :param amount: 回退金额，单位为分，示例值:888
    :param description: 回退描述，分账回退的原因描述，示例值:'用户退款'
    :param order_id: 微信分账单号，与out_order_no参数二选一，示例值:'3008450740201411110007820472'
    :param out_order_no: 商户分账单号，只能是数字、大小写字母_-|*@，示例值:'P20150806125346'
    """
    params = {}
    if not (order_id and out_order_no):
        raise Exception('order_id or out_order_no is not assigned')
    if order_id:
        params.update({'order_id': order_id})
    elif out_order_no:
        params.update({'out_order_no': out_order_no})
    else:
        raise Exception('order_id or out_order_no is not assigned.')
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
    if sub_mchid:
        params.update({'sub_mchid': sub_mchid})
    else:
        raise Exception('sub_mchid is not assigned.')
    path = '/v3/brand/profitsharing/returnorders'
    return self._core.request(path, method=RequestType.POST, data=params)


def brand_profitsharing_return_query(self, sub_mchid, out_return_no, order_id=None, out_order_no=None):
    """查询连锁品牌分账回退结果
    :param sub_mchid: 子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
    :param out_return_no: 商户回退单号，商户在自己后台生成的一个新的回退单号，在商户后台唯一，示例值:'R20190516001'
    :param order_id: 微信分账单号，与out_order_no参数二选一，示例值:'3008450740201411110007820472'
    :param out_order_no: 商户分账单号，只能是数字、大小写字母_-|*@，示例值:'P20150806125346'
    """
    if sub_mchid:
        path = '/v3/brand/profitsharing/returnorders?sub_mchid=%s' % sub_mchid
    else:
        raise Exception('sub_mchid is not assigned.')
    if out_return_no:
        path = '%s&out_return_no=%s' % (path, out_return_no)
    else:
        raise Exception('out_return_no is not assigned')
    if order_id:
        path = '%s&order_id=%s' % (path, order_id)
    elif out_order_no:
        path = '%s&out_order_no=%s' % (path, out_order_no)
    else:
        raise Exception('order_id or out_order_no is not assigned.')
    return self._core.request(path)


def brand_profitsharing_unfreeze(self, sub_mchid, transaction_id, out_order_no, description):
    """完结连锁品牌分账
    :param sub_mchid: 子商户的商户号，由微信支付生成并下发。示例值:'1900000109'
    :param transaction_id: 微信支付订单号，示例值:'4208450740201411110007820472'
    :param out_order_no: 商户分账单号，只能是数字、大小写字母_-|*@，示例值:'P20150806125346'
    :param description: 分账描述，分账的原因描述，分账账单中需要体现，示例值:'解冻全部剩余资金'
    """
    params = {}
    if sub_mchid:
        params.update({'sub_mchid': sub_mchid})
    else:
        raise Exception('sub_mchid is not assigned.')
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
    path = '/v3/brand/profitsharing/finish-order'
    return self._core.request(path, method=RequestType.POST, data=params)


def brand_profitsharing_amount_query(self, transaction_id):
    """查询连锁品牌分账剩余待分金额
    :param transaction_id: 微信支付订单号，示例值:'4208450740201411110007820472'
    """
    if transaction_id:
        path = '/v3/brand/profitsharing/orders/%s/amounts' % transaction_id
    else:
        raise Exception('transaction_id is not assigned')
    return self._core.request(path)


def brand_profitsharing_config_query(self, brand_mchid):
    """查询连锁品牌分账最大分账比例
    :param brand_mchid: 品牌商户号，示例值:'1900000108'
    """
    if brand_mchid:
        path = '/v3/brand/profitsharing/brand-configs/%s' % brand_mchid
    else:
        raise Exception('brand_mchid is not assigned')
    return self._core.request(path)


def brand_profitsharing_add_receiver(self, brand_mchid, account_type, account, relation_type,
                                     name=None, appid=None, sub_appid=None):
    """添加分账接收方
    :param brand_mchid: 品牌商户号，示例值:'1900000108'
    :param account_type: 分账接收方类型，枚举值:'MERCHANT_ID':商户ID，'PERSONAL_OPENID':个人openid
    :param account: 分账接收方账号，类型是'MERCHANT_ID'时，是商户号，类型是'PERSONAL_OPENID'时，是个人openid，示例值:'86693852'
    :param relation_type:与分账方的关系类型，枚举值:'STORE':门店，'STAFF':员工，'STORE_OWNER':店主，
                            'PARTNER':合作伙伴，'HEADQUARTER':总部，'BRAND':品牌方，'DISTRIBUTOR':分销商，
                            'USER':用户，'SUPPLIER': 供应商，'CUSTOM':自定义，示例值:'STORE'
    :param name: 分账个人接收方姓名，分账接收方类型是'MERCHANT_ID'时，是商户全称（必传），当商户是小微商户或个体户时，是开户人姓名，
                            分账接收方类型是'PERSONAL_OPENID'时，是个人姓名
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    :param sub_appid: 子商户应用ID，示例值:'wxd678efh567hg6999'
    """
    params = {}
    if brand_mchid:
        params.update({'brand_mchid': brand_mchid})
    else:
        raise Exception('brand_mchid is not assigned.')
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
    cipher_data = False
    if name:
        params.update({'name': self._core.encrypt(name)})
        cipher_data = True
    params.update({'appid': appid or self._appid})
    if sub_appid:
        params.update({'sub_appid': sub_appid})
    path = '/v3/brand/profitsharing/receivers/add'
    return self._core.request(path, method=RequestType.POST, data=params, cipher_data=cipher_data)


def brand_profitsharing_delete_receiver(self, brand_mchid, account_type, account, appid=None, sub_appid=None):
    """删除连锁品牌分账接收方
    :param brand_mchid: 品牌商户号，示例值:'1900000108'
    :param account_type: 分账接收方类型，枚举值:'MERCHANT_ID':商户ID，'PERSONAL_OPENID':个人openid
    :param account: 分账接收方账号，类型是'MERCHANT_ID'时，是商户号，类型是'PERSONAL_OPENID'时，是个人openid，示例值:'86693852'
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    :param sub_appid: (服务商模式)子商户应用ID，示例值:'wxd678efh567hg6999'
    """
    params = {}
    if brand_mchid:
        params.update({'brand_mchid': brand_mchid})
    else:
        raise Exception('brand_mchid is not assigned.')
    if account_type:
        params.update({'type': account_type})
    else:
        raise Exception('account_type is not assigned')
    if account:
        params.update({'account': account})
    else:
        raise Exception('account is not assigned')
    params.update({'appid': appid or self._appid})
    if sub_appid:
        params.update({'sub_appid': sub_appid})
    path = '/v3/profitsharing/receivers/delete'
    return self._core.request(path, method=RequestType.POST, data=params)
