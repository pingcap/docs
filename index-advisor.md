---
title: Index Advisor
summary: Learn how to optimize query performance with TiDB Index Advisor.
---

# Index Advisor

In v8.5.0, TiDB introduces the Index Advisor feature, which helps optimize your workload by recommending indexes that improve query performance. Using the new SQL statement, `RECOMMEND INDEX`, you can generate index recommendations for a single query or an entire workload. To avoid the resource-intensive process of physically creating indexes for evaluation, TiDB supports [hypothetical indexes](#hypothetical-indexes), which are logical indexes that are not materialized.

The Index Advisor analyzes queries to identify indexable columns from clauses such as `WHERE`, `GROUP BY`, and `ORDER BY`. Then, it generates index candidates and estimates their performance benefits using hypothetical indexes. TiDB uses a genetic search algorithm to select the optimal set of indexes starting with single-column indexes and iteratively exploring multi-column indexes, leveraging a "What-If" analysis to evaluate potential indexes based on their impact on optimizer plan costs. The advisor recommends indexes when they reduce the overall cost compared to executing queries without them.

In addition to [recommending new indexes](#recommend-indexes-using-the-recommend-index-statement), the Index Advisor also suggests [removing inactive indexes](#remove-unused-indexes) to ensure efficient index management.

## Recommend indexes using the `RECOMMEND INDEX` statement

TiDB introduces the `RECOMMEND INDEX` SQL statement for index advisor tasks. The `RUN` subcommand analyzes historical workloads and saves recommendations in system tables. With the `FOR` option, you can target a specific SQL statement, even if it was not executed previously. You can also use additional [options](#recommend-index-options) for advanced control. The syntax is as follows:

```sql
RECOMMEND INDEX RUN [ FOR <SQL> ] [<Options>] 
```

### Recommend indexes for a single query

The following example shows how to generate an index recommendation for a query on table `t`, which contains 5,000 rows. For brevity, the `INSERT` statements are omitted.

```sql
CREATE TABLE t (a INT, b INT, c INT);
RECOMMEND INDEX RUN for "SELECT a, b FROM t WHERE a = 1 AND b = 1"\G
*************************** 1. row ***************************
              database: test
                 table: t
            index_name: idx_a_b
         index_columns: a,b
        est_index_size: 0
                reason: Column [a b] appear in Equal or Range Predicate clause(s) in query: select `a` , `b` from `test` . `t` where `a` = ? and `b` = ?
    top_impacted_query: [{"Query":"SELECT `a`,`b` FROM `test`.`t` WHERE `a` = 1 AND `b` = 1","Improvement":0.999994}]
create_index_statement: CREATE INDEX idx_a_b ON t(a,b);
```

The Index Advisor evaluates single-column indexes on `a` and `b` separately and ultimately combines them into a single index for optimal performance.

The following `EXPLAIN` results compare the query execution without indexes and with the recommended two-column hypothetical index. The Index Advisor internally evaluates both cases and selects the option with the minimum cost. The Index Advisor also considers single-column hypothetical indexes on `a` and `b`, but these do not provide better performance than the combined two-column index. For brevity, the execution plans are omitted.

```sql
EXPLAIN FORMAT='VERBOSE' SELECT a, b FROM t WHERE a=1 AND b=1;

+-------------------------+---------+------------+-----------+---------------+----------------------------------+
| id                      | estRows | estCost    | task      | access object | operator info                    |
+-------------------------+---------+------------+-----------+---------------+----------------------------------+
| TableReader_7           | 0.01    | 196066.71  | root      |               | data:Selection_6                 |
| └─Selection_6           | 0.01    | 2941000.00 | cop[tikv] |               | eq(test.t.a, 1), eq(test.t.b, 1) |
|   └─TableFullScan_5     | 5000.00 | 2442000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo   |
+-------------------------+---------+------------+-----------+---------------+----------------------------------+

EXPLAIN FORMAT='VERBOSE' SELECT /*+ HYPO_INDEX(t, idx_ab, a, b) */ a, b FROM t WHERE a=1 AND b=1;
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| id                     | estRows | estCost | task      | access object               | operator info                                   |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| IndexReader_6          | 0.05    | 1.10    | root      |                             | index:IndexRangeScan_5                          |
| └─IndexRangeScan_5     | 0.05    | 10.18   | cop[tikv] | table:t, index:idx_ab(a, b) | range:[1 1,1 1], keep order:false, stats:pseudo |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
```

### Recommend indexes for a workload

The following example shows how to generate index recommendations for an entire workload. Assume tables `t1` and `t2` each contain 5,000 rows:

```sql
CREATE TABLE t1 (a INT, b INT, c INT, d INT);
CREATE TABLE t2 (a INT, b INT, c INT, d INT);

-- Run some queries in this workload.
SELECT a, b FROM t1 WHERE a=1 AND b<=5;
SELECT d FROM t1 ORDER BY d LIMIT 10;
SELECT * FROM t1, t2 WHERE t1.a=1 AND t1.d=t2.d;

RECOMMEND INDEX RUN;
+----------+-------+------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+
| database | table | index_name | index_columns | est_index_size | reason                                                                                                                                                                | top_impacted_query                                                                                                                                                                                                              | create_index_statement           |
+----------+-------+------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+
| test     | t1    | idx_a_b    | a,b           | 19872      | Column [a b] appear in Equal or Range Predicate clause(s) in query: select `a` , `b` from `test` . `t1` where `a` = ? and `b` <= ?                                    | [{"Query":"SELECT `a`,`b` FROM `test`.`t1` WHERE `a` = 1 AND `b` \u003c= 5","Improvement":0.998214},{"Query":"SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`","Improvement":0.336837}] | CREATE INDEX idx_a_b ON t1(a,b); |
| test     | t1    | idx_d      | d             | 9936       | Column [d] appear in Equal or Range Predicate clause(s) in query: select `d` from `test` . `t1` order by `d` limit ?                                                  | [{"Query":"SELECT `d` FROM `test`.`t1` ORDER BY `d` LIMIT 10","Improvement":0.999433}]                                                                                                                                          | CREATE INDEX idx_d ON t1(d);     |
| test     | t2    | idx_d      | d             | 9936       | Column [d] appear in Equal or Range Predicate clause(s) in query: select * from ( `test` . `t1` ) join `test` . `t2` where `t1` . `a` = ? and `t1` . `d` = `t2` . `d` | [{"Query":"SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`","Improvement":0.638567}]                                                                                                    | CREATE INDEX idx_d ON t2(d);     |
+----------+-------+------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+
```

In this case, the Index Advisor identifies optimal indexes for the entire workload rather than a single query. The workload queries are sourced from the TiDB system table `INFORMATION_SCHEMA.STATEMENTS_SUMMARY`.

This table can contain tens of thousands to hundreds of thousands of queries, which might affect the performance of the Index Advisor. To address this issue, the Index Advisor prioritizes the most frequently executed queries, as these queries have a greater impact on overall workload performance. By default, the Index Advisor selects the top 1,000 queries. You can adjust this value using the [`max_num_query`](#recommend-index-options) parameter.

The results of the `RECOMMEND INDEX` statements are stored in the `mysql.index_advisor_results` table. You can query this table to view the recommended indexes. The following example shows the contents of this system table after the previous two `RECOMMEND INDEX` statements are executed:

```sql
SELECT * FROM mysql.index_advisor_results;
+----+---------------------+---------------------+-------------+------------+------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+-------+
| id | created_at          | updated_at          | schema_name | table_name | index_name | index_columns | index_details                                                                                                                                                                                       | top_impacted_queries                                                                                                                                                                                                              | workload_impact                   | extra |
+----+---------------------+---------------------+-------------+------------+------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+-------+
|  1 | 2024-12-10 11:44:45 | 2024-12-10 11:44:45 | test        | t1         | idx_a_b    | a,b           | {"IndexSize": 0, "Reason": "Column [a b] appear in Equal or Range Predicate clause(s) in query: select `a` , `b` from `test` . `t1` where `a` = ? and `b` <= ?"}                                    | [{"Improvement": 0.998214, "Query": "SELECT `a`,`b` FROM `test`.`t1` WHERE `a` = 1 AND `b` <= 5"}, {"Improvement": 0.337273, "Query": "SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`"}] | {"WorkloadImprovement": 0.395235} | NULL  |
|  2 | 2024-12-10 11:44:45 | 2024-12-10 11:44:45 | test        | t1         | idx_d      | d             | {"IndexSize": 0, "Reason": "Column [d] appear in Equal or Range Predicate clause(s) in query: select `d` from `test` . `t1` order by `d` limit ?"}                                                  | [{"Improvement": 0.999715, "Query": "SELECT `d` FROM `test`.`t1` ORDER BY `d` LIMIT 10"}]                                                                                                                                         | {"WorkloadImprovement": 0.225116} | NULL  |
|  3 | 2024-12-10 11:44:45 | 2024-12-10 11:44:45 | test        | t2         | idx_d      | d             | {"IndexSize": 0, "Reason": "Column [d] appear in Equal or Range Predicate clause(s) in query: select * from ( `test` . `t1` ) join `test` . `t2` where `t1` . `a` = ? and `t1` . `d` = `t2` . `d`"} | [{"Improvement": 0.639393, "Query": "SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`"}]                                                                                                   | {"WorkloadImprovement": 0.365871} | NULL  |
+----+---------------------+---------------------+-------------+------------+------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+-------+
```

### `RECOMMEND INDEX` options

You can configure and view options for the `RECOMMEND INDEX` statement to fine-tune its behavior for your workloads as follows:

```sql
RECOMMEND INDEX SET <option> = <value>;
RECOMMEND INDEX SHOW OPTION;
```

The following options are available:

- `timeout`: specifies the maximum time allowed for running the `RECOMMEND INDEX` command.
- `max_num_index`: specifies the maximum number of indexes to include in the result of `RECOMMEND INDEX`.
- `max_index_columns`: specifies the maximum number of columns allowed in multi-column indexes in the result.
- `max_num_query`: specifies the maximum number of queries to select from the statement summary workload.

To check your current option settings, execute the `RECOMMEND INDEX SHOW OPTION` statement:

```sql
RECOMMEND INDEX SHOW OPTION;
+-------------------+-------+---------------------------------------------------------+
| option            | value | description                                             |
+-------------------+-------+---------------------------------------------------------+
| max_num_index     | 5     | The maximum number of indexes to recommend.             |
| max_index_columns | 3     | The maximum number of columns in an index.              |
| max_num_query     | 1000  | The maximum number of queries to recommend indexes.     |
| timeout           | 30s   | The timeout of index advisor.                           |
+-------------------+-------+---------------------------------------------------------+
4 rows in set (0.00 sec)
```

To modify an option, use the `RECOMMEND INDEX SET` statement. For example, to change the `timeout` option:

```sql
RECOMMEND INDEX SET timeout='20s';
Query OK, 1 row affected (0.00 sec)
```

### Limitations

The index recommendation feature has the following limitations:

- Currently, it does not support [prepared statements](/develop/dev-guide-prepared-statement.md). The `RECOMMEND INDEX RUN` statement cannot recommend indexes for queries executed through the `Prepare` and `Execute` protocol.
- Currently, it does not provide recommendations for deleting indexes.
- Currently, a user interface (UI) for the Index Advisor is not yet available.

## Remove unused indexes

For v8.0.0 or later versions, you can identify inactive indexes in your workload using [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) and [`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md). Removing these indexes can save storage space and reduce overhead. For production environments, it is highly recommended to make the target indexes invisible first and observe the impact for one complete business cycle before permanently removing them.

### Use `sys.schema_unused_indexes`

The [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) view identifies indexes that have not been used since the last startup of all TiDB instances. This view, based on system tables containing schema, table, and column information, provides the full specification for each index, including schema, table, and index names. You can query this view to decide which indexes to make invisible or delete.

> **Warning:**
>
> Because the `sys.schema_unused_indexes` view shows unused indexes since the last startup of all TiDB instances, ensure that the TiDB instances have been running long enough. Otherwise, the view might show false candidates if certain workloads have not yet run. Use the following SQL query to identify the uptime of all TiDB instances.
>
> ```sql
> SELECT START_TIME,UPTIME FROM INFORMATION_SCHEMA.CLUSTER_INFO WHERE TYPE='tidb';
> ```

### Use `INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`

The [`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) table provides metrics such as selectivity buckets, last access time, and rows accessed. The following examples show queries to identify unused or inefficient indexes based on this table:

```sql
-- Find indexes that have not been accessed in the last 30 days.
SELECT table_schema, table_name, index_name, last_access_time
FROM information_schema.cluster_tidb_index_usage
WHERE last_access_time IS NULL
  OR last_access_time < NOW() - INTERVAL 30 DAY;

-- Find indexes that are consistently scanned with over 50% of total records.
SELECT table_schema, table_name, index_name,
       query_total, rows_access_total,
       percentage_access_0 as full_table_scans
FROM information_schema.cluster_tidb_index_usage
WHERE last_access_time IS NOT NULL AND percentage_access_0 + percentage_access_0_1 + percentage_access_1_10 + percentage_access_10_20 + percentage_access_20_50 = 0;
```

> **Note:**
>
> The data in `INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE` might be delayed by up to five minutes, and the usage data is reset whenever a TiDB node restarts. Additionally, index usage is only recorded if the table has valid statistics.

## Hypothetical indexes

Hypothetical indexes (Hypo Indexes) are created using SQL comments, similar to [query hints](/optimizer-hints.md), rather than through the `CREATE INDEX` statement. This approach enables lightweight experimentation with indexes without the overhead of physically materializing them.

For example, the `/*+ HYPO_INDEX(t, idx_ab, a, b) */` comment instructs the query planner to create a hypothetical index named `idx_ab` on table `t` for columns `a` and `b`. The planner generates the index's metadata but does not physically materialize it. If applicable, the planner considers this hypothetical index during query optimization without incurring the costs associated with index creation.

The `RECOMMEND INDEX` advisor uses hypothetical indexes for "What-If" analysis to evaluate potential benefits of different indexes. You can also use hypothetical indexes directly to experiment with index designs before proceeding to create them.

The following example shows a query using a hypothetical index:

```sql
CREATE TABLE t(a INT, b INT, c INT);
Query OK, 0 rows affected (0.02 sec)

EXPLAIN FORMAT='verbose' SELECT a, b FROM t WHERE a=1 AND b=1;
+-------------------------+----------+------------+-----------+---------------+----------------------------------+
| id                      | estRows  | estCost    | task      | access object | operator info                    |
+-------------------------+----------+------------+-----------+---------------+----------------------------------+
| TableReader_7           | 0.01     | 392133.42  | root      |               | data:Selection_6                 |
| └─Selection_6           | 0.01     | 5882000.00 | cop[tikv] |               | eq(test.t.a, 1), eq(test.t.b, 1) |
|   └─TableFullScan_5     | 10000.00 | 4884000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo   |
+-------------------------+----------+------------+-----------+---------------+----------------------------------+

EXPLAIN FORMAT='verbose' SELECT /*+ HYPO_INDEX(t, idx_ab, a, b) */ a, b FROM t WHERE a=1 AND b=1;
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| id                     | estRows | estCost | task      | access object               | operator info                                   |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| IndexReader_6          | 0.10    | 2.20    | root      |                             | index:IndexRangeScan_5                          |
| └─IndexRangeScan_5     | 0.10    | 20.35   | cop[tikv] | table:t, index:idx_ab(a, b) | range:[1 1,1 1], keep order:false, stats:pseudo |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
```

In this example, the `HYPO_INDEX` comment specifies a hypothetical index. Using this index reduces the estimated cost from `392133.42` to `2.20` by enabling an index range scan (`IndexRangeScan`) instead of a full table scan (`TableFullScan`).

Based on queries in your workload, TiDB can automatically generate index candidates that could benefit your workload. It uses hypothetical indexes to estimate their potential benefits and recommend the most effective ones.