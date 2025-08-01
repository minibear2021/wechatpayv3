# Changelog

## [2.0.1] - 2025-07-30

### Fixed

- 修复“查询转账明细电子回单受理结果”接口bug

## [2.0.0] - 2025-07-29

### Added

- 新增对微信接口异步调用的支持

## [1.3.11] - 2025-06-04

### Fixed

- 修复接口返回非200状态码可能导致的异常

## [1.3.10] - 2025-03-01

### Fixed

- 修复循环调用request的bug

## [1.3.9] - 2025-02-26

### Added

- 平台公钥模式下始终添加Wechatpay-Serial头

## [1.3.8] - 2025-02-21

### Fixed

- 修复撤销商家转账接口bug

## [1.3.7] - 2025-01-15

### Added

- 支持新版商家转账功能

## [1.3.6] - 2024-12-23

### Fixed

- 异常信息使用f字符串连接

## [1.3.5] - 2024-11-06

### Fixed

- 修复public_key_id未赋值bug

## [1.3.4] - 2024-11-05

### Added

- 兼容平台证书向公钥模式过渡

## [1.3.3] - 2024-10-23

### Added

- 优化回调接口对部分框架的处理

## [1.3.2] - 2024-10-23

### Fixed

- 修复平台公钥ID处理的bug

## [1.3.1] - 2024-10-22

### Fixed

- update readme

## [1.3.0] - 2024-10-22

### Added

- 新增微信支付平台公钥模式初始化

## [1.2.53] - 2024-10-10

### Added

- 提交投诉回复接口添加mini_program_jump_info参数

## [1.2.52] - 2024-05-22

### Fixed

- 修复未导入撤销付款码支付订单接口bug

## [1.2.51] - 2024-04-19

### Added

- 添加付款码支付接口

## [1.2.50] - 2024-04-15

### Fixed

- 商家转账到零钱的回调地址参数修改为非必填

## [1.2.49] - 2024-04-15

### Fixed

- 商家转账到零钱添加回调地址参数

## [1.2.48] - 2024-04-03

### Fixed

- 修复timeout延迟赋值导致的bug

## [1.2.47] - 2024-04-01

### Added

- 添加请求超时配置项

## [1.2.45] - 2024-02-25

### Fixed

- 兼容高版本cryptography库

## [1.2.44] - 2024-02-05

### Fixed

- 兼容高版本cryptography库

## [1.2.43] - 2023-12-13

### Fixed

- 兼容微信支付签名探测流量

## [1.2.42] - 2023-11-15

### Fixed

- 修复电子发票-配置开发选项请求类型bug

## [1.2.41] - 2023-09-01

### Fixed

- 修正发起异常退款参数说明

## [1.2.40] - 2023-08-31

### Added

- 检查子商户开票功能状态
- 获取发票下载信息
- 下载发票文件
- 发起异常退款

## [1.2.39] - 2023-05-16

### Fixed

- 获取用户填写的抬头bug

## [1.2.38] - 2023-05-04

### Fixed

- 批次单号查询批次单bug

## [1.2.37] - 2023-04-02

### Added

- 查询结算账户修改申请状态

## [1.2.36] - 2023-02-24

### Added

- 导入定向用户协议号

## [1.2.35] - 2022-12-29

### Updated

- 发起批量转账接口增加transfer_scene_id参数

## [1.2.34] - 2022-09-23

### Fixed

- 下单接口pay_type未赋值异常

## [1.2.33] - 2022-09-20

### Added

- 所有下单接口新增请求参数字段： pay_type

## [1.2.32] - 2022-09-13

### Added

- 所有下单接口新增请求参数字段： support_fapiao

## [1.2.31] - 2022-09-01

### Added

- 商圈会员待积分状态查询
- 商圈会员停车状态同步

## [1.2.30] - 2022-07-20

### Added

- 出行券切卡组件预下单

### Fixed

- 修改商家券基本信息bug

## [1.2.29] - 2022-06-30

### Fixed

- 申请单个子商户资金账单bug

## [1.2.28] - 2022-06-16

### Updated

- 商户开户意愿确认-提交申请单参数调整
- 特约商户进件-提交申请单参数调整

## [1.2.27] - 2022-06-09

### Fixed

- 根据过滤条件查询用户券接口bug
- 修复电子发票国密SM3算法bug

## [1.2.26] - 2022-05-26

### Fixed

- 分账相关接口bug

## [1.2.25] - 2022-05-23

### Added

- 更新退款进度接口

## [1.2.24] - 2022-05-20

### Added

- 商家转账到零钱接口

## [1.2.23] - 2022-04-03

### Fixed

- 微信支付分请求退款接口bug

## [1.2.22] - 2022-04-07

### Fixed

- 请求分账回退bug

## [1.2.21] - 2022-04-06

### Fixed

- 创建代金券批次bug

## [1.2.20] - 2022-04-02

### Fixed

- 连锁品牌请求分账参数bug

## [1.2.19] - 2022-04-01

### Fixed

- 获取对私银行卡号开户银行加密bug

## [1.2.18] - 2022-04-01

### Added

- 银行组件接口

## [1.2.17] - 2022-03-23

### Fixed

- 修复请求分账接口加密参数bug

## [1.2.16] - 2022-03-14

### Fixed

- 修复开具电子发票时敏感信息未加密的bug

## [1.2.15] - 2022-03-14

### Added

- 支持电子发票相关接口

## [1.2.14] - 2022-03-07

### Fixed

- 修复商户进件提交申请单的bug

## [1.2.13] - 2022-02-17

### Added

- 初始化加载证书失败时抛出异常

