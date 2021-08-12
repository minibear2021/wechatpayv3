# -*- coding: utf-8 -*-

import os.path
from hashlib import sha256

from .type import RequestType, WeChatPayType


def _media_upload(self, filepath, filename, image=True):
    if not (filepath and os.path.exists(filepath) and os.path.isfile(filepath)):
        raise Exception('filepath is not assigned or not exists')
    h = sha256()
    f = open(filepath, mode='rb')
    content = f.read()
    f.close()
    h.update(content)
    digest = h.hexdigest()
    if not filename:
        filename = os.path.basename(filepath)
    params = {}
    params.update({'meta': '{"filename":"%s","sha256":"%s"}' % (filename, digest)})
    if image:
        files = [('file', (filename, content, 'image/' + os.path.split(filename)[1]))]
        path = '/v3/merchant/media/upload'
    else:
        files = [('file', (filename, content, 'image/png'))]
        path = '/v3/merchant/media/video_upload'
    return self._core.request(path, method=RequestType.POST, data=params, sign_data=params['meta'], files=files)


def image_upload(self, filepath, filename=None):
    """图片上传
    :param filepath: 图片文件路径
    :param filename: 文件名称，未指定则从filepath参数中截取
    """
    return _media_upload(self, filepath, filename)


def video_upload(self, filepath, filename=None):
    """视频上传
    :param filepath: 视频文件路径
    :param filename: 文件名称，未指定则从filepath参数中截取
    """
    return _media_upload(self, filepath, filename, image=False)
