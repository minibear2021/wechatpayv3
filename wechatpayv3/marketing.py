# -*- coding: utf-8 -*-

import os

from .media import _media_upload
from .type import RequestType
from .utils import sha256


def marketing_image_upload(self, filepath, filename=None):
    """图片上传(营销专用)
    :param filepath: 图片文件路径
    :param filename: 文件名称，未指定则从filepath参数中截取
    """
    return _media_upload(self, filepath, filename, '/v3/marketing/favor/media/image-upload')


def marketing_card_send(self, card_id, openid, out_request_no, send_time, appid=None):
    """发放消费卡
    :card_id: 消费卡ID。示例值:'pIJMr5MMiIkO_93VtPyIiEk2DZ4w'
    :openid: 用户openid，待发卡用户的openid。示例值:'obLatjhnqgy2syxrXVM3MJirbkdI'
    :out_request_no: 商户单据号。示例值:'oTYhjfdsahnssddj_0136'
    :send_time: 请求发卡时间，单次请求发卡时间，消费卡在商户系统的实际发放时间，为东八区标准时间（UTC+8）。示例值:'2019-12-31T13:29:35.120+08:00'
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
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
    params.update({'appid': appid or self._appid})
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_partnership_build(self, idempotency_key, partner_type, business_type, partner_appid=None,
                                partner_merchant_id=None, stock_id=None):
    """建立合作关系
    :idempotency_key: 业务请求幂等值，商户侧需保持唯一性，可包含英文字母，数字，｜，_，*，-等内容，不允许出现其他不合法符号。示例值:'12345'
    :partner_type: 合作方类别，枚举值:'APPID':合作方为APPID，'MERCHANT':合作方为商户。示例值:'APPID'
    :business_type: 授权业务类别，枚举值:'FAVOR_STOCK':代金券批次，'BUSIFAVOR_STOCK':商家券批次。示例值:'FAVOR_STOCK'
    :partner_appid: 合作方APPID，合作方类别为APPID时必填。示例值:'wx4e1916a585d1f4e9'
    :partner_merchant_id: 合作方商户ID，合作方类别为MERCHANT时必填。特殊规则:最小字符长度为8。示例值:'2480029552'
    :stock_id: 授权批次ID，授权业务类别为商家券批次或代金券批次时，此参数必填。示例值:'2433405'
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
    :business_type: 授权业务类别，枚举值:'FAVOR_STOCK':代金券批次，'BUSIFAVOR_STOCK':商家券批次。示例值:'FAVOR_STOCK'
    :stock_id: 授权批次ID，授权业务类别为商家券批次或代金券批次时，此参数必填。示例值:'2433405'
    :partner_type: 合作方类别，枚举值:'APPID':合作方为APPID，'MERCHANT':合作方为商户。示例值:'APPID'
    :partner_appid: 合作方APPID，合作方类别为APPID时必填。示例值:'wx4e1916a585d1f4e9'
    :partner_merchant_id: 合作方商户ID，合作方类别为MERCHANT时必填。特殊规则:最小字符长度为8。示例值:'2480029552'
    :limit: 分页大小，最大50。不传默认为20。示例值:5
    :offset: 分页页码，页码从0开始。示例值:10
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


def marketing_paygift_activity_create(self, activity_base_info, award_send_rule, advanced_setting=None):
    """创建全场满额送活动
    :param activity_base_info: 活动基本信息
    :param award_send_rule: 活动奖品发放规则
    :param advanced_setting: 活动高级设置
    """
    params = {}
    if not activity_base_info or not award_send_rule:
        raise Exception('activity_base_info or award_send_rule is not assigned.')
    params.update({'activity_base_info': activity_base_info})
    params.update({'award_send_rule': award_send_rule})
    if advanced_setting:
        params.update({'advanced_setting': advanced_setting})
    path = '/v3/marketing/paygiftactivity/unique-threshold-activity'
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_paygift_activity_detail(self, activity_id):
    """查询活动详情接口
    :param activity_id: 活动id，示例值:'10028001'
    """
    if activity_id:
        path = '/v3/marketing/paygiftactivity/activities/%s' % activity_id
    else:
        raise Exception('activity_id is not assigned.')
    return self._core.request(path)


def marketing_paygift_merchants_list(self, activity_id, offset=0, limit=20):
    """查询活动发券商户号
    :param activity_id: 活动id，示例值:'10028001'
    :param offset:分页页码，页面从0开始。示例值:1
    :param limit: 分页大小，限制分页最大数据条目。示例值:20
    """
    if activity_id:
        path = '/v3/marketing/paygiftactivity/activities/%s/merchants' % activity_id
    else:
        raise Exception('activity_id is not assigned.')
    path = '%s?offset=%s&limit=%s' % (path, offset, limit)
    return self._core.request(path)


def marketing_paygift_goods_list(self, activity_id, offset=0, limit=20):
    """查询活动指定商品列表
    :param activity_id: 活动id，示例值:'10028001'
    :param offset:分页页码，页面从0开始。示例值:1
    :param limit: 分页大小，限制分页最大数据条目。示例值:20
    """
    if activity_id:
        path = '/v3/marketing/paygiftactivity/activities/%s/goods' % activity_id
    else:
        raise Exception('activity_id is not assigned.')
    path = '%s?offset=%s&limit=%s' % (path, offset, limit)
    return self._core.request(path)


def marketing_paygift_activity_terminate(self, activity_id):
    """终止活动
    :param activity_id: 活动id，示例值:'10028001'
    """
    if activity_id:
        path = '/v3/marketing/paygiftactivity/activities/%s/terminate' % activity_id
    else:
        raise Exception('activity_id is not assigned.')
    return self._core.request(path, method=RequestType.POST)


