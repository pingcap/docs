---
title: PROCESSLIST
summary: 了解 `PROCESSLIST` information_schema 表。
---

# PROCESSLIST

`PROCESSLIST`，与 [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md) 类似，用于查看正在处理的请求。

`PROCESSLIST` 表包含了一些 `SHOW PROCESSLIST` 中没有的额外列：

<CustomContent platform="tidb">

* `DIGEST` 列，用于显示 SQL 语句的摘要。
* `MEM` 列，用于显示当前请求已使用的内存，单位为字节。
* `DISK` 列，用于显示磁盘使用量，单位为字节。
* `TxnStart` 列，用于显示事务的开始时间。
* `RESOURCE_GROUP` 列，用于显示资源组名称。
* `SESSION_ALIAS` 列，用于显示当前会话的别名。
* `ROWS_AFFECTED` 列，用于显示当前语句影响的行数。
* `TIDB_CPU` 列，用于显示该语句在 TiDB 服务器上消耗的 CPU 时间，单位为纳秒。只有在启用 [Top SQL](/dashboard/top-sql.md) 功能时，该列才有意义，否则值为 `0`。
* `TIKV_CPU` 列，用于显示该语句在 TiKV 服务器上消耗的 CPU 时间，单位为纳秒。

</CustomContent>

<CustomContent platform="tidb-cloud">

* `DIGEST` 列，用于显示 SQL 语句的摘要。
* `MEM` 列，用于显示当前请求已使用的内存，单位为字节。
* `DISK` 列，用于显示磁盘使用量，单位为字节。
* `TxnStart` 列，用于显示事务的开始时间。
* `RESOURCE_GROUP` 列，用于显示资源组名称。
* `SESSION_ALIAS` 列，用于显示当前会话的别名。
* `ROWS_AFFECTED` 列，用于显示当前语句影响的行数。
* `TIDB_CPU` 列，用于显示该语句在 TiDB 服务器上消耗的 CPU 时间，单位为纳秒。只有在启用 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) 功能时，该列才有意义，否则值为 `0`。
* `TIKV_CPU` 列，用于显示该语句在 TiKV 服务器上消耗的 CPU 时间，单位为纳秒。

</CustomContent>

```sql
USE information_schema;
DESC processlist;
```

```sql
+----------------+---------------------+------+------+---------+-------+
| Field          | Type                | Null | Key  | Default | Extra |
+----------------+---------------------+------+------+---------+-------+
| ID             | bigint(21) unsigned | NO   |      | 0       |       |
| USER           | varchar(16)         | NO   |      |         |       |
| HOST           | varchar(64)         | NO   |      |         |       |
| DB             | varchar(64)         | YES  |      | NULL    |       |
| COMMAND        | varchar(16)         | NO   |      |         |       |
| TIME           | int(7)              | NO   |      | 0       |       |
| STATE          | varchar(7)          | YES  |      | NULL    |       |
| INFO           | longtext            | YES  |      | NULL    |       |
| DIGEST         | varchar(64)         | YES  |      |         |       |
| MEM            | bigint(21) unsigned | YES  |      | NULL    |       |
| DISK           | bigint(21) unsigned | YES  |      | NULL    |       |
| TxnStart       | varchar(64)         | NO   |      |         |       |
| RESOURCE_GROUP | varchar(32)         | NO   |      |         |       |
| SESSION_ALIAS  | varchar(64)         | NO   |      |         |       |
| ROWS_AFFECTED  | bigint(21) unsigned | YES  |      | NULL    |       |
| TIDB_CPU       | bigint(21)          | NO   |      | 0       |       |
| TIKV_CPU       | bigint(21)          | NO   |      | 0       |       |
+----------------+---------------------+------+------+---------+-------+
```

```sql
SELECT * FROM information_schema.processlist\G
```

```sql
*************************** 1. row ***************************
            ID: 1268776964
          USER: root
          HOST: 127.0.0.1:59922
            DB: NULL
       COMMAND: Query
          TIME: 0
         STATE: autocommit
          INFO: SELECT * FROM information_schema.processlist
        DIGEST: 4b5e7cdd5d3ed84d6c1a6d56403a3d512554b534313caf296268abdec1c9ea99
           MEM: 0
          DISK: 0
      TxnStart:
RESOURCE_GROUP: default
 SESSION_ALIAS:
 ROWS_AFFECTED: 0
      TIDB_CPU: 0
      TIKV_CPU: 0
```

