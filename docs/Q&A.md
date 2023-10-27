# 常见问题

## 获取不到微信支付平台证书

报异常："No wechatpay platform certificate ..."，检查所有初始化参数。
特别是无法显式确认是否正确的api v3 key，直接重置后再试。

## 回调验证失败处理

开发者遇到的难点之一就是回调验证失败的问题，由于众多的 python web 框架对回调消息的处理不完全一致，如果出现回调验证失败，请务必确认传入的 headers 和 body 的值和类型。
通常框架传过来的 headers 类型是 dict，而 body 类型是 bytes。flask 框架参考以下方法可直接获取到解密后的实际内容。

```python
@app.route('/notify', methods=['POST'])
def notify():
    result = wxpay.callback(request.headers, request.data)
    if result and result.get('event_type') == 'TRANSACTION.SUCCESS':
        resource = result.get('resource')
        appid = resource.get('appid')
        mchid = resource.get('mchid')
        out_trade_no = resource.get('out_trade_no')
        transaction_id = resource.get('transaction_id')
        trade_type = resource.get('trade_type')
        trade_state = resource.get('trade_state')
        trade_state_desc = resource.get('trade_state_desc')
        bank_type = resource.get('bank_type')
        attach = resource.get('attach')
        success_time = resource.get('success_time')
        payer = resource.get('payer')
        amount = resource.get('amount').get('total')
        # TODO: 根据返回参数进行必要的业务处理，处理完后返回200或204
        return jsonify({'code': 'SUCCESS', 'message': '成功'})
    else:
        return jsonify({'code': 'FAILED', 'message': '失败'}), 500
```

### flask 框架

如上面示例，直接传入 request.headers 和 request.data 即可。

```python
result = wxpay.callback(headers=request.headers, body=request.data)
```

### django 框架

由于 django 框架特殊性，会将 headers 做一定的预处理，可以参考以下方式调用。

```python
headers = {
    'Wechatpay-Signature': request.META.get('HTTP_WECHATPAY_SIGNATURE'),
    'Wechatpay-Timestamp': request.META.get('HTTP_WECHATPAY_TIMESTAMP'),
    'Wechatpay-Nonce': request.META.get('HTTP_WECHATPAY_NONCE'),
    'Wechatpay-Serial': request.META.get('HTTP_WECHATPAY_SERIAL')
}
result = wxpay.callback(headers=headers, body=request.body)
```

### FastAPI 框架

由于 FastAPI 框架特殊性，会将 headers 做一定的预处理，可以参考以下方式调用。

```python
headers = {
    'Wechatpay-Signature': request.headers.get('wechatpay-signature'),
    'Wechatpay-Timestamp': request.headers.get('wechatpay-timestamp'),
    'Wechatpay-Nonce': request.headers.get('wechatpay-nonce'),
    'Wechatpay-Serial': request.headers.get('wechatpay-serial')
}
result = wxpay.callback(headers=headers, body=await request.body())
```

### tornado 框架

直接传入 request.headers 和 request.body 即可。

```python
result = wxpay.callback(headers=request.headers, body=request.body)
```

### 其他框架

参考以上处理方法，大原则就是保证传给 callback 的参数值和收到的值一致，不要转换为 dict，也不要转换为 string。

## 反复收到同一个回调消息怎么处理

实际开发中处理微信支付通知消息时有两个问题需要注意。一是可能会重复收到同一个通知消息，需要在代码中进行判断处理。另一个是处理消息的时间如果过长，建议考虑异步处理，先缓存消息，避免微信支付服务器端认为超时，如果持续超时，微信支付服务器端可能会认为回调消息接口不可用。

## 接口清单里怎么没有回调接口

所有的回调接口都通过公用接口 callback 处理，因此清单里没有一一罗列。对于收到的回调消息，可以通过 event_type 参数判断消息类型进行下一步处理，具体参数清单参考微信支付官方文档。
如果多个商户号使用同一个回调地址进行处理的，可以在配置回调地址的时候加入特定的参数来进行区分。

## 账单下载得到的文件是什么格式的

SDK 里涉及到账单下载的接口默认都是返回的gzip格式，可以"import gzip"后解压，获取到实际的账单文件。

## 服务商模式如何接入

SDK 默认为直连商户接入，如果初始化时候指定 partner_mode=True，即切换为服务商模式。需要注意的是，一部分接口为直连商户专有，一部分接口为服务商模式专有，另有部分接口同时兼容直连商户和服务商，这些同时兼容的接口在两种模式下个别参数要求会稍有不同。

## 如何下载平台证书？

SDK 内部已经实现了自动下载和加载平台证书，无需预先下载。如需了解具体实现逻辑，可以参阅[core.py](../wechatpayv3/core.py)中的 \_update_certificates 函数。

## 参数确认无误，下载平台证书仍然失败

检查一下服务器时间，接口调用时，时间戳会被作为参数传递给微信支付服务器，偏差过大的时间戳会被服务器判断为不可信调用。另外，证书有效性验证也需要和本机时间作对比。

## 接口始终返回 500 错误

通常为初始化参数配置错误，如果反复检查无果，建议进入微信支付后台重置所有参数后再试。

## 回调接口始终校验失败

查阅 web 框架文档，确保传入 callback 的 body 参数没有经过任何转义，通常为 bytes 类型。

## 下载平台证书时解析失败

检查 APIV3_KEY 是否和微信支付后台设置的一致，如无法确认，建议重置后再试。
