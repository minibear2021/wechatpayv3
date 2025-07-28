# 微信支付 API v3 Python SDK - 异步版本使用指南

## 介绍

微信支付接口 V3 版异步 Python 库使用指南。基于 `httpx` 和 `asyncio` 提供高性能异步支付解决方案。

## 适用对象

**wechatpayv3 异步版本**同时支持微信支付[直连模式](https://pay.weixin.qq.com/wiki/doc/apiv3/index.shtml)及[服务商模式](https://pay.weixin.qq.com/wiki/doc/apiv3_partner/index.shtml)，完全兼容同步版本的所有配置参数。

## 异步版本特性

1. **高性能异步操作**：基于 `httpx` 实现非阻塞网络请求，显著提升并发性能；
2. **自动资源管理**：使用 `async with` 语法自动管理连接生命周期，防止资源泄露；
3. **兼容同步接口**：配置参数与同步版本完全一致，迁移成本低；
4. **支持批量操作**：可通过 `asyncio.gather()` 实现批量查询、退款等操作；
5. **Web框架集成**：提供 FastAPI、Tornado 等主流异步框架集成示例。

## 安装

### 异步版本安装
```bash
# 安装包含异步依赖的完整版本
pip install wechatpayv3[async]
```

## 使用方法

### 准备

配置参数与同步版本完全相同，请参考[主项目README](../../../README.md)准备以下参数：

- **商户 API 证书私钥：PRIVATE_KEY**
- **商户 API 证书序列号：CERT_SERIAL_NO**  
- **微信支付 APIv3 密钥：APIV3_KEY**
- **商户号：MCHID**
- **应用ID：APPID**

### 环境变量配置

复制并配置环境变量文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```bash
# 商户配置
WECHATPAY_MCHID=1230000109
WECHATPAY_APPID=wxd678efh567hg6787
WECHATPAY_APIV3_KEY=MIIEvwIBADANBgkqhkiG9w0BAQE...

# 证书配置
WECHATPAY_PRIVATE_KEY_PATH=/path/to/apiclient_key.pem
WECHATPAY_CERT_SERIAL_NO=444F4864EA9B34415...
WECHATPAY_CERT_DIR=./cert

# 业务配置
WECHATPAY_NOTIFY_URL=https://www.xxxx.com/notify
WECHATPAY_TYPE=NATIVE
WECHATPAY_PARTNER_MODE=false
```

### 基础异步使用示例

```python
import asyncio
import json
from wechatpayv3.async_ import AsyncWeChatPay, WeChatPayType

async def main():
    # 读取商户私钥
    with open('/path/to/apiclient_key.pem') as f:
        private_key = f.read()
    
    # 异步客户端配置（与同步版本参数一致）
    async with AsyncWeChatPay(
        wechatpay_type=WeChatPayType.NATIVE,
        mchid='1230000109',
        private_key=private_key,
        cert_serial_no='444F4864EA9B34415...',
        apiv3_key='MIIEvwIBADANBgkqhkiG9w0BAQE...',
        appid='wxd678efh567hg6787',
        notify_url='https://www.xxxx.com/notify',
        cert_dir='./cert',
        partner_mode=False
    ) as wxpay:
        
        # Native支付下单（异步）
        code, message = await wxpay.pay(
            description='异步支付测试',
            out_trade_no='async_demo_001',
            amount={'total': 100},
            pay_type=WeChatPayType.NATIVE
        )
        
        if code == 200:
            result = json.loads(message)
            print(f"支付二维码: {result.get('code_url')}")
            
        # 查询订单状态（异步）
        code, message = await wxpay.query(out_trade_no='async_demo_001')
        if code == 200:
            result = json.loads(message)
            print(f"订单状态: {result.get('trade_state')}")

# 运行异步程序
asyncio.run(main())
```

### 异步 Web 框架集成

#### FastAPI 集成示例

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from wechatpayv3.async_ import AsyncWeChatPay, WeChatPayType

# 全局异步客户端
wxpay = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global wxpay
    # 启动时初始化异步客户端
    with open('/path/to/apiclient_key.pem') as f:
        private_key = f.read()
    
    wxpay = AsyncWeChatPay(
        wechatpay_type=WeChatPayType.NATIVE,
        mchid='1230000109',
        private_key=private_key,
        cert_serial_no='444F4864EA9B34415...',
        apiv3_key='MIIEvwIBADANBgkqhkiG9w0BAQE...',
        appid='wxd678efh567hg6787',
        notify_url='https://www.xxxx.com/notify',
        cert_dir='./cert'
    )
    await wxpay.__aenter__()
    yield
    # 关闭时清理资源
    if wxpay:
        await wxpay.__aexit__(None, None, None)

app = FastAPI(lifespan=lifespan)

class PaymentRequest(BaseModel):
    description: str
    out_trade_no: str
    total: int

@app.post("/pay")
async def create_payment(payment: PaymentRequest):
    code, message = await wxpay.pay(
        description=payment.description,
        out_trade_no=payment.out_trade_no,
        amount={'total': payment.total},
        pay_type=WeChatPayType.NATIVE
    )
    
    if code == 200:
        return {"code": code, "message": message}
    else:
        raise HTTPException(status_code=code, detail=message)

@app.get("/query/{out_trade_no}")
async def query_payment(out_trade_no: str):
    code, message = await wxpay.query(out_trade_no=out_trade_no)
    return {"code": code, "message": message}

# 运行服务器
# uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Tornado 集成示例

```python
import tornado.web
import tornado.ioloop
from wechatpayv3.async_ import AsyncWeChatPay, WeChatPayType

# 配置参数
with open('/path/to/apiclient_key.pem') as f:
    private_key = f.read()

WECHATPAY_CONFIG = {
    'wechatpay_type': WeChatPayType.NATIVE,
    'mchid': '1230000109',
    'private_key': private_key,
    'cert_serial_no': '444F4864EA9B34415...',
    'apiv3_key': 'MIIEvwIBADANBgkqhkiG9w0BAQE...',
    'appid': 'wxd678efh567hg6787',
    'notify_url': 'https://www.xxxx.com/notify',
    'cert_dir': './cert'
}

class PaymentHandler(tornado.web.RequestHandler):
    async def post(self):
        # 每个请求使用独立的异步客户端
        async with AsyncWeChatPay(**WECHATPAY_CONFIG) as wxpay:
            import json
            data = json.loads(self.request.body)
            
            code, message = await wxpay.pay(
                description=data['description'],
                out_trade_no=data['out_trade_no'],
                amount={'total': data['total']},
                pay_type=WeChatPayType.NATIVE
            )
            
            self.write({"code": code, "message": message})

class QueryHandler(tornado.web.RequestHandler):
    async def get(self, out_trade_no):
        async with AsyncWeChatPay(**WECHATPAY_CONFIG) as wxpay:
            code, message = await wxpay.query(out_trade_no=out_trade_no)
            self.write({"code": code, "message": message})

def make_app():
    return tornado.web.Application([
        (r"/pay", PaymentHandler),
        (r"/query/([^/]+)", QueryHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Tornado server started on port 8888")
    tornado.ioloop.IOLoop.current().start()
```

### 异步操作模式对比

| 操作场景 | 同步版本 | 异步版本 |
|---------|---------|---------|
| 单笔支付 | `wxpay.pay(...)` | `await wxpay.pay(...)` |
| 批量查询 | 循环调用，阻塞等待 | `await asyncio.gather(*tasks)` |
| Web集成 | Flask/Django等同步框架 | FastAPI/Tornado等异步框架 |
| 并发性能 | 受GIL限制，需要多进程 | 单进程高并发，资源利用率高 |

### 异步批量操作示例

```python
async def batch_query_orders(wxpay, order_list):
    """批量查询订单状态"""
    tasks = []
    for order_no in order_list:
        task = wxpay.query(out_trade_no=order_no)
        tasks.append(task)
    
    # 并发执行所有查询
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    success_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"订单 {order_list[i]} 查询失败: {result}")
        else:
            code, message = result
            if code == 200:
                success_results.append((order_list[i], message))
    
    return success_results

# 使用示例
async with AsyncWeChatPay(**config) as wxpay:
    order_list = ['order_001', 'order_002', 'order_003']
    results = await batch_query_orders(wxpay, order_list)
```


## 常见问题


### 1. 同步转异步
**问题**: 将同步代码改为异步版本

**解决方案**:
```python
# 同步版本
wxpay = WeChatPay(**config)
code, result = wxpay.pay(...)

# 异步版本
async with AsyncWeChatPay(**config) as wxpay:
    code, result = await wxpay.pay(...)
```

## 完整示例项目

查看以下完整示例：

- [FastAPI集成示例](fastapi_example.py) - 展示FastAPI框架集成
- [Tornado集成示例](tornado_example.py) - 展示Tornado框架集成
- [环境配置示例](.env.example) - 环境变量配置模板

## 接口说明

异步版本支持同步版本的所有接口，调用方式为在接口前加 `await`：

| 功能 | 同步调用 | 异步调用 |
|------|---------|---------|
| 支付下单 | `wxpay.pay(...)` | `await wxpay.pay(...)` |
| 查询订单 | `wxpay.query(...)` | `await wxpay.query(...)` |
| 申请退款 | `wxpay.refund(...)` | `await wxpay.refund(...)` |
| 关闭订单 | `wxpay.close(...)` | `await wxpay.close(...)` |

详细接口列表请参考[主项目文档](../../../docs/apis.md)。

## 注意事项

1. **必须使用异步上下文管理器**：`async with AsyncWeChatPay(...) as wxpay:`
2. **所有接口调用必须使用await**：`await wxpay.pay(...)`
3. **配置参数与同步版本完全一致**，迁移成本低
4. **适合高并发场景**，单个请求延迟略高于同步版本
5. **需要异步框架支持**，如FastAPI、Tornado、aiohttp等

异步版本在高并发场景下具有显著性能优势，特别适合需要处理大量支付请求的电商、金融等应用场景。