---
title: Recovery Group Billing
summary: 了解 TiDB Cloud 中恢复组的计费方式。
---

# 恢复组计费

TiDB Cloud 会根据恢复组主集群中已部署的 TiKV 节点的规模对恢复组进行计费。当你为集群 [创建恢复组](/tidb-cloud/recovery-group-get-started.md) 时，可以为恢复组选择主集群。TiKV 配置越大，恢复组保护的成本就越高。

TiDB Cloud 还会按照每 GiB 的数据处理量进行计费。数据处理的价格会根据数据是复制到另一个区域的辅助集群，还是在同一区域内复制而有所不同。

## 价格

要了解 TiDB Cloud 恢复组支持的区域和定价，请参见 [Recovery Group Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#recovery-group-cost)。