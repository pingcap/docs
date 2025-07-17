---
title: FLASHBACK CLUSTER
summary: 了解 TiDB 数据库中 FLASHBACK CLUSTER 的用法。
---

# FLASHBACK CLUSTER

TiDB v6.4.0 引入了 `FLASHBACK CLUSTER TO TIMESTAMP` 语法。你可以使用它将集群恢复到某个特定的时间点。在指定时间戳时，可以设置为日期时间值或使用时间函数。日期时间的格式类似于 '2016-10-08 16:45:26.999'，毫秒为最小时间单位。但在大多数情况下，使用秒作为时间单位的时间戳（例如 '2016-10-08 16:45:26'）已足够。

从 v6.5.6、v7.1.3、v7.5.1 和 v7.6.0 开始，TiDB 引入了 `FLASHBACK CLUSTER TO TSO` 语法。该语法允许你使用 [TSO](/tso.md) 来指定更精确的恢复点，从而增强数据恢复的灵活性。

> **Warning:**
>
> `FLASHBACK CLUSTER TO [TIMESTAMP|TSO]` 语法不适用于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群。为了避免意外结果，不要在 {{{ .starter }}} 集群上执行此语句。

> **Warning:**
>
> - 在指定恢复时间点时，确保目标时间戳或 TSO 的有效性，避免指定超过 PD 当前分配的最大 TSO 的未来时间（可在 Grafana PD 面板的 `Current TSO` 查看）。否则，可能会违反并发处理线性一致性和事务隔离级别，导致严重的数据正确性问题。
> - 在 `FLASHBACK CLUSTER` 执行期间，数据清理过程不保证事务一致性。`FLASHBACK CLUSTER` 完成后，如果你打算使用 TiDB 的任何历史版本读取功能（如 [Stale Read](/stale-read.md) 或 [`tidb_snapshot`](/read-historical-data.md)），请确保指定的历史时间戳在 `FLASHBACK CLUSTER` 执行期间之外。读取包含未完全恢复数据的历史版本可能会违反并发处理线性一致性和事务隔离级别，导致严重的数据正确性问题。

<CustomContent platform="tidb">

> **Warning:**
>
> 在 TiDB v7.1.0 中使用此功能时，部分 Region 在完成 FLASHBACK 操作后仍可能处于 FLASHBACK 过程中。建议避免在 v7.1.0 中使用此功能。更多信息请参见 issue [#44292](https://github.com/pingcap/tidb/issues/44292)。
>
> 如果遇到此问题，可以使用 [TiDB snapshot backup and restore](/br/br-snapshot-guide.md) 功能进行数据恢复。

</CustomContent>

> **Note:**
>
> `FLASHBACK CLUSTER TO [TIMESTAMP|TSO]` 的工作原理是用最新的时间戳写入某个时间点的旧数据，而不会删除当前数据。因此，在使用此功能前，需要确保有足够的存储空间容纳旧数据和当前数据。

## 语法

```sql
FLASHBACK CLUSTER TO TIMESTAMP '2022-09-21 16:02:50';
FLASHBACK CLUSTER TO TSO 445494839813079041;
```

### 语法结构

```ebnf+diagram
FlashbackToTimestampStmt
         ::= 'FLASHBACK' 'CLUSTER' 'TO' ('TIMESTAMP' stringLit | 'TSO' LengthNum)
```

## 注意事项

* `FLASHBACK` 语句中指定的时间必须在 Garbage Collection (GC) 生命周期内。系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)（默认值：`10m0s`）定义了行的早期版本的保留时间。可以通过以下查询获取当前已执行 GC 的 `safePoint`：

    ```sql
    SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
    ```

<CustomContent platform='tidb'>

* 只有具有 `SUPER` 权限的用户才能执行 `FLASHBACK CLUSTER` SQL 语句。
* `FLASHBACK CLUSTER` 不支持回滚修改 PD 相关信息的 DDL 语句，例如 `ALTER TABLE ATTRIBUTE`、`ALTER TABLE REPLICA` 和 `CREATE PLACEMENT POLICY`。
* 在 `FLASHBACK` 语句指定的时间点，不能存在未完全执行的 DDL 语句。如果存在，TiDB 会拒绝执行。
* 在执行 `FLASHBACK CLUSTER` 之前，TiDB 会断开所有相关连接，并禁止对这些表进行读写操作，直到 `FLASHBACK CLUSTER` 完成。
* `FLASHBACK CLUSTER` 语句一旦执行后不能取消。TiDB 会持续重试直到成功。
* 在 `FLASHBACK CLUSTER` 执行期间，如果需要备份数据，只能使用 [Backup & Restore](/br/br-snapshot-guide.md)，并指定一个早于 `FLASHBACK CLUSTER` 开始时间的 `BackupTS`。此外，在 `FLASHBACK CLUSTER` 执行期间启用 [log backup](/br/br-pitr-guide.md) 会失败，建议在完成后再启用。
* 如果 `FLASHBACK CLUSTER` 语句导致元数据（表结构、数据库结构）回滚，相关修改不会被 TiCDC 复制。因此，你需要手动暂停任务，等待 `FLASHBACK CLUSTER` 完成，并手动同步上游和下游的 schema 定义，确保一致性。之后，还需重新创建 TiCDC changefeed。

