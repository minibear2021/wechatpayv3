# -*- coding: utf-8 -*-

from .type import RequestType


def applyment_submit(self, business_code, contact_info, subject_info, business_info, settlement_info, bank_account_info, addition_info=None):
    """提交申请单
    https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/chapter10_1_1.shtml
    :param business_code: 业务申请编号，示例值:'APPLYMENT_00000000001'
    :param contact_info: 超级管理员信息，示例值:{'contact_name':'张三','contact_id_number':'320311770706001','mobile_phone':'13900000000','contact_email':'admin@demo.com'}
    :param subject_info: 主体资料，示例值:{'subject_type':'SUBJECT_TYPE_ENTERPRISE','business_license_info':{'license_copy':'demo-media-id','license_number':'123456789012345678','merchant_name':'腾讯科技有限公司','legal_person':'张三'},'identity_info':{'id_doc_type':'IDENTIFICATION_TYPE_IDCARD','id_card_info'{'id_card_copy':'demo-media-id'}}}
    :param business_info: 经营资料，示例值:{'merchant_shortname':'张三餐饮店','service_phone':'0758xxxxxx','sales_info':{'sales_scenes_type':['SALES_SCENES_STORE','SALES_SCENES_MP']}}
    :param settlement_info: 结算规则，示例值:{'settlement_id':'719','qualification_type':'餐饮'}
    :param bank_account_info: 结算银行账户，示例值:{'bank_account_type':'BANK_ACCOUNT_TYPE_CORPORATE','account_name':'xx公司','account_bank':'工商银行','bank_address_code':'110000','account_number':'1234567890'}
    :param addition_info: 补充材料，示例值:{'legal_person_commitment':'demo-media-id'}
    """
    params = {}
    if business_code:
        params.update({'business_code': business_code})
    else:
        raise Exception('business_code is not assigned.')
    if contact_info:
        params.update({'contact_info': contact_info})
    else:
        raise Exception('contact_info is not assigned.')
    if subject_info:
        params.update({'subject_info': subject_info})
    else:
        raise Exception('subject_info is not assigned.')
    if business_info:
        params.update({'business_info': business_info})
    else:
        raise Exception('business_info is not assigned')
    if settlement_info:
        params.update({'settlement_info': settlement_info})
    else:
        raise Exception('settlement_info is not assigned.')
    if bank_account_info:
        params.update({'bank_account_info': bank_account_info})
    else:
        raise Exception('bank_account_info is not assigned.')
    if addition_info:
        params.update({'addition_info': addition_info})
    if params.get('contact_info').get('contact_name'):
        params['contact_info']['contact_name'] = self._core.encrypt(params['contact_info']['contact_name'])
    if params.get('contact_info').get('contact_id_number'):
        params['contact_info']['contact_id_number'] = self._core.encrypt(params['contact_info']['contact_id_number'])
    if params.get('contact_info').get('openid'):
        params['contact_info']['openid'] = self._core.encrypt(params['contact_info']['openid'])
    if params.get('contact_info').get('mobile_phone'):
        params['contact_info']['mobile_phone'] = self._core.encrypt(params['contact_info']['mobile_phone'])
    if params.get('contact_info').get('contact_email'):
        params['contact_info']['contact_email'] = self._core.encrypt(params['contact_info']['contact_email'])
    id_card_name = params.get('subject_info').get('identity_info').get('id_card_info', {}).get('id_card_name')
    if id_card_name:
        params['subject_info']['identity_info']['id_card_info']['id_card_name'] = self._core.encrypt(id_card_name)
    id_card_number = params.get('subject_info').get('identity_info').get('id_card_info', {}).get('id_card_number')
    if id_card_number:
        params['subject_info']['identity_info']['id_card_info']['id_card_number'] = self._core.encrypt(id_card_number)
    id_card_address = params.get('subject_info').get('identity_info').get('id_card_info', {}).get('id_card_address')
    if id_card_address:
        params['subject_info']['identity_info']['id_card_info']['id_card_address'] = self._core.encrypt(id_card_address)
    id_doc_name = params.get('subject_info').get('identity_info').get('id_doc_info', {}).get('id_doc_name')
    if id_doc_name:
        params['subject_info']['identity_info']['id_doc_info']['id_doc_name'] = self._core.encrypt(id_doc_name)
    id_doc_number = params.get('subject_info').get('identity_info').get('id_doc_info', {}).get('id_doc_number')
    if id_doc_number:
        params['subject_info']['identity_info']['id_doc_info']['id_doc_number'] = self._core.encrypt(id_doc_number)
    id_doc_address = params.get('subject_info').get('identity_info').get('id_doc_info', {}).get('id_doc_address')
    if id_doc_address:
        params['subject_info']['identity_info']['id_doc_info']['id_doc_address'] = self._core.encrypt(id_doc_address)
    if params.get('subject_info').get('ubo_info_list'):
        for ubo_info in params['subject_info']['ubo_info_list']:
            ubo_info['ubo_id_doc_name'] = self._core.encrypt(ubo_info['ubo_id_doc_name'])
            ubo_info['ubo_id_doc_number'] = self._core.encrypt(ubo_info['ubo_id_doc_number'])
            ubo_info['ubo_id_doc_address'] = self._core.encrypt(ubo_info['ubo_id_doc_address'])
    params['bank_account_info']['account_name'] = self._core.encrypt(params['bank_account_info']['account_name'])
    params['bank_account_info']['account_number'] = self._core.encrypt(params['bank_account_info']['account_number'])
    path = '/v3/applyment4sub/applyment/'
    return self._core.request(path, method=RequestType.POST, data=params, cipher_data=True)


