---
title: Use PLAN REPLAYER to Save and Restore the On-Site Information of a Cluster
summary: Learn how to use PLAN REPLAYER to save and restore the on-site information of a cluster.
---

# Use PLAN REPLAYER to Save and Restore the On-Site Information of a Cluster

When you locate and troubleshoot the issues of a TiDB cluster, you often need to provide information on the system and the execution plan. To help you get the information and troubleshoot cluster issues in a more convenient and efficient way, the `PLAN REPLAYER` command is introduced in TiDB v5.3.0. This command enables you to easily save and restore the on-site information of a cluster, improves the efficiency of troubleshooting, and helps you more easily archive the issue for management.

The features of `PLAN REPLAYER` are as follows:

- Exports the information of a TiDB cluster at an on-site troubleshooting to a ZIP-formatted file for storage.
- Imports into a cluster the ZIP-formatted file exported from another TiDB cluster. This file contains the information of the latter TiDB cluster at an on-site troubleshooting.

## Use `PLAN REPLAYER` to export cluster information

You can use `PLAN REPLAYER` to save the on-site information of a TiDB cluster. The export interface is as follows:

{{< copyable "sql" >}}

```sql
PLAN REPLAYER DUMP EXPLAIN [ANALYZE] [WITH STATS AS OF TIMESTAMP expression] sql-statement;
```

Based on `sql-statement`, TiDB sorts out and exports the following on-site information:

- TiDB version
- TiDB configuration
- TiDB session variables
- TiDB SQL bindings
- The table schema in `sql-statement`
- The statistics of the table in `sql-statement`
- The result of `EXPLAIN [ANALYZE] sql-statement`
- Some internal procedures of query optimization

