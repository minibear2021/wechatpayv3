# -*- coding: utf-8 -*-

from .type import RequestType

async def mch_transfer_bills(self, out_bill_no, transfer_scene_id, openid, transfer_amount, transfer_remark, user_name=None, user_recv_perception=None, transfer_scene_report_infos=[], appid=None, notify_url=None):
    """发起转账
    :param out_bill_no: 商户单号，商户系统内部的商家单号，要求此参数只能由数字、大小写字母组成，在商户系统内部唯一，示例值：'plfk2020042013'
    :param transfer_scene_id: 转账场景ID，示例值:'1001'
    :param openid: 收款用户OpenID，商户AppID下，某用户的OpenID，示例值：'o-MYE42l80oelYMDE34nYD456Xoy'
    :param transfer_amount: 转账金额，单位为“分”，示例值: 1000
    :param transfer_remark: 转账备注，用户收款时可见该备注信息，最多允许32个字符，示例值:'2020年4月报销'
    :param user_name: 收款用户姓名，转账金额 >= 2,000元时，该笔明细必须填写。若商户传入收款用户姓名，微信支付会校验收款用户与输入姓名是否一致，并提供电子回单，示例值:'张三'
    :param user_recv_perception: 用户收款时感知到的收款原因，将根据转账场景自动展示默认内容。如有其他展示需求，可在本字段传入。示例值: '现金奖励'
    :param transfer_scene_report_infos: 转账场景报备信息，info_type的值必需按文档指示传入，示例值: [{'info_type':'活动名称', 'info_content':'新会员有礼'}, {'info_type':'奖励说明', 'info_content':'注册会员抽奖'}]
    :param appid: 应用ID，可不填，默认传入初始化时的appid，示例值:'wx1234567890abcdef'
    :param notify_url: 通知地址，异步接收微信支付结果通知的回调地址，示例值:'https://www.weixin.qq.com/wxpay/pay.php'
    """
    params={}
    if out_bill_no:
        params.update({'out_bill_no':out_bill_no})
    else:
        raise Exception('out_batch_no is not assigned')
    if transfer_scene_id:
        params.update({'transfer_scene_id':transfer_scene_id})
    else:
        raise Exception('transfer_scene_id is not assigned')
    if openid:
        params.update({'openid':openid})
    else:
        raise Exception('openid is not assigned')
    if transfer_amount:
        params.update({'transfer_amount':transfer_amount})
    else:
        raise Exception('transfer_amount is not assigned')
    if transfer_remark:
        params.update({'transfer_remark':transfer_remark})
    else:
        raise Exception('transfer_remark is not assigned')
    cipher_data = False
    if user_name and transfer_amount >= 30:
        params.update({'user_name':self._core.encrypt(user_name)})
        cipher_data = True
    if transfer_amount >= 200000 and not user_name:
        raise Exception('user_name is not assigned')
    if user_recv_perception:
        params.update({'user_recv_perception':user_recv_perception})
    if transfer_scene_report_infos:
        params.update({'transfer_scene_report_infos':transfer_scene_report_infos})
    params.update({'appid': appid or self._appid})
    params.update({'notify_url': notify_url or self._notify_url})
    path = '/v3/fund-app/mch-transfer/transfer-bills'
    return await self._core.request(path, method=RequestType.POST, data=params, cipher_data=cipher_data)

async def mch_transfer_bills_cancel(self, out_bill_no):
    """撤销转账
    :param out_bill_no: 商户单号，商户系统内部的商家单号，要求此参数只能由数字、大小写字母组成，在商户系统内部唯一，示例值：'plfk2020042013'
    """
    if out_bill_no:
        path = f'/v3/fund-app/mch-transfer/transfer-bills/out-bill-no/{out_bill_no}/cancel'
    else:
        raise Exception('out_bill_no is not assigned')
    return await self._core.request(path, method=RequestType.POST)

async def mch_transfer_bills_query(self, out_bill_no=None, transfer_bill_no=None):
    """查询转账单
    :param out_bill_no: 商户单号，商户系统内部的商家单号，要求此参数只能由数字、大小写字母组成，在商户系统内部唯一，示例值：'plfk2020042013'
    :param transfer_bill_no: 微信转账单号，微信商家转账系统返回的唯一标识，示例值: '1330000071100999991182020050700019480001'
    """
    if not (out_bill_no or transfer_bill_no):
        raise Exception('out_bill_no or transfer_bill_no is not assigned')
    if out_bill_no:
        path = f'/v3/fund-app/mch-transfer/transfer-bills/out-bill-no/{out_bill_no}'
    else:
        path = f'/v3/fund-app/mch-transfer/transfer-bills/transfer-bill-no/{transfer_bill_no}'
    return await self._core.request(path)

async def mch_transfer_elecsign(self, out_bill_no=None, transfer_bill_no=None):
    """申请电子回单
    :param out_bill_no: 商户单号，商户系统内部的商家单号，要求此参数只能由数字、大小写字母组成，在商户系统内部唯一，示例值：'plfk2020042013'
    :param transfer_bill_no: 微信转账单号，微信商家转账系统返回的唯一标识，示例值: '1330000071100999991182020050700019480001'
    """
    if not (out_bill_no or transfer_bill_no):
        raise Exception('out_bill_no or transfer_bill_no is not assigned')
    params = {}
    if out_bill_no:
        params.update({'out_bill_no':out_bill_no})
        path = '/v3/fund-app/mch-transfer/elecsign/out-bill-no'
    else:
        params.update({'transfer_bill_no':transfer_bill_no})
        path = '/v3/fund-app/mch-transfer/elecsign/transfer-bill-no'
    return await self._core.request(path, method=RequestType.POST, data=params)

async def mch_transfer_elecsign_query(self, out_bill_no=None, transfer_bill_no=None):
    """查询电子回单
    :param out_bill_no: 商户单号，商户系统内部的商家单号，要求此参数只能由数字、大小写字母组成，在商户系统内部唯一，示例值：'plfk2020042013'
    :param transfer_bill_no: 微信转账单号，微信商家转账系统返回的唯一标识，示例值: '1330000071100999991182020050700019480001'
    """
    if not (out_bill_no or transfer_bill_no):
        raise Exception('out_bill_no or transfer_bill_no is not assigned')
    if out_bill_no:
        path = f'/v3/fund-app/mch-transfer/elecsign/out-bill-no/{out_bill_no}'
    else:
        path = f'/v3/fund-app/mch-transfer/elecsign/transfer-bill-no/{transfer_bill_no}'
    return await self._core.request(path)