def applyment_query(self, business_code=None, applyment_id=None):
    """查询申请单状态
    https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/chapter11_1_2.shtml
    :param business_code: 业务申请编号，示例值:'APPLYMENT_00000000001'
    :param applyment_id: 申请单号，示例值:2000001234567890
    """
    if business_code:
        path = '/v3/applyment4sub/applyment/business_code/%s' % business_code
    elif applyment_id:
        path = '/v3/applyment4sub/applyment/applyment_id/%s' % applyment_id
    else:
        raise Exception('business_code or applyment_id is not assigned.')
    return self._core.request(path)


def applyment_settlement_modify(self, sub_mchid, account_type, account_bank, bank_address_code, account_number, bank_name=None, bank_branch_id=None):
    """修改结算账号
    https://pay.weixin.qq.com/docs/partner/apis/modify-settlement/sub-merchants/modify-settlement.html
    :param sub_mchid: 特约商户号，示例值:'1511101111'
    :param account_type: 账户类型，枚举值:'ACCOUNT_TYPE_BUSINESS':对公银行账户，'ACCOUNT_TYPE_PRIVATE':经营者个人银行卡。示例值:'ACCOUNT_TYPE_BUSINESS'
    :param account_bank: 开户银行，示例值:'工商银行'
    :param bank_address_code: 开户银行省市编码，示例值:'110000'
    :param account_number: 银行账号，示例值:'1234567890'
    :param bank_name: 开户银行全称（含支行），示例值:'施秉县农村信用合作联社城关信用社'
    :param bank_branch_id: 开户银行联行号，示例值:'402713354941'
    """
    params = {}
    if sub_mchid:
        path = '/v3/apply4sub/sub_merchants/%s/modify-settlement' % sub_mchid
    else:
        raise Exception('sub_mchid is not assigned.')
    if account_type:
        params.update({'account_type': account_type})
    else:
        raise Exception('account_type is not assigned.')
    if account_bank:
        params.update({'account_bank': account_bank})
    else:
        raise Exception('account_bank is not assigned.')
    if bank_address_code:
        params.update({'bank_address_code': bank_address_code})
    else:
        raise Exception('bank_address_code is not assigned.')
    cipher_data = False
    if account_number:
        params.update({'account_number': self._core.encrypt(account_number)})
        cipher_data = True
    else:
        raise Exception('account_number is not assigned.')
    if bank_name:
        params.update({'bank_name': bank_name})
    if bank_branch_id:
        params.update({'bank_branch_id': bank_branch_id})
    return self._core.request(path, method=RequestType.POST, data=params, cipher_data=cipher_data)


def applyment_settlement_query(self, sub_mchid):
    """查询结算账户
    https://pay.weixin.qq.com/docs/partner/apis/modify-settlement/sub-merchants/get-settlement.html
    :param sub_mchid: 特约商户号，示例值:'1511101111'
    """
    if sub_mchid:
        path = '/v3/apply4sub/sub_merchants/%s/settlement' % sub_mchid
    else:
        raise Exception('sub_mchid is not assigned.')
    return self._core.request(path)


def applyment_settlement_modify_state(self, sub_mchid, application_no):
    """查询结算账户修改申请状态
    https://pay.weixin.qq.com/docs/partner/apis/modify-settlement/sub-merchants/get-application.html
    :param sub_mchid: 【特约商户/二级商户号】 请填写本服务商负责进件的特约商户/二级商户号。
    :param application_no: 【修改结算账户申请单号】 提交二级商户修改结算账户申请后，由微信支付返回的单号，作为查询申请状态的唯一标识。
    """
    if not (sub_mchid and application_no):
        raise Exception('sub_mchid and/or application_no is not assigned.')
    path = '/v3/apply4sub/sub_merchants/%s/application/%s' % (sub_mchid, application_no)
    return self._core.request(path)
