---
title: 优化 SQL 性能概述
summary: 提供 TiDB 应用开发者关于 SQL 性能调优的概述。
---

# 优化 SQL 性能概述

本文介绍了如何优化 TiDB 中 SQL 语句的性能。为了获得良好的性能，你可以从以下几个方面入手：

* SQL 性能调优
* 架构设计：根据你的应用负载模式，可能需要调整表结构以避免事务冲突或热点问题。

## SQL 性能调优

为了获得良好的 SQL 语句性能，你可以遵循以下指南：

* 扫描尽可能少的行。建议只扫描你需要的数据，避免扫描多余的数据。
* 使用合适的索引。确保在 SQL 的 `WHERE` 子句中的列上有对应的索引。如果没有，语句将涉及全表扫描，从而导致性能下降。
* 使用合适的连接类型。根据查询中涉及的表的相对大小，选择合适的连接类型。一般来说，TiDB 的基于成本的优化器会选择性能最优的连接类型。但在少数情况下，你可能需要手动指定更优的连接类型。
* 使用合适的存储引擎。对于混合 OLTP 和 OLAP 负载，推荐使用 TiFlash 引擎。详情请参见 [HTAP Query](/develop/dev-guide-hybrid-oltp-and-olap-queries.md)。

## 架构设计

在 [调优 SQL 性能](#sql-performance-tuning) 后，如果你的应用仍然无法获得良好的性能，可能需要检查你的架构设计和数据访问模式，以避免以下问题：

<CustomContent platform="tidb">

* Transaction contention. 有关如何诊断和解决事务冲突，参见 [Troubleshoot Lock Conflicts](/troubleshoot-lock-conflicts.md)。
* Hot spots. 有关如何诊断和解决热点问题，参见 [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

* Transaction contention. 有关如何诊断和解决事务冲突，参见 [Troubleshoot Lock Conflicts](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)。
* Hot spots. 有关如何诊断和解决热点问题，参见 [Troubleshoot Hotspot Issues](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues)。

</CustomContent>

### 另请参见

<CustomContent platform="tidb">

* [SQL Performance Tuning](/sql-tuning-overview.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

* [SQL Performance Tuning](/tidb-cloud/tidb-cloud-sql-tuning-overview.md)

</CustomContent>

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上向社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>