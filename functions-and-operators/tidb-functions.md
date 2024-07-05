---
title: TiDB Specific Functions
summary: Learn about the usage of TiDB specific functions.
---

# TiDB Specific Functions

The following functions are TiDB extensions, and are not present in MySQL:

<CustomContent platform="tidb">

| Function name | Function description |
| :-------------- | :------------------------------------- |
| `TIDB_BOUNDED_STALENESS()` | The `TIDB_BOUNDED_STALENESS` function instructs TiDB to read the data as new as possible within the time range. See also: [Read Historical Data Using the `AS OF TIMESTAMP` Clause](/as-of-timestamp.md) |
| [`TIDB_DECODE_KEY(str)`](#tidb_decode_key) | The `TIDB_DECODE_KEY` function can be used to decode a TiDB-encoded key entry into a JSON structure containing `_tidb_rowid` and `table_id`. These encoded keys can be found in some system tables and in logging outputs. |
| [`TIDB_DECODE_PLAN(str)`](#tidb_decode_plan) | The `TIDB_DECODE_PLAN` function can be used to decode a TiDB execution plan. |
| `TIDB_IS_DDL_OWNER()` | The `TIDB_IS_DDL_OWNER` function can be used to check whether or not the TiDB instance you are connected to is the one that is the DDL Owner. The DDL Owner is the TiDB instance that is tasked with executing DDL statements on behalf of all other nodes in the cluster. |
| [`TIDB_PARSE_TSO(num)`](#tidb_parse_tso) | The `TIDB_PARSE_TSO` function can be used to extract the physical timestamp from a TiDB TSO timestamp. See also: [`tidb_current_ts`](/system-variables.md#tidb_current_ts). |
| `TIDB_PARSE_TSO_LOGICAL(num)` | The `TIDB_PARSE_TSO_LOGICAL` function can be used to extract the logical timestamp from a TiDB TSO timestamp. |
| [`TIDB_VERSION()`](#tidb_version) | The `TIDB_VERSION` function returns the TiDB version with additional build information. |
| [`TIDB_DECODE_SQL_DIGESTS(digests, stmtTruncateLength)`](#tidb_decode_sql_digests) | The `TIDB_DECODE_SQL_DIGESTS()` function is used to query the normalized SQL statements (a form without formats and arguments) corresponding to the set of SQL digests in the cluster. |
| `VITESS_HASH(str)` | The `VITESS_HASH` function returns the hash of a string that is compatible with Vitess' `HASH` function. This is intended to help the data migration from Vitess. |
| `TIDB_SHARD()` | The `TIDB_SHARD` function can be used to create a shard index to scatter the index hotspot. A shard index is an expression index with a `TIDB_SHARD` function as the prefix.|
| `TIDB_ROW_CHECKSUM()` | The `TIDB_ROW_CHECKSUM` function is used to query the checksum value of a row. This function can only be used in `SELECT` statements within the FastPlan process. That is, you can query through statements like `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` or `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)`. See also: [Data integrity validation for single-row data](/ticdc/ticdc-integrity-check.md). |
| `CURRENT_RESOURCE_GROUP()`  | The `CURRENT_RESOURCE_GROUP` function is used to return the resource group name that the current session is bound to. See also: [Use Resource Control to Achieve Resource Isolation](/tidb-resource-control.md). |

</CustomContent>

<CustomContent platform="tidb-cloud">

| Function name | Function description |
| :-------------- | :------------------------------------- |
| `TIDB_BOUNDED_STALENESS()` | The `TIDB_BOUNDED_STALENESS` function instructs TiDB to read the data as new as possible within the time range. See also: [Read Historical Data Using the `AS OF TIMESTAMP` Clause](/as-of-timestamp.md) |
| [`TIDB_DECODE_KEY(str)`](#tidb_decode_key) | The `TIDB_DECODE_KEY` function can be used to decode a TiDB-encoded key entry into a JSON structure containing `_tidb_rowid` and `table_id`. These encoded keys can be found in some system tables and in logging outputs. |
| [`TIDB_DECODE_PLAN(str)`](#tidb_decode_plan) | The `TIDB_DECODE_PLAN` function can be used to decode a TiDB execution plan. |
| `TIDB_IS_DDL_OWNER()` | The `TIDB_IS_DDL_OWNER` function can be used to check whether or not the TiDB instance you are connected to is the one that is the DDL Owner. The DDL Owner is the TiDB instance that is tasked with executing DDL statements on behalf of all other nodes in the cluster. |
| [`TIDB_PARSE_TSO(num)`](#tidb_parse_tso) | The `TIDB_PARSE_TSO` function can be used to extract the physical timestamp from a TiDB TSO timestamp. See also: [`tidb_current_ts`](/system-variables.md#tidb_current_ts). |
| `TIDB_PARSE_TSO_LOGICAL(num)` | The `TIDB_PARSE_TSO_LOGICAL` function can be used to extract the logical timestamp from a TiDB TSO timestamp. |
| [`TIDB_VERSION()`](#tidb_version) | The `TIDB_VERSION` function returns the TiDB version with additional build information. |
| [`TIDB_DECODE_SQL_DIGESTS(digests, stmtTruncateLength)`](#tidb_decode_sql_digests) | The `TIDB_DECODE_SQL_DIGESTS()` function is used to query the normalized SQL statements (a form without formats and arguments) corresponding to the set of SQL digests in the cluster. |
| `VITESS_HASH(str)` | The `VITESS_HASH` function returns the hash of a string that is compatible with Vitess' `HASH` function. This is intended to help the data migration from Vitess. |
| `TIDB_SHARD()` | The `TIDB_SHARD` function can be used to create a shard index to scatter the index hotspot. A shard index is an expression index with a `TIDB_SHARD` function as the prefix.|
| `TIDB_ROW_CHECKSUM()` | The `TIDB_ROW_CHECKSUM` function is used to query the checksum value of a row. This function can only be used in `SELECT` statements within the FastPlan process. That is, you can query through statements like `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` or `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)`. See also: [Data integrity validation for single-row data](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check). |
| `CURRENT_RESOURCE_GROUP()`  | The `CURRENT_RESOURCE_GROUP` function is used to return the resource group name that the current session is bound to. See also: [Use Resource Control to Achieve Resource Isolation](/tidb-resource-control.md). |

</CustomContent>

## Examples

This section provides examples for some of the functions above.

### TIDB_DECODE_KEY

In the following example, the table `t1` has a hidden `rowid` that is generated by TiDB. The `TIDB_DECODE_KEY` is used in the statement. From the result, you can see that the hidden `rowid` is decoded and output, which is a typical result for the non-clustered primary key.

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
  `a` tinyint(3) unsigned NOT NULL,
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

The first Region of a table starts with a key that only has the `table_id` of the table. The last Region of the table ends with `table_id + 1`. Any Regions in between have longer keys that includes a `_tidb_rowid` or `handle`.

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

### TIDB_DECODE_PLAN

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

### TIDB_PARSE_TSO

The `TIDB_PARSE_TSO` function can be used to extract the physical timestamp from a TiDB TSO timestamp. TSO stands for Time Stamp Oracle and is a monotonically increasing timestamp given out by PD (Placement Driver) for every transaction.

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

### TIDB_VERSION

The `TIDB_VERSION` function can be used to get the version and build details of the TiDB server that you are connected to. You can use this function when reporting issues on GitHub.

```sql
SELECT TIDB_VERSION()\G
```

```sql
*************************** 1. row ***************************
TIDB_VERSION(): Release Version: v5.1.0-alpha-13-gd5e0ed0aa-dirty
Edition: Community
Git Commit Hash: d5e0ed0aaed72d2f2dfe24e9deec31cb6cb5fdf0
Git Branch: master
UTC Build Time: 2021-05-24 14:39:20
GoVersion: go1.13
Race Enabled: false
TiKV Min Version: v3.0.0-60965b006877ca7234adaced7890d7b029ed1306
Check Table Before Drop: false
1 row in set (0.00 sec)
```

### TIDB_DECODE_SQL_DIGESTS

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
set @digests = '["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821","e5796985ccafe2f71126ed6c0ac939ffa015a8c0744a24b7aee6d587103fd2f7"]';

select tidb_decode_sql_digests(@digests);
```

```sql
+------------------------------------+
| tidb_decode_sql_digests(@digests)  |
+------------------------------------+
| ["begin",null,"select * from `t`"] |
+------------------------------------+
1 row in set (0.00 sec)
```

In the above example, the parameter is a JSON array containing 3 SQL digests, and the corresponding SQL statements are the three items in the query results. But the SQL statement corresponding to the second SQL digest cannot be found from the cluster, so the second item in the result is `null`.

```sql
select tidb_decode_sql_digests(@digests, 10);
```

```sql
+---------------------------------------+
| tidb_decode_sql_digests(@digests, 10) |
+---------------------------------------+
| ["begin",null,"select * f..."]        |
+---------------------------------------+
1 row in set (0.01 sec)
```

The above call specifies the second parameter (that is, the truncation length) as 10, and the length of the third statement in the query result is greater than 10. Therefore, only the first 10 characters are retained, and `"..."` is added at the end, which indicates the truncation.

See also:

- [`Statement Summary Tables`](/statement-summary-tables.md)
- [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

### TIDB_SHARD

The `TIDB_SHARD` function can be used to create a shard index to scatter the index hotspot. A shard index is an expression index prefixed with a `TIDB_SHARD` function.

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

The following example shows how to use the `TIDB_SHARD` function.

- Use the `TIDB_SHARD` function to calculate the SHARD value.

    The following statement shows how to use the `TIDB_SHARD` function to calculate the SHARD value of `12373743746`:

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

- Create a shard index using the `TIDB_SHARD` function:

    ```sql
    CREATE TABLE test(id INT PRIMARY KEY CLUSTERED, a INT, b INT, UNIQUE KEY uk((tidb_shard(a)), a));
    ```

### TIDB_ROW_CHECKSUM

The `TIDB_ROW_CHECKSUM` function is used to query the checksum value of a row. This function can only be used in `SELECT` statements within the FastPlan process. That is, you can query through statements like `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?` or `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)`.

To enable the checksum feature of single-row data in TiDB (controlled by the system variable [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710)), run the following statement:

```sql
SET GLOBAL tidb_enable_row_level_checksum = ON;
```

This configuration only takes effect for newly created sessions, so you need to reconnect to TiDB.

Create table `t` and insert data:

```sql
USE test;
CREATE TABLE t (id INT PRIMARY KEY, k INT, c CHAR(1));
INSERT INTO t values (1, 10, 'a');
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

### CURRENT_RESOURCE_GROUP

The `CURRENT_RESOURCE_GROUP` function is used to show the resource group name that the current session is bound to. When the [Resource control](/tidb-resource-control.md) feature is enabled, the available resources that can be used by SQL statements are restricted by the resource quota of the bound resource group.

When a session is established, TiDB binds the session to the resource group that the login user is bound to by default. If the user is not bound to any resource groups, the session is bound to the `default` resource group. Once the session is established, the bound resource group will not change by default, even if the bound resource group of the user is changed via [modifying the resource group bound to the user](/sql-statements/sql-statement-alter-user.md#modify-basic-user-information). To change the bound resource group of the current session, you can use [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md).

#### Example

Create a user `user1`, create two resource groups `rg1` and `rg2`, and bind the user `user1` to the resource group `rg1`:

```sql
CREATE USER 'user1';
CREATE RESOURCE GROUP 'rg1' RU_PER_SEC = 1000;
CREATE RESOURCE GROUP 'rg2' RU_PER_SEC = 2000;
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