def marketing_paygift_merchant_add(self, activity_id, add_request_no, merchant_id_list=[]):
    """新增活动发券商户号
    :param activity_id: 活动id，示例值:'10028001'
    :param add_request_no: 请求业务单据号，商户添加发券商户号的凭据号，商户侧需保持唯一性。示例值:'100002322019090134234sfdf'
    :param merchant_id_list: 发券商户号，新增到活动中的发券商户号列表，特殊规则:最小字符长度为8，最大为15，条目个数限制:[1，500]。示例值:["10000022"，"10000023"]
    """
    if activity_id:
        path = '/v3/marketing/paygiftactivity/activities/%s/merchants/add' % activity_id
    else:
        raise Exception('activity_id is not assigned.')
    params = {}
    if add_request_no:
        params.update({'add_request_no': add_request_no})
    else:
        raise Exception('add_request_no is not assigned.')
    if merchant_id_list:
        params.update({'merchant_id_list': merchant_id_list})
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_paygift_activity_list(self, offset=0, limit=20, activity_name=None, activity_status=None, award_type=None):
    """获取支付有礼活动列表
    :param offset:分页页码，页面从0开始。示例值:1
    :param limit: 分页大小，限制分页最大数据条目。示例值:20
    :param activity_name: 活动名称，支持模糊搜索。示例值:'良品铺子回馈活动'
    :param activity_status: 活动状态，枚举值:'ACT_STATUS_UNKNOWN':状态未知，'CREATE_ACT_STATUS':已创建，'ONGOING_ACT_STATUS':运行中，'TERMINATE_ACT_STATUS':已终止，
                            'STOP_ACT_STATUS':已暂停，'OVER_TIME_ACT_STATUS':已过期，'CREATE_ACT_FAILED':创建活动失败。示例值:'CREATE_ACT_STATUS'
    :param award_type: 奖品类型，暂时只支持商家券。'BUSIFAVOR':商家券。示例值:'BUSIFAVOR'
    """
    params = {}
    params.update({'offset': offset})
    params.update({'limit': limit})
    if activity_name:
        params.update({'activity_name': activity_name})
    if activity_status:
        params.update({'activity_status': activity_status})
    if award_type:
        params.update({'award_type': award_type})
    path = '/v3/marketing/paygiftactivity/activities'
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_paygift_merchant_delete(self, activity_id, merchant_id_list=[], delete_request_no=None):
    """删除活动发券商户号
    :param activity_id: 活动id，示例值:'10028001'
    :param delete_request_no: 请求业务单据号，商户创建批次凭据号（格式:商户id+日期+流水号），商户侧需保持唯一性，可包含英文字母，数字，｜，_，*，-等内容，不允许出现其他不合法符号。示例值:'100002322019090134234sfdf'
    :param merchant_id_list: 删除的发券商户号，从活动已有的发券商户号中移除的商户号列表，特殊规则:最小字符长度为8，最大为15，条目个数限制:[1，500]。示例值:["10000022"，"10000023"]
    """
    if activity_id:
        path = '/v3/marketing/paygiftactivity/activities/%s/merchants/delete' % activity_id
    else:
        raise Exception('activity_id is not assigned.')
    params = {}
    if merchant_id_list:
        params.update({'merchant_id_list': merchant_id_list})
    if delete_request_no:
        params.update({'delete_request_no': delete_request_no})
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_favor_stock_create(self,
                                 stock_name,
                                 belong_merchant,
                                 available_begin_time,
                                 available_end_time,
                                 stock_use_rule,
                                 coupon_use_rule,
                                 out_request_no,
                                 stock_type='NORMAL',
                                 no_cash=False,
                                 comment=None,
                                 pattern_info=None,
                                 ext_info=None):
    """创建代金券批次
    :param stock_name: 批次名称，示例值:'微信支付代金券批次'
    :param belong_merchant: 归属商户号。示例值:'98568865'
    :param available_begin_time: 可用时间-开始时间，格式为YYYY-MM-DDTHH:mm:ss.sss+TIMEZONE。示例值:'2015-05-20T13:29:35.120+08:00'
    :param available_end_time: 可用时间-结束时间，格式为YYYY-MM-DDTHH:mm:ss.sss+TIMEZONE。示例值:'2015-05-20T13:29:35.120+08:00'
    :param stock_use_rule: 发放规则。示例值:{'max_coupons':5, 'max_amount':100, 'max_coupons_per_user':1, 'natural_person_limit':False, 'prevent_api_abuse':True}
    :param coupon_use_rule: 核销规则。示例值:{'available_merchants':['9856000','9856111']}
    :param out_request_no: 商户单据号，可包含英文字母，数字，|，_，*，-等内容，不允许出现其他不合法符号，商户侧需保持商户单据号全局唯一。示例值:'89560002019101000121'
    :param stock_type: 批次类型，仅支持:'NORMAL':固定面额满减券批次。示例值:'NORMAL'
    :param no_cash: 营销经费，枚举值:True:免充值，False:预充值。示例值:False
    :param comment: 批次备注，仅制券商户可见，用于自定义信息。校验规则:批次备注最多60个UTF8字符数。示例值:'零售批次'
    :param pattern_info: 样式设置，示例值:{'description':'微信支付营销代金券'}
    :param ext_info: 扩展属性，json格式字符串，如无需要则不填写。示例值:"{'exinfo1':'1234','exinfo2':'3456'}"
    """
    params = {}
    if stock_name:
        params.update({'stock_name': stock_name})
    else:
        raise Exception('stock_name is not assigned.')
    if belong_merchant:
        params.update({'belong_merchant': belong_merchant})
    else:
        raise Exception('belong_merchant is not assigned.')
    if available_begin_time:
        params.update({'available_begin_time': available_begin_time})
    else:
        raise Exception('available_begin_time is not assigned.')
    if available_end_time:
        params.update({'available_end_time': available_end_time})
    else:
        raise Exception('available_end_time is not assigned.')
    if stock_use_rule:
        params.update({'stock_use_rule': stock_use_rule})
    else:
        raise Exception('stock_use_rule is not assigned.')
    if coupon_use_rule:
        params.update({'coupon_use_rule': coupon_use_rule})
    else:
        raise Exception('coupon_use_rule is not assigned.')
    if stock_type:
        params.update({'stock_type': stock_type})
    else:
        raise Exception('stock_type is not assigned.')
    if out_request_no:
        params.update({'out_request_no': out_request_no})
    else:
        raise Exception('out_request_no is not assigned.')
    if no_cash:
        params.update({'no_cash': no_cash})
    if comment:
        params.update({'comment': comment})
    if pattern_info:
        params.update({'pattern_info': pattern_info})
    if ext_info:
        params.update({'ext_info': ext_info})
    path = '/v3/marketing/favor/coupon-stocks'
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_favor_stock_start(self, stock_creator_mchid, stock_id):
    """激活代金券批次
    :param stock_creator_mchid: 创建批次的商户号，示例值:'8956000'
    :param stock_id: 批次号，示例值:'9856000'
    """
    params = {}
    if stock_creator_mchid:
        params.update({'stock_creator_mchid': stock_creator_mchid})
    else:
        raise Exception('stock_creator_mchid is not assigned.')
    if stock_id:
        path = '/v3/marketing/favor/stocks/%s/start' % stock_id
    else:
        raise Exception('stock_id is not assigned.')
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_favor_stock_send(self,
                               stock_id,
                               openid,
                               out_request_no,
                               stock_creator_mchid,
                               coupon_value=None,
                               coupon_minimum=None,
                               appid=None):
    """发放代金券批次
    :param stock_id: 批次号。示例值:'9856000'
    :param openid: 用户openid，示例值:'2323dfsdf342342'
    :param out_request_no: 商户单据号，示例值: '89560002019101000121'
    :param stock_creator_mchid: 创建批次的商户号，示例值:'8956000'
    :param coupon_value: 指定面额发券，面额。示例值:100
    :param coupon_minimum: 指定面额发券，券门槛。示例值:100
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    """
    params = {}
    if stock_id:
        params.update({'stock_id': stock_id})
    else:
        raise Exception('stock_id is not assigned.')
    if openid:
        path = '/v3/marketing/favor/users/%s/coupons' % openid
    else:
        raise Exception('openid is not assigned.')
    if out_request_no:
        params.update({'out_request_no': out_request_no})
    else:
        raise Exception('out_request_no is not assigned.')
    if stock_creator_mchid:
        params.update({'stock_creator_mchid': stock_creator_mchid})
    else:
        raise Exception('stock_creator_mchid is not assigned.')
    if coupon_value:
        params.update({'coupon_value': coupon_value})
    if coupon_minimum:
        params.update({'coupon_minimum': coupon_minimum})
    params.update({'appid': appid or self._appid})
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_favor_stock_pause(self, stock_creator_mchid, stock_id):
    """暂停代金券批次
    :param stock_creator_mchid: 创建批次的商户号，示例值:'8956000'
    :param stock_id: 批次号，示例值:'9856000'
    """
    params = {}
    if stock_creator_mchid:
        params.update({'stock_creator_mchid': stock_creator_mchid})
    else:
        raise Exception('stock_creator_mchid is not assigned.')
    if stock_id:
        path = '/v3/marketing/favor/stocks/%s/pause' % stock_id
    else:
        raise Exception('stock_id is not assigned.')
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_favor_stock_restart(self, stock_creator_mchid, stock_id):
    """重启代金券批次
    :param stock_creator_mchid: 创建批次的商户号，示例值:'8956000'
    :param stock_id: 批次号，示例值:'9856000'
    """
    params = {}
    if stock_creator_mchid:
        params.update({'stock_creator_mchid': stock_creator_mchid})
    else:
        raise Exception('stock_creator_mchid is not assigned.')
    if stock_id:
        path = '/v3/marketing/favor/stocks/%s/restart' % stock_id
    else:
        raise Exception('stock_id is not assigned.')
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_favor_stock_list(self,
                               stock_creator_mchid,
                               offset=0,
                               limit=10,
                               create_start_time=None,
                               create_end_time=None,
                               status=None):
    """条件查询批次列表
    :param stock_creator_mchid: 创建批次的商户号，示例值:'8956000'
    :param offset: 分页页码，页码从0开始，默认第0页。示例值:0
    :param limit: 分页大小，最大10。示例值:8
    :param create_start_time: 起始创建时间，格式为YYYY-MM-DDTHH:mm:ss.sss+TIMEZONE。示例值:'2015-05-20T13:29:35.120+08:00'
    :param create_end_time: 终止创建时间，格式为YYYY-MM-DDTHH:mm:ss.sss+TIMEZONE。示例值:'2015-05-20T13:29:35.120+08:00'
    :param status: 批次状态，枚举值:'unactivated':未激活，'audit':审核中，'running':运行中，'stoped':已停止，'paused':暂停发放。示例值:'paused'
    """
    if stock_creator_mchid:
        path = '/v3/marketing/favor/stocks?offset=%s&limit=%s&stock_creator_mchid=%s' % (offset, limit, stock_creator_mchid)
    else:
        raise Exception('stock_creator_mchid is not assigned.')
    if create_start_time:
        path = '%s&create_start_time=%s' % (path, create_start_time)
    if create_end_time:
        path = '%s&create_end_time=%s' % (path, create_end_time)
    if status:
        path = '%s&status=%s' % (path, status)
    return self._core.request(path)


