---
title: SQL Non-Prepared Execution Plan Cache
summary: 了解 TiDB 中 SQL 非预处理执行计划缓存的原理、用法和示例。
---

# SQL 非预处理执行计划缓存

TiDB 支持对部分非 `PREPARE` 语句的执行计划进行缓存，类似于 [`Prepare`/`Execute` 语句](/sql-prepared-plan-cache.md)。该功能允许这些语句跳过优化阶段，从而提升性能。

启用非预处理执行计划缓存可能会带来额外的内存和 CPU 开销，并不适用于所有场景。是否在你的场景中启用此功能，请参考 [性能收益](#performance-benefits) 和 [内存监控](#monitoring) 部分。

## 原理

非预处理执行计划缓存是会话级别的功能，与 [预处理计划缓存](/sql-prepared-plan-cache.md) 共享缓存。其基本原理如下：

1. 启用非预处理计划缓存后，TiDB 首先根据抽象语法树（AST）对查询进行参数化。例如，`SELECT * FROM t WHERE b < 10 AND a = 1` 会被参数化为 `SELECT * FROM t WHERE b < ? and a = ?`。
2. 然后，TiDB 使用参数化后的查询在计划缓存中查找。
3. 如果找到可重用的执行计划，则直接使用，跳过优化阶段。
4. 否则，优化器会生成新的执行计划，并将其加入缓存，以便后续查询复用。

## 用法

你可以通过设置 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache) 系统变量，开启或关闭非预处理执行计划缓存。还可以通过 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710) 系统变量控制非预处理计划缓存的大小。当缓存的计划数超过 `tidb_session_plan_cache_size` 时，TiDB 会采用最近最少使用（LRU）策略进行淘汰。