</CustomContent>

<CustomContent platform='tidb-cloud'>

* 只有具有 `SUPER` 权限的用户才能执行 `FLASHBACK CLUSTER` SQL 语句。
* `FLASHBACK CLUSTER` 不支持回滚修改 PD 相关信息的 DDL 语句，例如 `ALTER TABLE ATTRIBUTE`、`ALTER TABLE REPLICA` 和 `CREATE PLACEMENT POLICY`。
* 在 `FLASHBACK` 语句指定的时间点，不能存在未完全执行的 DDL 语句。如果存在，TiDB 会拒绝执行。
* 在执行 `FLASHBACK CLUSTER` 之前，TiDB 会断开所有相关连接，并禁止对这些表进行读写操作，直到 `FLASHBACK CLUSTER` 完成。
* `FLASHBACK CLUSTER` 语句一旦执行后不能取消。TiDB 会持续重试直到成功。
* 如果 `FLASHBACK CLUSTER` 语句导致元数据（表结构、数据库结构）回滚，相关修改不会被 TiCDC 复制。因此，你需要手动暂停任务，等待 `FLASHBACK CLUSTER` 完成，并手动同步上游和下游的 schema 定义，确保一致性。之后，还需重新创建 TiCDC changefeed。

</CustomContent>

## 示例

以下示例演示如何将集群回滚到某个时间戳，以恢复新插入的数据：

```sql
mysql> CREATE TABLE t(a INT);
Query OK, 0 rows affected (0.09 sec)

mysql> SELECT * FROM t;
Empty set (0.01 sec)

mysql> SELECT now();
+---------------------+
| now()               |
+---------------------+
| 2022-09-28 17:24:16 |
+---------------------+
1 row in set (0.02 sec)

mysql> INSERT INTO t VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.01 sec)

mysql> FLASHBACK CLUSTER TO TIMESTAMP '2022-09-28 17:24:16';
Query OK, 0 rows affected (0.20 sec)

mysql> SELECT * FROM t;
Empty set (0.00 sec)
```

以下示例演示如何将集群回滚到某个 TSO，以精确恢复误删的数据：

```sql
mysql> INSERT INTO t VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.01 sec)


mysql> BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT @@tidb_current_ts;  -- 获取当前 TSO
+--------------------+
| @@tidb_current_ts  |
+--------------------+
| 446113975683252225 |
+--------------------+
1 row in set (0.00 sec)

mysql> ROLLBACK;
Query OK, 0 rows affected (0.00 sec)


mysql> DELETE FROM t;
Query OK, 1 rows affected (0.00 sec)


mysql> FLASHBACK CLUSTER TO TSO 446113975683252225;
Query OK, 0 rows affected (0.20 sec)

mysql> SELECT * FROM t;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.01 sec)
```

如果在 `FLASHBACK` 语句指定的时间点存在未完全执行的 DDL 语句，`FLASHBACK` 会失败：

```sql
mysql> ALTER TABLE t ADD INDEX k(a);
Query OK, 0 rows affected (0.56 sec)

mysql> ADMIN SHOW DDL JOBS 1;
+--------+---------+-----------------------+------------------------+--------------+-----------+----------+-----------+---------------------+---------------------+---------------------+--------+
| JOB_ID | DB_NAME | TABLE_NAME            | JOB_TYPE               | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | CREATE_TIME         | START_TIME          | END_TIME            | STATE  |
+--------+---------+-----------------------+------------------------+--------------+-----------+----------+-----------+---------------------+---------------------+---------------------+--------+
|     84 | test    | t                     | add index /* ingest */ | public       |         2 |       82 |         0 | 2023-01-29 14:33:11 | 2023-01-29 14:33:11 | 2023-01-29 14:33:12 | synced |
+--------+---------+-----------------------+------------------------+--------------+-----------+----------+-----------+---------------------+---------------------+---------------------+--------+
1 rows in set (0.01 sec)

mysql> FLASHBACK CLUSTER TO TIMESTAMP '2023-01-29 14:33:12';
ERROR 1105 (HY000): Detected another DDL job at 2023-01-29 14:33:12 +0800 CST, can't do flashback
```

通过日志可以获取 `FLASHBACK` 的执行进度，示例如下：

```
[2022/10/09 17:25:59.316 +08:00] [INFO] [cluster.go:463] ["flashback cluster stats"] ["complete regions"=9] ["total regions"=10] []
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。