---
title: TiDB-X-CLOUD.202603.1 Release Notes
summary: Learn about the features for the TiDB-X-CLOUD.202603.1 kernel.
---

# TiDB-X-CLOUD.202603.1 Release Notes

**Release date**: July 16, 2026

**Applicable TiDB Cloud plan**: {{{ .premium }}}

**TiDB X kernel version**: `TiDB-X-CLOUD.202603.1`

Starting from July 16, 2026, the default kernel version of newly created {{{ .premium }}} instances is `TiDB-X-CLOUD.202603.1`.

In `TiDB-X-CLOUD.202603.1`:

- `202603` indicates that the baseline code branch of this kernel version was created in March 2026, which is different from the release date.
- `1` indicates that it is the first patch release built from the `TiDB-X-CLOUD.202603` baseline branch.

## Features

### Performance

* Introduce significant performance improvements for certain lossy DDL operations (such as `BIGINT → INT` and `CHAR(120) → VARCHAR(60)`): when no data truncation occurs, the execution time of these operations can be reduced from hours to minutes, seconds, or even milliseconds, delivering performance gains ranging from tens to hundreds of thousands of times [#63366](https://github.com/pingcap/tidb/issues/63366) @[wjhuang2016](https://github.com/wjhuang2016), @[tangenta](https://github.com/tangenta), @[fzzf678](https://github.com/fzzf678) <!-- (dup): release-8.5.5.md > Features > Performance --> <!-- exclude author wjhuang2016 in release-8.5.5.md --> <!-- pr: https://github.com/pingcap/tidb/pull/64834, https://github.com/pingcap/tidb/pull/64337, https://github.com/pingcap/tidb/pull/64188, https://github.com/pingcap/tidb/pull/64111, https://github.com/pingcap/tidb/pull/63465, https://github.com/pingcap/tidb/pull/63970, https://github.com/pingcap/tidb/pull/63965 -->

    The optimization strategies are as follows:

    - In strict SQL mode, TiDB pre-checks for potential data truncation risks during type conversion.
    - If no data truncation risk is detected, TiDB updates only the metadata and avoids index rebuilding whenever possible.
    - If index rebuilding is required, TiDB uses a more efficient ingest process to significantly improve index rebuild performance.

  The following table shows example performance improvements based on benchmark tests on a table with 114 GiB of data and 600 million rows. The test cluster consists of 3 TiDB nodes, 6 TiKV nodes, and 1 PD node. All nodes are configured with 16 CPU cores and 32 GiB of memory.

    | Scenario | Operation type | Before optimization | After optimization | Performance improvement |
    |----------|----------------|---------------------|--------------------|--------------------------|
    | Non-indexed column | `BIGINT → INT` | 2 hours 34 minutes | 1 minute 5 seconds | 142× faster |
    | Indexed column | `BIGINT → INT` | 6 hours 25 minutes | 0.05 seconds | 460,000× faster |
    | Indexed column | `CHAR(120) → VARCHAR(60)` | 7 hours 16 minutes | 12 minutes 56 seconds | 34× faster |

    Note that the preceding test results are based on the condition that no data truncation occurs during the DDL execution. The optimizations do not apply to conversions between signed and unsigned integer types, conversions between character sets, or tables with TiFlash replicas.

    For more information, see [documentation](/sql-statements/sql-statement-modify-column.md).

* Support pushing index lookups down to TiKV to improve query performance [#62575](https://github.com/pingcap/tidb/issues/62575) @[lcwangchao](https://github.com/lcwangchao) <!-- (dup): release-8.5.5.md > Features > Performance --> <!-- pr: https://github.com/pingcap/tidb/pull/65167, https://github.com/pingcap/tidb/pull/64932, https://github.com/pingcap/tidb/pull/65001, https://github.com/pingcap/tidb/pull/64839, https://github.com/pingcap/tidb/pull/64732, https://github.com/pingcap/tidb/pull/62615, https://github.com/pingcap/tidb/pull/64704 -->

    Now TiDB supports using [optimizer hints](/optimizer-hints.md) to push the `IndexLookUp` operator down to TiKV nodes. This reduces the number of remote procedure calls (RPCs) and can improve query performance. The actual performance improvement varies depending on the specific workload and requires testing for verification.

    To explicitly instruct the optimizer to push index lookups down to TiKV for a specific table, you can use the [`INDEX_LOOKUP_PUSHDOWN(t1_name, idx1_name [, idx2_name ...])`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855) hint. It is recommended to combine this hint with the table's AFFINITY attribute. For example, set `AFFINITY="table"` for regular tables and `AFFINITY="partition"` for partitioned tables.

    To disable index lookup pushdown to TiKV for a specific table, use the [`NO_INDEX_LOOKUP_PUSHDOWN(t1_name)`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#no_index_lookup_pushdownt1_name-new-in-v855) hint.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855).

* Support table-level data affinity to improve query performance (experimental) [#9764](https://github.com/tikv/pd/issues/9764) @[lhy1024](https://github.com/lhy1024) <!-- (dup): release-8.5.5.md > Features > Performance --> <!-- pr: https://github.com/tikv/pd/pull/10157, https://github.com/tikv/pd/pull/10042, https://github.com/tikv/pd/pull/10103, https://github.com/tikv/pd/pull/10091, https://github.com/tikv/pd/pull/10080, https://github.com/tikv/pd/pull/10081, https://github.com/tikv/pd/pull/10043, https://github.com/tikv/pd/pull/10040, https://github.com/tikv/pd/pull/10041, https://github.com/tikv/pd/pull/10050, https://github.com/tikv/pd/pull/10038, https://github.com/tikv/pd/pull/9999, https://github.com/tikv/pd/pull/9998, https://github.com/tikv/pd/pull/9997, https://github.com/tikv/pd/pull/9993 -->

    Now you can configure the `AFFINITY` table option as `table` or `partition` when creating or altering a table. When this option is enabled, PD groups Regions that belong to the same table or the same partition into a single affinity group. During scheduling, PD prioritizes placing the Leaders and Voter replicas of these Regions on the same subset of a few TiKV nodes. In this scenario, by using the [`INDEX_LOOKUP_PUSHDOWN`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints#index_lookup_pushdownt1_name-idx1_name--idx2_name--new-in-v855) hint in queries, you can explicitly instruct the optimizer to push index lookups down to TiKV, reducing the latency caused by cross-node scattered queries and improving query performance.

    Note that this feature is currently experimental and is disabled by default. To enable it, set the PD configuration item [`schedule.affinity-schedule-limit`](https://docs.pingcap.com/tidb/v8.5/pd-configuration-file#affinity-schedule-limit-new-in-v855) to a value greater than `0`. This configuration item controls the maximum number of affinity scheduling tasks that PD can perform concurrently.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/table-affinity).

* Foreign key checks now support shared locks [#66154](https://github.com/pingcap/tidb/issues/66154) @[you06](https://github.com/you06) <!-- (dup): release-8.5.6.md > Features > Performance --> <!-- pr: https://github.com/pingcap/tidb/pull/69167, https://github.com/pingcap/tidb/pull/65752 -->

    In pessimistic transactions, when you run `INSERT` or `UPDATE` on a child table with foreign key constraints, foreign key checks lock the corresponding parent table rows with exclusive locks by default. In high-concurrency write scenarios on the child table, if many transactions access the same parent table rows, severe lock contention can occur.

    Now you can set the [`tidb_foreign_key_check_in_shared_lock`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_foreign_key_check_in_shared_lock-new-in-v856) system variable to `ON` to let foreign key checks use shared locks on the parent table, thereby reducing lock contention and improving concurrent write performance on the child table.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/foreign-key#locking).

### Stability

* The feature of setting the maximum limit on resource usage for background tasks of resource control becomes generally available (GA) [#56019](https://github.com/pingcap/tidb/issues/56019) @[glorv](https://github.com/glorv) <!-- (dup): release-8.5.6.md > Features > Stability --> <!-- pr: https://github.com/pingcap/tidb/pull/66381 -->

    TiDB resource control can identify and lower the priority of background tasks. In certain scenarios, you might want to limit the resource consumption of background tasks, even when resources are available. Starting from v8.4.0, you can use the `UTILIZATION_LIMIT` parameter to set the maximum percentage of resources that background tasks can consume. Each node will keep the resource usage of all background tasks below this percentage. This feature enables precise control over resource consumption for background tasks, further enhancing cluster stability.

    Now this feature is generally available (GA).

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/tidb-resource-control-background-tasks).

### Observability

* Support defining multi-dimensional, fine-grained trigger rules for slow query logs [#62959](https://github.com/pingcap/tidb/issues/62959), [#64010](https://github.com/pingcap/tidb/issues/64010) @[zimulala](https://github.com/zimulala) <!-- (dup): release-8.5.6.md > Features > Observability --> <!-- miss issue https://github.com/pingcap/tidb/issues/64010 in release-8.5.6.md --> <!-- pr: https://github.com/pingcap/tidb/pull/66132, https://github.com/pingcap/tidb/pull/66064, https://github.com/pingcap/tidb/pull/65086 -->

    Before v8.5.6, the main way to identify slow queries in TiDB is to set the [`tidb_slow_log_threshold`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_slow_log_threshold) system variable. This mechanism provides only coarse-grained control over slow query log triggering because it applies globally at the instance level and does not support fine-grained control at the session or SQL level. In addition, it supports only one trigger condition, execution time (`Query_time`), which cannot meet the need to capture slow query logs more precisely in complex scenarios.

    Starting from v8.5.6, TiDB enhances slow query log control. You can use the [`tidb_slow_log_rules`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_slow_log_rules-new-in-v856) system variable to define multi-dimensional slow query log output rules at the instance, session, and SQL levels, based on conditions such as `Query_time`, `Digest`, `Mem_max`, and `KV_total`. You can use [`tidb_slow_log_max_per_sec`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_slow_log_max_per_sec-new-in-v856) to limit the number of log entries written per second, and use the [`WRITE_SLOW_LOG`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints) hint to force slow query logging for specific SQL statements. This enables more flexible and fine-grained control over slow query logs.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/identify-slow-queries).

### SQL

* Support using table aliases in the `FOR UPDATE OF` clause [#63035](https://github.com/pingcap/tidb/issues/63035) @[cryo-zd](https://github.com/cryo-zd) <!-- (dup): release-8.5.6.md > Features > SQL --> <!-- pr: https://github.com/pingcap/tidb/pull/65532 -->

    Before this release, when a `SELECT ... FOR UPDATE OF <table>` statement references a table alias in the locking clause, TiDB might fail to resolve the alias correctly and return the `table not exists` error even if the alias is valid.

    Now TiDB supports using table aliases in the `FOR UPDATE OF` clause. TiDB can now correctly resolve locking targets from the `FROM` clause, including aliased tables, ensuring that row locks take effect as expected. This improves MySQL compatibility and makes `SELECT ... FOR UPDATE OF` statements more stable and reliable in queries that use table aliases.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/sql-statement-select).

* Support partial indexes to reduce index storage and DML maintenance overhead [#62664](https://github.com/pingcap/tidb/issues/62664) [#62761](https://github.com/pingcap/tidb/issues/62761) [#62758](https://github.com/pingcap/tidb/issues/62758) [#63447](https://github.com/pingcap/tidb/issues/63447) [#64344](https://github.com/pingcap/tidb/issues/64344) @[YangKeao](https://github.com/YangKeao) @[winoros](https://github.com/winoros) @[wjhuang2016](https://github.com/wjhuang2016) <!-- (dup): release-8.5.7.md > Features > SQL --> <!-- miss issue https://github.com/pingcap/tidb/issues/63447 in release-8.5.7.md --> <!-- exclude author wjhuang2016 in release-8.5.7.md --> <!-- pr: https://github.com/pingcap/tidb/pull/64434, https://github.com/pingcap/tidb/pull/62762, https://github.com/pingcap/tidb/pull/62759, https://github.com/pingcap/tidb/pull/65051 -->

    Now TiDB supports partial indexes, which index only rows that satisfy a predicate defined in the index `WHERE` clause. You can create a partial index using `CREATE INDEX ... WHERE ...`, `ALTER TABLE ... ADD INDEX ... WHERE ...`, or an index definition in `CREATE TABLE`.

    Partial indexes are useful when you frequently query a subset of rows based on specific conditions or need unique constraints that apply only under specific conditions. Because rows outside the predicate are not written to the index, partial indexes help reduce index storage and can lower index maintenance overhead during `INSERT`, `UPDATE`, and `DELETE` operations.

    To use partial indexes effectively, define a predicate that matches the filters in your common queries. TiDB selects a partial index only when the query predicates match or imply the partial index predicate. Currently, partial index predicates support basic comparison operators (`=`, `!=`, `<`, `<=`, `>`, `>=`), `IS NULL`, `IS NOT NULL`, and `IN` predicates with constant values.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/sql-statement-create-index#partial-indexes).

## Compatibility changes

### MySQL compatibility

* Dumpling supports exporting data from MySQL 8.4 by adapting to the updated MySQL binary log naming. [#53082](https://github.com/pingcap/tidb/issues/53082) @[dveeden](https://github.com/dveeden) <!-- (dup): release-8.5.6.md > Compatibility changes > MySQL compatibility --> <!-- pr: https://github.com/pingcap/tidb/pull/66704 -->

* Support parsing the `LATERAL` syntax for derived tables to improve MySQL 8.0 compatibility, including comma joins, `CROSS JOIN LATERAL`, and `INNER JOIN LATERAL` <!-- (dup): release-8.5.7.md > Compatibility changes > MySQL compatibility --> <!-- pr: https://github.com/pingcap/tidb/pull/67131, https://github.com/pingcap/tidb/pull/67076 -->

    Currently, TiDB only supports parsing [the `LATERAL` derived table syntax](https://docs.pingcap.com/tidb/v8.5/lateral-derived-tables) and does not support executing queries that use this syntax. If you attempt to execute such a query, TiDB returns an error. You can track the progress of full execution capability for this feature in issue [#40328](https://github.com/pingcap/tidb/issues/40328).

## Improvements

- Enhance the parsing mechanism for Parquet files to improve the import performance of Parquet-formatted data [#62906](https://github.com/pingcap/tidb/issues/62906) @[joechenrh](https://github.com/joechenrh) <!-- (dup): release-8.5.5.md > Improvements > TiDB --> <!-- pr: https://github.com/pingcap/tidb/pull/66564, https://github.com/pingcap/tidb/pull/63979 -->
- Change the default value of `tidb_analyze_column_options` to `ALL` to collect statistics for all columns by default [#64992](https://github.com/pingcap/tidb/issues/64992) @[0xPoe](https://github.com/0xPoe) <!-- (dup): release-8.5.5.md > Improvements > TiDB --> <!-- pr: https://github.com/pingcap/tidb/pull/65020, https://github.com/pingcap/tidb/pull/64994 -->
- Optimize the execution logic of the `IndexHashJoin` operator by using incremental processing in specific JOIN scenarios to avoid loading large amounts of data at once, significantly reducing memory usage and improving performance [#63303](https://github.com/pingcap/tidb/issues/63303) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan) <!-- (dup): release-8.5.5.md > Improvements > TiDB --> <!-- pr: https://github.com/pingcap/tidb/pull/63723 -->
- Improve slow query log readability by outputting non-printable prepared statement arguments as hexadecimal values [#65383](https://github.com/pingcap/tidb/issues/65383) @[dveeden](https://github.com/dveeden) <!-- (dup): release-8.5.6.md > Improvements > TiDB --> <!-- pr: https://github.com/pingcap/tidb/pull/65384 -->
- Improve slow query observability by logging client connection attributes in the slow query log and making them queryable in `INFORMATION_SCHEMA.SLOW_QUERY` and `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`; `performance_schema_session_connect_attrs_size` now controls attribute truncation, and truncated bytes are recorded in `_truncated` [#66616](https://github.com/pingcap/tidb/issues/66616) @[jiong-nba](https://github.com/jiong-nba) <!-- (dup): release-8.5.7.md > Improvements > TiDB --> <!-- pr: https://github.com/pingcap/tidb/pull/66617 -->
- Improve the performance and stability of runaway query watch handling, including more reliable watch synchronization across TiDB instances and more efficient background flushing and syncing [#65746](https://github.com/pingcap/tidb/issues/65746) @[JmPotato](https://github.com/JmPotato) <!-- (dup): release-8.5.7.md > Improvements > TiDB --> <!-- pr: https://github.com/pingcap/tidb/pull/66182, https://github.com/pingcap/tidb/pull/66171, https://github.com/pingcap/tidb/pull/65834, https://github.com/pingcap/tidb/pull/66155, https://github.com/pingcap/tidb/pull/65828, https://github.com/pingcap/tidb/pull/65747 -->
- Add the global system variable `tidb_enable_batch_query_region` to control whether TiDB uses batched Region queries to PD, improving the efficiency of fetching Region information; this variable is disabled by default [#58439](https://github.com/pingcap/tidb/issues/58439) [#8690](https://github.com/tikv/pd/issues/8690) @[JmPotato](https://github.com/JmPotato) <!-- (dup): release-8.5.7.md > Improvements > TiDB --> <!-- miss issue https://github.com/pingcap/tidb/issues/58439 in release-8.5.7.md --> <!-- pr: https://github.com/tikv/pd/pull/10139, https://github.com/tikv/pd/pull/10105 -->
- Improve the optimizer performance for queries on tables with many indexes by pruning irrelevant indexes before cost estimation, reducing query planning time and avoiding unnecessary full-range out-of-range estimation [#63856](https://github.com/pingcap/tidb/issues/63856) @[terry1purcell](https://github.com/terry1purcell) @[qw4990](https://github.com/qw4990) <!-- (dup): release-8.5.7.md > Improvements > TiDB --> <!-- exclude author qw4990 in release-8.5.7.md --> <!-- pr: https://github.com/pingcap/tidb/pull/66304, https://github.com/pingcap/tidb/pull/65854, https://github.com/pingcap/tidb/pull/64999, https://github.com/pingcap/tidb/pull/64794, https://github.com/pingcap/tidb/pull/64675, https://github.com/pingcap/tidb/pull/64484, https://github.com/pingcap/tidb/pull/64115, https://github.com/pingcap/tidb/pull/64053, https://github.com/pingcap/tidb/pull/64086, https://github.com/pingcap/tidb/pull/64054 -->
- Support partial ordered index optimization for `ORDER BY ... LIMIT/OFFSET` queries on matching prefix indexes. When `tidb_opt_partial_ordered_index_for_topn` is set to `COST`, TiDB can use the partial ordering of indexes to reduce full table scans and improve `TOPN` query performance [#63280](https://github.com/pingcap/tidb/issues/63280) [#65813](https://github.com/pingcap/tidb/issues/65813) [#66338](https://github.com/pingcap/tidb/issues/66338) @[elsa0520](https://github.com/elsa0520) @[xzhangxian1008](https://github.com/xzhangxian1008) @[winoros](https://github.com/winoros) <!-- (dup): release-8.5.7.md > Improvements > TiDB --> <!-- miss issue https://github.com/pingcap/tidb/issues/66338 in release-8.5.7.md --> <!-- exclude author xzhangxian1008, winoros in release-8.5.7.md --> <!-- pr: https://github.com/pingcap/tidb/pull/65314, https://github.com/pingcap/tidb/pull/66268, https://github.com/pingcap/tidb/pull/66181, https://github.com/pingcap/tidb/pull/65799, https://github.com/pingcap/tidb/pull/65533 -->
- Mitigate coprocessor request bursts for `IndexLookUp` queries on highly partitioned tables with local indexes to improve query stability and reduce performance spikes [#67545](https://github.com/pingcap/tidb/issues/67545) @[gengliqi](https://github.com/gengliqi) <!-- (dup): release-8.5.7.md > Improvements > TiDB --> <!-- pr: https://github.com/pingcap/tidb/pull/69334 -->
- Optimize CPU and memory usage for `INSERT ... ON DUPLICATE KEY UPDATE` statements by reducing unnecessary expression buffer allocations during execution [#65003](https://github.com/pingcap/tidb/issues/65003) @[windtalker](https://github.com/windtalker) <!-- (dup): release-8.5.7.md > Improvements > TiDB --> <!-- pr: https://github.com/pingcap/tidb/pull/65244 -->
- Add the `tidb_opt_enable_alternative_logical_plans` system variable to enable alternative logical plan optimization for subquery decorrelation [#66676](https://github.com/pingcap/tidb/issues/66676) @[AilinKid](https://github.com/AilinKid) <!-- (dup): release-8.5.7.md > Improvements > TiDB --> <!-- pr: https://github.com/pingcap/tidb/pull/66677 -->
- Optimize the logic for timestamp advancement and leader election [#9981](https://github.com/tikv/pd/issues/9981) @[bufferflies](https://github.com/bufferflies) <!-- (dup): release-8.5.5.md > Improvements > PD --> <!-- pr: https://github.com/tikv/pd/pull/9986 -->
- Support batch configuration of TiKV store limits by storage engine (TiKV or TiFlash) [#9970](https://github.com/tikv/pd/issues/9970) @[bufferflies](https://github.com/bufferflies) <!-- (dup): release-8.5.5.md > Improvements > PD --> <!-- pr: https://github.com/tikv/pd/pull/9978 -->
- Add the `store` label to the `pd_cluster_status` metric [#9855](https://github.com/tikv/pd/issues/9855) @[SerjKol80](https://github.com/SerjKol80) <!-- (dup): release-8.5.5.md > Improvements > PD --> <!-- pr: https://github.com/tikv/pd/pull/9898 -->
- Return `404` instead of `200` when deleting a non-existent label [#10089](https://github.com/tikv/pd/issues/10089) @[lhy1024](https://github.com/lhy1024) <!-- (dup): release-8.5.6.md > Improvements > PD --> <!-- pr: https://github.com/tikv/pd/pull/10090 -->
