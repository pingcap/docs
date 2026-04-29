---
title: {{{ .premium }}} 的 Changefeed 计费
summary: 了解 {{{ .premium }}} 中 changefeeds 的计费方式。
---

# {{{ .premium }}} 的 Changefeed 计费

本文档介绍 {{{ .premium }}} 中 changefeeds 的计费详情。

## CCU 成本 {#ccu-cost}

{{{ .premium }}} 使用 TiCDC Changefeed Capacity Units (CCUs) 来衡量 [changefeeds](/tidb-cloud/changefeed-overview.md) 的容量。当你为实例[创建 changefeed](/tidb-cloud/changefeed-overview.md#create-a-changefeed) 时，可以选择合适的规格。CCU 越高，复制性能越好。你将按这些 TiCDC CCU 收费。

### TiCDC CCU 数量 {#number-of-ticdc-ccus}

下表列出了 changefeeds 的规格及其对应的复制性能：

| Specification | Maximum replication performance |
|---------------|---------------------------------|
| 2 CCUs        | 5,000 rows/s                    |
| 4 CCUs        | 10,000 rows/s                   |
| 8 CCUs        | 20,000 rows/s                   |
| 16 CCUs       | 40,000 rows/s                   |
| 24 CCUs       | 60,000 rows/s                   |
| 32 CCUs       | 80,000 rows/s                   |
| 40 CCUs       | 100,000 rows/s                  |
| 64 CCUs       | 160,000 rows/s                  |
| 96 CCUs       | 240,000 rows/s                  |
| 128 CCUs      | 320,000 rows/s                  |
| 192 CCUs      | 480,000 rows/s                  |
| 256 CCUs      | 640,000 rows/s                  |
| 320 CCUs      | 800,000 rows/s                  |
| 384 CCUs      | 960,000 rows/s                  |

> **注意：**
>
> 以上性能数据仅供参考，在不同场景下可能会有所差异。强烈建议你在生产环境中使用 changefeed 功能之前，先进行真实工作负载测试。如需进一步帮助，请联系 [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md)。

### 价格 {#price}

目前，{{{ .premium }}} 处于公开预览阶段。更多信息，请参见 [{{{ .premium }}} Pricing Details](https://www.pingcap.com/tidb-cloud-premium-pricing-details/)。

## Private Data Link 成本 {#private-data-link-cost}

如果你选择 **Private Link** 或 **Private Service Connect** 网络连接方式，将产生额外的 **Private Data Link** 费用。这些费用属于 [Data Transfer Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#data-transfer-cost) 类别。

**Private Data Link** 的价格为 **$0.01/GiB**，与 [AWS Interface Endpoint pricing](https://aws.amazon.com/privatelink/pricing/#Interface_Endpoint_pricing) 中的 **Data Processed**、[Google Cloud Private Service Connect pricing](https://cloud.google.com/vpc/pricing#psc-forwarding-rules) 中的 **Consumer data processing**，以及 [Azure Private Link pricing](https://azure.microsoft.com/en-us/pricing/details/private-link/) 中的 **Inbound/Outbound Data Processed** 相同。