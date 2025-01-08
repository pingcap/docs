---
title: Index Advisor
summary: TiDB Index Advisor.
---

# Index Advisor Overview

TiDB's Index Advisor helps users optimize their workload by recommending indexes to improve query performance. The new SQL instruction, `RECOMMEND INDEX`, allows users to generate index recommendations for a single query or an entire workload. To avoid the resource-intensive process of physically creating indexes for evaluation, TiDB supports hypothetical indexes—logical indexes that are not materialized. The syntax and usage of Hypo Indexes are detailed in the Appendix.

The Index Advisor analyzes queries to identify indexable columns from relevant clauses (for example, `WHERE`, `GROUP BY`, `ORDER BY`) and generates index candidates. Using the Hypo Index feature, it estimates the performance benefits of these candidates and employs a genetic search algorithm to select the optimal set of indexes. This algorithm begins with single-column indexes and iteratively explores multi-column indexes, leveraging a `What-If` analysis to evaluate potential indexes based on their impact on optimizer plan costs. Indexes are recommended if they reduce the overall cost compared to executing queries without them.

In addition to recommending new indexes, TiDB also offers a feature to suggest dropping inactive indexes, ensuring efficient index management.

# Recommend Index command

SQL command `RECOMMEND INDEX` is introduced for index advisor tasks.  Sub command `RUN` explores historical workloads and saves the recommendations in system tables. With option `FOR`,  the command targets particular SQL statement even if it was not executed in the past. The command also accepts extra options for advance control. 

```sql
Recommend Index Run [ For <SQL> ] [<Options>] 
```

## Single Query Option

Below is an example of a single query, assuming 5,000 rows in table  `t` (we omit the insert statements for brevity):

```sql
mysql> CREATE TABLE t(a int, b int, c int);
mysql> RECOMMEND INDEX RUN for "select a, b from t where a=1 and b=1";
+----------+-------+------------+---------------+------------+----------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+---------------------------------+
| database | table | index_name | index_columns | index_size | reason                                                                                                                           | top_impacted_query                                                                            | create_index_statement          |
+----------+-------+------------+---------------+------------+----------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+---------------------------------+
| test     | t     | idx_a_b    | a,b           | 19872      | Column [a b] appear in Equal or Range Predicate clause(s) in query: select `a` , `b` from `test` . `t` where `a` = ? and `b` = ? | [{"Query":"SELECT `a`,`b` FROM `test`.`t` WHERE `a` = 1 AND `b` = 1","Improvement":0.999994}] | CREATE INDEX idx_a_b ON t(a,b); |
+----------+-------+------------+---------------+------------+----------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------+---------------------------------+
```

The index advisor considers single column indexes on `a` and `b` seperately and end up combining them in a single index which provides the best performance for the above singel query. 

Below, we show explain result for two cases: (1) query without indexes and (2) same query with the two column indexes using hypo (`what if`) index. The index advisor internally attempts both cases and pick the one with the least cost. Note that the search space also includes hypo indexes on `a` and `b`  seperatley which does not provide lower cost than the two column iondex on both columns. For space limitation, we do not show these plans. 

```sql
mysql> explain format='verbose' select a, b from t where a=1 and b=1;
+-------------------------+---------+------------+-----------+---------------+----------------------------------+
| id                      | estRows | estCost    | task      | access object | operator info                    |
+-------------------------+---------+------------+-----------+---------------+----------------------------------+
| TableReader_7           | 0.01    | 196066.71  | root      |               | data:Selection_6                 |
| └─Selection_6           | 0.01    | 2941000.00 | cop[tikv] |               | eq(test.t.a, 1), eq(test.t.b, 1) |
|   └─TableFullScan_5     | 5000.00 | 2442000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo   |
+-------------------------+---------+------------+-----------+---------------+----------------------------------+

mysql> explain format='verbose' select /*+ HYPO_INDEX(t, idx_ab, a, b) */ a, b from t where a=1 and b=1;
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| id                     | estRows | estCost | task      | access object               | operator info                                   |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| IndexReader_6          | 0.05    | 1.10    | root      |                             | index:IndexRangeScan_5                          |
| └─IndexRangeScan_5     | 0.05    | 10.18   | cop[tikv] | table:t, index:idx_ab(a, b) | range:[1 1,1 1], keep order:false, stats:pseudo |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
```

## Workload Option

We illustrate this option through an example below, assuming 5,000 rows in `t1` and `t2`:

