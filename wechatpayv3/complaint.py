# -*- coding: utf-8 -*-

from datetime import datetime

from .media import _media_upload
from .type import RequestType


def complaint_list_query(self, begin_date=None, end_date=None, limit=10, offset=0, complainted_mchid=None):
    """查询投诉单列表
    :param begin_date: 开始日期，投诉发生的开始日期，格式为YYYY-MM-DD。注意，查询日期跨度不超过30天，当前查询为实时查询。示例值:'2019-01-01'
    :param end_date: 结束日期，投诉发生的结束日期，格式为YYYY-MM-DD。注意，查询日期跨度不超过30天，当前查询为实时查询。示例值:'2019-01-01'
    :param limit: 分页大小，设置该次请求返回的最大投诉条数，范围【1,50】,商户自定义字段，不传默认为10。示例值:5
    :param offset: 分页开始位置，该次请求的分页开始位置，从0开始计数，例如offset=10，表示从第11条记录开始返回，不传默认为0 。示例值:10
    :param complainted_mchid: 被诉商户号，投诉单对应的被诉商户号。示例值:'1900012181'
    """
    if not begin_date:
        begin_date = datetime.now().strftime("%Y-%m-%d")
    if not end_date:
        end_date = begin_date
    if not complainted_mchid:
        complainted_mchid = self._mchid
    path = '/v3/merchant-service/complaints-v2?limit=%s&offset=%s&begin_date=%s&end_date=%s&complainted_mchid=%s'
    path = path % (limit, offset, begin_date, end_date, complainted_mchid)
    return self._core.request(path)


def complaint_detail_query(self, complaint_id):
    """查询投诉单详情
    :param complaint_id: 投诉单对应的投诉单号。示例值:'200201820200101080076610000'
    """
    if not complaint_id:
        raise Exception('complaint_id is not assigned.')
    path = '/v3/merchant-service/complaints-v2/%s' % complaint_id
    return self._core.request(path)


def complaint_history_query(self, complaint_id, limit=100, offset=0):
    """查询投诉协商历史
    :param complaint_id: 投诉单对应的投诉单号。示例值:'200201820200101080076610000'
    :param limit: 分页大小，设置该次请求返回的最大协商历史条数，范围[1,300]，不传默认为100。。示例值:5
    :param offset: 分页开始位置，该次请求的分页开始位置，从0开始计数，例如offset=10，表示从第11条记录开始返回，不传默认为0。示例值:10
    """
    if not complaint_id:
        raise Exception('complaint_id is not assigned.')
    if limit not in range(1, 301):
        limit = 100
    path = '/v3/merchant-service/complaints-v2/%s/negotiation-historys?limit=%s&offset=%s' % (complaint_id, limit, offset)
    return self._core.request(path)


def complaint_notification_create(self, url):
    """创建投诉通知回调地址
    :param: url: 通知地址，仅支持https。示例值:'https://www.xxx.com/notify'
    """
    params = {}
    if url:
        params.update({'url': url})
    else:
        raise Exception('url is not assigned.')
    path = '/v3/merchant-service/complaint-notifications'
    return self._core.request(path, method=RequestType.POST, data=params)


def complaint_notification_query(self):
    """查询投诉通知回调地址
    :param: url: 通知地址，仅支持https。示例值:'https://www.xxx.com/notify'
    """
    path = '/v3/merchant-service/complaint-notifications'
    return self._core.request(path)


def complaint_notification_update(self, url):
    """更新投诉通知回调地址
    :param: url: 通知地址，仅支持https。示例值:'https://www.xxx.com/notify'
    """
    params = {}
    if url:
        params.update({'url': url})
    else:
        raise Exception('url is not assigned.')
    path = '/v3/merchant-service/complaint-notifications'
    return self._core.request(path, method=RequestType.PUT, data=params)


def complaint_notification_delete(self):
    """删除投诉通知回调地址
    :param: url: 通知地址，仅支持https。示例值:'https://www.xxx.com/notify'
    """
    path = '/v3/merchant-service/complaint-notifications'
    return self._core.request(path, method=RequestType.DELETE)


def complaint_response(self, complaint_id, response_content, response_images=None, jump_url=None, jump_url_text=None):
    """提交投诉回复
    :param complaint_id: 投诉单对应的投诉单号。示例值:'200201820200101080076610000'
    :param response_content: 回复内容，具体的投诉处理方案，限制200个字符以内。示例值:'已与用户沟通解决'
    :param response_images: 回复图片，传入调用商户上传反馈图片接口返回的media_id，最多上传4张图片凭证。示例值:['file23578_21798531.jpg', 'file23578_21798532.jpg']
    :param jump_url: 跳转链接，附加跳转链接，引导用户跳转至商户客诉处理页面，链接需满足https格式。示例值:"https://www.xxx.com/notify"
    :param jump_url_text: 转链接文案，展示给用户的文案，附在回复内容之后。用户点击文案，即可进行跳转。示例值:"查看订单详情"
    """
    params = {}
    if not complaint_id:
        raise Exception('complaint_id is not assigned')
    if response_content:
        params.update({'response_content': response_content})
    else:
        raise Exception('response_content is not assigned')
    params.update({'complainted_mchid': self._core._mchid})
    if response_images:
        params.update({'response_images': response_images})
    if jump_url:
        params.update({'jump_url': jump_url})
    if jump_url_text:
        params.update({'jump_url_text': jump_url_text})
    path = '/v3/merchant-service/complaints-v2/%s/response' % complaint_id
    return self._core.request(path, method=RequestType.POST, data=params)


def complaint_complete(self, complaint_id):
    """反馈投诉处理完成
    :param complaint_id: 投诉单对应的投诉单号。示例值:'200201820200101080076610000'
    """
    params = {}
    if not complaint_id:
        raise Exception('complaint_id is not assigned')
    params.update({'complainted_mchid': self._core._mchid})
    path = '/v3/merchant-service/complaints-v2/%s/complete' % complaint_id
    return self._core.request(path, method=RequestType.POST, data=params)


def complaint_image_upload(self, filepath, filename=None):
    """商户上传投诉反馈图片
    :param filepath: 图片文件路径
    :param filename: 文件名称，未指定则从filepath参数中截取
    """
    return _media_upload(self, filepath, filename, '/v3/merchant-service/images/upload')


def complaint_image_download(self, media_url):
    """下载客户投诉图片
    :param media_url: 图片下载地址，示例值:'https://api.mch.weixin.qq.com/v3/merchant-service/images/xxxxx'
    """
    path = media_url[len(self._core._gate_way):] if media_url.startswith(self._core._gate_way) else media_url
    return self._core.request(path, skip_verify=True)