## [1.2.12] - 2022-01-15

### Added

- 增加hmac_sha256签名方法，用于支持调起支付分订单时签名

### Fixed

- 创建支付分订单非必须参数值的 bug

## [1.2.11] - 2021-12-15

### Fixed

- notify_url 未赋值的 bug
- 连锁品牌请求分账的 bug

## [1.2.10] - 2021-12-05

### Fixed

- 请求分账的 bug

## [1.2.9] - 2021-12-05

### Fixed

- 请求分账的 bug

## [1.2.8] - 2021-12-05

### Fixed

- 查询代金券批次详情的一个 bug

## [1.2.7] - 2021-11-23

### Fixed

- 拼写错误

## [1.2.6] - 2021-11-20

### Added

- 新增 callback 接口，解密并保留所有回调参数，替代原 decrypt_callback 接口

## [1.2.5] - 2021-11-19

### Added

- 提交投诉回复新增可选参数
- 商户开户意愿确认接口
- 商户违规通知回调接口

## [1.2.4] - 2021-11-19

### Fixed

- 请求分账接口参数传递错误的 bug

## [1.2.3] - 2021-11-05

### Added

- 访问请求支持代理

## [1.2.2] - 2021-11-05

### Fixed

- 特约商户进件缺少 Wechatpay-Serial 的 bug

## [1.2.1] - 2021-11-04

### Fixed

- 拼写错误

## [1.2.0] - 2021-11-04

### Added

- 服务商模式接口(电商收付通除外)

### Fixed

- 直连模式部分接口 bug

## [1.1.0] - 2021-10-11

### Added

- 营销工具下代金券接口
- 营销工具下商家券接口

## [1.0.22] - 2021-10-09

### Fixed

- 查询支付分订单接口 bug

## [1.0.21] - 2021-09-29

### Added

- 商户申请获取对账单

## [1.0.20] - 2021-09-27

### Fixed

- 未引入支付分接口函数

## [1.0.19] - 2021-09-19

### Added

- 经营能力下微信支付分接口

### Changed

- 提前加载平台证书

## [1.0.18] - 2021-09-18

### Added

- 营销工具下支付有礼接口

## [1.0.17] - 2021-09-18

### Changed

- 日志信息内容

## [1.0.16] - 2021-09-18

### Added

- 初始化时支持日志记录

## [1.0.15] - 2021-09-17

### Added

- 营销工具下委托营销接口
- CHANGLOG.md

### Changed

- 示例 example

## [1.0.14] - 2021-09-14

### Changed

- 微调账单和图像下载接口返回值类型，message 参数从 string 变更为 bytes

## [1.0.13] - 2021-09-14

### Fixed

- 敏感信息解密 bug

## [1.0.12] - 2021-09-14

### Added

- 风险合规下消费者投诉 2.0 接口

## [1.0.11] - 2021-09-09

### Added

- 资金应用下分账接口

## [1.0.10] - 2021-09-05

### Changed

- 增强回调消息验证接口兼容性

## [1.0.9] - 2021-08-13

### Added

- 营销工具下图片上传(营销专用)接口

## [1.0.8] - 2021-08-13

### Added

- 行业方案下微信支付分停车接口

## [1.0.7] - 2021-08-12

### Added

- 其他能力下图片及视频上传接口

## [1.0.6] - 2021-08-09

### Changed

- 增强回调消息验证接口兼容性

## [1.0.5] - 2021-07-30

### Added

- 敏感信息参数自动加密

## [1.0.4] - 2021-07-14

### Added

- 经营能力下支付即服务接口

## [1.0.3] - 2021-06-22

### Fixed

- 下载证书无需验证签名

## [1.0.2] - 2021-06-16

### Fixed

- 平台证书更新 bug

## [1.0.1] - 2021-04-20

### Changed

- 代码重构

## [1.0] - 2021-04-20

### Added

- 智慧商圈积分授权查询

## [0.54] - 2021-04-20

### Added

- 支持本地缓存平台证书，减少网络请求

## [0.54] - 2021-04-20

### Changed

- 移除无效的 import

## [0.53] - 2021-04-19

### Changed

- 移除对 pyOpenSSL 包的依赖

## [0.53] - 2021-04-19

### Changed

- 移除对 pyOpenSSL 包的依赖

## [0.52] - 2021-04-19

### Added

- 行业方案下智慧商圈积分同步接口

### Fixed

- 签名验证 bug

## [0.51] - 2021-04-16

### Added

- 调起支付时需要的签名
- 回调消息接口自动解密 resource 字段

## [0.50] - 2021-04-16

### Added

- 微信平台证书自动下载及更新，无需提前准备

### Removed

- 证书下载接口

## [0.49] - 2021-04-16

### Changed

- 未提供平台证书时跳过接口验证

## [0.48] - 2021-04-16

### Fixed

- 验证签名 bug

## [0.47] - 2021-04-15

### Changed

- 接口返回类型从 bytes 更换为 string

## [0.46] - 2021-04-15

### Added

- 验证应答签名有效性

## [0.45] - 2021-04-15

### Fixed

- POST 接口签名错误

## [0.44] - 2021-04-15

### Added

- 基础支付下合单支付接口

## [0.43] - 2021-04-14

### Changed

- sdk 结构
- pypi 发布包格式

## [0.1] - 2021-04-14

### Added

- 基础支付(JSAPI 支付、APP 支付、H5 支付、Native 支付、小程序支付)下的：
  下单、查询订单、关闭订单、退款、退款查询、交易账单、资金账单及账单下载接口
- 新增证书下载接口