```sql
mysql> CREATE TABLE t1 (a int, b int, c int, d int);
mysql> CREATE TABLE t2 (a int, b int, c int, d int);

-- run some queires in this workload
mysql> select a, b from t1 where a=1 and b<=5;
mysql> select d from t1 order by d limit 10;
mysql> select * from t1, t2 where t1.a=1 and t1.d=t2.d;

mysql> RECOMMEND INDEX RUN;
+----------+-------+------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+
| database | table | index_name | index_columns | index_size | reason                                                                                                                                                                | top_impacted_query                                                                                                                                                                                                              | create_index_statement           |
+----------+-------+------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+
| test     | t1    | idx_a_b    | a,b           | 19872      | Column [a b] appear in Equal or Range Predicate clause(s) in query: select `a` , `b` from `test` . `t1` where `a` = ? and `b` <= ?                                    | [{"Query":"SELECT `a`,`b` FROM `test`.`t1` WHERE `a` = 1 AND `b` \u003c= 5","Improvement":0.998214},{"Query":"SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`","Improvement":0.336837}] | CREATE INDEX idx_a_b ON t1(a,b); |
| test     | t1    | idx_d      | d             | 9936       | Column [d] appear in Equal or Range Predicate clause(s) in query: select `d` from `test` . `t1` order by `d` limit ?                                                  | [{"Query":"SELECT `d` FROM `test`.`t1` ORDER BY `d` LIMIT 10","Improvement":0.999433}]                                                                                                                                          | CREATE INDEX idx_d ON t1(d);     |
| test     | t2    | idx_d      | d             | 9936       | Column [d] appear in Equal or Range Predicate clause(s) in query: select * from ( `test` . `t1` ) join `test` . `t2` where `t1` . `a` = ? and `t1` . `d` = `t2` . `d` | [{"Query":"SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`","Improvement":0.638567}]                                                                                                    | CREATE INDEX idx_d ON t2(d);     |
+----------+-------+------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+
```

In this case, the index advisor identifies optimal indexes for an entire workload rather than focusing on a single query. The workload queries are sourced from the TiDB system table `information_schema.statements_summary`. 

This table can contain a vast number of queries, ranging from tens to hundreds of thousands, which can impact the performance of the index advisor. To address this, the index advisor prioritizes the most important queries in the workload based on their frequency, as frequent queries have a greater impact on overall workload performance. By default, the index advisor selects the top 1,000 queries, a configurable value controlled by the parameter `max_num_query` (see below).

The results of the `RECOMMEND INDEX` commands are stored in the `mysql.index_advisor_results` table. Users can query this table to view the recommended indexes. Below is an example of the contents of this system table after executing the two `RECOMMEND INDEX` commands mentioned above.

```sql
mysql> select * from mysql.index_advisor_results;
+----+---------------------+---------------------+-------------+------------+------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+-------+
| id | created_at          | updated_at          | schema_name | table_name | index_name | index_columns | index_details                                                                                                                                                                                       | top_impacted_queries                                                                                                                                                                                                              | workload_impact                   | extra |
+----+---------------------+---------------------+-------------+------------+------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+-------+
|  1 | 2024-12-10 11:44:45 | 2024-12-10 11:44:45 | test        | t1         | idx_a_b    | a,b           | {"IndexSize": 0, "Reason": "Column [a b] appear in Equal or Range Predicate clause(s) in query: select `a` , `b` from `test` . `t1` where `a` = ? and `b` <= ?"}                                    | [{"Improvement": 0.998214, "Query": "SELECT `a`,`b` FROM `test`.`t1` WHERE `a` = 1 AND `b` <= 5"}, {"Improvement": 0.337273, "Query": "SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`"}] | {"WorkloadImprovement": 0.395235} | NULL  |
|  2 | 2024-12-10 11:44:45 | 2024-12-10 11:44:45 | test        | t1         | idx_d      | d             | {"IndexSize": 0, "Reason": "Column [d] appear in Equal or Range Predicate clause(s) in query: select `d` from `test` . `t1` order by `d` limit ?"}                                                  | [{"Improvement": 0.999715, "Query": "SELECT `d` FROM `test`.`t1` ORDER BY `d` LIMIT 10"}]                                                                                                                                         | {"WorkloadImprovement": 0.225116} | NULL  |
|  3 | 2024-12-10 11:44:45 | 2024-12-10 11:44:45 | test        | t2         | idx_d      | d             | {"IndexSize": 0, "Reason": "Column [d] appear in Equal or Range Predicate clause(s) in query: select * from ( `test` . `t1` ) join `test` . `t2` where `t1` . `a` = ? and `t1` . `d` = `t2` . `d`"} | [{"Improvement": 0.639393, "Query": "SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`"}]                                                                                                   | {"WorkloadImprovement": 0.365871} | NULL  |
+----+---------------------+---------------------+-------------+------------+------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+-------+
```

## Index Advisor Options

The `RECOMMEND INDEX` syntax supports configuring and displaying options related to the command, as shown below:

```sql
Recommend Index Set <option> = <value>;
Recommend Index Show;
```

There are four configurable options available, detailed below:
1. timeout: Specifies the time limit for running the `RECOMMEND INDEX` command.
2. max_num_index: Defines the maximum total number of indexes to include in the result of `RECOMMEND INDEX`.
3. max_index_columns: Sets the maximum number of columns allowed in multi-column indexes in the result.
4. max_num_query: Specifies the maximum number of queries to select from the statement summary workload.

Users can view the current settings using the `RECOMMEND INDEX SHOW` command. Below is an example that displays the current option values and demonstrates how to modify the timeout option:

```sql
mysql> recommend index show;
+-------------------+-------+---------------------------------------------------------+
| option            | value | description                                             |
+-------------------+-------+---------------------------------------------------------+
| max_num_index     | 5     | The maximum number of indexes to recommend.             |
| max_index_columns | 3     | The maximum number of columns in an index.              |
| max_num_query     | 1000  | The maximum number of queries to recommend indexes.     |
| timeout           | 30s   | The timeout of index advisor.                           |
+-------------------+-------+---------------------------------------------------------+
4 rows in set (0.00 sec)

