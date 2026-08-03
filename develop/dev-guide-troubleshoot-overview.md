---
title: SQL or Transaction Issues
summary: Learn how to troubleshoot SQL or transaction issues that might occur during application development.
aliases: ['/tidb/stable/dev-guide-troubleshoot-overview/','/tidb/dev/dev-guide-troubleshoot-overview/','/tidbcloud/dev-guide-troubleshoot-overview/']
---

# SQL or Transaction Issues

This document introduces problems that may occur during application development and related documents.

## Troubleshoot SQL query problems

If you want to improve SQL query performance, follow the instructions in [SQL Performance Tuning](/develop/dev-guide-optimize-sql-overview.md) to solve performance problems such as full table scans and missing indexes.

If you still have performance issues, see the following documents:

<SimpleTab groupId="platform">

<div label="TiDB Cloud" value="tidb-cloud">

- [Slow Queries](/tidb-cloud/tune-performance.md#slow-query)
- [Statement Analysis](/tidb-cloud/tune-performance.md#statement-analysis)
- [Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer)

</div>

<div label="TiDB Self-Managed" value="tidb">

- [Analyze Slow Queries](/analyze-slow-queries.md)
- [Identify Expensive Queries Using Top SQL](/dashboard/top-sql.md)

</div>
</SimpleTab>

If you have questions about SQL operations, see [SQL FAQs](/faq/sql-faq.md).

## Troubleshoot transaction issues

See [Handle transaction errors](/develop/dev-guide-transaction-troubleshoot.md).

## See also

- [Unsupported features](/mysql-compatibility.md#unsupported-features)
- [FAQs for TiDB Cloud](/tidb-cloud/tidb-cloud-faq.md)
- [FAQs for TiDB Self-Managed](/faq/faq-overview.md)

## Need help?

- Ask the community on [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) or [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs).
- [Submit a support ticket for TiDB Cloud](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [Submit a support ticket for TiDB Self-Managed](/support.md)