def marketing_favor_stock_detail(self, stock_creator_mchid, stock_id):
    """查询批次详情
    :param stock_creator_mchid: 创建批次的商户号，示例值:'8956000'
    :param stock_id: 批次号，示例值:'9856000'
    """
    if stock_id:
        path = '/v3/marketing/favor/stocks/%s' % stock_id
    else:
        raise Exception('stock_id is not assigned.')
    if stock_creator_mchid:
        path = '%s?stock_creator_mchid=%s' % (path, stock_creator_mchid)
    else:
        raise Exception('stock_creator_mchid is not assigned.')
    return self._core.request(path)


def marketing_favor_coupon_detail(self, coupon_id, openid):
    """查询代金券详情
    :param coupon_id: 代金券id，示例值:'9856888'
    :param openid: 用户openid，示例值:'2323dfsdf342342'
    """
    if coupon_id and openid:
        path = '/v3/marketing/favor/users/%s/coupons/%s?appid=%s' % (openid, coupon_id, self._appid)
    else:
        raise Exception('coupon_id or openid is not assigned.')
    return self._core.request(path)


def marketing_favor_stock_merchant(self, stock_creator_mchid, stock_id, offset=0, limit=50):
    """查询代金券可用商户
    :param stock_creator_mchid: 创建批次的商户号，示例值:'8956000'
    :param stock_id: 批次号，示例值:'9856000'
    :param offset: 分页页码，最大1000。示例值: 10
    :param limit: 分页大小，最大50。示例值: 10
    """
    if stock_id:
        path = '/v3/marketing/favor/stocks/%s/merchants' % stock_id
    else:
        raise Exception('stock_id is not assigned.')
    if stock_creator_mchid:
        path = '%s?stock_creator_mchid=%s&offset=%s&limit=%s&' % (path, stock_creator_mchid, offset, limit)
    return self._core.request(path)


