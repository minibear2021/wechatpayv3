# -*- coding: utf-8 -*-

from .type import RequestType


def apply4subject_submit(self, business_code, contact_info, subject_info, identification_info, channel_id=None, addition_info=None, ubo_info_list=[]):
    """（商户开户意愿）提交申请单
    :param business_code: 业务申请编号，示例值:'APPLYMENT_00000000001'
    :param contact_info: 联系人信息，示例值:{'name':'张三','id_card_number':'320311770706001','mobile':'13900000000'}
    :param subject_info: 主体信息，示例值:{'subject_type':'SUBJECT_TYPE_ENTERPRISE','business_license_info':{'license_copy':'demo-media-id','license_number':'123456789012345678','merchant_name':'腾讯科技有限公司','legal_person':'张三','company_address':'广东省深圳市南山区xx路xx号','licence_valid_date':'["1970-01-01","forever"]'}}
    :param business_info: 经营资料，示例值:{'merchant_shortname':'张三餐饮店','service_phone':'0758xxxxxx','sales_info':{'sales_scenes_type':['SALES_SCENES_STORE','SALES_SCENES_MP']}}
    :param identification_info: 法人身份信息，示例值:{'identification_type':'IDENTIFICATION_TYPE_IDCARD','identification_name':'张三','identification_number':'110220330044005500','identification_valid_date':'["1970-01-01","forever"]','identification_front_copy':'0P3ng6KTIW4-Q_l2FjKLZ...','identification_back_copy':'0P3ng6KTIW4-Q_l2FjKLZ...'}
    :param channel_id: 渠道商户号，示例值:'20001111'
    :param addition_info: 补充材料，示例值:{'confirm_mchid_list':['20001113']}
    :param ubo_info_list: 最终受益人信息列表，示例值:[{'ubo_id_doc_type':'IDENTIFICATION_TYPE_IDCARD','ubo_id_doc_name':'张三','ubo_id_doc_number':'110220330044005500'}]
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
    if identification_info:
        params.update({'identification_info': identification_info})
    else:
        raise Exception('identification_info is not assigned')
    if channel_id:
        params.update({'channel_id': channel_id})
    if addition_info:
        params.update({'addition_info': addition_info})
    if ubo_info_list:
        params.update({'ubo_info_list': ubo_info_list})
    contact_name = params.get('contact_info').get('name')
    if contact_name:
        params['contact_info']['name'] = self._core.encrypt(contact_name)
    contact_mobile = params.get('contact_info').get('mobile')
    if contact_mobile:
        params['contact_info']['mobile'] = self._core.encrypt(contact_mobile)
    contact_number = params.get('contact_info').get('id_card_number')
    if contact_number:
        params['contact_info']['id_card_number'] = self._core.encrypt(contact_number)
    identification_name = params.get('identification_info').get('identification_name')
    if identification_name:
        params['identification_info']['identification_name'] = self._core.encrypt(identification_name)
    identification_number = params.get('identification_info').get('identification_number')
    if identification_number:
        params['identification_info']['identification_number'] = self._core.encrypt(identification_number)
    identification_address = params.get('identification_info').get('identification_address')
    if identification_address:
        params['identification_info']['identification_address'] = self._core.encrypt(identification_address)
    if params.get('ubo_info_list'):
        for ubo_info in params['ubo_info_list']:
            ubo_info['ubo_id_doc_name'] = self._core.encrypt(ubo_info['ubo_id_doc_name'])
            ubo_info['ubo_id_doc_number'] = self._core.encrypt(ubo_info['ubo_id_doc_number'])
            ubo_info['ubo_id_doc_address'] = self._core.encrypt(ubo_info['ubo_id_doc_address'])
    path = '/v3/apply4subject/applyment'
    return self._core.request(path, method=RequestType.POST, data=params, cipher_data=True)


def apply4subject_cancel(self, business_code=None, applyment_id=None):
    """（商户开户意愿）撤销申请单
    :param business_code: 业务申请编号，示例值:'2000001234567890'
    :param applyment_id: 申请单编号，示例值:2000001234567890
    """
    if business_code:
        path = '/v3/apply4subject/applyment/%s/cancel' % business_code
    elif applyment_id:
        path = '/v3/apply4subject/applyment/%s/cancel' % applyment_id
    else:
        raise Exception('business_code or applyment_id is not assigned.')
    return self._core.request(path)


def apply4subject_query(self, business_code=None, applyment_id=None):
    """（商户开户意愿）查询申请单审核结果
    :param business_code: 业务申请编号，示例值:'2000001234567890'
    :param applyment_id: 申请单编号，示例值:2000001234567890
    """
    if business_code:
        path = '/v3/apply4subject/applyment?business_code=%s' % business_code
    elif applyment_id:
        path = '/v3/apply4subject/applyment?applyment_id=%s' % applyment_id
    else:
        raise Exception('business_code or applyment_id is not assigned.')
    return self._core.request(path)


def apply4subject_state(self, sub_mchid):
    """（商户开户意愿）获取商户开户意愿确认状态
    :param sub_mchid: 特约商户号，示例值:'1511101111'
    """
    if sub_mchid:
        path = '/v3/apply4subject/applyment/merchants/%s/state' % sub_mchid
    else:
        raise Exception('sub_mchid is not assigned.')
    return self._core.request(path)
