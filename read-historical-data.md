---
title: 使用系统变量 `tidb_snapshot` 读取历史数据
summary: 了解 TiDB 如何使用系统变量 `tidb_snapshot` 从历史版本中读取数据。
---

# 使用系统变量 `tidb_snapshot` 读取历史数据

本文档介绍了如何使用系统变量 `tidb_snapshot` 从历史版本中读取数据，包括具体的使用示例和保存历史数据的策略。

> **Note:**
>
> 你也可以使用 [Stale Read](/stale-read.md) 功能来读取历史数据，更加推荐。

## 功能描述

TiDB 实现了一个功能，可以通过标准的 SQL 接口直接读取历史数据，无需特殊的客户端或驱动。

> **Note:**
>
> - 即使数据被更新或删除，其历史版本仍然可以通过 SQL 接口读取。
> - 在读取历史数据时，TiDB 会返回使用旧表结构的数据，即使当前表结构已发生变化。

## TiDB 如何从历史版本中读取数据

引入 [`tidb_snapshot`](/system-variables.md#tidb_snapshot) 系统变量以支持读取历史数据。关于 `tidb_snapshot` 变量：

- 该变量在 `SESSION` 作用域内有效。
- 可以使用 `SET` 语句修改其值。
- 变量的数据类型为文本。
- 该变量接受 TSO（Timestamp Oracle）和 datetime。TSO 是由 PD 获取的全局唯一时间服务。可接受的 datetime 格式为 "2016-10-08 16:45:26.999"。通常，datetime 可以设置为秒级精度，例如 "2016-10-08 16:45:26"。
- 设置该变量后，TiDB 会根据其值创建一个 Snapshot，使用该值作为时间戳，仅用于数据结构，不会带来任何开销。之后，所有的 `SELECT` 操作都将从此 Snapshot 中读取数据。

> **Note:**
>
> 由于 TiDB 事务中的时间戳由 Placement Driver（PD）分配，存储数据的版本号也会根据 PD 分配的时间戳标记。当创建 Snapshot 时，版本号基于 `tidb_snapshot` 变量的值。如果 TiDB 服务器的本地时间与 PD 服务器存在较大差异，应使用 PD 服务器的时间。

从历史版本中读取数据后，可以通过结束当前 Session 或使用 `SET` 语句将 `tidb_snapshot` 变量的值设置为空字符串 ""，以读取最新版本的数据。

## TiDB 如何管理数据版本

TiDB 实现了多版本并发控制（MVCC）来管理数据版本。数据的历史版本被保留，因为每次更新/删除都会创建一个新的数据版本，而不是就地更新/删除数据对象。但并非所有版本都被保留。如果版本早于某个特定时间，它们将被完全删除，以减少存储占用和由过多历史版本带来的性能开销。

在 TiDB 中，垃圾回收（GC）会定期运行，以删除过时的数据版本。关于 GC 的详细信息，请参见 [TiDB 垃圾回收（GC）](/garbage-collection-overview.md)。

特别注意以下内容：

- [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)：此系统变量用于配置早期修改的保留时间（默认：`10m0s`）。
- 通过执行 `SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point'` 可以查看当前的 `safePoint`，即你可以读取历史数据的最大时间点。该值在每次垃圾回收运行时更新。

## 示例

1. 初始阶段，创建表并插入几行数据：

    ```sql
    mysql> create table t (c int);
    Query OK, 0 rows affected (0.01 sec)

    mysql> insert into t values (1), (2), (3);
    Query OK, 3 rows affected (0.00 sec)
    ```

2. 查看表中的数据：

    ```sql
    mysql> select * from t;
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

3. 查看表的时间戳：

    ```sql
    mysql> select now();
    +---------------------+
    | now()               |
    +---------------------+
    | 2016-10-08 16:45:26 |
    +---------------------+
    1 row in set (0.00 sec)
    ```

4. 更新一行数据：

    ```sql
    mysql> update t set c=22 where c=2;
    Query OK, 1 row affected (0.00 sec)
    ```

5. 确认数据已更新：

    ```sql
    mysql> select * from t;
    +------+
    | c    |
    +------+
    |    1 |
    |   22 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

6. 设置 `tidb_snapshot` 变量（作用域为 Session），使其值为更新前的时间点，以便读取更新前的历史数据。

    > **Note:**
    >
    > 在此示例中，值设置为更新操作之前的时间。

    ```sql
    mysql> set @@tidb_snapshot="2016-10-08 16:45:26";
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **Note:**
    >
    > 你应使用 `@@` 而非 `@`，因为 `@@` 用于表示系统变量，`@` 用于表示用户变量。

    **结果：** 从以下查询中读取到的是更新操作之前的数据，即历史数据。

    ```sql
    mysql> select * from t;
    +------+  
    | c    |
    +------+  
    |    1 |
    |    2 |
    |    3 |
    +------+  
    3 rows in set (0.00 sec)
    ```

7. 将 `tidb_snapshot` 变量设置为空字符串 ""，即可读取最新版本的数据：

    ```sql
    mysql> set @@tidb_snapshot="";
    Query OK, 0 rows affected (0.00 sec)
    ```

    ```sql
    mysql> select * from t;
    +------+  
    | c    |
    +------+  
    |    1 |
    |   22 |
    |    3 |
    +------+  
    3 rows in set (0.00 sec)
    ```

    > **Note:**
    >
    > 你应使用 `@@` 而非 `@`，因为 `@@` 用于表示系统变量，`@` 用于表示用户变量。

## 如何恢复历史数据

在恢复较旧版本的数据之前，确保垃圾回收（GC）不会在你操作期间清除历史数据。可以通过设置 `tidb_gc_life_time` 变量实现，如以下示例所示。恢复后不要忘记将变量恢复到之前的值。

```sql
SET GLOBAL tidb_gc_life_time="60m";
```

> **Note:**
>
> 将 GC 生命周期从默认的 10 分钟增加到半小时或更长时间，会导致额外版本的行被保留，可能需要更多的磁盘空间。这也可能影响某些操作的性能，比如扫描，因为 TiDB 在读取数据时需要跳过这些额外的版本。

要从较旧版本恢复数据，可以使用以下方法之一：

- 对于简单情况，在设置 `tidb_snapshot` 变量后使用 [`SELECT`](/sql-statements/sql-statement-select.md)，复制粘贴输出，或使用 `SELECT ... INTO OUTFILE`，然后用 [`LOAD DATA`](/sql-statements/sql-statement-load-data.md) 导入数据。
- 使用 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-historical-data-snapshots-of-tidb) 导出历史快照。Dumpling 在导出较大数据集时表现良好。