mysql> recommend index set timeout='20s';
Query OK, 1 row affected (0.00 sec)
```

This example shows how users can inspect and update the index advisor's settings to fine-tune its behavior for their workloads.

## Limitations

Here are some current limitations of the index recommendation feature, which we plan to address in the future:
1. It does not support prepared statements, meaning `RECOMMEND INDEX RUN` cannot recommend indexes for queries executed through the `Prepare` and `Execute` protocol.
2. It does not provide recommendations for deleting indexes. We need to merge the removing index logic (see below) to the `RECOMMEND` command in the future. 
3. A UI for the Index Advisor will be available in the future.

# Removing Unused Indexes
TiDB provides two system views/tables to help users identify inactive indexes in their workload. Users can either mark such indexes as invisible as a transitional state before dropping them or drop them right away. 

## View sys.schema_unused_indexes

The `sys.schema_unused_indexes` view identifies indexes that have not been used since the startup of all TiDB instances. The view is defined based on system tables that have schema, table and column information. The view provides the full specification for the index including index, table and schema names. Users can query this view and decide on making indexes invisible or deleting them. 

## View information_schema.tidb_index_usage

This table provides metrics like access patterns, last access time, and rows accessed. Below, we show SQL query recommendations on how to identify unused or inefficient indexes based on this table. 

```sql
-- Find indexes that haven't been accessed recently
SELECT table_schema, table_name, index_name, last_access_time
FROM information_schema.cluster_tidb_index_usage
WHERE last_access_time IS NULL
  OR last_access_time < NOW() - INTERVAL 30 DAY;

-- Find indexes with low efficiency
SELECT table_schema, table_name, index_name,
       query_total, rows_access_total,
       percentage_access_0 as full_table_scans
FROM information_schema.cluster_tidb_index_usage
WHERE last_access_time IS NOT NULL AND percentage_access_0 + percentage_access_0_1 + percentage_access_1_10 + percentage_access_10_20 + percentage_access_20_50 = 0;
```

Users should be aware that the data in `tidb_index_usage` may be delayed by up to 5 minutes, and the usage data is reset whenever a TiDB node restarts. Additionally, index usage is only recorded if the table has valid statistics.



# Appendix

## Hypo Indexes

Hypothetical indexes (Hypo Indexes) are created using SQL comments, similar to query hints, rather than through the `CREATE INDEX` command. This method allows for lightweight index experimentation without the overhead of physically materializing the index.

For example, the comment `/*+ HYPO_INDEX(t, idx_ab, a, b) */` instructs the query planner to create a hypothetical index named `idx_ab` on table `t`, spanning columns `a` and `b`. The planner generates the index's metadata but does not physically materialize it. If applicable, the planner considers the hypothetical index during query optimization, without incurring any index creation costs.

The `RECOMMEND INDEX` advisor uses hypothetical indexes for `What-If` analysis to evaluate the potential benefits of different indexes. Users can also directly leverage hypothetical indexes to experiment with index designs before committing to their creation.

Below is an example of a query that utilizes a hypothetical index:

```sql
mysql> CREATE TABLE t(a int, b int, c int);
Query OK, 0 rows affected (0.02 sec)

mysql> explain format='verbose' select a, b from t where a=1 and b=1;
+-------------------------+----------+------------+-----------+---------------+----------------------------------+
| id                      | estRows  | estCost    | task      | access object | operator info                    |
+-------------------------+----------+------------+-----------+---------------+----------------------------------+
| TableReader_7           | 0.01     | 392133.42  | root      |               | data:Selection_6                 |
| └─Selection_6           | 0.01     | 5882000.00 | cop[tikv] |               | eq(test.t.a, 1), eq(test.t.b, 1) |
|   └─TableFullScan_5     | 10000.00 | 4884000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo   |
+-------------------------+----------+------------+-----------+---------------+----------------------------------+

mysql> explain format='verbose' select /*+ HYPO_INDEX(t, idx_ab, a, b) */ a, b from t where a=1 and b=1;
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| id                     | estRows | estCost | task      | access object               | operator info                                   |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| IndexReader_6          | 0.10    | 2.20    | root      |                             | index:IndexRangeScan_5                          |
| └─IndexRangeScan_5     | 0.10    | 20.35   | cop[tikv] | table:t, index:idx_ab(a, b) | range:[1 1,1 1], keep order:false, stats:pseudo |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
```

In this example, the `HYPO_INDEX` hint specifies a hypothetical index. By using this index, we avoid the `TableFullScan` on table `t`, and the overall plan cost is reduced from `392133.42` to `2.20`.

Based on queries in your workload, TiDB can automatically generate possible index candidates that could benefit your workload. It uses hypothetical indexes to estimate their potential benefits and recommends the best ones.