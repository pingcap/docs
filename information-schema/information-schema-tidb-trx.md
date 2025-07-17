---
title: TIDB_TRX
summary: 了解 `TIDB_TRX` INFORMATION_SCHEMA 表。
---

# TIDB_TRX

`TIDB_TRX` 表提供关于当前在 TiDB 节点上执行的事务的信息。

```sql
USE INFORMATION_SCHEMA;
DESC TIDB_TRX;
```

输出结果如下：

```sql
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| Field                   | Type                                                            | Null | Key  | Default | Extra |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| ID                      | bigint(21) unsigned                                             | NO   | PRI  | NULL    |       |
| START_TIME              | timestamp(6)                                                    | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST      | varchar(64)                                                     | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST_TEXT | text                                                            | YES  |      | NULL    |       |
| STATE                   | enum('Idle','Running','LockWaiting','Committing','RollingBack') | YES  |      | NULL    |       |
| WAITING_START_TIME      | timestamp(6)                                                    | YES  |      | NULL    |       |
| MEM_BUFFER_KEYS         | bigint(64)                                                      | YES  |      | NULL    |       |
| MEM_BUFFER_BYTES        | bigint(64)                                                      | YES  |      | NULL    |       |
| SESSION_ID              | bigint(21) unsigned                                             | YES  |      | NULL    |       |
| USER                    | varchar(16)                                                     | YES  |      | NULL    |       |
| DB                      | varchar(64)                                                     | YES  |      | NULL    |       |
| ALL_SQL_DIGESTS         | text                                                            | YES  |      | NULL    |       |
| RELATED_TABLE_IDS       | text                                                            | YES  |      | NULL    |       |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
```

`TIDB_TRX` 表中每个字段的含义如下：

* `ID`：事务 ID，即事务的 `start_ts`（开始时间戳）。
* `START_TIME`：事务的开始时间，即对应事务的 `start_ts` 的物理时间。
* `CURRENT_SQL_DIGEST`：事务当前正在执行的 SQL 语句的 digest。
* `CURRENT_SQL_DIGEST_TEXT`：事务当前执行的 SQL 语句的规范化形式，即不带参数和格式的 SQL 语句。它对应 `CURRENT_SQL_DIGEST`。
* `STATE`：事务的当前状态。可能的取值包括：
    * `Idle`：事务处于空闲状态，即等待用户输入查询。
    * `Running`：事务正在执行查询。
    * `LockWaiting`：事务正在等待获取悲观锁。注意，事务在开始悲观锁操作时，无论是否被其他事务阻塞，都会进入此状态。
    * `Committing`：事务正在提交中。
    * `RollingBack`：事务正在回滚。
* `WAITING_START_TIME`：当 `STATE` 为 `LockWaiting` 时，此列显示等待开始的时间。
* `MEM_BUFFER_KEYS`：当前事务写入内存缓冲区的键数量。
* `MEM_BUFFER_BYTES`：当前事务写入内存缓冲区的键值对总字节数。
* `SESSION_ID`：所属会话的 ID。
* `USER`：执行事务的用户名称。
* `DB`：事务执行时的当前默认数据库名称。
* `ALL_SQL_DIGESTS`：事务已执行的语句的 digest 列表。以 JSON 格式的字符串数组显示。每个事务最多记录前 50 条语句。可以使用 [`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests) 函数，将此列中的信息转换为对应的规范化 SQL 语句列表。
* `RELATED_TABLE_IDS`：事务访问的表、视图及其他对象的 ID 列表。

> **Note:**
>
> * 只有具有 [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) 权限的用户才能获取此表的完整信息。没有 PROCESS 权限的用户只能查询自己执行的事务信息。
> * `CURRENT_SQL_DIGEST` 和 `ALL_SQL_DIGESTS` 列中的信息（SQL digest）是由规范化 SQL 语句计算得到的哈希值。`CURRENT_SQL_DIGEST_TEXT` 列中的信息以及通过 `TIDB_DECODE_SQL_DIGESTS` 函数返回的结果，是从语句摘要表内部查询得到的，因此可能找不到对应的语句。关于 SQL digest 和语句摘要表的详细说明，请参见 [Statement Summary Tables](/statement-summary-tables.md)。
> * 调用 [`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests) 函数的开销较大。如果在查询大量事务的历史 SQL 语句时调用此函数，可能会导致查询耗时较长。集群中存在大量并发事务时，避免在查询完整的 `TIDB_TRX` 表时直接使用此函数。
> * 目前 `TIDB_TRX` 表不支持显示 TiDB 内部事务的信息。

## Example

查看 `TIDB_TRX` 表：

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_TRX\G
```

输出结果如下：

```sql
*************************** 1. row ***************************
                     ID: 426789913200689153
             START_TIME: 2021-08-04 10:51:54.883000
     CURRENT_SQL_DIGEST: NULL
