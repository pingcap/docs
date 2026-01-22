---
title: TiDB 专有函数
summary: 了解 TiDB 专有函数的用法。
---

# TiDB 专有函数

以下函数是 TiDB 的扩展，在 MySQL 中不存在：

<CustomContent platform="tidb">

| 函数名 | 函数描述 |
| :-------------- | :------------------------------------- |
| [`CURRENT_RESOURCE_GROUP()`](#current_resource_group)  | 返回当前会话绑定的资源组名称。参见 [使用资源管控实现资源组限制与流控](/tidb-resource-control-ru-groups.md)。 |
| [`TIDB_BOUNDED_STALENESS()`](#tidb_bounded_staleness) | 指示 TiDB 在指定的时间范围内读最新的数据。参见 [使用 `AS OF TIMESTAMP` 子句读历史数据](/as-of-timestamp.md)。 |
| [`TIDB_CURRENT_TSO()`](#tidb_current_tso) | 返回当前 [TiDB 中的 TimeStamp Oracle (TSO)](/tso.md)。 |
| [`TIDB_DECODE_BINARY_PLAN()`](#tidb_decode_binary_plan) | 解码二进制执行计划。 |
| [`TIDB_DECODE_KEY()`](#tidb_decode_key) | 将 TiDB 编码的 key 条目解码为包含 `_tidb_rowid` 和 `table_id` 的 JSON 结构体。这些编码 key 可在部分系统表和日志输出中找到。 |
| [`TIDB_DECODE_PLAN()`](#tidb_decode_plan) | 解码 TiDB 执行计划。 |
| [`TIDB_DECODE_SQL_DIGESTS()`](#tidb_decode_sql_digests) | 查询集群中一组 SQL digest 对应的标准化 SQL 语句（无格式和参数的形式）。 |
| [`TIDB_ENCODE_INDEX_KEY()`](#tidb_encode_index_key) | 编码索引 key。 |
| [`TIDB_ENCODE_RECORD_KEY()`](#tidb_encode_record_key) | 编码记录 key。 |
| [`TIDB_ENCODE_SQL_DIGEST()`](#tidb_encode_sql_digest) | 获取查询字符串的 digest。 |
| [`TIDB_IS_DDL_OWNER()`](#tidb_is_ddl_owner) | 检查你所连接的 TiDB 实例是否为 DDL Owner。DDL Owner 是负责代表集群中所有其他节点执行 DDL 语句的 TiDB 实例。 |
| [`TIDB_MVCC_INFO()`](#tidb_mvcc_info) | 返回某个 key 的 [MVCC (多版本并发控制)](https://docs.pingcap.com/tidb/stable/glossary#multi-version-concurrency-control-mvcc) 信息。 |
| [`TIDB_PARSE_TSO()`](#tidb_parse_tso) | 从 TiDB TSO 时间戳中提取物理时间戳。参见：[`tidb_current_ts`](/system-variables.md#tidb_current_ts)。 |
| [`TIDB_PARSE_TSO_LOGICAL()`](#tidb_parse_tso_logical) | 从 TiDB TSO 时间戳中提取逻辑时间戳。 |
| [`TIDB_ROW_CHECKSUM()`](#tidb_row_checksum) | 查询某一行的校验和值。该函数只能在 FastPlan 流程中的 `SELECT` 语句中使用。即，你可以通过 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` 或 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)` 这类语句进行查询。参见：[单行数据的数据完整性校验](/ticdc/ticdc-integrity-check.md)。 |
| [`TIDB_SHARD()`](#tidb_shard) | 创建分片索引以打散索引热点。分片索引是以 `TIDB_SHARD` 函数为前缀的表达式索引。|
| [`TIDB_VERSION()`](#tidb_version) | 返回带有额外构建信息的 TiDB 版本。 |
| [`VITESS_HASH()`](#vitess_hash) | 返回一个数字的 hash 值。该函数与 Vitess 的 `HASH` 函数兼容，旨在帮助从 Vitess 迁移数据。 |

</CustomContent>

<CustomContent platform="tidb-cloud">

| 函数名 | 函数描述 |
| :-------------- | :------------------------------------- |
| [`CURRENT_RESOURCE_GROUP()`](#current_resource_group)  | 返回当前会话绑定的资源组名称。参见 [使用资源管控实现资源组限制与流控](/tidb-resource-control-ru-groups.md)。 |
| [`TIDB_BOUNDED_STALENESS()`](#tidb_bounded_staleness) | 指示 TiDB 在指定的时间范围内读最新的数据。参见 [使用 `AS OF TIMESTAMP` 子句读历史数据](/as-of-timestamp.md)。 |
| [`TIDB_CURRENT_TSO()`](#tidb_current_tso) | 返回当前 [TiDB 中的 TimeStamp Oracle (TSO)](/tso.md)。 |
| [`TIDB_DECODE_BINARY_PLAN()`](#tidb_decode_binary_plan) | 解码二进制执行计划。 |
| [`TIDB_DECODE_KEY()`](#tidb_decode_key) | 将 TiDB 编码的 key 条目解码为包含 `_tidb_rowid` 和 `table_id` 的 JSON 结构体。这些编码 key 可在部分系统表和日志输出中找到。 |
| [`TIDB_DECODE_PLAN()`](#tidb_decode_plan) | 解码 TiDB 执行计划。 |
| [`TIDB_DECODE_SQL_DIGESTS()`](#tidb_decode_sql_digests) | 查询集群中一组 SQL digest 对应的标准化 SQL 语句（无格式和参数的形式）。 |
| [`TIDB_ENCODE_INDEX_KEY()`](#tidb_encode_index_key) | 编码索引 key。 |
| [`TIDB_ENCODE_RECORD_KEY()`](#tidb_encode_record_key) | 编码记录 key。 |
| [`TIDB_ENCODE_SQL_DIGEST()`](#tidb_encode_sql_digest) | 获取查询字符串的 digest。 |
| [`TIDB_IS_DDL_OWNER()`](#tidb_is_ddl_owner) | 检查你所连接的 TiDB 实例是否为 DDL Owner。DDL Owner 是负责代表集群中所有其他节点执行 DDL 语句的 TiDB 实例。 |
| [`TIDB_PARSE_TSO()`](#tidb_parse_tso) | 从 TiDB TSO 时间戳中提取物理时间戳。参见：[`tidb_current_ts`](/system-variables.md#tidb_current_ts)。 |
| [`TIDB_MVCC_INFO()`](#tidb_mvcc_info) | 返回某个 key 的 [MVCC (多版本并发控制)](https://docs.pingcap.com/tidb/stable/glossary#multi-version-concurrency-control-mvcc) 信息。 |
| [`TIDB_PARSE_TSO_LOGICAL()`](#tidb_parse_tso_logical) | 从 TiDB TSO 时间戳中提取逻辑时间戳。 |
| [`TIDB_ROW_CHECKSUM()`](#tidb_row_checksum) | 查询某一行的校验和值。该函数只能在 FastPlan 流程中的 `SELECT` 语句中使用。即，你可以通过 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` 或 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)` 这类语句进行查询。参见：[单行数据的数据完整性校验](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check)。 |
| [`TIDB_SHARD()`](#tidb_shard) | 创建分片索引以打散索引热点。分片索引是以 `TIDB_SHARD` 函数为前缀的表达式索引。|
| [`TIDB_VERSION()`](#tidb_version) | 返回带有额外构建信息的 TiDB 版本。 |
| [`VITESS_HASH()`](#vitess_hash) | 返回一个数字的 hash 值。该函数与 Vitess 的 `HASH` 函数兼容，旨在帮助从 Vitess 迁移数据。 |

</CustomContent>

## CURRENT_RESOURCE_GROUP

`CURRENT_RESOURCE_GROUP()` 函数用于显示当前会话绑定的资源组名称。当启用 [资源管控](/tidb-resource-control-ru-groups.md) 功能时，SQL 语句可用的资源会受到所绑定资源组资源配额的限制。

当会话建立时，TiDB 默认将会话绑定到登录用户所绑定的资源组。如果用户未绑定任何资源组，则会话绑定到 `default` 资源组。会话建立后，默认情况下绑定的资源组不会改变，即使通过 [修改用户绑定的资源组](/sql-statements/sql-statement-alter-user.md#modify-basic-user-information) 更改了用户的资源组。要更改当前会话绑定的资源组，可以使用 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)。

示例：

创建用户 `user1`，创建两个资源组 `rg1` 和 `rg2`，并将用户 `user1` 绑定到资源组 `rg1`：

```sql
CREATE USER 'user1';
CREATE RESOURCE GROUP rg1 RU_PER_SEC = 1000;
CREATE RESOURCE GROUP rg2 RU_PER_SEC = 2000;
ALTER USER 'user1' RESOURCE GROUP `rg1`;
```

使用 `user1` 登录并查看当前用户绑定的资源组：

```sql
SELECT CURRENT_RESOURCE_GROUP();
```

```
+--------------------------+
| CURRENT_RESOURCE_GROUP() |
+--------------------------+
| rg1                      |
+--------------------------+
1 row in set (0.00 sec)
```

执行 `SET RESOURCE GROUP` 将当前会话的资源组设置为 `rg2`，然后查看当前用户绑定的资源组：

```sql
SET RESOURCE GROUP `rg2`;
SELECT CURRENT_RESOURCE_GROUP();
```

```
+--------------------------+
| CURRENT_RESOURCE_GROUP() |
+--------------------------+
| rg2                      |
+--------------------------+
1 row in set (0.00 sec)
```

## TIDB_BOUNDED_STALENESS

`TIDB_BOUNDED_STALENESS()` 函数作为 [`AS OF TIMESTAMP`](/as-of-timestamp.md) 语法的一部分使用。

## TIDB_CURRENT_TSO

`TIDB_CURRENT_TSO()` 函数返回当前 [TSO](/tso.md)（时间戳 oracle）。这类似于 [`tidb_current_ts`](/system-variables.md#tidb_current_ts) 系统变量。

```sql
BEGIN;
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
SELECT TIDB_CURRENT_TSO();
```

```
+--------------------+
| TIDB_CURRENT_TSO() |
+--------------------+
| 450456244814610433 |
+--------------------+
1 row in set (0.00 sec)
```

```sql
SELECT @@tidb_current_ts;
```

```
+--------------------+
| @@tidb_current_ts  |
+--------------------+
| 450456244814610433 |
+--------------------+
1 row in set (0.00 sec)
```

## TIDB_DECODE_BINARY_PLAN

`TIDB_DECODE_BINARY_PLAN(binary_plan)` 函数用于解码二进制执行计划，例如 [`STATEMENTS_SUMMARY`](/statement-summary-tables.md) 表中的 `BINARY_PLAN` 列。

要使二进制执行计划可用，需将 [`tidb_generate_binary_plan`](/system-variables.md#tidb_generate_binary_plan-new-in-v620) 变量设置为 `ON`。

示例：

```sql
SELECT BINARY_PLAN,TIDB_DECODE_BINARY_PLAN(BINARY_PLAN) FROM information_schema.STATEMENTS_SUMMARY LIMIT 1\G
```

```
*************************** 1. row ***************************
                         BINARY_PLAN: lQLwPgqQAgoMUHJvamVjdGlvbl8zEngKDk1lbVRhYmxlU2Nhbl80KQAAAAAAiMNAMAM4AUABSioKKAoSaW5mb3JtYQU00HNjaGVtYRISU1RBVEVNRU5UU19TVU1NQVJZWhV0aW1lOjI5LjPCtXMsIGxvb3BzOjJw////CQIEAXgJCBD///8BIQFnDOCb+EA6cQCQUjlDb2x1bW4jOTIsIHRpZGJfZGVjb2RlX2JpbmFyeV9wbGFuKBUjCCktPg0MEDEwM1oWBYAIMTA4NoEAeGINQ29uY3VycmVuY3k6NXDIZXj///////////8BGAE=
TIDB_DECODE_BINARY_PLAN(BINARY_PLAN):
| id               | estRows  | estCost   | actRows | task | access object            | execution info                       | operator info                                             | memory  | disk  |
| Projection_3     | 10000.00 | 100798.00 | 3       | root |                          | time:108.3µs, loops:2, Concurrency:5 | Column#92, tidb_decode_binary_plan(Column#92)->Column#103 | 12.7 KB | N/A   |
| └─MemTableScan_4 | 10000.00 | 0.00      | 3       | root | table:STATEMENTS_SUMMARY | time:29.3µs, loops:2                 |                                                           | N/A     | N/A   |

1 row in set (0.00 sec)
```

## TIDB_DECODE_KEY

`TIDB_DECODE_KEY()` 函数将 TiDB 编码的 key 条目解码为包含 `_tidb_rowid` 和 `table_id` 的 JSON 结构体。这些编码 key 存在于部分系统表和日志输出中。

在以下示例中，表 `t1` 有一个由 TiDB 生成的隐藏 `rowid`。在语句中使用了 `TIDB_DECODE_KEY()` 函数。从结果可以看到，隐藏的 `rowid` 被解码并输出，这是非聚簇主键的典型结果。

```sql
SELECT START_KEY, TIDB_DECODE_KEY(START_KEY) FROM information_schema.tikv_region_status WHERE table_name='t1' AND REGION_ID=2\G
```

```sql
*************************** 1. row ***************************
                 START_KEY: 7480000000000000FF3B5F728000000000FF1DE3F10000000000FA
TIDB_DECODE_KEY(START_KEY): {"_tidb_rowid":1958897,"table_id":"59"}
1 row in set (0.00 sec)
```

在下一个示例中，表 `t2` 有一个复合聚簇主键。从 JSON 输出可以看到 `handle`，其中包含主键各列的名称和值。

```sql
SHOW CREATE TABLE t2\G
```

```sql
*************************** 1. row ***************************
       Table: t2
Create Table: CREATE TABLE `t2` (
  `id` binary(36) NOT NULL,
  `a` tinyint unsigned NOT NULL,
  `v` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`a`,`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.001 sec)
```

```sql
SELECT * FROM information_schema.tikv_region_status WHERE table_name='t2' LIMIT 1\G
```

```sql
*************************** 1. row ***************************
                REGION_ID: 48
                START_KEY: 7480000000000000FF3E5F720400000000FF0000000601633430FF3338646232FF2D64FF3531632D3131FF65FF622D386337352DFFFF3830653635303138FFFF61396265000000FF00FB000000000000F9
                  END_KEY:
                 TABLE_ID: 62
                  DB_NAME: test
               TABLE_NAME: t2
                 IS_INDEX: 0
                 INDEX_ID: NULL
               INDEX_NAME: NULL
           EPOCH_CONF_VER: 1
            EPOCH_VERSION: 38
            WRITTEN_BYTES: 0
               READ_BYTES: 0
         APPROXIMATE_SIZE: 136
         APPROXIMATE_KEYS: 479905
  REPLICATIONSTATUS_STATE: NULL
REPLICATIONSTATUS_STATEID: NULL
1 row in set (0.005 sec)
```

```sql
SELECT tidb_decode_key('7480000000000000FF3E5F720400000000FF0000000601633430FF3338646232FF2D64FF3531632D3131FF65FF622D386337352DFFFF3830653635303138FFFF61396265000000FF00FB000000000000F9');
```

```sql
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tidb_decode_key('7480000000000000FF3E5F720400000000FF0000000601633430FF3338646232FF2D64FF3531632D3131FF65FF622D386337352DFFFF3830653635303138FFFF61396265000000FF00FB000000000000F9') |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| {"handle":{"a":"6","id":"c4038db2-d51c-11eb-8c75-80e65018a9be"},"table_id":62}                                                                                                        |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.001 sec)
```

在下一个示例中，表的第一个 Region 以只包含该表 `table_id` 的 key 开始。表的最后一个 Region 以 `table_id + 1` 结束。中间的 Region key 更长，包含 `_tidb_rowid` 或 `handle`。

```sql
SELECT
  TABLE_NAME,
  TIDB_DECODE_KEY(START_KEY),
  TIDB_DECODE_KEY(END_KEY)
FROM
  information_schema.TIKV_REGION_STATUS
WHERE
  TABLE_NAME='stock'
  AND IS_INDEX=0
ORDER BY
  START_KEY;
```

```sql
+------------+-----------------------------------------------------------+-----------------------------------------------------------+
| TABLE_NAME | TIDB_DECODE_KEY(START_KEY)                                | TIDB_DECODE_KEY(END_KEY)                                  |
+------------+-----------------------------------------------------------+-----------------------------------------------------------+
| stock      | {"table_id":143}                                          | {"handle":{"s_i_id":"32485","s_w_id":"3"},"table_id":143} |
| stock      | {"handle":{"s_i_id":"32485","s_w_id":"3"},"table_id":143} | {"handle":{"s_i_id":"64964","s_w_id":"5"},"table_id":143} |
| stock      | {"handle":{"s_i_id":"64964","s_w_id":"5"},"table_id":143} | {"handle":{"s_i_id":"97451","s_w_id":"7"},"table_id":143} |
| stock      | {"handle":{"s_i_id":"97451","s_w_id":"7"},"table_id":143} | {"table_id":145}                                          |
+------------+-----------------------------------------------------------+-----------------------------------------------------------+
4 rows in set (0.031 sec)
```

`TIDB_DECODE_KEY` 解码成功时返回有效的 JSON，解码失败时返回参数值本身。

## TIDB_DECODE_PLAN

你可以在慢查询日志中找到编码形式的 TiDB 执行计划。`TIDB_DECODE_PLAN()` 函数可将编码后的执行计划解码为可读形式。

该函数的意义在于，执行计划是在语句执行时捕获的。重新用 `EXPLAIN` 执行语句可能会因数据分布和统计信息的变化而产生不同的结果。

```sql
SELECT tidb_decode_plan('8QIYMAkzMV83CQEH8E85LjA0CWRhdGE6U2VsZWN0aW9uXzYJOTYwCXRpbWU6NzEzLjHCtXMsIGxvb3BzOjIsIGNvcF90YXNrOiB7bnVtOiAxLCBtYXg6IDU2OC41wgErRHByb2Nfa2V5czogMCwgcnBjXxEpAQwFWBAgNTQ5LglZyGNvcHJfY2FjaGVfaGl0X3JhdGlvOiAwLjAwfQkzLjk5IEtCCU4vQQoxCTFfNgkxXzAJMwm2SGx0KHRlc3QudC5hLCAxMDAwMCkNuQRrdgmiAHsFbBQzMTMuOMIBmQnEDDk2MH0BUgEEGAoyCTQzXzUFVwX1oGFibGU6dCwga2VlcCBvcmRlcjpmYWxzZSwgc3RhdHM6cHNldWRvCTk2ISE2aAAIMTUzXmYA')\G
```

```sql
*************************** 1. row ***************************
  tidb_decode_plan('8QIYMAkzMV83CQEH8E85LjA0CWRhdGE6U2VsZWN0aW9uXzYJOTYwCXRpbWU6NzEzLjHCtXMsIGxvb3BzOjIsIGNvcF90YXNrOiB7bnVtOiAxLCBtYXg6IDU2OC41wgErRHByb2Nfa2V5czogMCwgcnBjXxEpAQwFWBAgNTQ5LglZyGNvcHJfY2FjaGVfaGl0X3JhdGlvOiAwLjAwfQkzLjk5IEtCCU4vQQoxCTFfNgkxXz:     id                     task         estRows    operator info                              actRows    execution info                                                                                                                         memory     disk
    TableReader_7          root         319.04     data:Selection_6                           960        time:713.1µs, loops:2, cop_task: {num: 1, max: 568.5µs, proc_keys: 0, rpc_num: 1, rpc_time: 549.1µs, copr_cache_hit_ratio: 0.00}    3.99 KB    N/A
    └─Selection_6          cop[tikv]    319.04     lt(test.t.a, 10000)                        960        tikv_task:{time:313.8µs, loops:960}                                                                                                   N/A        N/A
      └─TableFullScan_5    cop[tikv]    960        table:t, keep order:false, stats:pseudo    960        tikv_task:{time:153µs, loops:960}                                                                                                     N/A        N/A
```

## TIDB_DECODE_SQL_DIGESTS

`TIDB_DECODE_SQL_DIGESTS()` 函数用于查询集群中一组 SQL digest 对应的标准化 SQL 语句（无格式和参数的形式）。该函数接受 1 个或 2 个参数：

* `digests`：字符串。该参数为 JSON 字符串数组格式，数组中的每个字符串为一个 SQL digest。
* `stmtTruncateLength`：整数（可选）。用于限制返回结果中每条 SQL 语句的长度。如果某条 SQL 语句超过指定长度，则会被截断。`0` 表示不限制长度。

该函数返回一个字符串，格式为 JSON 字符串数组。数组中的第 *i* 项为 `digests` 参数中第 *i* 个元素对应的标准化 SQL 语句。如果 `digests` 参数中的某个元素不是有效的 SQL digest，或系统无法找到对应的 SQL 语句，则返回结果中对应项为 `null`。如果指定了截断长度（`stmtTruncateLength > 0`），则返回结果中每条超出该长度的语句只保留前 `stmtTruncateLength` 个字符，并在末尾加上 `"..."` 表示被截断。如果 `digests` 参数为 `NULL`，则函数返回值为 `NULL`。

> **注意：**
>
> * 只有拥有 [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) 权限的用户才能使用该函数。
> * 执行 `TIDB_DECODE_SQL_DIGESTS` 时，TiDB 会从语句概要表中查询每个 SQL digest 对应的语句，因此不能保证任何 SQL digest 都能查到对应语句。只能查到集群中已执行过的语句，且能否查询到还受语句概要表相关配置影响。关于语句概要表的详细说明，参见 [语句概要表](/statement-summary-tables.md)。
> * 该函数开销较大。在大集群或繁忙集群上（如全表查询 `information_schema.cluster_tidb_trx`），使用该函数可能导致查询耗时过长，请谨慎使用。
>     * 该函数开销较大是因为每次调用时，内部会查询 `STATEMENTS_SUMMARY`、`STATEMENTS_SUMMARY_HISTORY`、`CLUSTER_STATEMENTS_SUMMARY` 和 `CLUSTER_STATEMENTS_SUMMARY_HISTORY` 表，且查询涉及 `UNION` 操作。该函数目前不支持向量化，即对多行数据调用时，每行都会单独执行上述查询。

```sql
SET @digests = '["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821","e5796985ccafe2f71126ed6c0ac939ffa015a8c0744a24b7aee6d587103fd2f7"]';

SELECT TIDB_DECODE_SQL_DIGESTS(@digests);
```

```sql
+------------------------------------+
| TIDB_DECODE_SQL_DIGESTS(@digests)  |
+------------------------------------+
| ["begin",null,"select * from `t`"] |
+------------------------------------+
1 row in set (0.00 sec)
```

在上述示例中，参数为包含 3 个 SQL digest 的 JSON 数组，查询结果中对应的 SQL 语句为三项。但第二个 SQL digest 无法在集群中查到对应 SQL 语句，因此结果中第二项为 `null`。

```sql
SELECT TIDB_DECODE_SQL_DIGESTS(@digests, 10);
```

```sql
+---------------------------------------+
| TIDB_DECODE_SQL_DIGESTS(@digests, 10) |
+---------------------------------------+
| ["begin",null,"select * f..."]        |
+---------------------------------------+
1 row in set (0.01 sec)
```

上述调用指定了第二个参数（即截断长度）为 10，查询结果中第三条语句长度大于 10，因此只保留前 10 个字符，并在末尾加上 `"..."`，表示被截断。

参见：

- [语句概要表](/statement-summary-tables.md)
- [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

## TIDB_ENCODE_SQL_DIGEST

`TIDB_ENCODE_SQL_DIGEST(query_str)` 返回查询字符串的 SQL digest。

在下例中可以看到，两条查询语句得到的 query digest 相同，因为 digest 对应的标准化语句都是 `select ?`。

```sql
SELECT TIDB_ENCODE_SQL_DIGEST('SELECT 1');
```

```
+------------------------------------------------------------------+
| TIDB_ENCODE_SQL_DIGEST('SELECT 1')                               |
+------------------------------------------------------------------+
| e1c71d1661ae46e09b7aaec1c390957f0d6260410df4e4bc71b9c8d681021471 |
+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT TIDB_ENCODE_SQL_DIGEST('SELECT 2');
```

```
+------------------------------------------------------------------+
| TIDB_ENCODE_SQL_DIGEST('SELECT 2')                               |
+------------------------------------------------------------------+
| e1c71d1661ae46e09b7aaec1c390957f0d6260410df4e4bc71b9c8d681021471 |
+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## TIDB_IS_DDL_OWNER

`TIDB_IS_DDL_OWNER()` 函数如果你所连接的实例为 DDL owner，则返回 `1`。

```sql
SELECT TIDB_IS_DDL_OWNER();
```

```
+---------------------+
| TIDB_IS_DDL_OWNER() |
+---------------------+
|                   1 |
+---------------------+
1 row in set (0.00 sec)
```

## TIDB_PARSE_TSO

`TIDB_PARSE_TSO()` 函数用于从 TiDB TSO 时间戳中提取物理时间戳。[TSO](/tso.md)（Time Stamp Oracle）是 PD（Placement Driver）为每个事务分配的单调递增时间戳。

TSO 是一个由两部分组成的数字：

- 物理时间戳
- 逻辑计数器

```sql
BEGIN;
SELECT TIDB_PARSE_TSO(@@tidb_current_ts);
ROLLBACK;
```

```sql
+-----------------------------------+
| TIDB_PARSE_TSO(@@tidb_current_ts) |
+-----------------------------------+
| 2021-05-26 11:33:37.776000        |
+-----------------------------------+
1 row in set (0.0012 sec)
```

这里 `TIDB_PARSE_TSO` 用于从 `tidb_current_ts` 会话变量中的时间戳数字提取物理时间戳。由于时间戳是按事务分配的，因此该函数需在事务中运行。

## TIDB_PARSE_TSO_LOGICAL

`TIDB_PARSE_TSO_LOGICAL(tso)` 函数返回 [TSO](/tso.md) 时间戳的逻辑部分。

```sql
SELECT TIDB_PARSE_TSO_LOGICAL(450456244814610433);
```

```
+--------------------------------------------+
| TIDB_PARSE_TSO_LOGICAL(450456244814610433) |
+--------------------------------------------+
|                                          1 |
+--------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT TIDB_PARSE_TSO_LOGICAL(450456244814610434);
```

```
+--------------------------------------------+
| TIDB_PARSE_TSO_LOGICAL(450456244814610434) |
+--------------------------------------------+
|                                          2 |
+--------------------------------------------+
1 row in set (0.00 sec)
```

## TIDB_ROW_CHECKSUM

`TIDB_ROW_CHECKSUM()` 函数用于查询某一行的校验和值。该函数只能在 FastPlan 流程中的 `SELECT` 语句中使用。即，你可以通过 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` 或 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)` 这类语句进行查询。

要启用 TiDB 单行数据的校验和功能（由系统变量 [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710) 控制），可执行如下语句：

```sql
SET GLOBAL tidb_enable_row_level_checksum = ON;
```

该配置仅对新建会话生效，因此需要重新连接 TiDB。

创建表 `t` 并插入数据：

```sql
USE test;
CREATE TABLE t (id INT PRIMARY KEY, k INT, c CHAR(1));
INSERT INTO t VALUES (1, 10, 'a');
```

以下语句展示了如何查询表 `t` 中 `id = 1` 行的校验和值：

```sql
SELECT *, TIDB_ROW_CHECKSUM() FROM t WHERE id = 1;
```

输出如下：

```sql
+----+------+------+---------------------+
| id | k    | c    | TIDB_ROW_CHECKSUM() |
+----+------+------+---------------------+
|  1 |   10 | a    | 3813955661          |
+----+------+------+---------------------+
1 row in set (0.000 sec)
```

## TIDB_SHARD

`TIDB_SHARD()` 函数用于创建分片索引以打散索引热点。分片索引是以 `TIDB_SHARD()` 函数为前缀的表达式索引。

- 创建方式：

    若要为索引字段 `a` 创建分片索引，可以使用 `uk((tidb_shard(a)), a))`。当唯一二级索引 `uk((tidb_shard(a)), a))` 的索引字段 `a` 上因数据单调递增或递减导致出现热点时，索引前缀 `tidb_shard(a)` 可打散热点，提升集群扩展性。

- 适用场景：

    - 唯一二级索引上因 key 单调递增或递减导致写入热点，且索引包含整数型字段。
    - SQL 语句基于二级索引所有字段做等值查询，无论是单独的 `SELECT`，还是 `UPDATE`、`DELETE` 等内部生成的查询。等值查询包括 `a = 1` 或 `a IN (1, 2, ......)` 两种方式。

- 限制：

    - 不能用于不等值查询。
    - 不能用于包含 `OR` 且最外层为 `AND` 运算符的查询。
    - 不能用于 `GROUP BY` 子句。
    - 不能用于 `ORDER BY` 子句。
    - 不能用于 `ON` 子句。
    - 不能用于 `WHERE` 子查询。
    - 只能用于打散整数型字段的唯一索引。
    - 在组合索引中可能不生效。
    - 不能走 FastPlan 流程，影响优化器性能。
    - 不能用于准备执行计划缓存。

以下示例展示了如何使用 `TIDB_SHARD()` 函数。

- 使用 `TIDB_SHARD()` 函数计算 SHARD 值。

    以下语句展示了如何用 `TIDB_SHARD()` 计算 `12373743746` 的 SHARD 值：

    ```sql
    SELECT TIDB_SHARD(12373743746);
    ```

- SHARD 值为：

    ```sql
    +-------------------------+
    | TIDB_SHARD(12373743746) |
    +-------------------------+
    |                     184 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

- 使用 `TIDB_SHARD()` 函数创建分片索引：

    ```sql
    CREATE TABLE test(id INT PRIMARY KEY CLUSTERED, a INT, b INT, UNIQUE KEY uk((tidb_shard(a)), a));
    ```

## TIDB_VERSION

`TIDB_VERSION()` 函数用于获取你所连接的 TiDB 服务器的版本和构建详情。你可以在 GitHub 提交 issue 时使用该函数。

```sql
SELECT TIDB_VERSION()\G
```

```sql
*************************** 1. row ***************************
TIDB_VERSION(): Release Version: v8.5.5
Edition: Community
Git Commit Hash: 821e491a20fbab36604b36b647b5bae26a2c1418
Git Branch: HEAD
UTC Build Time: 2026-01-15 19:16:25
GoVersion: go1.21.10
Race Enabled: false
Check Table Before Drop: false
Store: tikv
1 row in set (0.00 sec)
```

## VITESS_HASH

`VITESS_HASH(num)` 函数用于以 Vitess 的方式对数字进行 hash。这有助于从 Vitess 迁移到 TiDB。

示例：

```sql
SELECT VITESS_HASH(123);
```

```
+---------------------+
| VITESS_HASH(123)    |
+---------------------+
| 1155070131015363447 |
+---------------------+
1 row in set (0.00 sec)
```

## TIDB_ENCODE_INDEX_KEY

`TIDB_ENCODE_INDEX_KEY()` 函数将指定的索引 key 编码为十六进制字符串。语法如下：

```sql
TIDB_ENCODE_INDEX_KEY(<db_name>, <table_name>, <index_name>, <index_columns>..., <handle_columns>...)
```

参数说明：

* `<db_name>`：包含目标索引的数据库名称。
* `<table_name>`：包含目标索引的表名。对于分区表，可以指定分区名，例如 `'t(p0)'`。
* `<index_name>`：目标索引的名称。
* `<index_columns>...`：索引列的值。必须按照索引定义的顺序指定所有索引列的值。对于组合索引，必须为所有索引列指定值。
* `<handle_columns>...`：该行的句柄值，具体取决于表的主键类型：

    * 如果表没有主键，或主键为 `NONCLUSTERED`，则句柄值为隐藏列 `_tidb_rowid` 的值。
    * 如果主键为 `CLUSTERED` 且为单列整数型，则句柄值为主键列的值。
    * 如果主键为 `CLUSTERED` 且为复合主键或非整数型（common handle），则句柄值为所有主键列的值，顺序与定义一致。

以下示例展示了在不同主键类型下，如何为组合二级索引 `idx(c1, c2)` 调用该函数。

```sql
-- 对于无主键或 NONCLUSTERED 主键的表，使用 _tidb_rowid 列。
SELECT TIDB_ENCODE_INDEX_KEY(
    '<db_name>', '<table_name>', '<index_name>', 
    <c1>, <c2>, <_tidb_rowid>
);

-- 对于 CLUSTERED 整数型主键（主键列为 id）的表，使用 id 列。
SELECT TIDB_ENCODE_INDEX_KEY(
    '<db_name>', '<table_name>', '<index_name>', 
    <c1>, <c2>, <id>
);

-- 对于 CLUSTERED 复合主键（主键列为 p1, p2）的表，按定义顺序提供 p1 和 p2 的值。
SELECT TIDB_ENCODE_INDEX_KEY(
    '<db_name>', '<table_name>', '<index_name>', 
    <c1>, <c2>, <p1>, <p2>
);
```

```sql
CREATE TABLE t(id int PRIMARY KEY, a int, KEY `idx` (a));
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
INSERT INTO t VALUES(1,2);
```

```
Query OK, 1 row affected (0.00 sec)
```

```sql
SELECT TIDB_ENCODE_INDEX_KEY('test', 't', 'idx', 2, 1);
```

```
+----------------------------------------------------------------------------+
| TIDB_ENCODE_INDEX_KEY('test', 't', 'idx', 2, 1)                            |
+----------------------------------------------------------------------------+
| 7480000000000000b45f698000000000000001038000000000000002038000000000000001 |
+----------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## TIDB_ENCODE_RECORD_KEY

`TIDB_ENCODE_RECORD_KEY()` 函数将指定的行记录 key 编码为十六进制字符串。函数语法如下：

```sql
TIDB_ENCODE_RECORD_KEY(<db_name>, <table_name>, <handle_columns>...)
```

参数说明：

* `<db_name>`：包含目标表的数据库名称。
* `<table_name>`：目标表名。对于分区表，可以在 `<table_name>` 中指定分区名，例如 `'t(p0)'`。
* `<handle_columns>...`：对应行的句柄（行 key）值。句柄的具体组成取决于表的主键类型，如是否为 `CLUSTERED`、common handle 或使用隐藏列 `_tidb_rowid`。详细说明参见 [`TIDB_ENCODE_INDEX_KEY()`](#tidb_encode_index_key) 中 `<handle_columns>...` 的描述。

```sql
CREATE TABLE t(id int PRIMARY KEY, a int, KEY `idx` (a));
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
INSERT INTO t VALUES(1,2);
```

```
Query OK, 1 row affected (0.00 sec)
```

```sql
SELECT TIDB_ENCODE_RECORD_KEY('test', 't', 1);
```

```
+----------------------------------------+
| TIDB_ENCODE_RECORD_KEY('test', 't', 1) |
+----------------------------------------+
| 7480000000000000845f728000000000000001 |
+----------------------------------------+
1 row in set (0.00 sec)
```

```sql
SELECT TIDB_DECODE_KEY('7480000000000000845f728000000000000001');
```

```
+-----------------------------------------------------------+
| TIDB_DECODE_KEY('7480000000000000845f728000000000000001') |
+-----------------------------------------------------------+
| {"id":1,"table_id":"132"}                                 |
+-----------------------------------------------------------+
1 row in set (0.00 sec)
```

## TIDB_MVCC_INFO

返回某个 key 的 [MVCC (多版本并发控制)](https://docs.pingcap.com/tidb/stable/glossary#multi-version-concurrency-control-mvcc) 信息。你可以使用 [`TIDB_ENCODE_INDEX_KEY`](#tidb_encode_index_key) 函数获取 key。

```sql
SELECT JSON_PRETTY(TIDB_MVCC_INFO('74800000000000007f5f698000000000000001038000000000000001038000000000000001')) AS info\G
```

```
*************************** 1. row ***************************
info: [
  {
    "key": "74800000000000007f5f698000000000000001038000000000000001038000000000000001",
    "mvcc": {
      "info": {
        "values": [
          {
            "start_ts": 454654803134119936,
            "value": "MA=="
          }
        ],
        "writes": [
          {
            "commit_ts": 454654803134119937,
            "short_value": "MA==",
            "start_ts": 454654803134119936
          }
        ]
      }
    }
  }
]
1 row in set (0.00 sec)
```