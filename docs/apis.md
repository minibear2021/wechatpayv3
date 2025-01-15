已适配的微信支付 V3 版 API 接口列表如下，部分接口调用示例可以参考[这里](interface.md)：

| 大类| 小类 | 接口 | 接口函数| 直连商户适用 | 服务商适用 |
| ---- | ---------------------------------------- | ------------------------ | --------------------------------------- | ------------ | ---------- |
| 公用| 公用 | 调起支付签名| sign | 是 | 是 |
| 公用| 公用 | 回调通知| callback | 是 | 是 |
| 公用| 公用 | 敏感信息参数解密 | decrypt | 是 | 是 |
| 公用| 公用 | 下载(交易、资金)账单| download_bill| 是 | 是 |
| 商户进件 | 特约商户进件、小微商户进件| 提交申请单 | applyment_submit | 否| 是|
| 商户进件 | 特约商户进件、小微商户进件| 查询申请单状态| applyment_query| 否| 是|
| 商户进件 | 特约商户进件、小微商户进件| 修改结算账号| applyment_settlement_modify| 否| 是|
| 商户进件 | 特约商户进件、小微商户进件| 查询结算账号| applyment_settlement_query| 否| 是|
| 基础支付 | JSAPI、APP、H5、Native、小程序支付、付款码支付| 统一下单 | pay | 是| 是|
| 基础支付 | JSAPI、APP、H5、Native、小程序支付、付款码支付| 查询订单 | query | 是| 是|
| 基础支付 | JSAPI、APP、H5、Native、小程序支付| 关闭订单 | close | 是| 是|
| 基础支付 | 付款码支付 | 撤销订单 | codepay_reverse | 是| 是|
| 基础支付 | 合单支付 | 统一下单 | combine_pay| 是| 是|
| 基础支付 | 合单支付 | 查询订单 | combine_query| 是| 是|
| 基础支付 | 合单支付 | 关闭订单 | combine_close| 是| 是|
| 基础支付 | 退款 | 申请退款 | refund| 是| 是|
| 基础支付 | 退款 | 查询单笔退款| query_refund | 是| 是|
| 基础支付 | 退款 | 发起异常退款| abnormal_refund | 是| 是|
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
| 行业方案 | 智慧商圈 | 商圈会员待积分状态查询| business_point_status| 是| 是|
| 行业方案 | 智慧商圈 | 商圈会员停车状态同步| business_parking_sync| 是| 是|
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
| 营销工具 | 银行定向活促 | 出行券切卡组件预下单| industry_coupon_token| 否| 是|
| 营销工具 | 银行定向活促 | 导入定向用户协议号| bank_package_file| 否| 是|
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
| 资金应用 | 商家转账 | 发起转账 | mch_transfer_bills | 是 | 否
| 资金应用 | 商家转账 | 撤销转账 | mch_transfer_bills_cancel | 是 | 否
| 资金应用 | 商家转账 | 查询转账单 | mch_transfer_bills_query | 是 | 否
| 资金应用 | 商家转账 | 申请电子回单 | mch_transfer_elecsign | 是 | 否
| 资金应用 | 商家转账 | 查询电子回单 | mch_transfer_elecsign_query | 是 | 否
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
| 其他 | 电子发票 | 创建电子发票卡券模板 | fapiao_card_template | 是 | 是 |
| 其他 | 电子发票 | 配置开发选项 | fapiao_set_merchant_config | 是 | 是 |
| 其他 | 电子发票 | 查询商户配置的开发选项 | fapiao_merchant_config | 是 | 是 |
| 其他 | 电子发票 | 获取抬头填写链接 | fapiao_title_url | 是 | 是 |
| 其他 | 电子发票 | 获取用户填写的抬头 | fapiao_title | 是 | 是 |
| 其他 | 电子发票 | 获取商品和服务税收分类对照表 | fapiao_tax_codes | 是 | 是 |
| 其他 | 电子发票 | 获取商户开票基础信息 | fapiao_merchant_base_info | 是 | 是 |
| 其他 | 电子发票 | 开具电子发票 | fapiao_applications | 是 | 是 |
| 其他 | 电子发票 | 查询电子发票 | fapiao_query | 是 | 是 |
| 其他 | 电子发票 | 冲红电子发票 | fapiao_reverse | 是 | 是 |
| 其他 | 电子发票 | 上传电子发票文件 | fapiao_upload_file | 是 | 是 |
| 其他 | 电子发票 | 将电子发票插入微信用户卡包 | fapiao_insert_cards | 是 | 是 |
| 其他 | 电子发票 | 检查子商户开票功能状态 | fapiao_check_submch | 否 | 是 |
| 其他 | 电子发票 | 获取发票下载信息 | fapiao_query_files | 是 | 是 |
| 其他 | 电子发票 | 下载发票文件 | fapiao_download_file | 是 | 是 |
| 其他 | 银行组件 | 获取对私银行卡号开户银行 | capital_search_bank_number | 是 | 是 |
| 其他 | 银行组件 | 查询支持个人业务的银行列表 | capital_personal_banks | 是 | 是 |
| 其他 | 银行组件 | 查询支持对公业务的银行列表 | capital_corporate_banks | 是 | 是 |
| 其他 | 银行组件 | 查询省份列表 | capital_provinces | 是 | 是 |
| 其他 | 银行组件 | 查询城市列表 | capital_cities | 是 | 是 |
| 其他 | 银行组件 | 查询支行列表 | capital_branches | 是 | 是 |
