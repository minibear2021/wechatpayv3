# -*- coding: utf-8 -*-

from .type import RequestType


def merchantrisk_callback_create(self, notify_url=None):
    """创建商户违规通知回调地址
    :param notify_url: 通知地址，示例值:'https://www.weixin.qq.com/wxpay/pay.php'
    """
    params = {}
    if notify_url:
        params.update({'notify_url': notify_url})
    path = '/v3/merchant-risk-manage/violation-notifications'
    return self._core.request(path, method=RequestType.POST, data=params)


def merchantrisk_callback_query(self):
    """查询商户违规通知回调地址
    """
    path = '/v3/merchant-risk-manage/violation-notifications'
    return self._core.request(path)


def merchantrisk_callback_update(self, notify_url=None):
    """修改商户违规通知回调地址
    :param notify_url: 通知地址，示例值:'https://www.weixin.qq.com/wxpay/pay.php'
    """
    params = {}
    if notify_url:
        params.update({'notify_url': notify_url})
    path = '/v3/merchant-risk-manage/violation-notifications'
    return self._core.request(path, method=RequestType.PUT, data=params)


def merchantrisk_callback_delete(self):
    """查询商户违规通知回调地址
    """
    path = '/v3/merchant-risk-manage/violation-notifications'
    return self._core.request(path, method=RequestType.DELETE)
