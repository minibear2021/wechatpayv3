# -*- coding: utf-8 -*-

from .type import RequestType


def goldplan_plan_change(self, sub_mchid, operation_type):
    """点金计划管理
    :param sub_mchid: 子商户的商户号，由微信支付生成并下发。示例值:'1900000109' 
    :param operation_type: 操作类型, 枚举值:'OPEN':表示开通点金计划，'CLOSE':表示关闭点金计划。示例值:'OPEN'
    """
    params = {}
    if sub_mchid:
        params.update({'sub_mchid': sub_mchid})
    else:
        raise Exception('sub_mchid is not assigned.')
    if operation_type:
        params.update({'operation_type': operation_type})
    else:
        raise Exception('operation_type is not assigned.')
    path = '/v3/goldplan/merchants/changegoldplanstatus'
    return self._core.request(path, method=RequestType.POST, data=params)


def goldplan_custompage_change(self, sub_mchid, operation_type):
    """商家小票管理
    :param sub_mchid: 子商户的商户号，由微信支付生成并下发。示例值:'1900000109' 
    :param operation_type: 操作类型, 枚举值:'OPEN':表示开通商家自定义小票，'CLOSE':表示关闭商家自定义小票。示例值:'OPEN'
    """
    params = {}
    if sub_mchid:
        params.update({'sub_mchid': sub_mchid})
    else:
        raise Exception('sub_mchid is not assigned.')
    if operation_type:
        params.update({'operation_type': operation_type})
    else:
        raise Exception('operation_type is not assigned.')
    path = '/v3/goldplan/merchants/changecustompagestatus'
    return self._core.request(path, method=RequestType.POST, data=params)


def goldplan_advertising_filter(self, sub_mchid, advertising_industry_filters):
    """同业过滤标签管理
    :param sub_mchid: 子商户的商户号，由微信支付生成并下发。示例值:'1900000109' 
    :param advertising_industry_filters: 同业过滤标签值, 同业过滤标签最少传一个，最多三个。示例值:['SOFTWARE','SECURITY','LOVE_MARRIAGE']
    """
    params = {}
    if sub_mchid:
        params.update({'sub_mchid': sub_mchid})
    else:
        raise Exception('sub_mchid is not assigned.')
    if advertising_industry_filters:
        params.update({'advertising_industry_filters': advertising_industry_filters})
    else:
        raise Exception('advertising_industry_filters is not assigned.')
    path = '/v3/goldplan/merchants/set-advertising-industry-filter'
    return self._core.request(path, method=RequestType.POST, data=params)


def goldplan_advertising_open(self, sub_mchid, advertising_industry_filters=None):
    """开通广告展示
    :param sub_mchid: 子商户的商户号，由微信支付生成并下发。示例值:'1900000109' 
    :param advertising_industry_filters: 同业过滤标签值, 同业过滤标签最少传一个，最多三个。示例值:['SOFTWARE','SECURITY','LOVE_MARRIAGE']
    """
    params = {}
    if sub_mchid:
        params.update({'sub_mchid': sub_mchid})
    else:
        raise Exception('sub_mchid is not assigned.')
    if advertising_industry_filters:
        params.update({'advertising_industry_filters': advertising_industry_filters})
    else:
        raise Exception('advertising_industry_filters is not assigned.')
    path = '/v3/goldplan/merchants/open-advertising-show'
    return self._core.request(path, method=RequestType.POST, data=params)


def goldplan_advertising_close(self, sub_mchid):
    """关闭广告展示
    :param sub_mchid: 子商户的商户号，由微信支付生成并下发。示例值:'1900000109' 
    """
    params = {}
    if sub_mchid:
        params.update({'sub_mchid': sub_mchid})
    else:
        raise Exception('sub_mchid is not assigned.')
    path = '/v3/goldplan/merchants/close-advertising-show'
    return self._core.request(path, method=RequestType.POST, data=params)
