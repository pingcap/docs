---
title: SHOW ANALYZE STATUS
summary: An overview of the usage of SHOW ANALYZE STATUS for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-show-analyze-status/']
---

# SHOW ANALYZE STATUS

The `SHOW ANALYZE STATUS` statement shows the statistics collection tasks being executed by TiDB and a limited number of historical task records.

Starting from TiDB v6.1.0, the `SHOW ANALYZE STATUS` statement supports showing cluster-level tasks. Even after a TiDB restart, you can still view task records before the restart using this statement. Before TiDB v6.1.0, the `SHOW ANALYZE STATUS` statement can only show instance-level tasks, and task records are cleared after a TiDB restart.

Starting from TiDB v6.1.0, you can view the history tasks within the last 7 days through the system table `mysql.analyze_jobs`.

Starting from TiDB v7.3.0, you can view the progress of the current `ANALYZE` task through the system table `mysql.analyze_jobs` or `SHOW ANALYZE STATUS`.

Currently, the `SHOW ANALYZE STATUS` statement returns the following columns:

| Column name      | Description |
| :--------------- | :------------- |
| `Table_schema`   | The database name |
| `Table_name`     | The table name |
| `Partition_name` | The partition name |
| `Job_info`       | A brief description of the `ANALYZE` subtask. It shows the `ANALYZE` scope, such as columns, indexes, or global statistics merge, and might include the effective options used, such as `buckets`, `topn`, `samplerate`, or `samples`. |
| `Processed_rows` | The number of rows that have been analyzed |
| `Start_time`     | The time at which the task starts |
| `End_time`       | The time at which the task ends |
| `State`          | The state of a task, including `pending`, `running`, `finished`, and `failed` |
| `Fail_reason`    | The reason why the task fails. If the execution is successful, the value is `NULL`. |
| `Instance`       | The TiDB instance that executes the task |
| `Process_ID`     | The process ID that executes the task |
| `Remaining_seconds` | The estimated time (in seconds) remaining for the task to complete |
| `Progress`       | The progress of the task |
| `Estimated_total_rows` | The total rows that need to be analyzed by the task |

## Synopsis

```ebnf+diagram
ShowAnalyzeStatusStmt ::= 'SHOW' 'ANALYZE' 'STATUS' ShowLikeOrWhereOpt

ShowLikeOrWhereOpt ::= 'LIKE' SimpleExpr | 'WHERE' Expression
```

## Examples

> **Note:**
>
> Starting from v9.0.0, TiDB no longer supports using Statistics Version 1 (`tidb_analyze_version = 1`) for new statistics collection. The following example shows the `ANALYZE` behavior with Statistics Version 2.

```sql
mysql> create table t(x int, index idx(x)) partition by hash(x) partitions 2;
Query OK, 0 rows affected (0.69 sec)

<<<<<<< HEAD
=======
mysql> set @@tidb_analyze_version = 1;
Query OK, 0 rows affected (0.00 sec)

mysql> analyze table t;
Query OK, 0 rows affected (0.20 sec)

mysql> show analyze status;
+--------------+------------+----------------+-------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+------------------+----------+---------------------+
| Table_schema | Table_name | Partition_name | Job_info          | Processed_rows | Start_time          | End_time            | State    | Fail_reason | Instance       | Process_ID | Remaining_seconds| Progress | Estimated_total_rows|
+--------------+------------+----------------+-------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+------------------+----------+---------------------+
| test         | t          | p1             | analyze index idx |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL             | NULL     | NULL                |
| test         | t          | p0             | analyze index idx |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL             | NULL     | NULL                |
| test         | t          | p1             | analyze columns   |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL             | NULL     | NULL                |
| test         | t          | p0             | analyze columns   |              0 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL             | NULL     | NULL                |
| test         | t1         | p0             | analyze columns   |       28523259 | 2022-05-27 11:29:46 | 2022-05-27 11:29:46 | running  | NULL        | 127.0.0.1:4000 | 690208308  | 0s               | 0.9843   | 28978290            |
+--------------+------------+----------------+-------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+------------------+----------+---------------------+
5 rows in set (0.01 sec)

mysql> set @@tidb_analyze_version = 2;
Query OK, 0 rows affected (0.00 sec)

>>>>>>> 43829857d8 (sql-statements: fix the row count in the SHOW ANALYZE STATUS example output (#24050))
mysql> analyze table t;
Query OK, 0 rows affected, 2 warnings (0.03 sec)

mysql> show analyze status;
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+--------------------+----------+----------------------+
| Table_schema | Table_name | Partition_name | Job_info                                                           | Processed_rows | Start_time          | End_time            | State    | Fail_reason | Instance       | Process_ID | Remaining_seconds  | Progress | Estimated_total_rows |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+--------------------+----------+----------------------+
| test         | t          | p1             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-27 11:30:12 | 2022-05-27 11:30:12 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL               | NULL     | NULL                 |
| test         | t          | p0             | analyze table all columns with 256 buckets, 500 topn, 1 samplerate |              0 | 2022-05-27 11:30:12 | 2022-05-27 11:30:12 | finished | NULL        | 127.0.0.1:4000 | NULL       | NULL               | NULL     | NULL                 |
+--------------+------------+----------------+--------------------------------------------------------------------+----------------+---------------------+---------------------+----------+-------------+----------------+------------+--------------------+----------+----------------------+
2 rows in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [ANALYZE_STATUS table](/information-schema/information-schema-analyze-status.md)
