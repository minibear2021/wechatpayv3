# -*- coding: utf-8 -*-

from .type import RequestType


def transfer_batch(self, out_batch_no, batch_name, batch_remark, total_amount, total_num, transfer_detail_list=[], appid=None, transfer_scene_id=None, notify_url=None):
    """发起商家转账
    :param out_batch_no: 商户系统内部的商家批次单号，要求此参数只能由数字、大小写字母组成，在商户系统内部唯一，示例值：'plfk2020042013'
    :param batch_name: 该笔批量转账的名称，示例值：'2019年1月深圳分部报销单'
    :param batch_remark: 转账说明，UTF8编码，最多允许32个字符，示例值：'2019年1月深圳分部报销单'
    :param total_amount: 转账总金额，单位为分，必须与批次内所有明细转账金额之和保持一致，否则无法发起转账操作，示例值：'4000000'
    :param total_num: 转账总笔数，必须与批次内所有明细之和保持一致，否则无法发起转账操作，示例值：200
    :param transfer_detail_list: 发起批量转账的明细列表，最多三千笔，示例值：[{"out_detail_no": "x23zy545Bd5436", "transfer_amount": 200000, "transfer_remark": "2020年4月报销", "openid": "o-MYE42l80oelYMDE34nYD456Xoy", "user_name": "张三"}]
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    :param transfer_scene_id: 转账场景ID，示例值:'1001'
    :param notify_url: 通知地址，示例值:'https://www.weixin.qq.com/wxpay/pay.php'
    """
    params = {}
    if out_batch_no:
        params.update({'out_batch_no': out_batch_no})
    else:
        raise Exception('out_batch_no is not assigned')
    if batch_name:
        params.update({'batch_name': batch_name})
    else:
        raise Exception('batch_name is not assigned')
    if batch_remark:
        params.update({'batch_remark': batch_remark})
    else:
        raise Exception('batch_remark is not assigned')
    if total_amount:
        params.update({'total_amount': total_amount})
    else:
        raise Exception('total_amount is not assigned')
    if total_num:
        params.update({'total_num': total_num})
    else:
        raise Exception('total_num is not assigned')
    if transfer_detail_list:
        params.update({'transfer_detail_list': transfer_detail_list})
    else:
        raise Exception('transfer_detail_list is not assigned')
    cipher_data = False
    for transfer_detail in params.get('transfer_detail_list'):
        if transfer_detail.get('user_name'):
            transfer_detail['user_name'] = self._core.encrypt(transfer_detail.get('user_name'))
            cipher_data = True
    params.update({'appid': appid or self._appid})
    if notify_url or self._notify_url:
        params.update({'notify_url': notify_url or self._notify_url})
    if transfer_scene_id:
        params.update({'transfer_scene_id': transfer_scene_id})
    path = '/v3/transfer/batches'
    return self._core.request(path, method=RequestType.POST, data=params, cipher_data=cipher_data)


def transfer_query_batchid(self, batch_id, need_query_detail=False, offset=0, limit=20, detail_status='ALL'):
    """微信批次单号查询批次单
    :param batch_id: 微信批次单号，微信商家转账系统返回的唯一标识，示例值：1030000071100999991182020050700019480001
    :param need_query_detail: 是否查询转账明细单，枚举值：true：是；false：否，默认否。
    :param offset: 请求资源起始位置，默认值为0
    :param limit: 最大资源条数，默认值为20
    :param detail_status: 明细状态， ALL:全部。需要同时查询转账成功和转账失败的明细单；SUCCESS:转账成功。只查询转账成功的明细单；FAIL:转账失败。
    """
    if batch_id:
        path = '/v3/transfer/batches/batch-id/%s' % batch_id
    else:
        raise Exception('batch_id is not assigned')
    if need_query_detail:
        path += '?need_query_detail=true'
        path += '&detail_status=%s' % detail_status
    else:
        path += '?need_query_detail=false'
    path += '&offset=%s' % offset
    path += '&limit=%s' % limit
    return self._core.request(path)


