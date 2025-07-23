---
title: TiFlash Late Materialization
summary: 描述如何使用 TiFlash late materialization 功能在 OLAP 场景中加速查询。
---

# TiFlash Late Materialization

> **Note:**
>
> TiFlash late materialization 不会在 [fast scan mode](/tiflash/use-fastscan.md) 中生效。

TiFlash late materialization 是一种优化方法，用于在 OLAP 场景中加速查询。你可以使用 [`tidb_opt_enable_late_materialization`](/system-variables.md#tidb_opt_enable_late_materialization-new-in-v700) 系统变量来控制是否启用或禁用 TiFlash late materialization。

- 当其被禁用时，为了处理带有过滤条件（`WHERE` 子句）的 `SELECT` 语句，TiFlash 会读取所有查询所需列的数据，然后根据查询条件进行过滤和聚合。
- 当其被启用时，TiFlash 支持将部分过滤条件下推到 TableScan 操作符。也就是说，TiFlash 首先扫描与过滤条件相关的列数据（被下推到 TableScan 的过滤条件），过滤出满足条件的行，然后再扫描这些行的其他列数据进行后续计算，从而减少 IO 扫描和数据处理的计算量。

为了提升某些查询在 OLAP 场景中的性能，从 v7.1.0 版本开始，TiFlash late materialization 功能默认开启。TiDB 优化器可以根据统计信息和过滤条件判断哪些过滤条件需要下推，并优先下推过滤率高的条件。关于详细的算法细节，参见 [RFC 文档](https://github.com/pingcap/tidb/tree/release-8.5/docs/design/2022-12-06-support-late-materialization.md)。

例如：

```sql
EXPLAIN SELECT a, b, c FROM t1 WHERE a < 1;
```

```
+-------------------------+----------+--------------+---------------+-------------------------------------------------------+
| id                      | estRows  | task         | access object | operator info                                         |
+-------------------------+----------+--------------+---------------+-------------------------------------------------------+
| TableReader_12          | 12288.00 | root         |               | MppVersion: 1, data:ExchangeSender_11                 |
| └─ExchangeSender_11     | 12288.00 | mpp[tiflash] |               | ExchangeType: PassThrough                             |
|   └─TableFullScan_9     | 12288.00 | mpp[tiflash] | table:t1      | pushed down filter:lt(test.t1.a, 1), keep order:false |
+-------------------------+----------+--------------+---------------+-------------------------------------------------------+
```

在此示例中，过滤条件 `a < 1` 被下推到 TableScan 操作符。TiFlash 首先读取列 `a` 的所有数据，然后过滤出满足 `a < 1` 条件的行。接着，TiFlash 读取这些行的列 `b` 和 `c`。

## Enable or disable TiFlash late materialization

默认情况下，`tidb_opt_enable_late_materialization` 系统变量在会话和全局层面均为 `ON`，意味着 TiFlash late materialization 功能已启用。你可以使用以下语句查看对应的变量信息：

```sql
SHOW VARIABLES LIKE 'tidb_opt_enable_late_materialization';
```

```
+--------------------------------------+-------+
| Variable_name                        | Value |
+--------------------------------------+-------+
| tidb_opt_enable_late_materialization | ON    |
+--------------------------------------+-------+
```

```sql
SHOW GLOBAL VARIABLES LIKE 'tidb_opt_enable_late_materialization';
```

```
+--------------------------------------+-------+
| Variable_name                        | Value |
+--------------------------------------+-------+
| tidb_opt_enable_late_materialization | ON    |
+--------------------------------------+-------+
```

你可以在会话层面或全局层面修改 `tidb_opt_enable_late_materialization` 变量。

- 若要在当前会话中禁用 TiFlash late materialization，使用以下语句：

    ```sql
    SET SESSION tidb_opt_enable_late_materialization=OFF;
    ```

- 若要在全局层面禁用 TiFlash late materialization，使用以下语句：

    ```sql
    SET GLOBAL tidb_opt_enable_late_materialization=OFF;
    ```

    设置后，`tidb_opt_enable_late_materialization` 变量在新会话中默认会启用。

若要启用 TiFlash late materialization，使用以下语句：

```sql
SET SESSION tidb_opt_enable_late_materialization=ON;
```

```sql
SET GLOBAL tidb_opt_enable_late_materialization=ON;
```

## Implementation mechanism

当过滤条件被下推到 TableScan 操作符时，TableScan 的执行过程主要包括以下步骤：

1. 读取 `<handle, del_mark, version>` 三个列，进行多版本并发控制（MVCC）过滤，并生成 MVCC Bitmap。
2. 读取与过滤条件相关的列，过滤出满足条件的行，并生成 Filter Bitmap。
3. 对 MVCC Bitmap 和 Filter Bitmap 进行 `AND` 操作，生成 Final Bitmap。
4. 根据 Final Bitmap 读取剩余列的对应行数据。
5. 将步骤 2 和步骤 4 中读取的数据合并，返回结果。
