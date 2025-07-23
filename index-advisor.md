---
title: Index Advisor
summary: 了解如何使用 TiDB Index Advisor 优化查询性能。
---

# Index Advisor

在 v8.5.0 版本中，TiDB 引入了 Index Advisor 功能，帮助你通过推荐索引来优化工作负载，从而提升查询性能。借助新的 SQL 语句 `RECOMMEND INDEX`，你可以为单个查询或整个工作负载生成索引建议。为了避免在评估过程中物理创建索引带来的资源消耗，TiDB 支持 [hypothetical indexes](#hypothetical-indexes)，即不物化的逻辑索引。

> **Note:**
>
> 目前，该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

Index Advisor 会分析查询，识别出 `WHERE`、`GROUP BY` 和 `ORDER BY` 等子句中的可索引列。然后，它会生成索引候选项，并利用 hypothetical indexes 估算其性能提升。TiDB 使用遗传搜索算法，从单列索引开始，逐步探索多列索引，结合 “What-If” 分析，评估潜在索引对优化器执行计划成本的影响。索引建议会在其能显著降低整体成本时被推荐。

除了 [推荐新索引](#recommend-indexes-using-the-recommend-index-statement)，Index Advisor 还会建议 [删除未使用的索引](#remove-unused-indexes)，以确保索引管理的高效性。

## Recommend indexes using the `RECOMMEND INDEX` statement

TiDB 引入 `RECOMMEND INDEX` SQL 语句，用于索引建议任务。`RUN` 子命令会分析历史工作负载，并将建议存储在系统表中。通过 `FOR` 选项，你可以针对特定的 SQL 语句，即使它之前未执行过，也能生成建议。还可以使用其他 [options](#recommend-index-options) 进行高级控制。语法如下：

```sql
RECOMMEND INDEX RUN [ FOR <SQL> ] [<Options>] 
```

### Recommend indexes for a single query

以下示例演示如何为表 `t`（包含 5000 行）上的查询生成索引建议。为简洁起见，省略了 `INSERT` 语句。

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

Index Advisor 会分别评估 `a` 和 `b` 的单列索引，最终将它们合并成一个复合索引以获得最佳性能。

以下 `EXPLAIN` 结果对比了没有索引和使用推荐的两列 hypothetic 索引的执行计划。Index Advisor 会内部评估两种情况，选择成本最低的方案。它还会考虑在 `a` 和 `b` 上的单列 hypothetical indexes，但这些索引的性能不优于合并的两列索引。为简洁起见，省略了执行计划。

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

以下示例演示如何为整个工作负载生成索引建议。假设表 `t1` 和 `t2` 各包含 5000 行：

```sql
CREATE TABLE t1 (a INT, b INT, c INT, d INT);
CREATE TABLE t2 (a INT, b INT, c INT, d INT);

-- 在此工作负载中运行一些查询。
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

在此场景中，Index Advisor 识别出整个工作负载的最优索引，而非单个查询。工作负载中的查询来自 TiDB 系统表 `INFORMATION_SCHEMA.STATEMENTS_SUMMARY`。

该表可能包含数万到数十万的查询，可能影响 Index Advisor 的性能。为此，Index Advisor 会优先考虑执行频率较高的查询，这些查询对整体工作负载性能影响更大。默认情况下，Index Advisor 会选择前 1000 条查询。你可以通过 [`max_num_query`](#recommend-index-options) 参数调整。

`RECOMMEND INDEX` 语句的结果会存储在 `mysql.index_advisor_results` 表中。你可以查询此表以查看推荐的索引。以下示例显示在执行前述两个 `RECOMMEND INDEX` 语句后，该系统表的内容：

```sql
SELECT * FROM mysql.index_advisor_results;
+----+---------------------+---------------------+-------------+------------+------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+-------+
| id | created_at          | updated_at          | schema_name | table_name | index_name | index_columns | index_details                                                                                                                                                                                       | top_impacted_queries                                                                                                                                                                                                              | workload_impact                   | extra |
+----+---------------------+---------------------+-------------+------------+------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+-------+
|  1 | 2024-12-10 11:44:45 | 2024-12-10 11:44:45 | test        | t1         | idx_a_b    | a,b           | {"IndexSize": 0, "Reason": "Column [a b] appear in Equal or Range Predicate clause(s) in query: select `a` , `b` from `test` . `t1` where `a` = ? and `b` <= ?"}                                    | [{"Improvement": 0.998214, "Query": "SELECT `a`,`b` FROM `test`.`t1` WHERE `a` = 1 AND `b` <= 5"}, {"Improvement": 0.337273, "Query": "SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`"}] | {"WorkloadImprovement": 0.395235} | NULL  |
|  2 | 2024-12-10 11:44:45 | 2024-12-10 11:44:45 | test        | t1         | idx_d      | d             | {"IndexSize": 0, "Reason": "Column [d] appear in Equal or Range Predicate clause(s) in query: select `d` from `test` . `t1` order by `d` limit ?"}                                                  | [{"Query":"SELECT `d` FROM `test`.`t1` ORDER BY `d` LIMIT 10"}]                                                                                                                                         | {"WorkloadImprovement": 0.225116} | NULL  |
|  3 | 2024-12-10 11:44:45 | 2024-12-10 11:44:45 | test        | t2         | idx_d      | d             | {"IndexSize": 0, "Reason": "Column [d] appear in Equal or Range Predicate clause(s) in query: select * from ( `test` . `t1` ) join `test` . `t2` where `t1` . `a` = ? and `t1` . `d` = `t2` . `d`"} | [{"Improvement": 0.639393, "Query": "SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`"}]                                                                                                   | {"WorkloadImprovement": 0.365871} | NULL  |
+----+---------------------+---------------------+-------------+------------+------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+-------+
```

### `RECOMMEND INDEX` options

你可以配置和查看 `RECOMMEND INDEX` 语句的选项，以微调其对工作负载的适应性，方法如下：

```sql
RECOMMEND INDEX SET <option> = <value>;
RECOMMEND INDEX SHOW OPTION;
```

可用的选项包括：

- `timeout`: 指定运行 `RECOMMEND INDEX` 命令的最大时间。
- `max_num_index`: 指定 `RECOMMEND INDEX` 返回的最大索引数。
- `max_index_columns`: 指定多列索引中允许的最大列数。
- `max_num_query`: 指定从语句摘要工作负载中选择的最大查询数。

执行 `RECOMMEND INDEX SHOW OPTION` 查看当前设置：

```sql
RECOMMEND INDEX SHOW OPTION;
+-------------------+-------+---------------------------------------------------------+
| option            | value | description                                             |
+-------------------+-------+---------------------------------------------------------+
| max_num_index     | 5     | 推荐的最大索引数。                                       |
| max_index_columns | 3     | 索引中最大列数。                                         |
| max_num_query     | 1000  | 推荐索引的最大查询数。                                     |
| timeout           | 30s   | 索引建议器的超时时间。                                     |
+-------------------+-------+---------------------------------------------------------+
4 rows in set (0.00 sec)
```

若要修改某个选项，使用 `RECOMMEND INDEX SET` 语句。例如，修改 `timeout` 选项：

```sql
RECOMMEND INDEX SET timeout='20s';
Query OK, 1 row affected (0.00 sec)
```

### 限制

索引推荐功能存在以下限制：

- 目前不支持 [prepared statements](/develop/dev-guide-prepared-statement.md)。`RECOMMEND INDEX RUN` 语句无法为通过 `Prepare` 和 `Execute` 协议执行的查询推荐索引。
- 目前不提供删除索引的建议。
- 目前还没有索引建议器的用户界面（UI）。

## Remove unused indexes

对于 v8.0.0 及更高版本，你可以使用 [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) 和 [`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) 来识别工作负载中的未使用索引。删除这些索引可以节省存储空间，减少开销。对于生产环境，强烈建议先将目标索引设为不可见，并观察完整业务周期内的影响，再决定是否永久删除。

### Use `sys.schema_unused_indexes`

[`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) 视图会显示自所有 TiDB 实例上次启动以来未被使用的索引。该视图基于包含 schema、table 和 column 信息的系统表，提供每个索引的完整定义，包括 schema、table 和索引名。你可以查询此视图，决定将索引设为不可见或删除。

> **Warning:**
>
> 由于 `sys.schema_unused_indexes` 视图显示自所有 TiDB 实例上次启动以来未被使用的索引，确保 TiDB 实例已运行足够长时间，否则可能会显示误判的候选索引，特别是在某些工作负载尚未运行的情况下。你可以执行以下 SQL 查询，查看所有 TiDB 实例的启动时间：
>
> ```sql
> SELECT START_TIME,UPTIME FROM INFORMATION_SCHEMA.CLUSTER_INFO WHERE TYPE='tidb';
> ```

### Use `INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`

`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE` 表提供选择性桶、最后访问时间和访问行数等指标。以下示例演示如何通过此表识别未使用或低效的索引：

```sql
-- 查找在过去 30 天内未被访问的索引。
SELECT table_schema, table_name, index_name, last_access_time
FROM information_schema.cluster_tidb_index_usage
WHERE last_access_time IS NULL
  OR last_access_time < NOW() - INTERVAL 30 DAY;

-- 查找持续扫描且行数超过 50% 的索引。
SELECT table_schema, table_name, index_name,
       query_total, rows_access_total,
       percentage_access_0 as full_table_scans
FROM information_schema.cluster_tidb_index_usage
WHERE last_access_time IS NOT NULL AND percentage_access_0 + percentage_access_0_1 + percentage_access_1_10 + percentage_access_10_20 + percentage_access_20_50 = 0;
```

> **Note:**
>
> `INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE` 中的数据可能延迟最多五分钟，且在 TiDB 节点重启后会重置。索引使用情况仅在表具有有效统计信息时才会被记录。

## Hypothetical indexes

Hypothetical indexes（Hypo Indexes）通过 SQL 注释创建，类似 [query hints](/optimizer-hints.md)，而不是通过 `CREATE INDEX` 语句。这种方式允许轻量级地试验索引，无需物理物化。

例如，`/*+ HYPO_INDEX(t, idx_ab, a, b) */` 注释会指示查询计划生成器在表 `t` 上创建名为 `idx_ab` 的 hypothetic 索引，包含列 `a` 和 `b`。索引的元数据会被生成，但不会物理创建。如果适用，查询优化器会在优化过程中考虑此 hypothetic 索引，而不会产生索引创建的开销。

`RECOMMEND INDEX` 建议器会利用 hypothetic indexes 进行 “What-If” 分析，评估不同索引的潜在收益。你也可以直接使用 hypothetic indexes 来试验索引设计，然后再决定是否创建。

以下示例演示了使用 hypothetic index 的查询：

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

在此示例中，`HYPO_INDEX` 注释指定了一个 hypothetic 索引。使用此索引将估算成本从 `392133.42` 降低到 `2.20`，实现了从全表扫描（`TableFullScan`）到索引范围扫描（`IndexRangeScan`）的转换。

根据你的工作负载中的查询，TiDB 可以自动生成可能受益的索引候选项，利用 hypothetic indexes 估算潜在收益，从而推荐最有效的索引。