def marketing_favor_stock_item(self, stock_creator_mchid, stock_id, offset=0, limit=50):
    """查询代金券可用单品
    :param stock_creator_mchid: 创建批次的商户号，示例值:'8956000'
    :param stock_id: 批次号，示例值:'9856000'
    :param offset: 分页页码，最大500。示例值: 10
    :param limit: 分页大小，最大100。示例值: 10
    """
    if stock_id:
        path = '/v3/marketing/favor/stocks/%s/items' % stock_id
    else:
        raise Exception('stock_id is not assigned.')
    if stock_creator_mchid:
        path = '%s?stock_creator_mchid=%s&offset=%s&limit=%s&' % (path, stock_creator_mchid, offset, limit)
    return self._core.request(path)


def marketing_favor_user_coupon(self,
                                openid,
                                stock_id=None,
                                status=None,
                                creator_mchid=None,
                                sender_mchid=None,
                                available_mchid=None,
                                offset=0,
                                limit=20):
    """根据商户号查用户的券
    :param openid: 用户openid，示例值:'2323dfsdf342342'
    :param stock_id: 批次号，示例值:'9856000'
    :param status: 券状态，代金券状态:'SENDED':可用，'USED':已实扣，填写available_mchid参数则该字段不生效。示例值:'USED'
    :param creator_mchid: 创建批次的商户号.示例值:'9865002'
    :param sender_mchid: 批次发放商户号。示例值:'9865001'
    :param available_mchid: 可用商户号。示例值: '9865000'
    :param offset: 分页页码，默认0，填写available_mchid，该字段不生效。示例值:0
    :param limit: 分页大小，默认20，填写available_mchid，该字段不生效。示例值:20
    """
    if openid:
        path = '/v3/marketing/favor/users/%s/coupons?appid=%s&offset=%s&limit=%s' % (openid, self._appid, offset, limit)
    else:
        raise Exception('openid is not assigned.')
    if stock_id:
        path = '%s&stock_id=%s' % (path, stock_id)
    if status:
        path = '%s&status=%s' % (path, status)
    if creator_mchid:
        path = '%s&creator_mchid=%s' % (path, creator_mchid)
    elif sender_mchid:
        path = '%s&sender_mchid=%s' % (path, sender_mchid)
    elif available_mchid:
        path = '%s&available_mchid=%s' % (path, available_mchid)
    return self._core.request(path)


def marketing_favor_use_flow(self, stock_id):
    """下载批次核销明细
    :param stock_id: 批次号，微信为每个代金券批次分配的唯一id。示例值:'9865000'
    """
    if stock_id:
        path = '/v3/marketing/favor/stocks/%s/use-flow' % stock_id
    else:
        raise Exception('stock_id is not assigned.')
    return self._core.request(path)


def marketing_favor_refund_flow(self, stock_id):
    """下载批次退款明细
    :param stock_id: 批次号，微信为每个代金券批次分配的唯一id。示例值:'9865000'
    """
    if stock_id:
        path = '/v3/marketing/favor/stocks/%s/refund-flow' % stock_id
    else:
        raise Exception('stock_id is not assigned.')
    return self._core.request(path)


