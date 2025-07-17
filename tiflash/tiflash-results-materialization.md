---
title: TiFlash 查询结果物化
summary: 了解如何在事务中保存 TiFlash 的查询结果。
---

# TiFlash 查询结果物化

本文介绍如何在 `INSERT INTO SELECT` 事务中将 TiFlash 查询结果保存到指定的 TiDB 表中。

从 v6.5.0 版本开始，TiDB 支持将 TiFlash 查询结果保存到表中，即 TiFlash 查询结果物化。在执行 `INSERT INTO SELECT` 语句时，如果 TiDB 将 `SELECT` 子查询下推到 TiFlash，则可以将 TiFlash 查询结果保存到 `INSERT INTO` 子句中指定的 TiDB 表中。对于早于 v6.5.0 版本的 TiDB，TiFlash 查询结果是只读的，因此如果你想保存 TiFlash 查询结果，必须在应用层获取，然后在单独的事务或流程中保存。

> **Note:**
>
> 默认情况下 ([`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50))，优化器会根据 [SQL mode](/sql-mode.md) 和 TiFlash 副本的成本估算，智能判断是否将查询下推到 TiFlash。
>
> - 如果当前会话的 [SQL mode](/sql-mode.md) 不是严格模式（即 `sql_mode` 值不包含 `STRICT_TRANS_TABLES` 和 `STRICT_ALL_TABLES`），优化器会根据 TiFlash 副本的成本估算，智能判断是否将 `INSERT INTO SELECT` 中的 `SELECT` 子查询下推到 TiFlash。在此模式下，如果你想忽略优化器的成本估算，强制将查询下推到 TiFlash，可以将系统变量 [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51) 设置为 `ON`。
> - 如果当前会话的 [SQL mode](/sql-mode.md) 是严格模式（即 `sql_mode` 值包含 `STRICT_TRANS_TABLES` 或 `STRICT_ALL_TABLES`），则 `INSERT INTO SELECT` 中的 `SELECT` 子查询不能下推到 TiFlash。

`INSERT INTO SELECT` 的语法如下。

```sql
INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
    [INTO] tbl_name
    [PARTITION (partition_name [, partition_name] ...)]
    [(col_name [, col_name] ...)]
    SELECT ...
    [ON DUPLICATE KEY UPDATE assignment_list]
    {expr | DEFAULT}

assignment:
    col_name = value
assignment_list:
    assignment [, assignment] ...
```

例如，你可以使用以下 `INSERT INTO SELECT` 语句，将表 `t1` 中 `SELECT` 子句的查询结果保存到表 `t2` 中：

```sql
INSERT INTO t2 (name, country)
SELECT app_name, country FROM t1;
```

## 典型且推荐的使用场景

- 高效的 BI 解决方案

    对于许多 BI 应用，分析查询请求非常繁重。例如，当大量用户同时访问并刷新报告时，BI 应用需要处理大量的并发查询请求。为了有效应对这种情况，你可以使用 `INSERT INTO SELECT` 将报告的查询结果保存到 TiDB 表中。然后，用户在刷新报告时可以直接从结果表中查询数据，避免多次重复计算和分析。同样，通过保存历史分析结果，还可以进一步减少对长期历史数据分析的计算量。例如，你有一个用于分析每日销售利润的报告 `A`，可以使用 `INSERT INTO SELECT` 将报告 `A` 的结果保存到结果表 `T` 中。当你需要生成一个分析过去一个月销售利润的报告 `B` 时，可以直接使用表 `T` 中的每日分析结果。这不仅大大减少了计算量，还提升了查询响应速度，减轻了系统负载。

- 使用 TiFlash 支持在线应用

    TiFlash 支持的并发请求数取决于数据量和查询复杂度，但通常不超过 100 QPS。你可以使用 `INSERT INTO SELECT` 保存 TiFlash 查询结果，然后利用结果表支持高并发的在线请求。结果表中的数据可以在后台以较低频率（例如每 0.5 秒）更新，远低于 TiFlash 的并发限制，同时仍能保持较高的数据新鲜度。

## 执行流程

* 在执行 `INSERT INTO SELECT` 语句时，TiFlash 首先将 `SELECT` 子句的查询结果返回到集群中的 TiDB 服务器，然后将结果写入目标表（可以有 TiFlash 副本）。
* `INSERT INTO SELECT` 语句的执行保证了 ACID 属性。

## 限制

<CustomContent platform="tidb">

* 可以通过系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 调整 `INSERT INTO SELECT` 语句的 TiDB 内存限制。从 v6.5.0 开始，不建议使用 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 来控制事务内存大小。

    更多信息请参见 [TiDB 内存控制](/configure-memory-usage.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

* 可以通过系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 调整 `INSERT INTO SELECT` 语句的 TiDB 内存限制。从 v6.5.0 开始，不建议使用 [`txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit) 来控制事务内存大小。

    更多信息请参见 [TiDB 内存控制](https://docs.pingcap.com/tidb/stable/configure-memory-usage)。

</CustomContent>

* TiDB 对 `INSERT INTO SELECT` 语句的并发没有硬性限制，但建议考虑以下实践：

    * 当“写事务”较大（例如接近 1 GiB）时，建议将并发控制在不超过 10。
    * 当“写事务”较小时（例如少于 100 MiB），建议将并发控制在不超过 30。
    * 根据测试结果和具体情况确定并发数。

## 示例

数据定义：

```sql
CREATE TABLE detail_data (
    ts DATETIME,                -- 费用生成时间
    customer_id VARCHAR(20),    -- 客户编号
    detail_fee DECIMAL(20,2));  -- 费用金额

CREATE TABLE daily_data (
    rec_date DATE,              -- 数据采集日期
    customer_id VARCHAR(20),    -- 客户编号
    daily_fee DECIMAL(20,2));   -- 每日费用金额

ALTER TABLE detail_data SET TIFLASH REPLICA 2;
ALTER TABLE daily_data SET TIFLASH REPLICA 2;

-- ... (detail_data 表持续更新)
INSERT INTO detail_data(ts,customer_id,detail_fee) VALUES
('2023-1-1 12:2:3', 'cus001', 200.86),
('2023-1-2 12:2:3', 'cus002', 100.86),
('2023-1-3 12:2:3', 'cus002', 2200.86),
('2023-1-4 12:2:3', 'cus003', 2020.86),
('2023-1-5 12:2:3', 'cus003', 1200.86),
('2023-1-6 12:2:3', 'cus002', 20.86),
('2023-1-7 12:2:3', 'cus004', 120.56),
('2023-1-8 12:2:3', 'cus005', 320.16);

-- 执行以下 SQL 语句 13 次，将累计插入 65,536 行到表中。
INSERT INTO detail_data SELECT * FROM detail_data;
```

保存每日分析结果：

```sql
SET @@sql_mode='NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO';

INSERT INTO daily_data (rec_date, customer_id, daily_fee)
SELECT DATE(ts), customer_id, sum(detail_fee) FROM detail_data WHERE DATE(ts) > DATE('2023-1-1 12:2:3') GROUP BY DATE(ts), customer_id;
```

基于每日分析数据，分析每月数据：

```sql
SELECT MONTH(rec_date), customer_id, sum(daily_fee) FROM daily_data GROUP BY MONTH(rec_date), customer_id;
```

上述示例将每日分析结果物化到每日结果表中，基于此加速每月数据分析，从而提升数据分析效率。