`PROCESSLIST` 表中的各字段说明如下：

<CustomContent platform="tidb">

* `ID`：用户连接的 ID。
* `USER`：执行 `PROCESS` 的用户名。
* `HOST`：用户连接的地址。
* `DB`：当前连接的默认数据库名称。
* `COMMAND`：`PROCESS` 正在执行的命令类型。
* `TIME`：`PROCESS` 当前的执行时长，单位为秒。
* `STATE`：当前连接的状态。
* `INFO`：正在处理的请求语句。
* `DIGEST`：SQL 语句的摘要。
* `MEM`：当前请求已使用的内存，单位为字节。
* `DISK`：磁盘使用量，单位为字节。
* `TxnStart`：事务的开始时间。
* `RESOURCE_GROUP`：资源组名称。
* `SESSION_ALIAS`：当前会话的别名。
* `ROWS_AFFECTED`：当前语句影响的行数。
* `TIDB_CPU`：该语句在 TiDB 服务器上消耗的 CPU 时间，单位为纳秒。只有在启用 [Top SQL](/dashboard/top-sql.md) 功能时，该列才有意义，否则值为 `0`。
* `TIKV_CPU`：该语句在 TiKV 服务器上消耗的 CPU 时间，单位为纳秒。

</CustomContent>

<CustomContent platform="tidb-cloud">

* `ID`：用户连接的 ID。
* `USER`：执行 `PROCESS` 的用户名。
* `HOST`：用户连接的地址。
* `DB`：当前连接的默认数据库名称。
* `COMMAND`：`PROCESS` 正在执行的命令类型。
* `TIME`：`PROCESS` 当前的执行时长，单位为秒。
* `STATE`：当前连接的状态。
* `INFO`：正在处理的请求语句。
* `DIGEST`：SQL 语句的摘要。
* `MEM`：当前请求已使用的内存，单位为字节。
* `DISK`：磁盘使用量，单位为字节。
* `TxnStart`：事务的开始时间。
* `RESOURCE_GROUP`：资源组名称。
* `SESSION_ALIAS`：当前会话的别名。
* `ROWS_AFFECTED`：当前语句影响的行数。
* `TIDB_CPU`：该语句在 TiDB 服务器上消耗的 CPU 时间，单位为纳秒。只有在启用 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) 功能时，该列才有意义，否则值为 `0`。
* `TIKV_CPU`：该语句在 TiKV 服务器上消耗的 CPU 时间，单位为纳秒。

</CustomContent>

## CLUSTER_PROCESSLIST

`CLUSTER_PROCESSLIST` 是对应于 `PROCESSLIST` 的集群系统表，用于查询集群中所有 TiDB 节点的 `PROCESSLIST` 信息。`CLUSTER_PROCESSLIST` 的表结构比 `PROCESSLIST` 多一个 `INSTANCE` 列，用于存储该行数据所属的 TiDB 节点地址。

```sql
SELECT * FROM information_schema.cluster_processlist;
```

```sql
+-----------------+------------+------+-----------------+------+---------+------+------------+------------------------------------------------------+------------------------------------------------------------------+------+------+----------------------------------------+----------------+---------------+---------------+----------+----------+
| INSTANCE        | ID         | USER | HOST            | DB   | COMMAND | TIME | STATE      | INFO                                                 | DIGEST                                                           | MEM  | DISK | TxnStart                               | RESOURCE_GROUP | SESSION_ALIAS | ROWS_AFFECTED | TIDB_CPU | TIKV_CPU |
+-----------------+------------+------+-----------------+------+---------+------+------------+------------------------------------------------------+------------------------------------------------------------------+------+------+----------------------------------------+----------------+---------------+---------------+----------+----------+
| 127.0.0.1:10080 | 1268776964 | root | 127.0.0.1:59922 | NULL | Query   |    0 | autocommit | SELECT * FROM information_schema.cluster_processlist | b1e38e59fbbc3e2b35546db5c8053040db989a497ac6cd71ff8dd4394395701a |    0 |    0 | 07-29 12:39:24.282(451471727468740609) | default        |               |             0 |        0 |        0 |
+-----------------+------------+------+-----------------+------+---------+------+------------+------------------------------------------------------+------------------------------------------------------------------+------+------+----------------------------------------+----------------+---------------+---------------+----------+----------+
```

## 权限

如果当前用户没有 `PROCESS` 权限，`PROCESSLIST` 只会显示该用户自己会话的请求。