def marketing_favor_callback_update(self, notify_url=None, switch=True, mchid=None):
    """设置消息通知地址
    :param notify_url: 支付通知商户url地址。示例值:'https://pay.weixin.qq.com'
    :param switch: 回调开关，枚举值:True:开启推送，False:停止推送。示例值:True
    :param mchid: 微信支付商户号，可不填，默认传入初始化的mchid。示例值:'9856888'
    """
    params = {}
    params.update({'mchid': mchid or self._mchid})
    if not (notify_url or self._notify_url):
        raise Exception('notify_url is not assigned.')
    params.update({'notify_url': notify_url or self._notify_url})
    params.update({'switch': switch})
    path = '/v3/marketing/favor/callbacks'
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_busifavor_stock_create(self,
                                     stock_name,
                                     belong_merchant,
                                     goods_name,
                                     stock_type,
                                     coupon_use_rule,
                                     stock_send_rule,
                                     out_request_no,
                                     coupon_code_mode,
                                     comment=None,
                                     custom_entrance=None,
                                     display_pattern_info=None,
                                     notify_config=None,
                                     subsidy=False):
    """创建商家券
    :params stock_name: 商家券批次名称，字数上限为21个，一个中文汉字/英文字母/数字均占用一个字数。示例值:'8月1日活动券'
    :params belong_merchant: 批次归属商户号。注:普通直连模式，该参数为直连商户号。示例值:'10000022'
    :params goods_name: 适用商品范围，用来描述批次在哪些商品可用，会显示在微信卡包中。字数上限为15个。示例值:'xxx商品使用'
    :params stock_type: 批次类型，'NORMAL':固定面额满减券批次，'DISCOUNT':折扣券批次，'EXCHANGE':换购券批次。示例值:'NORMAL'
    :params coupon_use_rule: 核销规则。示例值:{'coupon_available_time':{}, 'fixed_normal_coupon':{}, 'use_method':'OFF_LINE', }
    :params stock_send_rule: 发放规则。示例值:{'max_coupons':100, 'max_coupons_per_user':5}
    :params out_request_no: 商户请求单号。示例值:'100002322019090134234sfdf'
    :params coupon_code_mode: 券code模式，枚举值:'WECHATPAY_MODE':系统分配券code。（固定22位纯数字），'MERCHANT_API':商户发放时接口指定券code，'MERCHANT_UPLOAD':商户上传自定义code，发券时系统随机选取上传的券code。示例值:'WECHATPAY_MODE'
    :params comment: 批次备注，仅配置商户可见，用于自定义信息。字数上限为20个。示例值:'活动使用'
    :params custom_entrance: 自定义入口。示例值:{'hall_id':'233455656'}
    :params display_pattern_info: 样式信息。示例值:{'description':'xxx门店可用'}
    :params notify_config: 事件通知配置。示例值:{'notify_appid':'wx23232232323'}
    :params subsidy=False: 是否允许营销补贴，该批次发放的券是否允许进行补差。示例值:False
    """
    params = {}
    if stock_name:
        params.update({'stock_name': stock_name})
    else:
        raise Exception('stock_name is not assigned.')
    if belong_merchant:
        params.update({'belong_merchant': belong_merchant})
    else:
        raise Exception('belong_merchant is not assigned.')
    if goods_name:
        params.update({'goods_name': goods_name})
    else:
        raise Exception('goods_name is not assigned.')
    if stock_type:
        params.update({'stock_type': stock_type})
    else:
        raise Exception('stock_type is not assigned.')
    if coupon_use_rule:
        params.update({'coupon_use_rule': coupon_use_rule})
    else:
        raise Exception('coupon_use_rule is not assigned.')
    if stock_send_rule:
        params.update({'stock_send_rule': stock_send_rule})
    else:
        raise Exception('stock_send_rule is not assigned.')
    if out_request_no:
        params.update({'out_request_no': out_request_no})
    else:
        raise Exception('out_request_no is not assigned.')
    if coupon_code_mode:
        params.update({'coupon_code_mode': coupon_code_mode})
    else:
        raise Exception('coupon_code_mode is not assigned.')
    if comment:
        params.update({'comment': comment})
    if custom_entrance:
        params.update({'custom_entrance': custom_entrance})
    if display_pattern_info:
        params.update({'display_pattern_info': display_pattern_info})
    if notify_config:
        params.update({'notify_config': notify_config})
    params.update({'subsidy': subsidy})
    path = '/v3/marketing/busifavor/stocks'
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_busifavor_stock_query(self, stock_id):
    """查询商家券详情
    :param stock_id: 批次号。示例值:1212
    """
    if stock_id:
        path = '/v3/marketing/busifavor/stocks/%s' % stock_id
    else:
        raise Exception('stock_id is not assigned.')
    return self._core.request(path)


