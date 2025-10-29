---
title: FLASHBACK CLUSTER
summary: 了解在 TiDB 数据库中使用 FLASHBACK CLUSTER 的方法。
---

# FLASHBACK CLUSTER

TiDB v6.4.0 引入了 `FLASHBACK CLUSTER TO TIMESTAMP` 语法。你可以使用该语法将集群恢复到某个特定的时间点。在指定时间戳时，你可以设置一个 datetime 值或使用时间函数。datetime 的格式类似于 '2016-10-08 16:45:26.999'，最小时间单位为毫秒。但在大多数情况下，指定以秒为单位的时间戳就足够了，例如 '2016-10-08 16:45:26'。

从 v6.5.6、v7.1.3、v7.5.1 和 v7.6.0 开始，TiDB 引入了 `FLASHBACK CLUSTER TO TSO` 语法。该语法允许你使用 [TSO](/tso.md) 来指定更精确的数据恢复时间点，从而提升数据恢复的灵活性。

> **Warning:**
>
> `FLASHBACK CLUSTER TO [TIMESTAMP|TSO]` 语法不适用于 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群。为避免出现不可预期的结果，请不要在 TiDB Cloud Starter 和 TiDB Cloud Essential 集群上执行该语句。

> **Warning:**
>
> - 在指定恢复时间点时，请务必检查目标 timestamp 或 TSO 的有效性，避免指定超过 PD 当前分配的最大 TSO（可在 Grafana PD 面板的 `Current TSO` 查看）的未来时间。否则，可能会破坏并发处理的线性一致性和事务隔离级别，导致严重的数据正确性问题。
> - 在执行 `FLASHBACK CLUSTER` 期间，数据清理过程不保证事务一致性。在 `FLASHBACK CLUSTER` 完成后，如果你打算使用 TiDB 的任何历史版本读取功能（如 [Stale Read](/stale-read.md) 或 [`tidb_snapshot`](/read-historical-data.md)），请确保指定的历史时间戳不在 `FLASHBACK CLUSTER` 执行期间。读取包含未被 FLASHBACK 完全恢复数据的历史版本，可能会破坏并发处理的线性一致性和事务隔离级别，导致严重的数据正确性问题。

<CustomContent platform="tidb">

> **Warning:**
>
> 当你在 TiDB v7.1.0 中使用该功能时，即使 FLASHBACK 操作完成，部分 Region 可能仍处于 FLASHBACK 过程中。建议避免在 v7.1.0 中使用该功能。详情可参考 issue [#44292](https://github.com/pingcap/tidb/issues/44292)。
>
> 如果你遇到此问题，可以使用 [TiDB 快照备份与恢复](/br/br-snapshot-guide.md) 功能进行数据恢复。

</CustomContent>

> **Note:**
>
> `FLASHBACK CLUSTER TO [TIMESTAMP|TSO]` 的工作原理是将指定时间点的旧数据以最新的时间戳写入，并不会删除当前数据。因此，在使用该功能前，你需要确保有足够的存储空间用于存放旧数据和当前数据。

## 语法

```sql
FLASHBACK CLUSTER TO TIMESTAMP '2022-09-21 16:02:50';
FLASHBACK CLUSTER TO TSO 445494839813079041;
```

### 语法说明

```ebnf+diagram
FlashbackToTimestampStmt
         ::= 'FLASHBACK' 'CLUSTER' 'TO' ('TIMESTAMP' stringLit | 'TSO' LengthNum)
```

## 注意事项

* `FLASHBACK` 语句中指定的时间必须在垃圾回收（GC）生命周期内。系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)（默认值：`10m0s`）定义了行的历史版本的保留时间。可以通过以下查询获取当前垃圾回收已执行到的 `safePoint`：

    ```sql
    SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
    ```

<CustomContent platform='tidb'>

* 只有拥有 `SUPER` 权限的用户才能执行 `FLASHBACK CLUSTER` SQL 语句。
* `FLASHBACK CLUSTER` 不支持回滚修改 PD 相关信息的 DDL 语句，如 `ALTER TABLE ATTRIBUTE`、`ALTER TABLE REPLICA` 和 `CREATE PLACEMENT POLICY`。
* 在 `FLASHBACK` 语句指定的时间点，不能存在未完全执行的 DDL 语句。如果存在此类 DDL，TiDB 会拒绝执行。
* 在执行 `FLASHBACK CLUSTER` 前，TiDB 会断开所有相关连接，并禁止对这些表的读写操作，直到 `FLASHBACK CLUSTER` 语句执行完成。
* `FLASHBACK CLUSTER` 语句在执行后无法取消，TiDB 会持续重试直到成功。
* 在执行 `FLASHBACK CLUSTER` 期间，如需备份数据，只能使用 [Backup & Restore](/br/br-snapshot-guide.md) 并指定早于 `FLASHBACK CLUSTER` 开始时间的 `BackupTS`。此外，在 `FLASHBACK CLUSTER` 执行期间，开启 [日志备份](/br/br-pitr-guide.md) 会失败。因此，建议在 `FLASHBACK CLUSTER` 完成后再开启日志备份。
* 如果 `FLASHBACK CLUSTER` 语句导致元数据（表结构、数据库结构）回滚，相关修改将**不会**被 TiCDC 同步。因此，你需要手动暂停任务，等待 `FLASHBACK CLUSTER` 完成后，手动同步上下游的 schema 定义以确保一致。之后需要重新创建 TiCDC changefeed。

</CustomContent>

<CustomContent platform='tidb-cloud'>

* 只有拥有 `SUPER` 权限的用户才能执行 `FLASHBACK CLUSTER` SQL 语句。
* `FLASHBACK CLUSTER` 不支持回滚修改 PD 相关信息的 DDL 语句，如 `ALTER TABLE ATTRIBUTE`、`ALTER TABLE REPLICA` 和 `CREATE PLACEMENT POLICY`。
* 在 `FLASHBACK` 语句指定的时间点，不能存在未完全执行的 DDL 语句。如果存在此类 DDL，TiDB 会拒绝执行。
* 在执行 `FLASHBACK CLUSTER` 前，TiDB 会断开所有相关连接，并禁止对这些表的读写操作，直到 `FLASHBACK CLUSTER` 语句执行完成。
* `FLASHBACK CLUSTER` 语句在执行后无法取消，TiDB 会持续重试直到成功。
* 如果 `FLASHBACK CLUSTER` 语句导致元数据（表结构、数据库结构）回滚，相关修改将**不会**被 TiCDC 同步。因此，你需要手动暂停任务，等待 `FLASHBACK CLUSTER` 完成后，手动同步上下游的 schema 定义以确保一致。之后需要重新创建 TiCDC changefeed。

</CustomContent>

## 示例

以下示例展示了如何将集群 flashback 到某个特定时间戳，以恢复新插入的数据：

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

以下示例展示了如何将集群 flashback 到某个特定 TSO，以精确恢复误删的数据：

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

如果在 `FLASHBACK` 语句指定的时间点存在未完全执行的 DDL 语句，则 `FLASHBACK` 语句会执行失败：

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

你可以通过日志获取 `FLASHBACK` 的执行进度。以下为示例：

```
[2022/10/09 17:25:59.316 +08:00] [INFO] [cluster.go:463] ["flashback cluster stats"] ["complete regions"=9] ["total regions"=10] []
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。