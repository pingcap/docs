---
title: 使用 TiDB 读取 TiFlash 副本
summary: 了解如何使用 TiDB 读取 TiFlash 副本。
---

# 使用 TiDB 读取 TiFlash 副本

本文介绍了如何使用 TiDB 读取 TiFlash 副本。

TiDB 提供了三种方式来读取 TiFlash 副本。如果你添加了 TiFlash 副本且没有进行引擎配置，默认使用的是 CBO（基于成本的优化）模式。

## 智能选择

对于具有 TiFlash 副本的表，TiDB 优化器会根据成本估算自动判断是否使用 TiFlash 副本。你可以使用 `desc` 或 `explain analyze` 语句来检查是否选择了 TiFlash 副本。例如：

```sql
desc select count(*) from test.t;
```

```
+--------------------------+---------+--------------+---------------+--------------------------------+
| id                       | estRows | task         | access object | operator info                  |
+--------------------------+---------+--------------+---------------+--------------------------------+
| StreamAgg_9              | 1.00    | root         |               | funcs:count(1)->Column#4       |
| └─TableReader_17         | 1.00    | root         |               | data:TableFullScan_16          |
|   └─TableFullScan_16     | 1.00    | cop[tiflash] | table:t       | keep order:false, stats:pseudo |
+--------------------------+---------+--------------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

```sql
explain analyze select count(*) from test.t;
```

```
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| id                       | estRows | actRows | task         | access object | execution info                                                       | operator info                  | memory    | disk |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| StreamAgg_9              | 1.00    | 1       | root         |               | time:83.8372ms, loops:2                                              | funcs:count(1)->Column#4       | 372 Bytes | N/A  |
| └─TableReader_17         | 1.00    | 1       | root         |               | time:83.7776ms, loops:2, rpc num: 1, rpc time:83.5701ms, proc keys:0 | data:TableFullScan_16          | 152 Bytes | N/A  |
|   └─TableFullScan_16     | 1.00    | 1       | cop[tiflash] | table:t       | tiflash_task:{time:43ms, loops:1, threads:1}, tiflash_scan:{...}     | keep order:false, stats:pseudo | N/A       | N/A  |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
```

`cop[tiflash]` 表示该任务会被发送到 TiFlash 进行处理。如果你没有选择 TiFlash 副本，可以尝试使用 `analyze table` 语句更新统计信息，然后再用 `explain analyze` 查看结果。

注意，如果一个表只有单个 TiFlash 副本且相关节点无法提供服务，在 CBO 模式下的查询会反复重试。在这种情况下，你需要指定引擎或使用手动提示从 TiKV 副本读取数据。

## 引擎隔离

引擎隔离是通过配置相应变量，指定所有查询都使用指定引擎的副本。可选的引擎有 "tikv"、"tidb"（表示 TiDB 的内部内存表区域，存储一些 TiDB 系统表，用户不能主动使用）和 "tiflash"。

<CustomContent platform="tidb">

你可以在以下两个配置层级指定引擎：

* TiDB 实例级别，即 INSTANCE 层级。在 TiDB 配置文件中添加以下配置项：

    ```
    [isolation-read]
    engines = ["tikv", "tidb", "tiflash"]
    ```

    **默认配置为 `["tikv", "tidb", "tiflash"]`。**

* SESSION 层级。使用以下语句进行配置：

    
    ```sql
    set @@session.tidb_isolation_read_engines = "engine list separated by commas";
    ```

    
    ```sql
    set SESSION tidb_isolation_read_engines = "engine list separated by commas";
    ```

    SESSION 层的默认配置继承自 TiDB 实例层的配置。

最终的引擎配置以会话层配置为准，即会话层配置会覆盖实例层配置。例如，你在实例层配置了 "tikv"，在会话层配置了 "tiflash"，则会读取 TiFlash 副本；如果最终配置为 "tikv" 和 "tiflash"，则会同时读取 TiKV 和 TiFlash 副本，优化器会自动选择更优的引擎执行。

> **Note:**
>
> 因为 [TiDB Dashboard](/dashboard/dashboard-intro.md) 和其他组件需要读取存储在 TiDB 内存表区域的系统表，建议始终在实例层引擎配置中添加 "tidb"。

</CustomContent>

<CustomContent platform="tidb-cloud">

你可以使用以下语句指定引擎：

```sql
set @@session.tidb_isolation_read_engines = "engine list separated by commas";
```

或者

```sql
set SESSION tidb_isolation_read_engines = "engine list separated by commas";
```

</CustomContent>

如果查询的表没有指定引擎的副本（例如，配置为 "tiflash" 但该表没有 TiFlash 副本），查询会返回错误。

## 手动提示

手动提示可以在满足引擎隔离的前提下，强制 TiDB 对特定表或语句使用指定的副本。以下是使用手动提示的示例：

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

如果在查询语句中为表设置了别名，必须在包含提示的语句中使用别名，提示才会生效。例如：

```sql
select /*+ read_from_storage(tiflash[alias_a,alias_b]) */ ... from table_name_1 as alias_a, table_name_2 as alias_b where alias_a.column_1 = alias_b.column_2;
```

上述语句中，`tiflash[]` 提示优化器读取 TiFlash 副本。你也可以使用 `tikv[]` 提示优化器读取 TiKV 副本。关于提示语法的详细信息，请参考 [READ_FROM_STORAGE](/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-)。

如果提示指定的表没有对应引擎的副本，提示会被忽略并报告警告。此外，提示仅在引擎隔离的前提下生效。如果提示中指定的引擎不在引擎隔离列表中，也会被忽略并报告警告。

> **Note:**
>
> 5.7.7 及之前版本的 MySQL 客户端默认会清除优化器提示。若要在这些早期版本中使用提示语法，需要以 `--comments` 选项启动客户端，例如：`mysql -h 127.0.0.1 -P 4000 -uroot --comments`。

## 智能选择、引擎隔离和手动提示的关系

在上述三种读取 TiFlash 副本的方式中，引擎隔离定义了引擎副本的整体范围；在此范围内，手动提示提供了更细粒度的语句级和表级引擎选择；最终，优化器会在指定的引擎列表中，根据成本估算自动选择更优的引擎副本。

> **Note:**
>
> - 在 v4.0.3 之前，非只读 SQL 语句（例如 `INSERT INTO ... SELECT`、`SELECT ... FOR UPDATE`、`UPDATE ...`、`DELETE ...`）读取 TiFlash 副本的行为未定义。
> - 从 v4.0.3 到 v6.2.0 版本，TiDB 内部会忽略非只读 SQL 语句的 TiFlash 副本，以保证数据正确性。也就是说，对于 [smart selection](#smart-selection)，TiDB 会自动选择非 TiFlash 副本；对于 [engine isolation](#engine-isolation) 只指定 TiFlash 副本，TiDB 会报错；对于 [manual hint](#manual-hint)，TiDB 会忽略提示。
> - 从 v6.3.0 到 v7.0.0 版本，如果启用了 TiFlash 副本，可以使用 [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630) 变量控制 TiDB 是否对非只读 SQL 语句使用 TiFlash 副本。
> - 从 v7.1.0 开始，如果启用了 TiFlash 副本，且当前会话的 [SQL Mode](/sql-mode.md) 不是严格模式（即 `sql_mode` 不包含 `STRICT_TRANS_TABLES` 或 `STRICT_ALL_TABLES`），TiDB 会根据成本估算自动决定是否对非只读 SQL 语句使用 TiFlash 副本。