从 v7.1.0 起，你还可以通过 [`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710) 系统变量控制可缓存计划的最大尺寸。默认值为 2 MB。如果计划的大小超过此值，则不会被缓存。

> **注意：**
>
> `tidb_session_plan_cache_size` 指定的内存是预处理和非预处理计划缓存共享的。如果你已启用当前集群的预处理计划缓存，启用非预处理计划缓存可能会降低原有预处理计划缓存的命中率。

## 示例

以下示例演示如何使用非预处理计划缓存：

1. 创建测试用表 `t`：

    ```sql
    CREATE TABLE t (a INT, b INT, KEY(b));
    ```

2. 开启非预处理计划缓存：

    ```sql
    SET tidb_enable_non_prepared_plan_cache = ON;
    ```

3. 执行以下两个查询：

    ```sql
    SELECT * FROM t WHERE b < 10 AND a = 1;
    SELECT * FROM t WHERE b < 5 AND a = 2;
    ```

4. 查看第二个查询是否命中缓存：

    ```sql
    SELECT @@last_plan_from_cache;
    ```

    如果输出中的 `last_plan_from_cache` 值为 `1`，表示第二个查询的执行计划来自缓存：

    ```sql
    +------------------------+
    | @@last_plan_from_cache |
    +------------------------+
    |                      1 |
    +------------------------+
    1 row in set (0.00 sec)
    ```

## 限制

### 缓存次优计划

TiDB 只会缓存一个参数化查询的执行计划。例如，`SELECT * FROM t WHERE a < 1` 和 `SELECT * FROM t WHERE a < 100000` 共享相同的参数化形式 `SELECT * FROM t WHERE a < ?`，因此共享同一个执行计划。

如果这导致性能问题，可以使用 `ignore_plan_cache()` 提示忽略缓存中的计划，让优化器每次都生成新的执行计划。如果 SQL 无法修改，可以创建绑定解决此问题。例如，`CREATE BINDING FOR SELECT ... USING SELECT /*+ ignore_plan_cache() */ ...`。

### 使用限制

鉴于上述风险，以及执行计划缓存只在简单查询中带来显著益处（如果查询复杂且耗时较长，使用执行计划缓存可能帮助不大），TiDB 对非预处理计划缓存的范围做了严格限制，具体如下：

- 不支持 [预处理计划缓存](/sql-prepared-plan-cache.md) 不支持的查询或计划。
- 不支持包含复杂操作符（如 `Window` 或 `Having`）的查询。
- 不支持包含三个或以上 `Join` 表或子查询的查询。
- 不支持在 `ORDER BY` 或 `GROUP BY` 后直接使用数字或表达式，例如 `ORDER BY 1` 和 `GROUP BY a+1`。只支持 `ORDER BY column_name` 和 `GROUP BY column_name`。
- 不支持对 `JSON`、`ENUM`、`SET` 或 `BIT` 类型列进行过滤的查询，例如 `SELECT * FROM t WHERE json_col = '{}'`。
- 不支持对 `NULL` 值进行过滤的查询，例如 `SELECT * FROM t WHERE a is NULL`。
- 默认不支持参数化后参数个数超过 200 的查询，例如 `SELECT * FROM t WHERE a in (1, 2, 3, ... 201)`。从 v7.3.0 起，可以通过设置 [`44823`](/optimizer-fix-controls.md#44823-new-in-v730) 修复在 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710) 系统变量中的值，修改此限制。
- 不支持访问虚拟列、临时表、视图或内存表的查询，例如 `SELECT * FROM INFORMATION_SCHEMA.COLUMNS`，其中 `COLUMNS` 是 TiDB 内存表。
- 不支持带提示或绑定的查询。
- 默认不支持带 `FOR UPDATE` 子句的 DML 语句或 `SELECT` 语句。若要取消此限制，可以执行 `SET tidb_enable_non_prepared_plan_cache_for_dml = ON`。

启用此功能后，优化器会快速评估查询。如果不满足非预处理计划缓存的支持条件，查询会回退到常规优化流程。

## 性能收益

在内部测试中，启用非预处理计划缓存功能在大多数 TP 场景下能带来显著的性能提升。例如，在 TPC-C 测试中约提升 4%，在某些银行业务负载中提升超过 10%，在 Sysbench RangeScan 中提升 15%。

但此功能也会带来一些额外的内存和 CPU 开销，包括判断查询是否支持、参数化查询以及在缓存中查找计划。如果你的工作负载中大部分查询未命中缓存，启用此功能反而可能影响性能。

在这种情况下，你需要观察 Grafana 中的 **Queries Using Plan Cache OPS** 面板中的 `non-prepared` 指标和 **Plan Cache Miss OPS** 面板中的 `non-prepared-unsupported` 指标。如果大部分查询不支持，只有少数命中计划缓存，可以考虑关闭此功能。

![non-prepared-unsupported](/media/non-prepapred-plan-cache-unsupprot.png)

## 诊断

启用非预处理计划缓存后，可以执行 `EXPLAIN FORMAT='plan_cache' SELECT ...` 来验证查询是否命中缓存。对于未命中的查询，系统会在警告中返回原因。

注意，如果不添加 `FORMAT='plan_cache'`，`EXPLAIN` 不会命中缓存。

要验证查询是否命中缓存，可以执行以下 `EXPLAIN FORMAT='plan_cache'` 语句：

```sql
EXPLAIN FORMAT='plan_cache' SELECT * FROM (SELECT a+1 FROM t) t;
```

输出示例：

```sql
3 rows in set, 1 warning (0.00 sec)
```

查看未命中缓存的查询，可以执行 `SHOW warnings;`：

```sql
SHOW warnings;
```

输出示例：

```sql
+---------+------+-------------------------------------------------------------------------------+
| Level   | Code | Message                                                                       |
+---------+------+-------------------------------------------------------------------------------+
| Warning | 1105 | skip non-prepared plan-cache: queries that have sub-queries are not supported |
+---------+------+-------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

在上述示例中，查询未命中缓存是因为非预处理计划缓存不支持 `+` 操作。

## 监控

启用非预处理计划缓存后，可以在以下面板监控内存使用情况、缓存中的计划数和命中率：

![non-prepare-plan-cache](/media/tidb-non-prepared-plan-cache-metrics.png)

还可以在 `statements_summary` 表和慢查询日志中监控命中率。以下示例演示如何在 `statements_summary` 表中查看命中率：

1. 创建表 `t`：

    ```sql
    CREATE TABLE t (a int);
    ```

2. 开启非预处理计划缓存：

    ```sql
    SET @@tidb_enable_non_prepared_plan_cache=ON;
    ```

3. 执行以下三条查询：

    ```sql
    SELECT * FROM t WHERE a<1;
    SELECT * FROM t WHERE a<2;
    SELECT * FROM t WHERE a<3;
    ```

4. 查询 `statements_summary` 表，查看命中率：

    ```sql
    SELECT digest_text, query_sample_text, exec_count, plan_in_cache, plan_cache_hits FROM INFORMATION_SCHEMA.STATEMENTS_SUMMARY WHERE query_sample_text LIKE '%SELECT * FROM %';
    ```

    输出示例：

    ```sql
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    | digest_text                     | query_sample_text                        | exec_count | plan_in_cache | plan_cache_hits |
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    | SELECT * FROM `t` WHERE `a` < ? | SELECT * FROM t WHERE a<1                |          3 |             1 |               2 |
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    1 row in set (0.01 sec)
    ```

    从输出可以看到，该查询执行了三次，命中缓存两次。