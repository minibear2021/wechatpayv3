#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI async example for WeChat Pay v3 SDK
演示如何在 FastAPI 中使用异步版本的微信支付 SDK
"""

import json
import logging
import os
from datetime import datetime
from typing import Optional

from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from wechatpayv3.async_ import AsyncWeChatPay, WeChatPayType

# 加载环境变量
load_dotenv()

# 配置日志
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

# 全局 WeChat Pay 实例
wxpay: Optional[AsyncWeChatPay] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    global wxpay
    
    # 启动时初始化 WeChat Pay 客户端
    # 从环境变量加载配置
    wechatpay_type_str = os.getenv('WECHATPAY_TYPE', 'NATIVE')
    wechatpay_type_map = {
        'NATIVE': WeChatPayType.NATIVE,
        'JSAPI': WeChatPayType.JSAPI,
        'APP': WeChatPayType.APP,
        'H5': WeChatPayType.H5,
        'MINIPROG': WeChatPayType.MINIPROG
    }

    with open(os.getenv('WECHATPAY_PRIVATE_KEY_PATH'), mode="r") as f:
        private_key = f.read()

    
    config = {
        'wechatpay_type': wechatpay_type_map.get(wechatpay_type_str, WeChatPayType.NATIVE),
        'mchid': os.getenv('WECHATPAY_MCHID'), # 商户ID
        'private_key':private_key, # 商户证书私钥私钥
        'cert_serial_no': os.getenv('WECHATPAY_CERT_SERIAL_NO'), # 商户证书序列号
        'appid': os.getenv('WECHATPAY_APPID'), # 应用ID（例如微信小程序、公众号..）
        'apiv3_key': os.getenv('WECHATPAY_APIV3_KEY'), # API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
        'notify_url': os.getenv('WECHATPAY_NOTIFY_URL'), # 回调地址，也可以在调用接口的时候覆盖
        'cert_dir': os.getenv('WECHATPAY_CERT_DIR', './certs'),
        'logger': logger,
        'partner_mode': os.getenv('WECHATPAY_PARTNER_MODE', 'false').lower() == 'true'
    }
    
    # 验证必需的配置
    required_fields = ['mchid', 'private_key', 'cert_serial_no', 'appid', 'apiv3_key']
    missing_fields = [field for field in required_fields if not config.get(field)]
    
    if missing_fields:
        logger.error(f"Missing required configuration: {', '.join(missing_fields)}")
        logger.error("Please check your .env file or environment variables")
        raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")
    
    # 初始化异步 WeChat Pay 客户端
    wxpay = AsyncWeChatPay(**config)
    await wxpay.__aenter__()
    logger.info("WeChat Pay client initialized successfully")
    
    yield
    
    # 关闭时清理资源
    if wxpay:
        await wxpay.__aexit__(None, None, None)
        logger.info("WeChat Pay client closed")


# 创建 FastAPI 应用
app = FastAPI(title="WeChat Pay v3 Async Example", lifespan=lifespan)


# 请求模型
class PaymentRequest(BaseModel):
    description: str
    out_trade_no: str
    total: int  # 金额，单位：分
    openid: Optional[str] = None  # JSAPI 支付时必填


class RefundRequest(BaseModel):
    out_trade_no: str
    out_refund_no: str
    refund: int  # 退款金额，单位：分
    total: int  # 原订单金额，单位：分
    reason: Optional[str] = "用户申请退款"


@app.post("/api/v1/payment/native")
async def create_native_payment(payment: PaymentRequest):
    """创建 Native 支付订单（扫码支付）"""
    try:
        code, result = await wxpay.pay(
            description=payment.description,
            out_trade_no=payment.out_trade_no,
            amount={'total': payment.total, 'currency': 'CNY'},
            pay_type=WeChatPayType.NATIVE
        )
        
        if code == 200:
            data = json.loads(result)
            return {
                "code": 0,
                "message": "success",
                "data": {
                    "code_url": data.get("code_url"),  # 二维码链接
                    "out_trade_no": payment.out_trade_no
                }
            }
        else:
            logger.error(f"Payment creation failed: {code} - {result}")
            raise HTTPException(status_code=code, detail=result)
            
    except Exception as e:
        logger.error(f"Payment error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/payment/jsapi")
async def create_jsapi_payment(payment: PaymentRequest):
    """创建 JSAPI 支付订单（公众号/小程序支付）"""
    if not payment.openid:
        raise HTTPException(status_code=400, detail="openid is required for JSAPI payment")
    
    try:
        code, result = await wxpay.pay(
            description=payment.description,
            out_trade_no=payment.out_trade_no,
            amount={'total': payment.total, 'currency': 'CNY'},
            payer={'openid': payment.openid},
            pay_type=WeChatPayType.JSAPI
        )
        
        if code == 200:
            data = json.loads(result)
            prepay_id = data.get("prepay_id")
            
            # 生成 JSAPI 调起支付参数
            timestamp = str(int(datetime.now().timestamp()))
            nonce_str = payment.out_trade_no  # 简单起见使用订单号作为随机字符串
            package = f"prepay_id={prepay_id}"
            
            # 签名
            sign_data = [wxpay._appid, timestamp, nonce_str, package]
            pay_sign = wxpay.sign(sign_data)
            
            return {
                "code": 0,
                "message": "success",
                "data": {
                    "appId": wxpay._appid,
                    "timeStamp": timestamp,
                    "nonceStr": nonce_str,
                    "package": package,
                    "signType": "RSA",
                    "paySign": pay_sign
                }
            }
        else:
            logger.error(f"Payment creation failed: {code} - {result}")
            raise HTTPException(status_code=code, detail=result)
            
    except Exception as e:
        logger.error(f"Payment error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/payment/query/{out_trade_no}")
async def query_payment(out_trade_no: str):
    """查询支付订单状态"""
    try:
        code, result = await wxpay.query(out_trade_no=out_trade_no)
        
        if code == 200:
            data = json.loads(result)
            return {
                "code": 0,
                "message": "success",
                "data": {
                    "out_trade_no": data.get("out_trade_no"),
                    "transaction_id": data.get("transaction_id"),
                    "trade_state": data.get("trade_state"),
                    "trade_state_desc": data.get("trade_state_desc"),
                    "amount": data.get("amount"),
                    "payer": data.get("payer")
                }
            }
        else:
            logger.error(f"Query failed: {code} - {result}")
            raise HTTPException(status_code=code, detail=result)
            
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/payment/refund")
async def create_refund(refund: RefundRequest):
    """申请退款"""
    try:
        code, result = await wxpay.refund(
            out_trade_no=refund.out_trade_no,
            out_refund_no=refund.out_refund_no,
            amount={
                'refund': refund.refund,
                'total': refund.total,
                'currency': 'CNY'
            },
            reason=refund.reason
        )
        
        if code == 200:
            data = json.loads(result)
            return {
                "code": 0,
                "message": "success",
                "data": {
                    "refund_id": data.get("refund_id"),
                    "out_refund_no": data.get("out_refund_no"),
                    "status": data.get("status"),
                    "amount": data.get("amount")
                }
            }
        else:
            logger.error(f"Refund failed: {code} - {result}")
            raise HTTPException(status_code=code, detail=result)
            
    except Exception as e:
        logger.error(f"Refund error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 健康检查端点
@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "service": "wechatpay-async"}


if __name__ == "__main__":
    import uvicorn
    import sys
    
    # 从环境变量读取服务器配置
    host = os.getenv('SERVER_HOST', '0.0.0.0')
    port = int(os.getenv('SERVER_PORT', '8000'))
    
    # 检查是否使用 reload 模式
    use_reload = '--reload' in sys.argv or os.getenv('RELOAD', 'false').lower() == 'true'
    
    # 运行服务器
    # 注意：如果遇到 NotImplementedError，可以尝试：
    # 1. 不使用 reload 模式
    # 2. 升级 uvloop: pip install --upgrade uvloop
    # 3. 使用 --loop asyncio 参数
    uvicorn.run(
        "fastapi_example:app",
        host=host,
        port=port,
        reload=use_reload,
        log_level=log_level.lower(),
        loop="asyncio" if use_reload else "auto"  # reload 模式下使用 asyncio 避免 uvloop 问题
    )