def marketing_busifavor_coupon_use(self,
                                   coupon_code,
                                   use_time,
                                   use_request_no,
                                   stock_id=None,
                                   openid=None,
                                   appid=None):
    """核销用户券
    :param coupon_code: 券code，券的唯一标识。示例值:'sxxe34343434'
    :param use_time: 请求核销时间，格式为YYYY-MM-DDTHH:mm:ss+TIMEZONE。示例值:'2015-05-20T13:29:35+08:00'
    :param use_request_no: 核销请求单据号，每次核销请求的唯一标识，商户需保证唯一。示例值:'1002600620019090123143254435'
    :param stock_id: 批次号。示例值:1212
    :param openid: 用户标识。示例值:'xsd3434454567676'
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    """
    params = {}
    if coupon_code:
        params.update({'coupon_code': coupon_code})
    else:
        raise Exception('coupon_code is not assigned.')
    if use_time:
        params.update({'use_time': use_time})
    else:
        raise Exception('use_time is not assigned.')
    if use_request_no:
        params.update({'use_request_no': use_request_no})
    else:
        raise Exception('use_request_no is not assigned.')
    if stock_id:
        params.update({'stock_id': stock_id})
    if openid:
        params.update({'openid': openid})
    params.update({'appid': appid or self._appid})
    path = '/v3/marketing/busifavor/coupons/use'
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_busifavor_user_coupon(self,
                                    openid,
                                    stock_id=None,
                                    coupon_state=None,
                                    creator_merchant=None,
                                    belong_merchant=None,
                                    sender_merchant=None,
                                    offset=0,
                                    limit=20):
    """根据过滤条件查询用户券
    :param openid: 用户标识。示例值:'xsd3434454567676'
    :param stock_id: 批次号。示例值:1212
    :param coupon_state: 券状态，枚举值:'SENDED':可用，'USED':已核销，'EXPIRED':已过期，示例值:'SENDED'
    :param creator_merchant: 创建批次的商户号。示例值:'1000000001'
    :param belong_merchant: 批次归属商户号。示例值:'1000000002'
    :param sender_merchant: 批次发放商户号。示例值:'1000000003'
    :param offset: 分页页码。示例值:0
    :param limit: 分页大小。示例值:20
    """
    if openid:
        path = '/v3/marketing/busifavor/users/%s/coupons?appid=%s&offset=%s&limit=%s' % (openid, self._appid, offset, limit)
    else:
        raise Exception('openid is not assigned.')
    if stock_id:
        path = '%s&stock_id=%s' % (path, stock_id)
    if coupon_state:
        path = '%s&coupon_state=%s' % (path, coupon_state)
    if creator_merchant:
        path = '%s&creator_merchant=%s' % (path, creator_merchant)
    if belong_merchant:
        path = '%s&belong_merchant=%s' % (path, belong_merchant)
    if sender_merchant:
        path = '%s&sender_merchant=%s' % (path, sender_merchant)
    return self._core.request(path)


def marketing_busifavor_coupon_detail(self, coupon_code, openid):
    """查询用户单张券详情
    :param coupon_code: 券code，券的唯一标识。示例值:'sxxe34343434'
    :param openid: 用户标识。示例值:'xsd3434454567676'
    """
    if not (coupon_code and openid):
        raise Exception('coupon_code or openid is not assigned.')
    path = '/v3/marketing/busifavor/users/%s/coupons/%s/appids/%s' % (openid, coupon_code, self._appid)
    return self._core.request(path)


def marketing_busifavor_couponcode_upload(self,
                                          stock_id,
                                          upload_request_no,
                                          coupon_code_list=[]):
    """上传预存code
    :param stock_id: 批次号。示例值:1212
    :param upload_request_no: 请求业务单据号。商户上传code的凭据号，商户侧需保持唯一性。示例值:'100002322019090134234sfdf'
    :param coupon_code_list: 券code列表。示例值:['ABC9588200'，'ABC9588201']
    """
    params = {}
    if stock_id:
        path = '/v3/marketing/busifavor/stocks/%s/couponcodes' % stock_id
    else:
        raise Exception('stock_id is not assigned.')
    if upload_request_no:
        params.update({'upload_request_no': upload_request_no})
    else:
        raise Exception('upload_request_no is not assigned.')
    if coupon_code_list:
        params.update({'coupon_code_list': coupon_code_list})
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_busifavor_callback_update(self, mchid=None, notify_url=None):
    """设置商家券事件通知地址
    :param mchid: 商户号，可不填，默认传入初始化的mchid。示例值:'10000098'
    :param notify_url: 通知URL地址，用于接收商家券事件通知的url地址，不填默认使用初始化的notify_url。示例值:'https://pay.weixin.qq.com'
    """
    params = {}
    params.update({'mchid': mchid or self._mchid})
    if not (notify_url or self._notify_url):
        raise Exception('notify_url is not assigned.')
    params.update({'notify_url': notify_url or self._notify_url})
    path = '/v3/marketing/busifavor/callbacks'
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_busifavor_callback_query(self, mchid=None):
    """查询商家券事件通知地址
    :param mchid: 商户号，不填默认使用初始化的mchid。示例值:'10000098'
    """
    path = '/v3/marketing/busifavor/callbacks?mchid=%s' % (mchid or self._mchid)
    return self._core.request(path)