CURRENT_SQL_DIGEST_TEXT: NULL
                  STATE: Idle
     WAITING_START_TIME: NULL
        MEM_BUFFER_KEYS: 1
       MEM_BUFFER_BYTES: 29
             SESSION_ID: 7
                   USER: root
                     DB: test
        ALL_SQL_DIGESTS: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","04fa858fa491c62d194faec2ab427261cc7998b3f1ccf8f6844febca504cb5e9","b83710fa8ab7df8504920e8569e48654f621cf828afbe7527fd003b79f48da9e"]
*************************** 2. row ***************************
                     ID: 426789921471332353
             START_TIME: 2021-08-04 10:52:26.433000
     CURRENT_SQL_DIGEST: 38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821
CURRENT_SQL_DIGEST_TEXT: update `t` set `v` = `v` + ? where `id` = ?
                  STATE: LockWaiting
     WAITING_START_TIME: 2021-08-04 10:52:35.106568
        MEM_BUFFER_KEYS: 0
       MEM_BUFFER_BYTES: 0
             SESSION_ID: 9
                   USER: root
                     DB: test
        ALL_SQL_DIGESTS: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821"]
2 rows in set (0.01 sec)
```

从此示例的查询结果可以看出：当前节点有两个正在进行的事务。一个事务处于空闲状态（`STATE` 为 `Idle`，`CURRENT_SQL_DIGEST` 为 `NULL`），该事务已执行了 3 条语句（`ALL_SQL_DIGESTS` 列表中有三条记录，分别是已执行的三条 SQL 语句的 digest）。另一个事务正在执行语句并等待锁（`STATE` 为 `LockWaiting`，`WAITING_START_TIME` 显示等待锁的开始时间）。该事务已执行 2 条语句，当前正在执行的语句为 ``"update `t` set `v` = `v` + ? where `id` = ?"``。

```sql
SELECT id, all_sql_digests, tidb_decode_sql_digests(all_sql_digests) AS all_sqls FROM INFORMATION_SCHEMA.TIDB_TRX\G
```

输出结果如下：

```sql
*************************** 1. row ***************************
             id: 426789913200689153
all_sql_digests: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","04fa858fa491c62d194faec2ab427261cc7998b3f1ccf8f6844febca504cb5e9","b83710fa8ab7df8504920e8569e48654f621cf828afbe7527fd003b79f48da9e"]
       all_sqls: ["begin","insert into `t` values ( ... )","update `t` set `v` = `v` + ?"]
*************************** 2. row ***************************
             id: 426789921471332353
all_sql_digests: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821"]
       all_sqls: ["begin","update `t` set `v` = `v` + ? where `id` = ?"]
```

此查询调用了 [`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests) 函数，将 `TIDB_TRX` 表中 `ALL_SQL_DIGESTS` 列的 SQL digest 数组转换为规范化 SQL 语句数组，通过系统内部查询帮助你直观获取事务历史执行的语句信息。然而，注意上述查询会扫描整个 `TIDB_TRX` 表，并对每一行调用 `TIDB_DECODE_SQL_DIGESTS` 函数，调用此函数的开销较大。因此，如果集群中存在大量并发事务，建议避免使用此类查询。

## CLUSTER_TIDB_TRX

`TIDB_TRX` 表仅提供单个 TiDB 节点上正在执行的事务信息。如果你想查看整个集群中所有 TiDB 节点上正在执行的事务信息，需要查询 `CLUSTER_TIDB_TRX` 表。与 `TIDB_TRX` 表的查询结果相比，`CLUSTER_TIDB_TRX` 表的查询结果多了一个 `INSTANCE` 字段。`INSTANCE` 字段显示集群中每个节点的 IP 地址和端口，用于区分事务所在的 TiDB 节点。

```sql
USE INFORMATION_SCHEMA;
DESC CLUSTER_TIDB_TRX;
```

输出结果如下：

```sql
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| Field                   | Type                                                            | Null | Key  | Default | Extra |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| INSTANCE                | varchar(64)                                                     | YES  |      | NULL    |       |
| ID                      | bigint(21) unsigned                                             | NO   | PRI  | NULL    |       |
| START_TIME              | timestamp(6)                                                    | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST      | varchar(64)                                                     | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST_TEXT | text                                                            | YES  |      | NULL    |       |
| STATE                   | enum('Idle','Running','LockWaiting','Committing','RollingBack') | YES  |      | NULL    |       |
| WAITING_START_TIME      | timestamp(6)                                                    | YES  |      | NULL    |       |
| MEM_BUFFER_KEYS         | bigint(64)                                                      | YES  |      | NULL    |       |
| MEM_BUFFER_BYTES        | bigint(64)                                                      | YES  |      | NULL    |       |
| SESSION_ID              | bigint(21) unsigned                                             | YES  |      | NULL    |       |
| USER                    | varchar(16)                                                     | YES  |      | NULL    |       |
| DB                      | varchar(64)                                                     | YES  |      | NULL    |       |
| ALL_SQL_DIGESTS         | text                                                            | YES  |      | NULL    |       |
| RELATED_TABLE_IDS       | text                                                            | YES  |      | NULL    |       |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
14 rows in set (0.00 sec)
```