def transfer_query_detail_id(self, batch_id, detail_id):
    """微信明细单号查询明细单
    :param batch_id: 微信批次单号，微信商家转账系统返回的唯一标识，示例值：1030000071100999991182020050700019480001
    :param detail_id: 微信明细单号，微信支付系统内部区分转账批次单下不同转账明细单的唯一标识，示例值：1040000071100999991182020050700019500100
    """
    if batch_id and detail_id:
        path = '/v3/transfer/batches/batch-id/%s/details/detail-id/%s' % (batch_id, detail_id)
    else:
        raise Exception('batch_id or detail_id is not assigned')
    return self._core.request(path)


def transfer_query_out_batch_no(self, out_batch_no, need_query_detail=False, offset=0, limit=20, detail_status='ALL'):
    """商家批次单号查询批次单
    :param out_batch_no: 商家批次单号，示例值：plfk2020042013
    :param need_query_detail: 是否查询转账明细单，枚举值：true：是；false：否，默认否。
    :param offset: 请求资源起始位置，默认值为0
    :param limit: 最大资源条数，默认值为20
    :param detail_status: 明细状态， ALL:全部。需要同时查询转账成功和转账失败的明细单；SUCCESS:转账成功。只查询转账成功的明细单；FAIL:转账失败。
    """
    if out_batch_no:
        path = '/v3/transfer/batches/out-batch-no/%s' % out_batch_no
    else:
        raise Exception('batch_id is not assigned')
    if need_query_detail:
        path += '?need_query_detail=true'
        path += '&detail_status=%s' % detail_status
    else:
        path += '?need_query_detail=false'
    path += '&offset=%s' % offset
    path += '&limit=%s' % limit
    return self._core.request(path)


def transfer_query_out_detail_no(self, out_detail_no, out_batch_no):
    """商家明细单号查询明细单
    :param out_detail_no: 商家明细单号，示例值：x23zy545Bd5436
    :param out_batch_no: 商家批次单号，示例值：plfk2020042013
    """
    if out_detail_no and out_batch_no:
        path = '/v3/transfer/batches/out-batch-no/%s/details/out-detail-no/%s' % (out_batch_no, out_detail_no)
    else:
        raise Exception('out_detail_no or out_batch_no is not assigned')
    return self._core.request(path)


def transfer_bill_receipt(self, out_batch_no):
    """转账电子回单申请受理
    :param out_batch_no: 商家批次单号，示例值：plfk2020042013
    """
    params = {}
    if out_batch_no:
        params.update({'out_batch_no': out_batch_no})
    else:
        raise Exception('out_batch_no is assigned')
    path = '/v3/transfer/bill-receipt'
    return self._core.request(path, method=RequestType.POST, params=params)


def transfer_query_bill_receipt(self, out_batch_no):
    """查询转账电子回单
    :param out_batch_no: 商家批次单号，示例值：plfk2020042013
    """
    if out_batch_no:
        path = '/v3/transfer/bill-receipt/%s' % out_batch_no
    else:
        raise Exception('out_batch_no is not assigned')
    return self._core.request(path)


def transfer_detail_receipt(self, accept_type, out_detail_no, out_batch_no=None,):
    """转账明细电子回单受理
    :param accept_type: 受理类型
    :param out_detail_no: 商家明细单号，示例值：x23zy545Bd5436
    :param out_batch_no: 商家批次单号，示例值：plfk2020042013
    """
    params = {}
    if accept_type:
        params.update({'accept_type': accept_type})
    else:
        raise Exception('accept_type is not assigned')
    if out_detail_no:
        params.update({'out_detail_no': out_detail_no})
    else:
        raise Exception('out_detail_no is not assigned')
    if out_batch_no:
        params.update({'out_batch_no': out_batch_no})
    path = '/v3/transfer-detail/electronic-receipts'
    return self._core.request(path, method=RequestType.POST, params=params)


def transfer_query_receipt(self, accept_type, out_detail_no, out_batch_no=None):
    """查询转账明细电子回单受理结果
    :param accept_type: 受理类型
    :param out_detail_no: 商家明细单号，示例值：x23zy545Bd5436
    :param out_batch_no: 商家批次单号，示例值：plfk2020042013
    """
    if accept_type:
        path = '/v3/transfer-detail/electronic-receipts?accept_type=%s' % accept_type
    else:
        raise Exception('accept_type is not assigned')
    if out_detail_no:
        path += '&out_batch_no=%s' % out_detail_no
    else:
        raise Exception('out_detail_no is not assigned')
    if out_batch_no:
        path += '&out_batch_no=%s' % out_batch_no
    return self._core_request(path)
