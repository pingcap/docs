---
title: 数据迁移计费
summary: 了解 TiDB Cloud 中数据迁移的计费方式。
---

# 数据迁移计费

本文档介绍了 TiDB Cloud 中数据迁移的计费方式。

## 数据迁移规格

TiDB Cloud 以复制容量单位（Replication Capacity Units，RCUs）来衡量数据迁移的容量。当你创建数据迁移任务时，可以选择合适的规格。RCU 越高，迁移性能越好。你需要为这些数据迁移 RCU 支付费用。

下表列出了每种数据迁移规格对应的性能以及可迁移的最大表数量。

| 规格 | 全量数据迁移 | 增量数据迁移 | 最大表数量 |
|------|--------------|--------------|------------|
| 2 RCUs  | 25 MiB/s | 10,000 行/s | 500   |
| 4 RCUs  | 35 MiB/s | 20,000 行/s | 10000 |
| 8 RCUs  | 40 MiB/s | 40,000 行/s | 30000 |
| 16 RCUs | 45 MiB/s | 80,000 行/s | 60000 |

关于数据迁移 RCU 的价格详情，请参见 [Data Migration Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#dm-cost)。

> **Note:**
>
> - 如果待迁移的表数量超过最大表数量，数据迁移任务可能仍会运行，但任务可能会变得不稳定，甚至失败。
> - 表中所有性能数值均为最大和最优值。假设上下游数据库不存在性能、网络带宽或其他瓶颈。性能数值仅供参考，实际场景中可能有所不同。

数据迁移任务以 MiB/s 衡量全量数据迁移性能。该单位表示数据迁移任务每秒迁移的数据量（以 MiB 计）。

数据迁移任务以行/s 衡量增量数据迁移性能。该单位表示每秒迁移到目标数据库的行数。例如，如果上游数据库在约 1 秒内执行了 10,000 行的 `INSERT`、`UPDATE` 或 `DELETE` 语句，则对应规格的数据迁移任务可以在约 1 秒内将这 10,000 行同步到下游。

## 价格

关于 TiDB Cloud 各区域支持情况及每个数据迁移 RCU 的价格，请参见 [Data Migration Cost](https://www.pingcap.com/tidb-dedicated-pricing-details/#dm-cost)。

数据迁移任务与目标 TiDB 节点处于同一区域。

请注意，如果你使用 AWS PrivateLink 或 VPC 对等连接，并且源数据库与 TiDB 节点不在同一区域或同一可用区（AZ），则会产生两项额外的流量费用：跨区域和跨可用区流量费用。

- 如果源数据库与 TiDB 节点不在同一区域，当数据迁移任务从源数据库采集数据时，会产生跨区域流量费用。

    ![Cross-region traffic charges](/media/tidb-cloud/dm-billing-cross-region-fees.png)

- 如果源数据库与 TiDB 节点在同一区域但不同可用区，当数据迁移任务从源数据库采集数据时，会产生跨可用区流量费用。

    ![Cross-AZ traffic charges](/media/tidb-cloud/dm-billing-cross-az-fees.png)

- 如果数据迁移任务与 TiDB 节点不在同一可用区，当数据迁移任务向目标 TiDB 节点写入数据时，会产生跨可用区流量费用。此外，如果数据迁移任务与 TiDB 节点和源数据库不在同一可用区（或区域），当数据迁移任务从源数据库采集数据时，会产生跨可用区（或跨区域）流量费用。

    ![Cross-region and cross-AZ traffic charges](/media/tidb-cloud/dm-billing-cross-region-and-az-fees.png)

跨区域和跨可用区流量的价格与 TiDB Cloud 保持一致。详情请参见 [TiDB Cloud Dedicated Pricing Details](https://www.pingcap.com/tidb-dedicated-pricing-details/)。

## 另请参阅

- [Migrate from MySQL-Compatible Databases Using Data Migration](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
