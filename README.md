# 微信支付 API v3 Python SDK

[![PyPI version](https://badge.fury.io/py/wechatpayv3.svg)](https://badge.fury.io/py/wechatpayv3)
[![Download count](https://img.shields.io/pypi/dm/wechatpayv3)](https://img.shields.io/pypi/dm/wechatpayv3)

## 介绍

微信支付接口 V3 版 python 库。

欢迎微信支付开发者扫码进 QQ 群(群号：973102221)讨论，欢迎提交代码，欢迎star、follow、fork：

![image](qq.png)

## 适用对象

**wechatpayv3**同时支持微信支付[直连模式](https://pay.weixin.qq.com/wiki/doc/apiv3/index.shtml)及[服务商模式](https://pay.weixin.qq.com/wiki/doc/apiv3_partner/index.shtml)，接口说明详见官网 。

## 特性

1. 平台证书自动更新，无需开发者关注平台证书有效性，无需手动下载更新；
2. 支持本地缓存平台证书，初始化时指定平台证书保存目录即可；
3. 敏感信息直接传入明文参数，SDK 内部自动加密，无需手动处理；
4. 回调通知自动验证回调消息，自动解密 resource 对象，并返回解密后的数据；
5. 已适配[直连模式](https://pay.weixin.qq.com/wiki/doc/apiv3/apis/index.shtml)和[服务商模式](https://pay.weixin.qq.com/wiki/doc/apiv3_partner/apis/index.shtml)中除“电商收付通”以外所有 v3 版接口。

## 源码

[github](https://github.com/minibear2021/wechatpayv3)

[gitee](https://gitee.com/minibear2021/wechatpayv3)

## 安装

```
$ pip install wechatpayv3
```

## 使用方法

### 准备

参考微信官方文档准备好密钥, 证书文件和配置([证书/密钥/签名介绍](https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_0.shtml))

- **商户 API 证书私钥：PRIVATE_KEY**。商户申请商户 API 证书时，会生成商户私钥，并保存在本地证书文件夹的文件 apiclient_key.pem 中。
  > :warning: 不要把私钥文件暴露在公共场合，如上传到 Github，写在客户端代码等。
- **商户 API 证书序列号：CERT_SERIAL_NO**。每个证书都有一个由 CA 颁发的唯一编号，即证书序列号。扩展阅读 [如何查看证书序列号](https://wechatpay-api.gitbook.io/wechatpay-api-v3/chang-jian-wen-ti/zheng-shu-xiang-guan#ru-he-cha-kan-zheng-shu-xu-lie-hao) 。
- **微信支付 APIv3 密钥：APIV3_KEY**，是在回调通知和微信支付平台证书下载接口中，为加强数据安全，对关键信息 `AES-256-GCM` 加密时使用的对称加密密钥。

### 一个最小的后端

[examples.py](examples.py) 演示了一个带有[Native 支付下单](https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter3_4_1.shtml)接口和[支付通知](https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter3_4_5.shtml)接口的后端。
首先，修改 **examplys.py** 里以下几项配置参数：

```python
# 微信支付商户号，服务商模式下为服务商户号，即官方文档中的sp_mchid。
MCHID = '1230000109'

# 商户证书私钥
with open('path_to_key/apiclient_key.pem') as f:
    PRIVATE_KEY = f.read()

# 商户证书序列号
CERT_SERIAL_NO = '444F4864EA9B34415...'

# API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
APIV3_KEY = 'MIIEvwIBADANBgkqhkiG9w0BAQE...'

# APPID，应用ID，服务商模式下为服务商应用ID，即官方文档中的sp_appid
APPID = 'wxd678efh567hg6787'

# 回调地址，也可以在调用接口的时候覆盖
NOTIFY_URL = 'https://www.xxxx.com/notify'

# 微信支付平台证书缓存目录，初始调试的时候可以设为None
CERT_DIR = './cert'

# 日志记录器，记录web请求和回调细节，便于调试排错
logging.basicConfig(filename=os.path.join(os.getcwd(), 'demo.log'), level=logging.DEBUG, filemode='a', format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger("demo")

# 接入模式：False=直连商户模式，True=服务商模式
PARTNER_MODE = False

# 代理设置，None或者{"https": "http://10.10.1.10:1080"}，详细格式参见https://docs.python-requests.org/zh_CN/latest/user/advanced.html
PROXY = None
```

接下来初始化 WechatPay 实例并配置一个合适的接口：

```python
wxpay = WeChatPay(
    wechatpay_type=WeChatPayType.NATIVE,
    mchid=MCHID,
    private_key=PRIVATE_KEY,
    cert_serial_no=CERT_SERIAL_NO,
    apiv3_key=APIV3_KEY,
    appid=APPID,
    notify_url=NOTIFY_URL,
    cert_dir=CERT_DIR,
    logger=LOGGER,
    partner_mode=PARTNER_MODE,
    proxy=PROXY)

app = Flask(__name__)

@app.route('/pay')
def pay():
    # 以native下单为例，下单成功后即可获取到'code_url'，将'code_url'转换为二维码，并用微信扫码即可进行支付测试。
    out_trade_no = ''.join(sample(ascii_letters + digits, 8))
    description = 'demo-description'
    amount = 1
    code, message = wxpay.pay(
        description=description,
        out_trade_no=out_trade_no,
        amount={'total': amount}
    )
    return jsonify({'code': code, 'message': message})
```

检查一下参数无误，现在就可以用 python 解释器来运行：

```shell
$ python examples.py
 * Serving Flask app "examples" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

现在访问 http://127.0.0.1:5000/pay ，如果一切正常，你会看到下面一串 json 字符串：

```python
{
  "code": 200,
  "message": "{\"code_url\":\"weixin://wxpay/bizpayurl?pr=abcdefghi\"}"
}
```

到这一步统一下单的后端就完成了，现在将 code_url 的值即"weixin://wxpay/bizpayurl?pr=abcdefghi"用[草料](https://cli.im/)转换为二维码即可用微信扫码进行支付测试。

**以上步骤如果不能正确执行，务必仔细检查各项初始化参数，必要的情况下，登录微信支付后台，将所有参数重置。**

Native 支付调试最简单便捷，调试通过没有问题证明初始化参数正确之后，如果需要采用其他（小程序、H5、JSAPI、APP）支付下单，可继续参考 examples.py。

## 接口清单

已适配的微信支付 V3 版 API 接口列表如下，部分接口调用示例可以参考[这里](interface.md)：

| 大类| 小类 | 接口 | 接口函数| 直连商户适用 | 服务商适用 |
| ---- | ---------------------------------------- | ------------------------ | --------------------------------------- | ------------ | ---------- |
| 公用| 公用 | 调起支付签名| sign | 是 | 是 |
| 公用| 公用 | 回调通知| callback | 是 | 是 |
| 公用| 公用 | 敏感信息参数解密 | decrypt | 是 | 是 |
| 公用| 公用 | 下载账单| download_bill| 是 | 是 |
| 商户进件 | 特约商户进件| 提交申请单 | applyment_submit | 否| 是|
| 商户进件 | 特约商户进件| 查询申请单状态| applyment_query| 否| 是|
| 商户进件 | 特约商户进件| 修改结算账号| applyment_settlement_modify| 否| 是|
| 商户进件 | 特约商户进件| 查询结算账号| applyment_settlement_query| 否| 是|
| 基础支付 | JSAPI、APP、H5、Native、小程序支付| 统一下单 | pay | 是| 是|
| 基础支付 | JSAPI、APP、H5、Native、小程序支付| 查询订单 | query | 是| 是|
| 基础支付 | JSAPI、APP、H5、Native、小程序支付| 关闭订单 | close | 是| 是|
| 基础支付 | 合单支付 | 统一下单 | combine_pay| 是| 是|
| 基础支付 | 合单支付 | 查询订单 | combine_query| 是| 是|
| 基础支付 | 合单支付 | 关闭订单 | combine_close| 是| 是|
| 基础支付 | JSAPI、APP、H5、Native、小程序、合单支付 | 申请退款 | refund| 是| 是|
| 基础支付 | JSAPI、APP、H5、Native、小程序、合单支付 | 查询单笔退款| query_refund | 是| 是|
| 基础支付 | JSAPI、APP、H5、Native、小程序、合单支付 | 申请交易账单| trade_bill | 是| 是|
| 基础支付 | JSAPI、APP、H5、Native、小程序、合单支付 | 申请资金账单| fundflow_bill| 是| 是|
| 基础支付 | JSAPI、APP、H5、Native、小程序、合单支付 | 申请单个子商户资金账单 | submch_fundflow_bill| 否| 是|
| 基础支付 | JSAPI、APP、H5、Native、小程序、合单支付 | 下载账单 | download_bill| 是| 是|
| 经营能力 | 微信支付分（免确认模式） | 创单结单合并| payscore_direct_complete| 是| 否|
| 经营能力 | 微信支付分（免确认预授权模式）| 商户预授权 | payscore_permission | 是| 否|
| 经营能力 | 微信支付分（免确认预授权模式）| 查询用户授权记录| payscore_permission_query | 是| 否|
| 经营能力 | 微信支付分（免确认预授权模式）| 解除用户授权关系| payscore_permission_terminate| 是| 否|
| 经营能力 | 微信支付分（公共 API） | 创建支付分订单| payscore_create| 是| 否|
| 经营能力 | 微信支付分（公共 API） | 查询支付分订单| payscore_query | 是| 否|
| 经营能力 | 微信支付分（公共 API） | 取消支付分订单| payscore_cancel| 是| 否|
| 经营能力 | 微信支付分（公共 API） | 修改订单金额| payscore_modify| 是| 否|
| 经营能力 | 微信支付分（公共 API） | 完结支付分订单| payscore_complete| 是| 否|
| 经营能力 | 微信支付分（公共 API） | 商户发起催收扣款| payscore_pay | 是| 否|
| 经营能力 | 微信支付分（公共 API） | 同步服务订单信息| payscore_sync| 是| 否|
| 经营能力 | 微信支付分（公共 API） | 申请退款 | payscore_refund| 是| 否|
| 经营能力 | 微信支付分（公共 API） | 查询单笔退款| payscore_refund_query | 是| 否|
| 经营能力 | 微信支付分（公共 API） | 商户申请获取对账单| payscore_merchant_bill| 是| 否|
| 经营能力 | 支付即服务| 服务人员注册| guides_register| 是| 是|
| 经营能力 | 支付即服务| 服务人员分配| guides_assign| 是| 是|
| 经营能力 | 支付即服务| 服务人员查询| guides_query | 是| 是|
| 经营能力 | 支付即服务| 服务人员信息更新| guides_update| 是| 是|
| 经营能力 | 点金计划 | 点金计划管理| goldplan_plan_change| 否| 是|
| 经营能力 | 点金计划 | 商家小票管理| goldplan_custompage_change| 否| 是|
| 经营能力 | 点金计划 | 同业过滤标签管理| goldplan_advertising_filter| 否| 是|
| 经营能力 | 点金计划 | 开通广告展示| goldplan_advertising_open | 否| 是|
| 经营能力 | 点金计划 | 关闭广告展示| goldplan_advertising_close| 否| 是|
| 行业方案 | 电商收付通| 尚未适配 | 尚未适配| 否| 是|
| 行业方案 | 智慧商圈 | 商圈积分同步| points_notify| 是| 是|
| 行业方案 | 智慧商圈 | 商圈积分授权查询| user_authorization| 是| 是|
| 行业方案 | 微信支付分停车服务| 查询车牌服务开通信息| parking_service_find| 是| 是|
| 行业方案 | 微信支付分停车服务| 创建停车入场| parking_enter| 是| 是|
| 行业方案 | 微信支付分停车服务| 扣费受理 | parking_order| 是| 是|
| 行业方案 | 微信支付分停车服务| 查询订单 | parking_query| 是| 是|
| 营销工具 | 代金券 | 创建代金券批次| marketing_favor_stock_create | 是| 是|
| 营销工具 | 代金券 | 激活代金券批次| marketing_favor_stock_start| 是| 是|
| 营销工具 | 代金券 | 发放代金券批次| marketing_favor_stock_send| 是| 是|
| 营销工具 | 代金券 | 暂停代金券批次| marketing_favor_stock_pause| 是| 是|
| 营销工具 | 代金券 | 重启代金券批次| marketing_favor_stock_restart| 是| 是|
| 营销工具 | 代金券 | 条件查询批次列表| marketing_favor_stock_list| 是| 是|
| 营销工具 | 代金券 | 查询批次详情| marketing_favor_stock_detail | 是| 是|
| 营销工具 | 代金券 | 查询代金券详情| marketing_favor_coupon_detail| 是| 是|
| 营销工具 | 代金券 | 查询代金券可用商户| marketing_favor_stock_merchant | 是| 是|
| 营销工具 | 代金券 | 查询代金券可用单品| marketing_favor_stock_item| 是| 是|
| 营销工具 | 代金券 | 根据商户号查用户的券| marketing_favor_user_coupon| 是| 是|
| 营销工具 | 代金券 | 下载批次核销明细| marketing_favor_use_flow| 是| 是|
| 营销工具 | 代金券 | 下载批次退款明细| marketing_favor_refund_flow| 是| 是|
| 营销工具 | 代金券 | 设置消息通知地址| marketing_favor_callback_update| 是| 是|
| 营销工具 | 商家券 | 创建商家券 | marketing_busifavor_stock_create | 是| 是|
| 营销工具 | 商家券 | 查询商家券详情| marketing_busifavor_stock_query| 是| 是|
| 营销工具 | 商家券 | 核销用户券 | marketing_busifavor_coupon_use | 是| 是|
| 营销工具 | 商家券 | 根据过滤条件查询用户券 | marketing_busifavor_user_coupon| 是| 是|
| 营销工具 | 商家券 | 查询用户单张券详情| marketing_busifavor_coupon_detail| 是| 是|
| 营销工具 | 商家券 | 上传预存 code | marketing_busifavor_couponcode_upload | 是| 是|
| 营销工具 | 商家券 | 设置商家券事件通知地址 | marketing_busifavor_callback_update| 是| 是|
| 营销工具 | 商家券 | 查询商家券事件通知地址 | marketing_busifavor_callback_query | 是| 是|
| 营销工具 | 商家券 | 关联订单信息| marketing_busifavor_coupon_associate| 是| 是|
| 营销工具 | 商家券 | 取消关联订单信息| marketing_busifavor_coupon_disassociate | 是| 是|
| 营销工具 | 商家券 | 修改批次预算| marketing_busifavor_stock_budget | 是| 是|
| 营销工具 | 商家券 | 修改商家券基本信息| marketing_busifavor_stock_modify | 是| 是|
| 营销工具 | 商家券 | 申请退券 | marketing_busifavor_coupon_return| 是| 是|
| 营销工具 | 商家券 | 使券失效 | marketing_busifavor_coupon_deactivate | 是| 是|
| 营销工具 | 商家券 | 营销补差付款| marketing_busifavor_subsidy_pay| 是| 是|
| 营销工具 | 商家券 | 查询营销补差付款单详情 | marketing_busifavor_subsidy_query| 是| 是|
| 营销工具 | 委托营销 | 建立合作关系| marketing_partnership_build| 是| 是|
| 营销工具 | 委托营销 | 查询合作关系列表| marketing_partnership_query| 是| 是|
| 营销工具 | 消费卡 | 发放消费卡 | marketing_card_send | 是| 否|
| 营销工具 | 支付有礼 | 创建全场满额送活动| marketing_paygift_activity_create| 是| 是|
| 营销工具 | 支付有礼 | 查询活动详情接口| marketing_paygift_activity_detail| 是| 是|
| 营销工具 | 支付有礼 | 查询活动发券商户号| marketing_paygift_merchants_list | 是| 是|
| 营销工具 | 支付有礼 | 查询活动指定商品列表| marketing_paygift_goods_list | 是| 是|
| 营销工具 | 支付有礼 | 终止活动 | marketing_paygift_activity_terminate| 是| 是|
| 营销工具 | 支付有礼 | 新增活动发券商户号| marketing_paygift_merchant_add | 是| 是|
| 营销工具 | 支付有礼 | 获取支付有礼活动列表| marketing_paygift_activity_list| 是| 是|
| 营销工具 | 支付有礼 | 删除活动发券商户号| marketing_paygift_merchant_delete| 是| 是|
| 营销工具 | 代扣服务切卡组件 | 出行券切卡组件预下单| industry_coupon_token| 是| 是|
| 营销工具 | 图片上传 | 图片上传(营销专用)| marketing_image_upload| 是| 是|
| 资金应用 | 商家转账到零钱 | 发起商家转账 | transfer_batch | 是| 否|
| 资金应用 | 商家转账到零钱 | 微信批次单号查询批次单| transfer_query_batchid | 是| 否|
| 资金应用 | 商家转账到零钱 | 微信明细单号查询明细单| transfer_query_detail_id | 是| 否|
| 资金应用 | 商家转账到零钱 | 商家批次单号查询批次单| transfer_query_out_batch_no | 是| 否|
| 资金应用 | 商家转账到零钱 | 商家明细单号查询明细单| transfer_query_out_detail_no | 是| 否|
| 资金应用 | 商家转账到零钱 | 转账电子回单申请受理 | transfer_bill_receipt | 是| 否|
| 资金应用 | 商家转账到零钱 | 查询转账电子回单| transfer_query_bill_receipt | 是| 否|
| 资金应用 | 商家转账到零钱 | 转账明细电子回单受理| transfer_detail_receipt | 是| 否|
| 资金应用 | 商家转账到零钱 | 查询转账明细电子回单受理结果| transfer_query_receipt | 是| 否|
| 资金应用 | 分账 | 请求分账 | profitsharing_order | 是| 是|
| 资金应用 | 分账 | 查询分账结果| profitsharing_order_query | 是| 是|
| 资金应用 | 分账 | 请求分账回退| profitsharing_return| 是| 是|
| 资金应用 | 分账 | 查询分账回退结果| profitsharing_return_query| 是| 是|
| 资金应用 | 分账 | 解冻剩余资金| profitsharing_unfreeze| 是| 是|
| 资金应用 | 分账 | 查询剩余待分金额| profitsharing_amount_query| 是| 是|
| 资金应用 | 分账 | 查询最大分账比例| profitsharing_config_query| 否| 是|
| 资金应用 | 分账 | 添加分账接收方| profitsharing_add_receiver| 是| 是|
| 资金应用 | 分账 | 删除分账接收方| profitsharing_delete_receiver| 是| 是|
| 资金应用 | 分账 | 申请分账账单| profitsharing_bill| 是| 是|
| 资金应用 | 分账 | 下载账单 | download_bill| 是| 是|
| 资金应用 | 连锁品牌分账 | 请求分账 | brand_profitsharing_order | 否| 是|
| 资金应用 | 连锁品牌分账 | 查询分账结果| brand_profitsharing_order_query| 否| 是|
| 资金应用 | 连锁品牌分账 | 请求分账回退| brand_profitsharing_return| 否| 是|
| 资金应用 | 连锁品牌分账 | 查询分账回退结果| brand_profitsharing_return_query | 否| 是|
| 资金应用 | 连锁品牌分账 | 完结分账 | brand_profitsharing_unfreeze | 否| 是|
| 资金应用 | 连锁品牌分账 | 查询剩余待分金额| brand_profitsharing_amount_query | 否| 是|
| 资金应用 | 连锁品牌分账 | 查询最大分账比例| brand_profitsharing_config_query | 否| 是|
| 资金应用 | 连锁品牌分账 | 添加分账接收方| brand_profitsharing_add_receiver | 否| 是|
| 资金应用 | 连锁品牌分账 | 删除分账接收方| brand_profitsharing_delete_receiver| 否| 是|
| 资金应用 | 连锁品牌分账 | 申请分账账单| profitsharing_bill| 否| 是|
| 资金应用 | 连锁品牌分账 | 下载账单 | download_bill| 是| 是|
| 风险合规 | 商户开户意愿确认 | 提交申请单 | apply4subject_submit| 否| 是|
| 风险合规 | 商户开户意愿确认 | 撤销申请单 | apply4subject_cancel| 否| 是|
| 风险合规 | 商户开户意愿确认 | 查询申请单审核结果| apply4subject_query | 否| 是|
| 风险合规 | 商户开户意愿确认 | 获取商户开户意愿确认状态 | apply4subject_state | 否| 是|
| 风险合规 | 消费者投诉 2.0 | 查询投诉单列表| complaint_list_query| 是| 是|
| 风险合规 | 消费者投诉 2.0 | 查询投诉单详情| complaint_detail_query| 是| 是|
| 风险合规 | 消费者投诉 2.0 | 查询投诉协商历史| complaint_history_query | 是| 是|
| 风险合规 | 消费者投诉 2.0 | 创建投诉通知回调地址| complaint_notification_create| 是| 是|
| 风险合规 | 消费者投诉 2.0 | 查询投诉通知回调地址| complaint_notification_query | 是| 是|
| 风险合规 | 消费者投诉 2.0 | 更新投诉通知回调地址| complaint_notification_update| 是| 是|
| 风险合规 | 消费者投诉 2.0 | 删除投诉通知回调地址| complaint_notification_delete| 是| 是|
| 风险合规 | 消费者投诉 2.0 | 提交回复 | complaint_response| 是| 是|
| 风险合规 | 消费者投诉 2.0 | 反馈处理完成| complaint_complete| 是| 是|
| 风险合规 | 消费者投诉 2.0 | 更新退款审批结果| complaint_update_refund| 是| 是|
| 风险合规 | 消费者投诉 2.0 | 商户上传反馈图片| complaint_image_upload| 是| 是|
| 风险合规 | 消费者投诉 2.0 | 图片下载 | complaint_image_download| 是| 是|
| 风险合规 | 商户违规通知回调 | 创建商户违规通知回调地址 | merchantrisk_callback_create | 否| 是|
| 风险合规 | 商户违规通知回调 | 查询商户违规通知回调地址 | merchantrisk_callback_query| 否| 是|
| 风险合规 | 商户违规通知回调 | 修改商户违规通知回调地址 | merchantrisk_callback_update | 否| 是|
| 风险合规 | 商户违规通知回调 | 删除商户违规通知回调地址 | merchantrisk_callback_delete | 否| 是|
| 其他能力 | 图片上传 | 图片上传 | image_upload | 是| 是|
| 其他能力 | 视频上传 | 视频上传 | video_upload | 是| 是|
| 其他 | 电子发票（公共API） | 创建电子发票卡券模板 | fapiao_card_template | 是 | 是 |
| 其他 | 电子发票（公共API） | 配置开发选项 | fapiao_set_merchant_config | 是 | 是 |
| 其他 | 电子发票（公共API） | 查询商户配置的开发选项 | fapiao_merchant_config | 是 | 是 |
| 其他 | 电子发票（公共API） | 获取抬头填写链接 | fapiao_title_url | 是 | 是 |
| 其他 | 电子发票（公共API） | 获取用户填写的抬头 | fapiao_title | 是 | 是 |
| 其他 | 电子发票(区块链模式) | 获取商品和服务税收分类对照表 | fapiao_tax_codes | 是 | 是 |
| 其他 | 电子发票(区块链模式) | 获取商户开票基础信息 | fapiao_merchant_base_info | 是 | 是 |
| 其他 | 电子发票(区块链模式) | 开具电子发票 | fapiao_applications | 是 | 是 |
| 其他 | 电子发票(区块链模式) | 查询电子发票 | fapiao_query | 是 | 是 |
| 其他 | 电子发票(区块链模式) | 冲红电子发票 | fapiao_reverse | 是 | 是 |
| 其他 | 电子发票(自建平台模式) | 上传电子发票文件 | fapiao_upload_file | 是 | 是 |
| 其他 | 电子发票(自建平台模式) | 将电子发票插入微信用户卡包 | fapiao_insert_cards | 是 | 是 |
| 其他 | 银行组件 | 获取对私银行卡号开户银行 | capital_search_bank_number | 是 | 是 |
| 其他 | 银行组件 | 查询支持个人业务的银行列表 | capital_personal_banks | 是 | 是 |
| 其他 | 银行组件 | 查询支持对公业务的银行列表 | capital_corporate_banks | 是 | 是 |
| 其他 | 银行组件 | 查询省份列表 | capital_provinces | 是 | 是 |
| 其他 | 银行组件 | 查询城市列表 | capital_cities | 是 | 是 |
| 其他 | 银行组件 | 查询支行列表 | capital_branches | 是 | 是 |

### 接口函数参数

参数类型对照参考下表：

| 微信支付官方文档声明 | **wechatpayv3 python sdk** |
| -------------------- | -------------------------- |
| string | str |
| int| int |
| object | dict: {} |
| array| list: [] |
| boolean| bool: True, False |
| message| bytes|

### 接口函数返回值

每个接口均同步返回 code 和 message，code 为 web 请求得到的 HTTP 状态码，message 为服务器返回的 json 字符串。
例外：

1. 回调通知（callback）接口将收到的参数解密后返回，回调验证不合规或解密失败则返回 None；
2. 下载账单（download_bill）和消费者投诉 2.0 的图片下载（complaint_image_download）接口返回的 message 为 bytes 类型，直接将 message 写入磁盘即可获得对应的目标文件。

## 常见问题

### 回调验证失败处理

开发者遇到的难点之一就是回调验证失败的问题，由于众多的 python web 框架对回调消息的处理不完全一致，如果出现回调验证失败，请务必确认传入的 headers 和 body 的值和类型。
通常框架传过来的 headers 类型是 dict，而 body 类型是 bytes。使用以下方法可直接获取到解密后的实际内容。

#### flask 框架

直接传入 request.headers 和 request.data 即可。

```python
result = wxpay.callback(headers=request.headers, body=request.data)
```

#### django 框架

由于 django 框架特殊性，会将 headers 做一定的预处理，可以参考以下方式调用。

```python
headers = {}
headers.update({'Wechatpay-Signature': request.META.get('HTTP_WECHATPAY_SIGNATURE')})
headers.update({'Wechatpay-Timestamp': request.META.get('HTTP_WECHATPAY_TIMESTAMP')})
headers.update({'Wechatpay-Nonce': request.META.get('HTTP_WECHATPAY_NONCE')})
headers.update({'Wechatpay-Serial': request.META.get('HTTP_WECHATPAY_SERIAL')})
result = wxpay.callback(headers=headers, body=request.body)
```

#### tornado 框架

直接传入 request.headers 和 request.body 即可。

```python
result = wxpay.callback(headers=request.headers, body=request.body)
```

#### 其他框架

参考以上处理方法，大原则就是保证传给 callback 的参数值和收到的值一致，不要转换为 dict，也不要转换为 string。

### 接口清单里怎么没有回调接口

所有的回调接口都通过公用接口 callback 处理，因此清单里没有一一罗列。

### 服务商模式如何接入

SDK 默认为直连商户接入，如果初始化时候指定 partner_mode=True，即切换为服务商模式。需要注意的是，一部分接口为直连商户专有，一部分接口为服务商模式专有，另有部分接口同时兼容直连商户和服务商，这些同时兼容的接口在两种模式下个别参数要求会稍有不同。

### 如何下载平台证书？

SDK 内部已经实现了自动下载和加载平台证书，无需预先下载。如需了解具体实现逻辑，可以参阅[core.py](wechatpayv3/core.py)中的\_update_certificates 函数。

### 接口始终返回 500 错误

通常为初始化参数配置错误，如果反复检查无果，建议进入微信支付后台重置所有参数后再试。

### 回调接口始终校验失败

查阅 web 框架文档，确保传入 callback 的 body 参数没有经过任何转义，通常为 bytes 类型。

### 下载平台证书时解析失败

检查 APIV3_KEY 是否和微信支付后台设置的一致，如无法确认，建议重置后再试。

## 签名、验签、加密、解密的内部实现

一般应用开发者可以不用向下看了，有心了解这几项内部实现的可以参考[这里](security.md)了解。
