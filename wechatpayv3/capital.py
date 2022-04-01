# -*- coding: utf-8 -*-


def capital_search_bank_number(self, account_number):
    """获取对私银行卡号开户银行
    :param account_number: 银行卡号，示例值：'1234567890123'
    """
    from urllib.parse import urlencode
    params = {}
    params.update({'account_number': self._core.encrypt(account_number)})
    path = '/v3/capital/capitallhh/banks/search-banks-by-bank-account?%s' % urlencode(params)
    return self._core.request(path, cipher_data=True)


def capital_personal_banks(self, offset=0, limit=200):
    """查询支持个人业务的银行列表
    :param offset: 本次查询偏移量，示例值：0
    :param offset: 本次请求最大查询条数，示例值：200
    """
    path = '/v3/capital/capitallhh/banks/personal-banking?offset=%s&limit=%s' % (offset, limit)
    return self._core.request(path)


def capital_corporate_banks(self, offset=0, limit=200):
    """查询支持对公业务的银行列表
    :param offset: 本次查询偏移量，示例值：0
    :param offset: 本次请求最大查询条数，示例值：200
    """
    path = '/v3/capital/capitallhh/banks/corporate-banking?offset=%s&limit=%s' % (offset, limit)
    return self._core.request(path)


def capital_provinces(self):
    """查询省份列表
    """
    path = '/v3/capital/capitallhh/areas/provinces'
    return self._core.request(path)


def capital_cities(self, province_code):
    """查询城市列表
    :param province_code: 省份编码，唯一标识一个省份。示例值：10
    """
    path = '/v3/capital/capitallhh/areas/provinces/%s/cities' % province_code
    return self._core.request(path)


def capital_branches(self, bank_alias_code, city_code, offset=0, limit=100):
    """查询支行列表
    :param bank_alias_code: 银行别名的编码，查询支行接口仅支持需要填写支行的银行别名编码。示例值：1000006247
    :param city_code: 城市编码，唯一标识一座城市，用于结合银行别名编码查询支行列表。示例值：536
    :param offset: 本次查询偏移量，示例值：0
    :param offset: 本次请求最大查询条数，示例值：100
    """
    if bank_alias_code and city_code:
        path = '/v3/capital/capitallhh/banks/%s/branches?city_code=%s&offset=%s&limit=%s' % (bank_alias_code, city_code, offset, limit)
    else:
        raise Exception('bank_alias_code or city_code is not assigned.')
    return self._core.request(path)