def marketing_busifavor_coupon_associate(self, stock_id, coupon_code, out_trade_no, out_request_no):
    """关联订单信息
    :param stock_id: 批次号。示例值:1212
    :param coupon_code: 券code，券的唯一标识。示例值:'sxxe34343434'
    :param out_trade_no: 关联的商户订单号，微信支付下单时的商户订单号，欲与该商家券关联的微信支付。示例值:'MCH_102233445'
    :param out_request_no: 商户请求单号，示例值:'1002600620019090123143254435'
    """
    params = {}
    if stock_id:
        params.update({'stock_id': stock_id})
    else:
        raise Exception('stock_id is not assigned.')
    if coupon_code:
        params.update({'coupon_code': coupon_code})
    else:
        raise Exception('coupon_code is not assigned.')
    if out_trade_no:
        params.update({'out_trade_no': out_trade_no})
    else:
        raise Exception('out_trade_no is not assigned.')
    if out_request_no:
        params.update({'out_request_no': out_request_no})
    else:
        raise Exception('out_request_no is not assigned.')
    path = '/v3/marketing/busifavor/coupons/associate'
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_busifavor_coupon_disassociate(self, stock_id, coupon_code, out_trade_no, out_request_no):
    """取消关联订单信息
    :param stock_id: 批次号。示例值:1212
    :param coupon_code: 券code，券的唯一标识。示例值:'sxxe34343434'
    :param out_trade_no: 关联的商户订单号，微信支付下单时的商户订单号，欲与该商家券关联的微信支付。示例值:'MCH_102233445'
    :param out_request_no: 商户请求单号，示例值:'1002600620019090123143254435'
    """
    params = {}
    if stock_id:
        params.update({'stock_id': stock_id})
    else:
        raise Exception('stock_id is not assigned.')
    if coupon_code:
        params.update({'coupon_code': coupon_code})
    else:
        raise Exception('coupon_code is not assigned.')
    if out_trade_no:
        params.update({'out_trade_no': out_trade_no})
    else:
        raise Exception('out_trade_no is not assigned.')
    if out_request_no:
        params.update({'out_request_no': out_request_no})
    else:
        raise Exception('out_request_no is not assigned.')
    path = '/v3/marketing/busifavor/coupons/disassociate'
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_busifavor_stock_budget(self,
                                     stock_id,
                                     modify_budget_request_no,
                                     target_max_coupons=None,
                                     target_max_coupons_by_day=None,
                                     current_max_coupons=None,
                                     current_max_coupons_by_day=None):
    """修改批次预算
    :param stock_id: 批次号。示例值:1212
    :param modify_budget_request_no: 修改预算请求单据号，示例值:'1002600620019090123143254436'
    :param target_max_coupons: 目标批次最大发放个数。示例值:3000
    :param target_max_coupons_by_day: 目标单天发放上限个数。示例值:500
    :param current_max_coupons: 当前批次最大发放个数。示例值:500
    :param current_max_coupons_by_day: 当前单天发放上限个数。示例值:300
    """
    params = {}
    if stock_id:
        path = '/v3/marketing/busifavor/stocks/%s/budget' % stock_id
    else:
        raise Exception('stock_id is not assigned.')
    if modify_budget_request_no:
        params.update({'modify_budget_request_no': modify_budget_request_no})
    else:
        raise Exception('modify_budget_request_no is not assigned.')
    if target_max_coupons:
        params.update({'target_max_coupons': target_max_coupons})
    elif target_max_coupons_by_day:
        params.update({'target_max_coupons_by_day': target_max_coupons_by_day})
    else:
        raise Exception('target_max_coupons or target_max_coupons_by_day is not assigned.')
    if current_max_coupons:
        params.update({'current_max_coupons': current_max_coupons})
    if current_max_coupons_by_day:
        params.update({'current_max_coupons_by_day': current_max_coupons_by_day})
    return self._core.request(path, method=RequestType.PATCH, data=params)


def marketing_busifavor_stock_modify(self,
                                     stock_id,
                                     out_request_no,
                                     custom_entrance=None,
                                     comment=None,
                                     goods_name=None,
                                     display_pattern_info=None,
                                     coupon_use_rule=None,
                                     stock_send_rule=None,
                                     notify_config=None):
    """修改商家券基本信息
    :param stock_id: 批次号。示例值:1212
    :param out_request_no: 商户请求单号，示例值:'1002600620019090123143254435'
    :param custom_entrance: 自定义入口。示例值:{'hall_id':'234567'}
    :param comment: 批次备注，字数上限为20个。示例值:'活动使用'
    :param goods_name: 适用商品范围。示例值:'xxx商品使用'
    :param display_pattern_info: 样式信息。示例值:{'description':'xxx门店可用'}
    :param coupon_use_rule: 核销规则。示例值:{'use_method':'OFF_LINE'}
    :param stock_send_rule: 发放规则。示例值:{'prevent_api_abuse':False}
    :param notify_config: 事件通知配置。示例值:{'notify_appid':'wx23232232323'}
    """
    if stock_id:
        path = '/v3/marketing/busifavor/stocks/%s' % stock_id
    else:
        raise Exception('stock_id is not assigned.')
    params = {}
    if out_request_no:
        params.update({'out_request_no': out_request_no})
    else:
        raise Exception('out_request_no is not assigned.')
    if custom_entrance:
        params.update({'custom_entrance': custom_entrance})
    if comment:
        params.update({'comment': comment})
    if goods_name:
        params.update({'goods_name': goods_name})
    if display_pattern_info:
        params.update({'display_pattern_info': display_pattern_info})
    if coupon_use_rule:
        params.update({'coupon_use_rule': coupon_use_rule})
    if stock_send_rule:
        params.update({'stock_send_rule': stock_send_rule})
    if notify_config:
        params.update({'notify_config': notify_config})
    return self._core.request(path, method=RequestType.PATCH, data=params)