If historical statistics are [enabled](/system-variables.md#tidb_enable_historical_stats), you can specify a time in the `PLAN REPLAYER` statement to get the historical statistics for the corresponding time. You can directly specify a time and date or specify a timestamp. TiDB looks for the historical statistics before the specified time and exports the latest one among them.

If there are no historical statistics before the specified time, TiDB exports the latest statistics, which is consistent with the behavior when no time is specified. In addition, TiDB prints the error messages in the `errors.txt` file within the exported `ZIP` file.

> **Note:**
>
> `PLAN REPLAYER` **DOES NOT** export any table data.

### Examples of exporting cluster information

{{< copyable "sql" >}}

```sql
use test;
create table t(a int, b int);
insert into t values(1,1), (2, 2), (3, 3);
analyze table t;

plan replayer dump explain select * from t;
plan replayer dump with stats as of timestamp '2023-07-17 12:00:00' explain select * from t;
plan replayer dump with stats as of timestamp '442012134592479233' explain select * from t;
```

`PLAN REPLAYER DUMP` packages the table information above into a `ZIP` file and returns the file identifier as the execution result.

> **Note:**
>
> The `ZIP` file is stored in a TiDB cluster for at most one hour. After one hour, TiDB will delete it.

```sql
MySQL [test]> plan replayer dump explain select * from t;
```

```sql
+------------------------------------------------------------------+
| Dump_link                                                        |
+------------------------------------------------------------------+
| replayer_JOGvpu4t7dssySqJfTtS4A==_1635750890568691080.zip |
+------------------------------------------------------------------+
1 row in set (0.015 sec)
```

Alternatively, you can use the session variable [`tidb_last_plan_replayer_token`](/system-variables.md#tidb_last_plan_replayer_token-new-in-v630) to obtain the result of the last `PLAN REPLAYER DUMP` execution.

```sql
SELECT @@tidb_last_plan_replayer_token;
```

```sql
+-----------------------------------------------------------+
| @@tidb_last_plan_replayer_token                           |
+-----------------------------------------------------------+
| replayer_Fdamsm3C7ZiPJ-LQqgVjkA==_1663304195885090000.zip |
+-----------------------------------------------------------+
1 row in set (0.00 sec)
```

When there are multiple SQL statements, you can obtain the result of the `PLAN REPLAYER DUMP` execution using a file. The results of multiple SQL statements are separated by `;` in this file.

```sql
plan replayer dump explain 'sqls.txt';
```

```sql
Query OK, 0 rows affected (0.03 sec)
```

```sql
SELECT @@tidb_last_plan_replayer_token;
```

```sql
+-----------------------------------------------------------+
| @@tidb_last_plan_replayer_token                           |
+-----------------------------------------------------------+
| replayer_LEDKg8sb-K0u24QesiH8ig==_1663226556509182000.zip |
+-----------------------------------------------------------+
1 row in set (0.00 sec)
```

Because the file cannot be downloaded on MySQL Client, you need to use the TiDB HTTP interface and the file identifier to download the file:

{{< copyable "shell-regular" >}}

```shell
http://${tidb-server-ip}:${tidb-server-status-port}/plan_replayer/dump/${file_token}
```

`${tidb-server-ip}:${tidb-server-status-port}` is the address of any TiDB server in the cluster. For example:

{{< copyable "shell-regular" >}}

```shell
curl http://127.0.0.1:10080/plan_replayer/dump/replayer_JOGvpu4t7dssySqJfTtS4A==_1635750890568691080.zip > plan_replayer.zip
```

## Use `PLAN REPLAYER` to import cluster information

> **Warning:**
>
> When you import the on-site information of a TiDB cluster to another cluster, the TiDB session variables, SQL bindings, table schemas and statistics of the latter cluster are modified.

With an existing `ZIP` file exported using `PLAN REPLAYER`, you can use the `PLAN REPLAYER` import interface to restore the on-site information of a cluster to any other TiDB cluster. The syntax is as follows:

{{< copyable "sql" >}}

```sql
PLAN REPLAYER LOAD 'file_name';
```

In the statement above, `file_name` is the name of the `ZIP` file to be imported.

For example:

{{< copyable "sql" >}}

```sql
PLAN REPLAYER LOAD 'plan_replayer.zip';
```

> **Note:**
>
> You need to disable auto analyze. Otherwise the imported statistics will be overwritten by analyze.

You can disable auto analyze by setting the [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610) system variable to `OFF`:

```sql
set @@global.tidb_enable_auto_analyze = OFF;
```

After the cluster information is imported, the TiDB cluster is loaded with the required table schema, statistics and other information that affects the construction of the execution plan. You can view the execution plan and verify statistics in the following way:

```sql
mysql> desc t;
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
| b     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
2 rows in set (0.01 sec)

mysql> explain select * from t where a = 1 or b =1;
+-------------------------+---------+-----------+---------------+--------------------------------------+
| id                      | estRows | task      | access object | operator info                        |
+-------------------------+---------+-----------+---------------+--------------------------------------+
| TableReader_7           | 0.01    | root      |               | data:Selection_6                     |
| └─Selection_6           | 0.01    | cop[tikv] |               | or(eq(test.t.a, 1), eq(test.t.b, 1)) |
|   └─TableFullScan_5     | 6.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo       |
+-------------------------+---------+-----------+---------------+--------------------------------------+
3 rows in set (0.00 sec)

mysql> show stats_meta;
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t          |                | 2022-08-26 15:52:07 |            3 |         6 |
+---------+------------+----------------+---------------------+--------------+-----------+
1 row in set (0.04 sec)
```

After the scene is loaded and restored, you can diagnose and improve the execution plan for the cluster.

> **Note:**
>
> If you use the `mysql` command-line client and encounter `ERROR 2068 (HY000): LOAD DATA LOCAL INFILE file request rejected due to restrictions on access.`, you can add `--local-infile=true` in the connection string.

## Use `PLAN REPLAYER CAPTURE` to capture target plans

When you locate the execution plan of TiDB in some scenarios, the target SQL statement and the target execution plan might only appear occasionally in the query, so you cannot directly capture the statement and the plan using `PLAN REPLAYER`. In such cases, you can use `PLAN REPLAYER CAPTURE` to help you capture the optimizer information of the target SQL statement and the target plan.

`PLAN REPLAYER CAPTURE` has the following main features:

- Registers the target SQL statement and the digest of the target execution plan in the TiDB cluster in advance, and starts matching the target query.
- When the target query is matched successfully, directly captures its optimizer-related information and exports it as a ZIP file.
- For each matched SQL and execution plan, the information is only captured once.
- Displays the ongoing matching tasks and generated files through the system table.
- Periodically cleans up historical files.

### Enable `PLAN REPLAYER CAPTURE`

`PLAN REPLAYER CAPTURE` is controlled by the system variable [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture). To enable `PLAN REPLAYER CAPTURE`, set the value of the system variable to `ON`.

### Use `PLAN REPLAYER CAPTURE`

You can register the digest of the target SQL statement and execution plan in the TiDB cluster using the following statement:

```sql
PLAN REPLAYER CAPTURE 'sql_digest' 'plan_digest';
```

If the target SQL statement has multiple execution plans and you want to capture all execution plans, you can register all the execution plans at once using the following statement:

```sql
PLAN REPLAYER CAPTURE 'sql_digest' '*';
```

### View the capture tasks

You can view the ongoing capture tasks of `PLAN REPLAYER CAPTURE` in the TiDB cluster using the following statement:

```sql
mysql> PLAN REPLAYER CAPTURE 'example_sql' 'example_plan';
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM mysql.plan_replayer_task;
+-------------+--------------+---------------------+
| sql_digest  | plan_digest  | update_time         |
+-------------+--------------+---------------------+
| example_sql | example_plan | 2023-01-28 11:58:22 |
+-------------+--------------+---------------------+
1 row in set (0.01 sec)
```

### View the capture results

After `PLAN REPLAYER CAPTURE` successfully captures the result, you can view the token used for file download using the following SQL statement:

```sql
mysql> SELECT * FROM mysql.plan_replayer_status;
+------------------------------------------------------------------+------------------------------------------------------------------+------------+-----------------------------------------------------------+---------------------+-------------+-----------------+
| sql_digest                                                       | plan_digest                                                      | origin_sql | token                                                     | update_time         | fail_reason | instance        |
+------------------------------------------------------------------+------------------------------------------------------------------+------------+-----------------------------------------------------------+---------------------+-------------+-----------------+
| 086e3fbd2732f7671c17f299d4320689deeeb87ba031240e1e598a0ca14f808c | 042de2a6652a6d20afc629ff90b8507b7587a1c7e1eb122c3e0b808b1d80cc02 |            | replayer_Utah4nkz2sIEzkks7tIRog==_1668746293523179156.zip | 2022-11-18 12:38:13 | NULL        | 172.16.4.4:4022 |
| b5b38322b7be560edb04f33f15b15a885e7c6209a22b56b0804622e397199b54 | 1770efeb3f91936e095f0344b629562bf1b204f6e46439b7d8f842319297c3b5 |            | replayer_Z2mUXNHDjU_WBmGdWQqifw==_1668746293560115314.zip | 2022-11-18 12:38:13 | NULL        | 172.16.4.4:4022 |
| 96d00c0b3f08795fe94e2d712fa1078ab7809faf4e81d198f276c0dede818cf9 | 8892f74ac2a42c2c6b6152352bc491b5c07c73ac3ed66487b2c990909bae83e8 |            | replayer_RZcRHJB7BaCccxFfOIAhWg==_1668746293578282450.zip | 2022-11-18 12:38:13 | NULL        | 172.16.4.4:4022 |
+------------------------------------------------------------------+------------------------------------------------------------------+------------+-----------------------------------------------------------+---------------------+-------------+-----------------+
3 rows in set (0.00 sec)
```

The method of downloading the file of `PLAN REPLAYER CAPTURE` is the same as that of `PLAN REPLAYER`. For details, see [Examples of exporting cluster information](#examples-of-exporting-cluster-information).

> **Note:**
>
> The result file of `PLAN REPLAYER CAPTURE` is kept in the TiDB cluster for up to one week. After one week, TiDB deletes the file.

### Remove the capture tasks

If a capture task is no longer needed, you can remove it using the `PLAN REPLAYER CAPTURE REMOVE` statement. For example:

```sql
mysql> PLAN REPLAYER CAPTURE '077a87a576e42360c95530ccdac7a1771c4efba17619e26be50a4cfd967204a0' '4838af52c1e07fc8694761ad193d16a689b2128bc5ced9d13beb31ae27b370ce';
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM mysql.plan_replayer_task;
+------------------------------------------------------------------+------------------------------------------------------------------+---------------------+
| sql_digest                                                       | plan_digest                                                      | update_time         |
+------------------------------------------------------------------+------------------------------------------------------------------+---------------------+
| 077a87a576e42360c95530ccdac7a1771c4efba17619e26be50a4cfd967204a0 | 4838af52c1e07fc8694761ad193d16a689b2128bc5ced9d13beb31ae27b370ce | 2024-05-21 11:26:10 |
+------------------------------------------------------------------+------------------------------------------------------------------+---------------------+
1 row in set (0.01 sec)

mysql> PLAN REPLAYER CAPTURE REMOVE '077a87a576e42360c95530ccdac7a1771c4efba17619e26be50a4cfd967204a0' '4838af52c1e07fc8694761ad193d16a689b2128bc5ced9d13beb31ae27b370ce';
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM mysql.plan_replayer_task;
Empty set (0.01 sec)
```

## Use `PLAN REPLAYER CONTINUOUS CAPTURE`

After `PLAN REPLAYER CONTINUOUS CAPTURE` is enabled, TiDB asynchronously records the applications' SQL statements with the `PLAN REPLAYER` method according to their `SQL DIGEST` and `PLAN DIGEST`. For SQL statements and execution plans that share the same DIGEST, `PLAN REPLAYER CONTINUOUS CAPTURE` does not record them repeatedly.

### Enable `PLAN REPLAYER CONTINUOUS CAPTURE`

`PLAN REPLAYER CONTINUOUS CAPTURE` is controlled by the system variable [`tidb_enable_plan_replayer_continuous_capture`](/system-variables.md#tidb_enable_plan_replayer_continuous_capture-new-in-v700). To enable `PLAN REPLAYER CONTINUOUS CAPTURE`, set the value of the system variable to `ON`.

### View the capture results

The method of viewing the capture results of `PLAN REPLAYER CONTINUOUS CAPTURE` is the same as that of [Viewing the capture results of `PLAN REPLAYER CAPTURE`](#view-the-capture-results).