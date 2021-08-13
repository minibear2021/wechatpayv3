# -*- coding: utf-8 -*-

from .media import _media_upload

def marketing_image_upload(self, filepath, filename=None):
    """图片上传(营销专用)
    :param filepath: 图片文件路径
    :param filename: 文件名称，未指定则从filepath参数中截取
    """
    return _media_upload(self, filepath, filename, '/v3/marketing/favor/media/image-upload')