---
title: TiDB Specific Functions
summary: Learn about the usage of TiDB specific functions.
---

# TiDB Specific Functions

The following functions are TiDB extensions, and are not present in MySQL:

<CustomContent platform="tidb">

| Function name | Function description |
| :-------------- | :------------------------------------- |
| [`CURRENT_RESOURCE_GROUP()`](#current_resource_group)  | Returns the name of the resource group that the current session is bound to. See [using resource control to achieve resource isolation](/tidb-resource-control.md). |
| [`TIDB_BOUNDED_STALENESS()`](#tidb_bounded_staleness) | Instructs TiDB to read the most recent data within a specified time range. See [reading historical data using the `AS OF TIMESTAMP` clause](/as-of-timestamp.md). |
| [`TIDB_CURRENT_TSO()`](#tidb_current_tso) | Returns the current [TimeStamp Oracle (TSO) in TiDB](/tso.md). |
| [`TIDB_DECODE_BINARY_PLAN()`](#tidb_decode_binary_plan) | Decodes binary plans. |
| [`TIDB_DECODE_KEY()`](#tidb_decode_key) | Decodes a TiDB-encoded key entry into a JSON structure containing `_tidb_rowid` and `table_id`. These encoded keys can be found in some system tables and logging outputs. |
| [`TIDB_DECODE_PLAN()`](#tidb_decode_plan) | Decodes a TiDB execution plan. |
| [`TIDB_DECODE_SQL_DIGESTS()`](#tidb_decode_sql_digests) | Queries the normalized SQL statements (a form without formats and arguments) corresponding to a set of SQL digests in the cluster. |
| [`TIDB_ENCODE_INDEX_KEY()`](#tidb_encode_index_key) | Encodes an index key. |
| [`TIDB_ENCODE_RECORD_KEY()`](#tidb_encode_record_key) | Encodes a record key. |
| [`TIDB_ENCODE_SQL_DIGEST()`](#tidb_encode_sql_digest) | Gets a digest for a query string. |
| [`TIDB_IS_DDL_OWNER()`](#tidb_is_ddl_owner) | Checks whether or not the TiDB instance you are connected to is the DDL Owner. The DDL Owner is the TiDB instance that is tasked with executing DDL statements on behalf of all other nodes in the cluster. |
| [`TIDB_MVCC_INFO()`](#tidb_mvcc_info) | Returns the [MVCC (Multi-Version Concurrency Control)](https://docs.pingcap.com/tidb/stable/glossary#multi-version-concurrency-control-mvcc) information about a key. |
| [`TIDB_PARSE_TSO()`](#tidb_parse_tso) | Extracts the physical timestamp from a TiDB TSO timestamp. See also: [`tidb_current_ts`](/system-variables.md#tidb_current_ts). |
| [`TIDB_PARSE_TSO_LOGICAL()`](#tidb_parse_tso_logical) | Extracts the logical timestamp from a TiDB TSO timestamp. |
| [`TIDB_ROW_CHECKSUM()`](#tidb_row_checksum) | Queries the checksum value of a row. This function can only be used in `SELECT` statements within the FastPlan process. That is, you can query through statements like `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` or `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)`. See also: [Data integrity validation for single-row data](/ticdc/ticdc-integrity-check.md). |
| [`TIDB_SHARD()`](#tidb_shard) | Creates a shard index to scatter the index hotspot. A shard index is an expression index with a `TIDB_SHARD` function as the prefix.|
| [`TIDB_VERSION()`](#tidb_version) | Returns the TiDB version with additional build information. |
| [`VITESS_HASH()`](#vitess_hash) | Returns the hash of a number. This function is compatible with the `HASH` function of Vitess, and is intended to help the data migration from Vitess. |

</CustomContent>

<CustomContent platform="tidb-cloud">

| Function name | Function description |
| :-------------- | :------------------------------------- |
| [`CURRENT_RESOURCE_GROUP()`](#current_resource_group)  | Returns the resource group name that the current session is bound to. See [using resource control to achieve resource isolation](/tidb-resource-control.md). |
| [`TIDB_BOUNDED_STALENESS()`](#tidb_bounded_staleness) | Instructs TiDB to read most recent data within a specified time range. See [reading historical data using the `AS OF TIMESTAMP` clause](/as-of-timestamp.md). |
| [`TIDB_CURRENT_TSO()`](#tidb_current_tso) | Returns the current [TimeStamp Oracle (TSO) in TiDB](/tso.md). |
| [`TIDB_DECODE_BINARY_PLAN()`](#tidb_decode_binary_plan) | Decodes binary plans. |
| [`TIDB_DECODE_KEY()`](#tidb_decode_key) | Decodes a TiDB-encoded key entry into a JSON structure containing `_tidb_rowid` and `table_id`. These encoded keys can be found in some system tables and logging outputs. |
| [`TIDB_DECODE_PLAN()`](#tidb_decode_plan) | Decodes a TiDB execution plan. |
| [`TIDB_DECODE_SQL_DIGESTS()`](#tidb_decode_sql_digests) | Queries the normalized SQL statements (a form without formats and arguments) corresponding to a set of SQL digests in the cluster. |
| [`TIDB_ENCODE_INDEX_KEY()`](#tidb_encode_index_key) | Encodes an index key. |
| [`TIDB_ENCODE_RECORD_KEY()`](#tidb_encode_record_key) | Encodes a record key. |
| [`TIDB_ENCODE_SQL_DIGEST()`](#tidb_encode_sql_digest) | Gets a digest for a query string. |
| [`TIDB_IS_DDL_OWNER()`](#tidb_is_ddl_owner) | Checks whether or not the TiDB instance you are connected to is the DDL Owner. The DDL Owner is the TiDB instance that is tasked with executing DDL statements on behalf of all other nodes in the cluster. |
| [`TIDB_PARSE_TSO()`](#tidb_parse_tso) | Extracts the physical timestamp from a TiDB TSO timestamp. See also: [`tidb_current_ts`](/system-variables.md#tidb_current_ts). |
| [`TIDB_MVCC_INFO()`](#tidb_mvcc_info) | Returns the [MVCC (Multi-Version Concurrency Control)](https://docs.pingcap.com/tidb/stable/glossary#multi-version-concurrency-control-mvcc) information about a key. |
| [`TIDB_PARSE_TSO_LOGICAL()`](#tidb_parse_tso_logical) | Extracts the logical timestamp from a TiDB TSO timestamp. |
| [`TIDB_ROW_CHECKSUM()`](#tidb_row_checksum) | Queries the checksum value of a row. This function can only be used in `SELECT` statements within the FastPlan process. That is, you can query through statements like `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` or `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)`. See also: [Data integrity validation for single-row data](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check). |
| [`TIDB_SHARD()`](#tidb_shard) | Creates a shard index to scatter the index hotspot. A shard index is an expression index with a `TIDB_SHARD` function as the prefix.|
| [`TIDB_VERSION()`](#tidb_version) | Returns the TiDB version with additional build information. |
| [`VITESS_HASH()`](#vitess_hash) | Returns the hash of a number. This function is compatible with the `HASH` function of Vitess, and is intended to help the data migration from Vitess. |

</CustomContent>

## CURRENT_RESOURCE_GROUP

The `CURRENT_RESOURCE_GROUP()` function is used to show the resource group name that the current session is bound to. When the [Resource control](/tidb-resource-control.md) feature is enabled, the available resources that can be used by SQL statements are restricted by the resource quota of the bound resource group.

When a session is established, TiDB binds the session to the resource group that the login user is bound to by default. If the user is not bound to any resource groups, the session is bound to the `default` resource group. Once the session is established, the bound resource group will not change by default, even if the bound resource group of the user is changed via [modifying the resource group bound to the user](/sql-statements/sql-statement-alter-user.md#modify-basic-user-information). To change the bound resource group of the current session, you can use [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md).

Examples:

Create a user `user1`, create two resource groups `rg1` and `rg2`, and bind the user `user1` to the resource group `rg1`:

```sql
CREATE USER 'user1';
CREATE RESOURCE GROUP rg1 RU_PER_SEC = 1000;
CREATE RESOURCE GROUP rg2 RU_PER_SEC = 2000;
ALTER USER 'user1' RESOURCE GROUP `rg1`;
```

Use `user1` to log in and view the resource group bound to the current user:

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

Execute `SET RESOURCE GROUP` to set the resource group for the current session to `rg2`, and then view the resource group bound to the current user:

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

The `TIDB_BOUNDED_STALENESS()` function is used as part of [`AS OF TIMESTAMP`](/as-of-timestamp.md) syntax.

## TIDB_CURRENT_TSO

The `TIDB_CURRENT_TSO()` function returns the [TSO](/tso.md) for the current transaction. This is similar to the [`tidb_current_ts`](/system-variables.md#tidb_current_ts) system variable.

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

The `TIDB_DECODE_BINARY_PLAN(binary_plan)` function decodes binary plans, like the ones in the `BINARY_PLAN` column of the [`STATEMENTS_SUMMARY`](/statement-summary-tables.md) table.

The [`tidb_generate_binary_plan`](/system-variables.md#tidb_generate_binary_plan-new-in-v620) variable must be set to `ON` for the binary plans to be available.

Example:

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

The `TIDB_DECODE_KEY()` function decodes a TiDB-encoded key entry into a JSON structure containing `_tidb_rowid` and `table_id`. These encoded keys exist in some system tables and logging outputs.

In the following example, the table `t1` has a hidden `rowid` that is generated by TiDB. The `TIDB_DECODE_KEY()` function is used in the statement. From the result, you can see that the hidden `rowid` is decoded and output, which is a typical result for the non-clustered primary key.

```sql
SELECT START_KEY, TIDB_DECODE_KEY(START_KEY) FROM information_schema.tikv_region_status WHERE table_name='t1' AND REGION_ID=2\G
```

```sql
*************************** 1. row ***************************
                 START_KEY: 7480000000000000FF3B5F728000000000FF1DE3F10000000000FA
TIDB_DECODE_KEY(START_KEY): {"_tidb_rowid":1958897,"table_id":"59"}
1 row in set (0.00 sec)
```

In the following example, the table `t2` has a compound clustered primary key. From the JSON output, you can see a `handle` that contains the name and value for both of the columns that are part of the primary key.

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

In the following example, the first Region of a table starts with a key that only has the `table_id` of the table. The last Region of the table ends with `table_id + 1`. Any Regions in between have longer keys that includes a `_tidb_rowid` or `handle`.

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

`TIDB_DECODE_KEY` returns valid JSON on success and returns the argument value if it fails to decode.

## TIDB_DECODE_PLAN

You can find TiDB execution plans in encoded form in the slow query log. The `TIDB_DECODE_PLAN()` function is then used to decode the encoded plans into a human-readable form.

This function is useful because a plan is captured at the time the statement is executed. Re-executing the statement in `EXPLAIN` might produce different results as data distribution and statistics evolves over time.

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

The `TIDB_DECODE_SQL_DIGESTS()` function is used to query the normalized SQL statements (a form without formats and arguments) corresponding to the set of SQL digests in the cluster. This function accepts 1 or 2 arguments:

* `digests`: A string. This parameter is in the format of a JSON string array, and each string in the array is a SQL digest.
* `stmtTruncateLength`: An integer (optional). It is used to limit the length of each SQL statement in the returned result. If a SQL statement exceeds the specified length, the statement is truncated. `0` means that the length is unlimited.

This function returns a string, which is in the format of a JSON string array. The *i*-th item in the array is the normalized SQL statement corresponding to the *i*-th element in the `digests` parameter. If an element in the `digests` parameter is not a valid SQL digest or the system cannot find the corresponding SQL statement, the corresponding item in the returned result is `null`. If the truncation length is specified (`stmtTruncateLength > 0`), for each statement in the returned result that exceeds this length, the first `stmtTruncateLength` characters are retained and the suffix `"..."` is added at the end to indicate the truncation. If the `digests` parameter is `NULL`, the returned value of the function is `NULL`.

> **Note:**
>
> * Only users with the [PROCESS](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process) privilege can use this function.
> * When `TIDB_DECODE_SQL_DIGESTS` is executed, TiDB queries the statement corresponding to each SQL digest from the statement summary tables, so there is no guarantee that the corresponding statement can always be found for any SQL digest. Only the statements that have been executed in the cluster can be found, and whether these SQL statements can be queried or not is also affected by the related configuration of the statement summary tables. For the detailed description of the statement summary table, see [Statement Summary Tables](/statement-summary-tables.md).
> * This function has a high overhead. In queries with a large number of rows (for example, querying the full table of `information_schema.cluster_tidb_trx` on a large and busy cluster), using this function might cause the queries to run for too long. Use it with caution.
>     * This function has a high overhead because every time it is called, it internally queries the `STATEMENTS_SUMMARY`, `STATEMENTS_SUMMARY_HISTORY`, `CLUSTER_STATEMENTS_SUMMARY`, and `CLUSTER_STATEMENTS_SUMMARY_HISTORY` tables, and the query involves the `UNION` operation. This function currently does not support vectorization, that is, when calling this function for multiple rows of data, the above query is performed separately for each row.

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

In the above example, the parameter is a JSON array containing 3 SQL digests, and the corresponding SQL statements are the three items in the query results. But the SQL statement corresponding to the second SQL digest cannot be found from the cluster, so the second item in the result is `null`.

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

The above call specifies the second parameter (that is, the truncation length) as 10, and the length of the third statement in the query result is greater than 10. Therefore, only the first 10 characters are retained, and `"..."` is added at the end, which indicates the truncation.

See also:

- [Statement summary tables](/statement-summary-tables.md)
- [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

## TIDB_ENCODE_SQL_DIGEST

The `TIDB_ENCODE_SQL_DIGEST(query_str)` returns the SQL digest for a query string.

In the following example you can see that both queries get the same query digest, which is because the digest will be `select ?` for both of them.

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

The `TIDB_IS_DDL_OWNER()` function returns `1` if the instance you are connected to is the DDL owner.

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

The `TIDB_PARSE_TSO()` function extracts the physical timestamp from a TiDB TSO timestamp. [TSO](/tso.md) stands for Time Stamp Oracle and is a monotonically increasing timestamp given out by PD (Placement Driver) for every transaction.

A TSO is a number that consists of two parts:

- A physical timestamp
- A logical counter

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

Here `TIDB_PARSE_TSO` is used to extract the physical timestamp from the timestamp number that is available in the `tidb_current_ts` session variable. Because timestamps are given out per transaction, this function is running in a transaction.

## TIDB_PARSE_TSO_LOGICAL

The `TIDB_PARSE_TSO_LOGICAL(tso)` function returns the logical part of a [TSO](/tso.md) timestamp.

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

The `TIDB_ROW_CHECKSUM()` function is used to query the checksum value of a row. This function can only be used in `SELECT` statements within the FastPlan process. That is, you can query through statements like `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` or `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)`.

To enable the checksum feature of single-row data in TiDB (controlled by the system variable [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710)), run the following statement:

```sql
SET GLOBAL tidb_enable_row_level_checksum = ON;
```

This configuration only takes effect for newly created sessions, so you need to reconnect to TiDB.

Create table `t` and insert data:

```sql
USE test;
CREATE TABLE t (id INT PRIMARY KEY, k INT, c CHAR(1));
INSERT INTO t VALUES (1, 10, 'a');
```

The following statement shows how to query the checksum value of the row where `id = 1` in table `t`:

```sql
SELECT *, TIDB_ROW_CHECKSUM() FROM t WHERE id = 1;
```

The output is as follows:

```sql
+----+------+------+---------------------+
| id | k    | c    | TIDB_ROW_CHECKSUM() |
+----+------+------+---------------------+
|  1 |   10 | a    | 3813955661          |
+----+------+------+---------------------+
1 row in set (0.000 sec)
```

## TIDB_SHARD

The `TIDB_SHARD()` function creates a shard index to scatter the index hotspot. A shard index is an expression index prefixed with a `TIDB_SHARD()` function.

- Creation:

    To create a shard index for the index field `a`, you can use `uk((tidb_shard(a)), a))`. When there is a hotspot caused by monotonically increasing or decreasing data on the index field `a` in the unique secondary index `uk((tidb_shard(a)), a))`, the index's prefix `tidb_shard(a)` can scatter the hotspot to improve the scalability of the cluster.

- Scenarios:

    - There is a write hotspot caused by monotonically increasing or decreasing keys on the unique secondary index, and the index contains integer type fields.
    - The SQL statement executes an equality query based on all fields of the secondary index, either as a separate `SELECT` or as an internal query generated by `UPDATE`, `DELETE` and so on. The equality query includes two ways: `a = 1` or `a IN (1, 2, ......)`.

- Limitations:

    - Cannot be used in inequality queries.
    - Cannot be used in queries that contain `OR` mixed with an outmost `AND` operator.
    - Cannot be used in the `GROUP BY` clause.
    - Cannot be used in the `ORDER BY` clause.
    - Cannot be used in the `ON` clause.
    - Cannot be used in the `WHERE` subquery.
    - Can be used to scatter unique indexes of only the integer fields.
    - Might not take effect in composite indexes.
    - Cannot go through FastPlan process, which affects optimizer performance.
    - Cannot be used to prepare the execution plan cache.

The following example shows how to use the `TIDB_SHARD()` function.

- Use the `TIDB_SHARD()` function to calculate the SHARD value.

    The following statement shows how to use the `TIDB_SHARD()` function to calculate the SHARD value of `12373743746`:

    ```sql
    SELECT TIDB_SHARD(12373743746);
    ```

- The SHARD value is:

    ```sql
    +-------------------------+
    | TIDB_SHARD(12373743746) |
    +-------------------------+
    |                     184 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

- Create a shard index using the `TIDB_SHARD()` function:

    ```sql
    CREATE TABLE test(id INT PRIMARY KEY CLUSTERED, a INT, b INT, UNIQUE KEY uk((tidb_shard(a)), a));
    ```

## TIDB_VERSION

The `TIDB_VERSION()` function is used to get the version and build details of the TiDB server that you are connected to. You can use this function when reporting issues on GitHub.

```sql
SELECT TIDB_VERSION()\G
```

```sql
*************************** 1. row ***************************
TIDB_VERSION(): Release Version: v8.5.0
Edition: Community
Git Commit Hash: 821e491a20fbab36604b36b647b5bae26a2c1418
Git Branch: HEAD
UTC Build Time: 2024-12-05 19:16:25
GoVersion: go1.21.10
Race Enabled: false
Check Table Before Drop: false
Store: tikv
1 row in set (0.00 sec)
```

## VITESS_HASH

The `VITESS_HASH(num)` function is used to hash a number in the same way Vitess does this. This is to aid migration from Vitess to TiDB.

Example:

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

Encodes an index key.

```sql
CREATE TABLE t(id int PRIMARY KEY, a int, KEY `idx` (a));
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
INSERT INTO t VALUES(1,1);
```

```
Query OK, 1 row affected (0.00 sec)
```

```sql
SELECT TIDB_ENCODE_INDEX_KEY('test', 't', 'idx', 1, 1);
```

```
+----------------------------------------------------------------------------+
| TIDB_ENCODE_INDEX_KEY('test', 't', 'idx', 1, 1)                            |
+----------------------------------------------------------------------------+
| 74800000000000007f5f698000000000000001038000000000000001038000000000000001 |
+----------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## TIDB_ENCODE_RECORD_KEY

Encodes a record key.

```sql
CREATE TABLE t(id int PRIMARY KEY, a int, KEY `idx` (a));
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
INSERT INTO t VALUES(1,1);
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

Returns the [MVCC (Multi-Version Concurrency Control)](https://docs.pingcap.com/tidb/stable/glossary#multi-version-concurrency-control-mvcc) information for a key. You can use the [`TIDB_ENCODE_INDEX_KEY`](#tidb_encode_index_key) function to obtain a key.

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
