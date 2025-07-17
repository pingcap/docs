---
title: SQL 或事务问题
summary: 了解在应用开发过程中可能出现的 SQL 或事务问题的排查方法。
---

# SQL 或事务问题

本文介绍在应用开发过程中可能出现的问题及相关文档。

## 排查 SQL 查询问题

如果你想提升 SQL 查询性能，请按照 [SQL Performance Tuning](/develop/dev-guide-optimize-sql-overview.md) 中的指引，解决全表扫描、缺少索引等性能问题。

<CustomContent platform="tidb">

如果你仍然遇到性能问题，请参考以下文档：

- [Analyze Slow Queries](/analyze-slow-queries.md)
- [Identify Expensive Queries Using Top SQL](/dashboard/top-sql.md)

如果你对 SQL 操作有疑问，请参阅 [SQL FAQs](/faq/sql-faq.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

如果你对 SQL 操作有疑问，请参阅 [SQL FAQs](https://docs.pingcap.com/tidb/stable/sql-faq)。

</CustomContent>

## 排查事务问题

请参阅 [Handle transaction errors](/develop/dev-guide-transaction-troubleshoot.md)。

## 相关内容

- [Unsupported features](/mysql-compatibility.md#unsupported-features)

<CustomContent platform="tidb">

- [Cluster Management FAQs](/faq/manage-cluster-faq.md)
- [TiDB FAQs](/faq/tidb-faq.md)

</CustomContent>

## 需要帮助？

<CustomContent platform="tidb">

可以在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

可以在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 社区提问，或 [提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>