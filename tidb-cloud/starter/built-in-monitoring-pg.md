---
title: PostgreSQL 兼容 TiDB Cloud Starter 的内置指标
summary: 了解 PostgreSQL 兼容 TiDB Cloud Starter 实例可用的内置指标。
---

# PostgreSQL 兼容 TiDB Cloud Starter 的内置指标

TiDB Cloud 会在 **Metrics** 页面收集并展示你的 TiDB 资源的一整套标准指标。通过查看这些指标，你可以轻松识别性能问题，并判断当前数据库部署是否满足你的需求。

## 查看 Metrics 页面 {#view-the-metrics-page}

要在 **Metrics** 页面查看指标，请执行以下步骤：

1. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，点击目标资源的名称，进入其概览页面。

    > **Tip:**
    >
    > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

2. 在左侧导航栏中，点击 **Monitoring** > **Metrics**。

## 指标保留策略 {#metrics-retention-policy}

在 TiDB Cloud 中，指标数据会保留 7 天。

## PostgreSQL 兼容 {{{ .starter }}} 实例的指标 {#metrics-for-postgresql-compatible-starter-instances}

以下各节介绍了 PostgreSQL 兼容 {{{ .starter }}} 实例在 **Metrics** 页面上的指标。

| 指标名称  | 标签 | 描述                                   |
| :------------| :------| :-------------------------------------------- |
| 已用存储大小 | Row-based storage, Row-based standard storage, Columnar storage | 行存储、行标准存储和列存储的大小。只有当每种存储类型的大小达到 50 MiB 或更大时，TiDB Cloud 才会显示此指标。**Row-based standard storage** 与 **Row-based storage** 含义相同。 |
| 每秒查询数 | All, {SQL type} | 每秒执行的 SQL 语句数量，按 SQL 类型收集，例如 `SELECT`、`INSERT` 和 `UPDATE`。 |
| 查询持续时间 | Avg, P99, P99-{SQL type} | 从 {{{ .starter }}} 实例接收到来自客户端的请求开始，到实例执行该请求并将结果返回给客户端为止的持续时间。 |
| 总连接数 | All | 到 {{{ .starter }}} 实例的连接数。 |

## FAQ {#faq}

**1. 为什么此页面上的某些面板为空？**

请检查所选时间范围是否包含实例上的活动。如果图表仍然为空，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 进行故障排查。

**2. 为什么在极少数情况下指标可能会不连续？**

在某些极少数情况下，指标可能会丢失，例如当指标系统压力过高时。

如果你遇到此问题，可以联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md) 进行故障排查。