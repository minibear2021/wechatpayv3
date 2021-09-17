# -*- coding: utf-8 -*-

from .media import _media_upload
from .type import RequestType


def marketing_image_upload(self, filepath, filename=None):
    """图片上传(营销专用)
    :param filepath: 图片文件路径
    :param filename: 文件名称，未指定则从filepath参数中截取
    """
    return _media_upload(self, filepath, filename, '/v3/marketing/favor/media/image-upload')


def marketing_card_send(self, card_id, openid, out_request_no, send_time):
    """发放消费卡
    :card_id: 消费卡ID。示例值：'pIJMr5MMiIkO_93VtPyIiEk2DZ4w'
    :openid: 用户openid，待发卡用户的openid。示例值：'obLatjhnqgy2syxrXVM3MJirbkdI'
    :out_request_no: 商户单据号。示例值：'oTYhjfdsahnssddj_0136'
    :send_time: 请求发卡时间，单次请求发卡时间，消费卡在商户系统的实际发放时间，为东八区标准时间（UTC+8）。示例值：'2019-12-31T13:29:35.120+08:00'
    """
    params = {}
    if card_id:
        path = '/v3/marketing/busifavor/coupons/%s/send' % card_id
    else:
        raise Exception('card_id is not assigned.')
    if openid:
        params.update({'openid': openid})
    else:
        raise Exception('openid is not assigned.')
    if out_request_no:
        params.update({'out_request_no': out_request_no})
    else:
        raise Exception('out_request_no is not assigned.')
    if send_time:
        params.update({'send_time': send_time})
    else:
        raise Exception('send_time is not assigned.')
    params.update({'appid': self._appid})
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_partnership_build(self, idempotency_key, partner_type, business_type, partner_appid=None,
                                partner_merchant_id=None, stock_id=None):
    """建立合作关系
    :idempotency_key: 业务请求幂等值，商户侧需保持唯一性，可包含英文字母，数字，｜，_，*，-等内容，不允许出现其他不合法符号。示例值：'12345'
    :partner_type: 合作方类别，枚举值：'APPID'：合作方为APPID，'MERCHANT'：合作方为商户。示例值：'APPID'
    :business_type: 授权业务类别，枚举值：'FAVOR_STOCK'：代金券批次，'BUSIFAVOR_STOCK'：商家券批次。示例值：'FAVOR_STOCK'
    :partner_appid: 合作方APPID，合作方类别为APPID时必填。示例值：'wx4e1916a585d1f4e9'
    :partner_merchant_id: 合作方商户ID，合作方类别为MERCHANT时必填。特殊规则：最小字符长度为8。示例值：'2480029552'
    :stock_id: 授权批次ID，授权业务类别为商家券批次或代金券批次时，此参数必填。示例值：'2433405'
    """
    headers = {}
    if idempotency_key:
        headers.update({'Idempotency-Key': idempotency_key})
    else:
        raise Exception('idempotency_key is not assigned.')
    params = {}
    if partner_type == 'APPID' and partner_appid:
        params.update({'partner': {'type': partner_type, 'appid': partner_appid}})
    elif partner_type == 'MERCHANT' and partner_merchant_id:
        params.update({'partner': {'type': partner_type, 'merchant_id': partner_merchant_id}})
    else:
        raise Exception('invalid value in partner_type/partner_appid/partner_merchant_id')
    if business_type not in ['FAVOR_STOCK', 'BUSIFAVOR_STOCK'] or not stock_id:
        raise Exception('invalid value in bussiness_type/stock_id.')
    params.update({'authorized_data': {'bussiness_type': business_type, 'stock_id': stock_id}})
    path = '/v3/marketing/partnerships/build'
    return self._core.request(path, method=RequestType.POST, data=params, headers=headers)


def marketing_partnership_query(self, business_type, stock_id, partner_type=None, partner_appid=None,
                                partner_merchant_id=None, limit=20, offset=None):
    """查询合作关系列表
    :business_type: 授权业务类别，枚举值：'FAVOR_STOCK'：代金券批次，'BUSIFAVOR_STOCK'：商家券批次。示例值：'FAVOR_STOCK'
    :stock_id: 授权批次ID，授权业务类别为商家券批次或代金券批次时，此参数必填。示例值：'2433405'
    :partner_type: 合作方类别，枚举值：'APPID'：合作方为APPID，'MERCHANT'：合作方为商户。示例值：'APPID'
    :partner_appid: 合作方APPID，合作方类别为APPID时必填。示例值：'wx4e1916a585d1f4e9'
    :partner_merchant_id: 合作方商户ID，合作方类别为MERCHANT时必填。特殊规则：最小字符长度为8。示例值：'2480029552'
    :limit: 分页大小，最大50。不传默认为20。示例值：5
    :offset: 分页页码，页码从0开始。示例值：10
    """
    path = '/v3/marketing/partnerships?'
    if business_type not in ['FAVOR_STOCK', 'BUSIFAVOR_STOCK'] or not stock_id:
        raise Exception('invalid value in bussiness_type/stock_id.')
    path = '%sauthorized_data={"business_type":"%s","stock_id":"%s"}' % (path, business_type, stock_id)
    if partner_type == 'APPID' and partner_appid:
        path = '%s&partner={"type":"%s","appid":"%s"}' % (path, partner_type, partner_appid)
    elif partner_type == 'MERCHANT' and partner_merchant_id:
        path = '%s&partner={"type":"%s","merchant_id":"%s"}' % (path, partner_type, partner_merchant_id)
    if limit in range(0, 51):
        path = '%s&limit=%s' % (path, limit)
    if offset:
        path = '%s&offset=%s' % (path, offset)
    return self._core.request(path)
