# -*- coding: utf-8 -*-

from .core import RequestType
from .type import WeChatPayType


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

def user_authorization(self, openid):
    """智慧商圈积分授权查询
    :param openid: 用户标识，示例值：'oWmnN4xxxxxxxxxxe92NHIGf1xd8'
    """
    if self._type != WeChatPayType.MINIPROG:
        raise Exception('points notify only supports wechat mini prog')
    if not openid:
        raise Exception('openid is not assigned.')
    path = '/v3/businesscircle/user-authorizations/%s?appid=%s' % (openid, self._mchid)
    return self._core.request(path)
