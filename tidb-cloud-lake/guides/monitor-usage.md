---
title: 监控使用情况
summary: TiDB Cloud Lake 提供监控功能，帮助你全面了解你自己以及组织成员在平台上的使用情况。要访问 Monitor 页面，请在首页的侧边栏菜单中点击 Monitor。该页面包含以下标签页。
---

# 监控使用情况

{{{ .lake }}} 提供监控功能，帮助你全面了解你自己以及组织成员在平台上的使用情况。要访问 **Monitor** 页面，请在首页的侧边栏菜单中点击 **Monitor**。该页面包含以下标签页：

- [Metrics](#metrics)
- [SQL History](#sql-history)
- [Task History](#task-history)
- [Audit](#audit)：仅对 `account_admin` 用户可见。

## Metrics {#metrics}

**Metrics** 标签页通过图表直观展示以下指标的使用统计信息，涵盖过去一小时、一天或一周的数据：

- 存储大小
- SQL 查询次数
- 会话连接数
- 扫描 / 写入的数据量
- 计算集群状态
- 扫描 / 写入的行数

## SQL History {#sql-history}

**SQL History** 标签页显示组织内所有用户已执行的 SQL 语句列表。点击列表顶部的 **Filter**，你可以按多个维度筛选记录。

在 **SQL History** 页面点击某条记录后，可以查看 {{{ .lake }}} 如何执行该 SQL 语句的详细信息，并访问以下标签页：

- **Query Details**：包括 Query State（成功或失败）、Rows Scanned、计算集群 (Warehouse)、Bytes Scanned、Start Time、End Time 和 Handler Type。
- **Query Profile**：展示该 SQL 语句的执行方式。

## Task History {#task-history}

**Task History** 标签页提供组织内所有已执行任务的完整日志，便于用户查看任务设置并监控其状态。

## Audit {#audit}

**Audit** 标签页记录所有组织成员的操作日志，包括操作类型、操作时间、IP 地址以及操作人的账户。点击列表顶部的 **Filter**，你可以按多个维度筛选记录。