def marketing_busifavor_coupon_return(self, coupon_code, stock_id, return_request_no):
    """申请退券
    :param coupon_code: 券code，券的唯一标识。示例值:'sxxe34343434'
    :param stock_id: 批次号。示例值:1212
    :param return_request_no: 退券请求单据号。示例值:'1002600620019090123143254436'
    """
    params = {}
    if coupon_code:
        params.update({'coupon_code': coupon_code})
    else:
        raise Exception('coupon_code is not assigned.')
    if stock_id:
        params.update({'stock_id': stock_id})
    else:
        raise Exception('stock_id is not assigned.')
    if return_request_no:
        params.update({'return_request_no': return_request_no})
    else:
        raise Exception('return_request_no is not assigned.')
    path = '/v3/marketing/busifavor/coupons/return'
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_busifavor_coupon_deactivate(self, coupon_code, stock_id, deactivate_request_no, deactivate_reason=None):
    """使券失效
    :param coupon_code: 券code，券的唯一标识。示例值:'sxxe34343434'
    :param stock_id: 批次号。示例值:1212
    :param deactivate_request_no: 失效请求单据号。示例值:'1002600620019090123143254436'
    :param deactivate_reason: 失效原因。示例值:'此券使用时间设置错误'
    """
    params = {}
    if coupon_code:
        params.update({'coupon_code': coupon_code})
    else:
        raise Exception('coupon_code is not assigned.')
    if stock_id:
        params.update({'stock_id': stock_id})
    else:
        raise Exception('stock_id is not assigned.')
    if deactivate_request_no:
        params.update({'deactivate_request_no': deactivate_request_no})
    else:
        raise Exception('deactivate_request_no is not assigned.')
    if deactivate_reason:
        params.update({'deactivate_reason': deactivate_reason})
    path = '/v3/marketing/busifavor/coupons/deactivate'
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_busifavor_subsidy_pay(self,
                                    stock_id,
                                    coupon_code,
                                    transaction_id,
                                    payer_merchant,
                                    payee_merchant,
                                    amount,
                                    description,
                                    out_subsidy_no):
    """营销补差付款
    :param stock_id: 批次号。示例值:1212
    :param coupon_code: 券code，券的唯一标识。示例值:'sxxe34343434'
    :param transaction_id: 微信支付订单号。示例值:'4200000913202101152566792388'
    :param payer_merchant: 营销补差扣款商户号。示例值:'1900000001'
    :param payee_merchant: 营销补差入账商户号。示例值:'1900000002'
    :param amount: 补差付款金额。示例值:100
    :param description: 补差付款描述。示例值:'20210115DESCRIPTION'
    :param out_subsidy_no: 业务请求唯一单号。示例值:'subsidy-abcd-12345678'
    """
    params = {}
    if coupon_code:
        params.update({'coupon_code': coupon_code})
    else:
        raise Exception('coupon_code is not assigned.')
    if stock_id:
        params.update({'stock_id': stock_id})
    else:
        raise Exception('stock_id is not assigned.')
    if transaction_id:
        params.update({'transaction_id': transaction_id})
    else:
        raise Exception('transaction_id is not assigned.')
    if payer_merchant:
        params.update({'payer_merchant': payer_merchant})
    else:
        raise Exception('payer_merchant is not assigned.')
    if payee_merchant:
        params.update({'payee_merchant': payee_merchant})
    else:
        raise Exception('payee_merchant is not assigned.')
    if amount:
        params.update({'amount': amount})
    else:
        raise Exception('amount is not assigned.')
    if description:
        params.update({'description': description})
    else:
        raise Exception('description is not assigned.')
    if out_subsidy_no:
        params.update({'out_subsidy_no': out_subsidy_no})
    else:
        raise Exception('out_subsidy_no is not assigned.')
    path = '/v3/marketing/busifavor/subsidy/pay-receipts'
    return self._core.request(path, method=RequestType.POST, data=params)


def marketing_busifavor_subsidy_query(self, subsidy_receipt_id):
    """查询营销补差付款单详情
    :param subsidy_receipt_id: 补差付款单号。示例值:'1120200119165100000000000001'
    """
    if subsidy_receipt_id:
        path = '/v3/marketing/busifavor/subsidy/pay-receipts/%s' % subsidy_receipt_id
    else:
        raise Exception('subsidy_receipt_id is not assigned.')
    return self._core.request(path)


def industry_coupon_token(self, open_id, coupon_list=[]):
    """出行券切卡组件预下单
    https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/chapter9_9_1.shtml
    :param open_id: 用户在商户AppID下的唯一标识，该用户为后续拉起切卡组件的用户。示例值：'obLatjrR8kUDlj4-nofQsPAJAAFI'
    :param coupon_list: 用户最近领取的出行券列表。示例值：[{"coupon_id": "11004999626", "stock_id": 16474341}]
    """
    params = {}
    if open_id:
        params.update({'open_id': open_id})
    else:
        raise Exception('open_id is not assigned.')
    if coupon_list:
        params.update({'coupon_list': coupon_list})
    else:
        raise Exception('coupon_list is not assigned.')
    path = '/v3/industry-coupon/tokens'
    return self._core.request(path, method=RequestType.POST, data=params)


def bank_package_file(self, package_id, bank_type, filepath):
    """导入定向用户协议号
    https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/chapter9_8_1.shtml
    :package_id: 号码包唯一标识符。可在微信支付商户平台创建号码包后获得。示例值：'8473295'
    :filepath: 电子发票文件路径，只支持txt和csv两种格式，示例值：'./active_user.csv'
    """
    if not (filepath and os.path.exists(filepath) and os.path.isfile(filepath)):
        raise Exception('filepath is not assigned or not exists')
    with open(filepath, mode='rb') as f:
        content = f.read()
    filename = os.path.basename(filepath)
    filetype = os.path.splitext(filename)[-1][1:].upper()
    mimes = {
        'TXT': ' text/plain',
        'CSV': 'text/csv'
    }
    if filetype not in mimes:
        raise Exception('wechatpayv3 does not support this file type: ' + filetype)
    if not package_id or bank_type:
        raise Exception('package_id or bank_type is not assigned.')
    params = {}
    params.update({'meta': '{"bank_type":"%s", "filename":"%s", "sha256":"%s"}' % (bank_type, filename, sha256(content))})
    files = [('file', (filename, content, mimes[filetype]))]
    path = '/v3/marketing/bank/packages/%s/tasks' % package_id
    return self._core.request(path, method=RequestType.POST, data=params, sign_data=params.get('meta'), files=files)
