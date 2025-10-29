---
title: Index Advisor
summary: 了解如何使用 TiDB Index Advisor 优化查询性能。
---

# Index Advisor

在 v8.5.0 版本中，TiDB 引入了 Index Advisor 功能，帮助你通过推荐索引来优化工作负载并提升查询性能。你可以使用新的 SQL 语句 `RECOMMEND INDEX`，为单条查询或整个工作负载生成索引推荐。为了避免物理创建索引进行评估时的高资源消耗，TiDB 支持 [假设索引](#hypothetical-indexes)，即不会实际落地的逻辑索引。

> **Note:**
>
> 目前，该功能不支持在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群上使用。

Index Advisor 会分析查询，识别如 `WHERE`、`GROUP BY` 和 `ORDER BY` 等子句中的可建索引列。随后，它会生成索引候选项，并通过假设索引评估其性能收益。TiDB 使用遗传搜索算法，从单列索引开始，迭代探索多列索引，利用 “What-If” 分析根据优化器执行计划的成本评估潜在索引。当索引能降低整体查询成本时，Advisor 会推荐这些索引。

除了 [推荐新索引](#recommend-indexes-using-the-recommend-index-statement) 外，Index Advisor 还会建议 [移除不活跃索引](#remove-unused-indexes)，以确保高效的索引管理。

## 使用 `RECOMMEND INDEX` 语句推荐索引

TiDB 引入了 `RECOMMEND INDEX` SQL 语句用于索引推荐任务。`RUN` 子命令会分析历史工作负载，并将推荐结果保存到系统表中。通过 `FOR` 选项，你可以针对特定 SQL 语句生成推荐，即使该语句之前未被执行过。你还可以使用额外的 [选项](#recommend-index-options) 进行高级控制。语法如下：

```sql
RECOMMEND INDEX RUN [ FOR <SQL> ] [<Options>] 
```

### 为单条查询推荐索引

以下示例展示了如何为包含 5,000 行的表 `t` 上的查询生成索引推荐。为简洁起见，省略了 `INSERT` 语句。

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

Index Advisor 会分别评估 `a` 和 `b` 的单列索引，并最终将它们合并为一个多列索引以获得最佳性能。

以下 `EXPLAIN` 结果对比了无索引和使用推荐的双列假设索引时的查询执行情况。Index Advisor 会在内部评估两种情况，并选择成本最低的方案。同时，Advisor 也会考虑 `a` 和 `b` 的单列假设索引，但这些索引的性能不如组合的双列索引。为简洁起见，省略了执行计划的详细内容。

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

### 为工作负载推荐索引

以下示例展示了如何为整个工作负载生成索引推荐。假设表 `t1` 和 `t2` 各包含 5,000 行：

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

在此场景下，Index Advisor 会为整个工作负载（而非单条查询）识别最优索引。工作负载中的查询来源于 TiDB 系统表 `INFORMATION_SCHEMA.STATEMENTS_SUMMARY`。

该表可能包含数万到数十万条查询，这可能会影响 Index Advisor 的性能。为了解决这个问题，Index Advisor 会优先分析执行频率最高的查询，因为这些查询对整体工作负载性能影响更大。默认情况下，Index Advisor 会选择前 1,000 条查询。你可以通过 [`max_num_query`](#recommend-index-options) 参数调整该值。

`RECOMMEND INDEX` 语句的结果会存储在 `mysql.index_advisor_results` 表中。你可以查询该表以查看推荐的索引。以下示例展示了前述两次 `RECOMMEND INDEX` 语句执行后的系统表内容：

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

### `RECOMMEND INDEX` 选项

你可以通过如下方式配置和查看 `RECOMMEND INDEX` 语句的选项，以便针对你的工作负载微调其行为：

```sql
RECOMMEND INDEX SET <option> = <value>;
RECOMMEND INDEX SHOW OPTION;
```

可用的选项包括：

- `timeout`：指定执行 `RECOMMEND INDEX` 命令的最大允许时间。
- `max_num_index`：指定 `RECOMMEND INDEX` 结果中最多包含的索引数量。
- `max_index_columns`：指定结果中多列索引允许的最大列数。
- `max_num_query`：指定从语句摘要工作负载中选取的最大查询数量。

要查看当前选项设置，可执行 `RECOMMEND INDEX SHOW OPTION` 语句：

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

要修改选项，可使用 `RECOMMEND INDEX SET` 语句。例如，修改 `timeout` 选项：

```sql
RECOMMEND INDEX SET timeout='20s';
Query OK, 1 row affected (0.00 sec)
```

### 限制

索引推荐功能存在以下限制：

- 目前不支持 [预处理语句](/develop/dev-guide-prepared-statement.md)。`RECOMMEND INDEX RUN` 语句无法为通过 `Prepare` 和 `Execute` 协议执行的查询推荐索引。
- 目前不提供删除索引的推荐。
- 目前尚未提供 Index Advisor 的用户界面（UI）。

## 移除未使用的索引

在 v8.0.0 及更高版本中，你可以通过 [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) 和 [`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) 识别工作负载中的不活跃索引。移除这些索引可以节省存储空间并减少开销。对于生产环境，强烈建议先将目标索引设置为不可见，并观察一个完整业务周期的影响后再彻底删除。

### 使用 `sys.schema_unused_indexes`

[`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) 视图用于识别自所有 TiDB 实例上次启动以来未被使用过的索引。该视图基于包含 schema、表和列信息的系统表，提供每个索引的完整规范，包括 schema、表和索引名。你可以查询该视图，决定哪些索引需要设置为不可见或删除。

> **Warning:**
>
> 由于 `sys.schema_unused_indexes` 视图展示的是自所有 TiDB 实例上次启动以来未被使用的索引，请确保 TiDB 实例已运行足够长时间。否则，如果某些工作负载尚未运行，视图可能会显示误报。你可以使用以下 SQL 查询所有 TiDB 实例的运行时长。
>
> ```sql
> SELECT START_TIME,UPTIME FROM INFORMATION_SCHEMA.CLUSTER_INFO WHERE TYPE='tidb';
> ```

### 使用 `INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`

[`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) 表提供了选择性分桶、最后访问时间和访问行数等指标。以下示例展示了如何基于该表查询未使用或低效的索引：

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
> `INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE` 中的数据可能会有最多五分钟的延迟，并且每当 TiDB 节点重启时，使用数据会被重置。此外，只有表拥有有效统计信息时，才会记录索引使用情况。

## 假设索引

假设索引（Hypothetical Indexes，Hypo Indexes）是通过 SQL 注释（类似于 [查询提示](/optimizer-hints.md)）而非 `CREATE INDEX` 语句创建的。这种方式可以让你在无需物理落地索引的情况下，轻量级地进行索引实验。

例如，`/*+ HYPO_INDEX(t, idx_ab, a, b) */` 注释会指示查询优化器为表 `t` 的 `a`、`b` 列创建名为 `idx_ab` 的假设索引。优化器会生成该索引的元数据，但不会实际创建物理索引。如果适用，优化器会在查询优化阶段考虑该假设索引，而不会产生索引创建的相关开销。

`RECOMMEND INDEX` Advisor 会利用假设索引进行 “What-If” 分析，评估不同索引的潜在收益。你也可以直接使用假设索引，在正式创建索引前进行设计实验。

以下示例展示了如何在查询中使用假设索引：

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

在本例中，`HYPO_INDEX` 注释指定了一个假设索引。使用该索引后，估算成本从 `392133.42` 降低到 `2.20`，因为优化器可以使用索引范围扫描（`IndexRangeScan`）而不是全表扫描（`TableFullScan`）。

基于你工作负载中的查询，TiDB 可以自动生成可能带来收益的索引候选项。它会利用假设索引评估这些索引的潜在收益，并推荐最有效的索引。