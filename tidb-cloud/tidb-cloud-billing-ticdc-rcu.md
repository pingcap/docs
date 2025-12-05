---
title: TiDB Cloud Dedicated Changefeed 计费
summary: 了解 TiDB Cloud 中 changefeed 的计费方式。
aliases: ['/tidbcloud/tidb-cloud-billing-tcu']
---

# TiDB Cloud Dedicated Changefeed 计费

本文档介绍了 TiDB Cloud Dedicated 中 changefeed 的计费详情。

## RCU 成本

TiDB Cloud Dedicated 通过 TiCDC 复制能力单位（RCU，Replication Capacity Units）来衡量 [changefeed](/tidb-cloud/changefeed-overview.md) 的容量。当你为集群 [创建 changefeed](/tidb-cloud/changefeed-overview.md#create-a-changefeed) 时，可以选择合适的规格。RCU 越高，复制性能越好。你需要为这些 TiCDC changefeed RCU 支付费用。

### TiCDC RCU 数量

下表列出了 changefeed 的规格及其对应的最大复制性能：

| 规格         | 最大复制性能           |
|--------------|-----------------------|
| 2 RCUs       | 5,000 行/秒           |
| 4 RCUs       | 10,000 行/秒          |
| 8 RCUs       | 20,000 行/秒          |
| 16 RCUs      | 40,000 行/秒          |
| 24 RCUs      | 60,000 行/秒          |
| 32 RCUs      | 80,000 行/秒          |
| 40 RCUs      | 100,000 行/秒         |
| 64 RCUs      | 160,000 行/秒         |
| 96 RCUs      | 240,000 行/秒         |
| 128 RCUs     | 320,000 行/秒         |
| 192 RCUs     | 480,000 行/秒         |
| 256 RCUs     | 640,000 行/秒         |
| 320 RCUs     | 800,000 行/秒         |
| 384 RCUs     | 960,000 行/秒         |

> **Note:**
>
> 上述性能数据仅供参考，实际场景下可能有所不同。强烈建议你在生产环境中使用 changefeed 功能前，先进行真实负载测试。如需进一步协助，请联系 [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md)。

### 价格

关于 TiDB Cloud 各区域支持情况及每个 TiCDC RCU 的价格，请参见 [Changefeed Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#changefeed-cost)。

## Private Data Link 成本

如果你选择 **Private Link** 或 **Private Service Connect** 网络连接方式，将会产生额外的 **Private Data Link** 费用。这部分费用属于 [Data Transfer Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#data-transfer-cost) 类别。

**Private Data Link** 的价格为 **$0.01/GiB**，与 [AWS Interface Endpoint pricing](https://aws.amazon.com/privatelink/pricing/#Interface_Endpoint_pricing) 的 **Data Processed**、[Google Cloud Private Service Connect pricing](https://cloud.google.com/vpc/pricing#psc-forwarding-rules) 的 **Consumer data processing** 以及 [Azure Private Link pricing](https://azure.microsoft.com/en-us/pricing/details/private-link/) 的 **Inbound/Outbound Data Processed** 相同。