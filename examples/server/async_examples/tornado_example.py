#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tornado async example for WeChat Pay v3 SDK
演示如何在 Tornado 中使用异步版本的微信支付 SDK
"""

import json
import logging
import os
from datetime import datetime

from dotenv import load_dotenv
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from wechatpayv3.async_ import AsyncWeChatPay, WeChatPayType

# 加载环境变量
load_dotenv()

# 配置日志
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

# 定义命令行参数
define("port", default=int(os.getenv('SERVER_PORT', '8888')), help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode", type=bool)

# 从环境变量加载 WeChat Pay 配置
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

WECHATPAY_CONFIG = {
    'wechatpay_type': wechatpay_type_map.get(wechatpay_type_str, WeChatPayType.NATIVE),
    'mchid': os.getenv('WECHATPAY_MCHID'),
    'private_key': private_key,
    'cert_serial_no': os.getenv('WECHATPAY_CERT_SERIAL_NO'),
    'appid': os.getenv('WECHATPAY_APPID'),
    'apiv3_key': os.getenv('WECHATPAY_APIV3_KEY'),
    'notify_url': os.getenv('WECHATPAY_NOTIFY_URL'),
    'cert_dir': os.getenv('WECHATPAY_CERT_DIR', './certs'),
    'logger': logger,
    'partner_mode': os.getenv('WECHATPAY_PARTNER_MODE', 'false').lower() == 'true'
}

# 验证必需的配置
required_fields = ['mchid', 'private_key', 'cert_serial_no', 'appid', 'apiv3_key']
missing_fields = [field for field in required_fields if not WECHATPAY_CONFIG.get(field)]

if missing_fields:
    logger.error(f"Missing required configuration: {', '.join(missing_fields)}")
    logger.error("Please check your .env file or environment variables")
    raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")


class BaseHandler(tornado.web.RequestHandler):
    """基础处理器"""
    
    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")
    
    def write_json(self, data):
        self.write(json.dumps(data, ensure_ascii=False))


class NativePaymentHandler(BaseHandler):
    """Native 支付处理器"""
    
    async def post(self):
        try:
            data = json.loads(self.request.body)
            
            if not all(k in data for k in ['description', 'out_trade_no', 'total']):
                self.set_status(400)
                self.write_json({"code": -1, "message": "Missing required fields"})
                return
            
            async with AsyncWeChatPay(**WECHATPAY_CONFIG) as wxpay:
                code, result = await wxpay.pay(
                    description=data['description'],
                    out_trade_no=data['out_trade_no'],
                    amount={'total': data['total'], 'currency': 'CNY'},
                    pay_type=WeChatPayType.NATIVE
                )
                
                if code == 200:
                    result_data = json.loads(result)
                    self.write_json({
                        "code": 0,
                        "message": "success",
                        "data": {
                            "code_url": result_data.get("code_url"),
                            "out_trade_no": data['out_trade_no']
                        }
                    })
                else:
                    self.set_status(code)
                    self.write_json({"code": code, "message": result})
                    
        except Exception as e:
            logger.error(f"Payment error: {str(e)}")
            self.set_status(500)
            self.write_json({"code": -1, "message": str(e)})


class JSAPIPaymentHandler(BaseHandler):
    """JSAPI 支付处理器"""
    
    async def post(self):
        try:
            data = json.loads(self.request.body)
            
            if not all(k in data for k in ['description', 'out_trade_no', 'total', 'openid']):
                self.set_status(400)
                self.write_json({"code": -1, "message": "Missing required fields"})
                return
            
            async with AsyncWeChatPay(**WECHATPAY_CONFIG) as wxpay:
                code, result = await wxpay.pay(
                    description=data['description'],
                    out_trade_no=data['out_trade_no'],
                    amount={'total': data['total'], 'currency': 'CNY'},
                    payer={'openid': data['openid']},
                    pay_type=WeChatPayType.JSAPI
                )
                
                if code == 200:
                    result_data = json.loads(result)
                    prepay_id = result_data.get("prepay_id")
                    
                    # 生成 JSAPI 调起支付参数
                    timestamp = str(int(datetime.now().timestamp()))
                    nonce_str = data['out_trade_no']
                    package = f"prepay_id={prepay_id}"
                    
                    # 签名
                    sign_data = [wxpay._appid, timestamp, nonce_str, package]
                    pay_sign = wxpay.sign(sign_data)
                    
                    self.write_json({
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
                    })
                else:
                    self.set_status(code)
                    self.write_json({"code": code, "message": result})
                    
        except Exception as e:
            logger.error(f"Payment error: {str(e)}")
            self.set_status(500)
            self.write_json({"code": -1, "message": str(e)})


class QueryPaymentHandler(BaseHandler):
    """查询支付订单处理器"""
    
    async def get(self, out_trade_no):
        try:
            async with AsyncWeChatPay(**WECHATPAY_CONFIG) as wxpay:
                code, result = await wxpay.query(out_trade_no=out_trade_no)
                
                if code == 200:
                    data = json.loads(result)
                    self.write_json({
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
                    })
                else:
                    self.set_status(code)
                    self.write_json({"code": code, "message": result})
                    
        except Exception as e:
            logger.error(f"Query error: {str(e)}")
            self.set_status(500)
            self.write_json({"code": -1, "message": str(e)})


class RefundHandler(BaseHandler):
    """退款处理器"""
    
    async def post(self):
        try:
            data = json.loads(self.request.body)
            
            if not all(k in data for k in ['out_trade_no', 'out_refund_no', 'refund', 'total']):
                self.set_status(400)
                self.write_json({"code": -1, "message": "Missing required fields"})
                return
            
            async with AsyncWeChatPay(**WECHATPAY_CONFIG) as wxpay:
                code, result = await wxpay.refund(
                    out_trade_no=data['out_trade_no'],
                    out_refund_no=data['out_refund_no'],
                    amount={
                        'refund': data['refund'],
                        'total': data['total'],
                        'currency': 'CNY'
                    },
                    reason=data.get('reason', '用户申请退款')
                )
                
                if code == 200:
                    result_data = json.loads(result)
                    self.write_json({
                        "code": 0,
                        "message": "success",
                        "data": {
                            "refund_id": result_data.get("refund_id"),
                            "out_refund_no": result_data.get("out_refund_no"),
                            "status": result_data.get("status"),
                            "amount": result_data.get("amount")
                        }
                    })
                else:
                    self.set_status(code)
                    self.write_json({"code": code, "message": result})
                    
        except Exception as e:
            logger.error(f"Refund error: {str(e)}")
            self.set_status(500)
            self.write_json({"code": -1, "message": str(e)})

class HealthHandler(BaseHandler):
    """健康检查处理器"""
    
    def get(self):
        self.write_json({"status": "healthy", "service": "wechatpay-tornado-async"})


def make_app():
    """创建 Tornado 应用"""
    return tornado.web.Application([
        # 支付相关接口
        (r"/api/v1/payment/native", NativePaymentHandler),
        (r"/api/v1/payment/jsapi", JSAPIPaymentHandler),
        (r"/api/v1/payment/query/([^/]+)", QueryPaymentHandler),
        (r"/api/v1/payment/refund", RefundHandler),

        # 健康检查
        (r"/health", HealthHandler),
    ], debug=options.debug)


async def main():
    """主函数"""
    tornado.options.parse_command_line()
    
    app = make_app()
    app.listen(options.port)
    
    logger.info(f"Tornado server started on port {options.port}")
    
    # 保持服务运行
    await asyncio.Event().wait()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())