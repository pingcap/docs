---
title: TiDB 8.5.6 Release Notes
summary: Learn about the features, compatibility changes, improvements, and bug fixes in TiDB 8.5.6.
---

# TiDB 8.5.6 Release Notes

Release date: April 14, 2026

TiDB version: 8.5.6

Quick access: [Quick start](https://docs.pingcap.com/tidb/v8.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v8.5/production-deployment-using-tiup)

## Features

### Performance

- Foreign key checks now support shared locks [#66154](https://github.com/pingcap/tidb/issues/66154) @[you06](https://github.com/you06)

    In pessimistic transactions, when you run `INSERT` or `UPDATE` on a child table with foreign key constraints, foreign key checks lock the corresponding parent table rows with exclusive locks by default. In high-concurrency write scenarios on the child table, if many transactions access the same parent table rows, severe lock contention can occur.

    Starting from v8.5.6, you can set the [`tidb_foreign_key_check_in_shared_lock`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_foreign_key_check_in_shared_lock-new-in-v856) system variable to `ON` to let foreign key checks use shared locks on the parent table, thereby reducing lock contention and improving concurrent write performance on the child table.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/foreign-key#locking).

### Stability

- The feature of setting the maximum limit on resource usage for background tasks of resource control becomes generally available (GA) [#56019](https://github.com/pingcap/tidb/issues/56019) @[glorv](https://github.com/glorv)

    TiDB resource control can identify and lower the priority of background tasks. In certain scenarios, you might want to limit the resource consumption of background tasks, even when resources are available. Starting from v8.4.0, you can use the `UTILIZATION_LIMIT` parameter to set the maximum percentage of resources that background tasks can consume. Each node will keep the resource usage of all background tasks below this percentage. This feature enables precise control over resource consumption for background tasks, further enhancing cluster stability.

    In v8.5.6, this feature is generally available (GA).

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/tidb-resource-control-background-tasks).

### Observability

- Support defining multi-dimensional, fine-grained trigger rules for slow query logs [#62959](https://github.com/pingcap/tidb/issues/62959), [#64010](https://github.com/pingcap/tidb/issues/64010) @[zimulala](https://github.com/zimulala)

    Before v8.5.6, the main way to identify slow queries in TiDB is to set the [`tidb_slow_log_threshold`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_slow_log_threshold) system variable. This mechanism provides only coarse-grained control over slow query log triggering because it applies globally at the instance level and does not support fine-grained control at the session or SQL level. In addition, it supports only one trigger condition, execution time (`Query_time`), which cannot meet the need to capture slow query logs more precisely in complex scenarios.

    Starting from v8.5.6, TiDB enhances slow query log control. You can use the [`tidb_slow_log_rules`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_slow_log_rules-new-in-v856) system variable to define multi-dimensional slow query log output rules at the instance, session, and SQL levels, based on conditions such as `Query_time`, `Digest`, `Mem_max`, and `KV_total`. You can use [`tidb_slow_log_max_per_sec`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_slow_log_max_per_sec-new-in-v856) to limit the number of log entries written per second, and use the [`WRITE_SLOW_LOG`](https://docs.pingcap.com/tidb/v8.5/optimizer-hints) hint to force slow query logging for specific SQL statements. This enables more flexible and fine-grained control over slow query logs.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/identify-slow-queries).

- The Top SQL page in TiDB Dashboard now supports collecting and displaying TiKV network traffic and logical I/O metrics [#62916](https://github.com/pingcap/tidb/issues/62916) @[yibin87](https://github.com/yibin87)

    In earlier versions, TiDB Dashboard identified Top SQL queries based only on CPU-related metrics, making it difficult to identify performance bottlenecks related to network or storage access in complex scenarios.

    Starting from v8.5.6, you can enable **TiKV Network IO collection (multi-dimensional)** in the Top SQL settings to view metrics such as `Network Bytes` and `Logical IO Bytes` for TiKV nodes. You can also analyze these metrics across multiple dimensions, including `By Query`, `By Table`, `By DB`, and `By Region`, helping you identify resource hotspots more comprehensively.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/top-sql).

### SQL

- Support column-level privilege management [#61706](https://github.com/pingcap/tidb/issues/61706) @[CbcWestwolf](https://github.com/CbcWestwolf) @[fzzf678](https://github.com/fzzf678)

    Before v8.5.6, TiDB privilege control covers the database and table levels and does not support granting or revoking privileges on specific columns, unlike MySQL. As a result, you cannot restrict users to access only a subset of sensitive columns in a table.

    Starting from v8.5.6, TiDB supports column-level privilege management. You can use the `GRANT` and `REVOKE` statements to manage privileges on specific columns. TiDB performs privilege checks based on column-level privileges during query processing and execution plan construction, enabling finer-grained access control and better support for sensitive data isolation and the principle of least privilege.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/column-privilege-management).

- Support using table aliases in the `FOR UPDATE OF` clause [#63035](https://github.com/pingcap/tidb/issues/63035) @[cryo-zd](https://github.com/cryo-zd)

    Before v8.5.6, when a `SELECT ... FOR UPDATE OF <table>` statement references a table alias in the locking clause, TiDB might fail to resolve the alias correctly and return the `table not exists` error even if the alias is valid.

    Starting from v8.5.6, TiDB supports using table aliases in the `FOR UPDATE OF` clause. TiDB can now correctly resolve locking targets from the `FROM` clause, including aliased tables, ensuring that row locks take effect as expected. This improves MySQL compatibility and makes `SELECT ... FOR UPDATE OF` statements more stable and reliable in queries that use table aliases.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/sql-statement-select).

### DB operations

- Support specifying the maximum number of nodes for Distributed eXecution Framework (DXF) tasks [#58944](https://github.com/pingcap/tidb/issues/58944) @[tangenta](https://github.com/tangenta) @[D3Hunter](https://github.com/D3Hunter)

    Before v8.5.6, TiDB does not provide a way to limit the number of nodes used by a distributed execution task. When you want to control resource usage for DXF, TiDB does not provide a dedicated option to constrain the maximum node count.

    Starting from v8.5.6, TiDB introduces the `tidb_max_dist_task_nodes` system variable to specify the maximum number of TiDB nodes used by a DXF task, enabling better resource control and workload-based tuning.

    For more information, see [documentation](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_max_dist_task_nodes-new-in-v856).

### Data Migration

- Migrate sync-diff-inspector from `pingcap/tidb-tools` to `pingcap/tiflow` repository [#11672](https://github.com/pingcap/tiflow/issues/11672) @[joechenrh](https://github.com/joechenrh)

## Compatibility changes

For TiDB clusters newly deployed in v8.5.5 (that is, not upgraded from versions earlier than v8.5.4), you can smoothly upgrade to v8.5.6. Most changes in v8.5.6 are safe for routine upgrades, but this release also includes several MySQL compatibility changes, system variable updates, configuration parameter updates, and deprecated features. Before upgrading, make sure to carefully review this section.

### MySQL compatibility

- Starting from v8.5.6, TiDB supports a MySQL-compatible column-level privilege management mechanism. You can grant or revoke `SELECT`, `INSERT`, `UPDATE`, and `REFERENCES` privileges for specific columns at the table level. For more information, see [Column-Level Privilege Management](https://docs.pingcap.com/tidb/v8.5/column-privilege-management).
- Starting from v8.5.6, TiDB supports using table aliases in the `FOR UPDATE OF` clause. To maintain backward compatibility, you can still reference the base table name when an alias is defined, but this triggers a warning recommending the use of an explicit alias. For more information, see [`SELECT`](https://docs.pingcap.com/tidb/v8.5/sql-statement-select).
- Starting from v8.5.6, Dumpling supports exporting data from MySQL 8.4 by adopting the updated MySQL binary log terminology. [#53082](https://github.com/pingcap/tidb/issues/53082) @[dveeden](https://github.com/dveeden)
- Starting from v8.5.6, TiDB Data Migration (DM) supports MySQL 8.4 as an upstream data source by adapting to the new terminology and version detection logic introduced in this version. [#11020](https://github.com/pingcap/tiflow/issues/11020) @[dveeden](https://github.com/dveeden)

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`tidb_analyze_version`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_analyze_version-new-in-v510) | Modified | Starting from v8.5.6, statistics Version 1 (`tidb_analyze_version = 1`) is deprecated and will be removed in a future release. It is recommended to use statistics Version 2 (`tidb_analyze_version = 2`). |
| [`tidb_ignore_inlist_plan_digest`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_ignore_inlist_plan_digest-new-in-v760) | Modified | Changes the default value from `OFF` to `ON`. The default value `ON` means that TiDB ignores the element differences (including the difference in the number of elements) in the `IN` list and uses `...` to replace elements in the `IN` list when generating Plan Digests. |
| [`tidb_service_scope`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_service_scope-new-in-v740) | Modified | Starting from v8.5.6, the value of this variable is case-insensitive. TiDB converts the input value to lowercase for storage and comparison. |
| [`InPacketBytes`](https://docs.pingcap.com/tidb/v8.5/system-variables#inpacketbytes-new-in-v856) | Newly added | This variable is used only for internal statistics and is not visible to users. |
| [`OutPacketBytes`](https://docs.pingcap.com/tidb/v8.5/system-variables#outpacketbytes-new-in-v856) | Newly added | This variable is used only for internal statistics and is not visible to users. |
| [`tidb_foreign_key_check_in_shared_lock`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_foreign_key_check_in_shared_lock-new-in-v856) | Newly added | Controls whether foreign key checks in pessimistic transactions use shared locks instead of exclusive locks on rows in the parent table. The default value is `OFF`, which means TiDB uses exclusive locks by default. |
| [`tidb_max_dist_task_nodes`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_max_dist_task_nodes-new-in-v856) | Newly added | Defines the maximum number of TiDB nodes that the Distributed eXecution Framework (DXF) tasks can use. The default value is `-1`, which indicates that automatic mode is enabled. In automatic mode, TiDB dynamically calculates the value as `min(3, tikv_nodes / 3)`, where `tikv_nodes` represents the number of TiKV nodes in the cluster. |
| [`tidb_opt_join_reorder_through_sel`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_join_reorder_through_sel-new-in-v856) | Newly added | Improves join reorder optimization for certain multi-table join queries. If you set it to `ON` and safety conditions are met, the optimizer evaluates `Selection` conditions between consecutive join operators together with join order candidates. During join tree reconstruction, the optimizer pushes these conditions down to more appropriate positions whenever possible, allowing more tables to participate in join order optimization. |
| [`tidb_opt_partial_ordered_index_for_topn`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_opt_partial_ordered_index_for_topn-new-in-v856) | Newly added | Controls whether the optimizer can leverage the partial ordering of an index to optimize TopN computation when a query contains `ORDER BY ... LIMIT`. The default value is `DISABLE`, which means the optimization is disabled. |
| [`tidb_slow_log_max_per_sec`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_slow_log_max_per_sec-new-in-v856) | Newly added | Controls the maximum number of slow query log entries that can be written per TiDB node per second. <ul><li>A value of `0` (the default) means there is no limit on the number of slow query log entries written per second.</li><li>A value greater than `0` means TiDB writes at most the specified number of slow query log entries per second. Any excess log entries are discarded and not written to the slow query log file.</li></ul> |
| [`tidb_slow_log_rules`](https://docs.pingcap.com/tidb/v8.5/system-variables#tidb_slow_log_rules-new-in-v856) | Newly added | Defines the triggering rules for slow query logs. It supports combining multi-dimensional metrics to provide more flexible and fine-grained logging. |

### Configuration parameters

| Configuration file or component | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiKV | [`gc.auto-compaction.mvcc-read-aware-enabled`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#mvcc-read-aware-enabled-new-in-v856) | Newly added | Controls whether to enable MVCC-read-aware compaction. The default value is `false`. |
| TiKV | [`gc.auto-compaction.mvcc-read-weight`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#mvcc-read-weight-new-in-v856) | Newly added | The weight multiplier applied to MVCC read activity when calculating the compaction priority score for a Region. The default value is `3.0`. |
| TiKV | [`gc.auto-compaction.mvcc-scan-threshold`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#mvcc-scan-threshold-new-in-v856) | Newly added | The minimum number of MVCC versions scanned per read request to mark a Region as a compaction candidate. The default value is `1000`. |
| TiKV | [`resource-metering.enable-network-io-collection`](https://docs.pingcap.com/tidb/v8.5/tikv-configuration-file#enable-network-io-collection-new-in-v856) | Newly added | Controls whether TiKV network traffic and logical I/O metrics are additionally collected in Top SQL. The default value is `false`. |
| TiCDC | [`sink.csv.output-field-header`](https://docs.pingcap.com/tidb/v8.5/ticdc-csv#use-csv) | Newly added | Controls whether a header row is output in CSV files. The default value is `false`. This parameter applies only to the TiCDC new architecture. |

### System table changes

| System table | Change type | Description |
| -------- | -------- | -------- |
| [`mysql.tidb`](https://docs.pingcap.com/tidb/v8.5/mysql-schema#cluster-status-system-tables) | Modified | Adds the `cluster_id` field, which represents the unique identifier of a TiDB cluster. Note that `cluster_id` is read-only and cannot be modified. |

## Deprecated features

- Starting from v8.5.6, statistics Version 1 (`tidb_analyze_version = 1`) is deprecated and will be removed in a future release. It is recommended that you use statistics Version 2 (`tidb_analyze_version = 2`) and [migrate existing objects that use statistics Version 1 to Version 2](https://docs.pingcap.com/tidb/v8.5/statistics#switch-between-statistics-versions) for more accurate statistics.
- Starting from v8.5.6, the TiDB Lightning Web Interface is deprecated and will be removed in v8.5.7. The web UI build has been broken since v8.4.0. Use the [CLI](/tidb-lightning/tidb-lightning-overview.md) or the [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) statement instead. If this affects your workflow, comment on [#67697](https://github.com/pingcap/tidb/issues/67697).

## Improvements

+ TiDB

    - Improve plan selection for queries with `IN` predicates on index prefix columns. TiDB can now use merge sort to preserve order for `ORDER BY ... LIMIT` queries, reducing unnecessary scans and improving performance. [#63449](https://github.com/pingcap/tidb/issues/63449) [#34882](https://github.com/pingcap/tidb/issues/34882) @[time-and-fate](https://github.com/time-and-fate)
    - Improve slow query log readability by outputting non-printable prepared statement arguments as hexadecimal values [#65383](https://github.com/pingcap/tidb/issues/65383) @[dveeden](https://github.com/dveeden)
    - Add `cluster_id` to `mysql.tidb`, enabling external tools to determine whether two TiDB instances belong to the same cluster [#59476](https://github.com/pingcap/tidb/issues/59476) @[YangKeao](https://github.com/YangKeao)

+ TiKV

    - Introduce a load-based compaction mechanism, which detects MVCC read overhead and prioritizes compaction for Regions with higher read cost to improve query performance [#19133](https://github.com/tikv/tikv/issues/19133) @[mittalrishabh](https://github.com/mittalrishabh)
    - Optimize the stale range cleanup logic during cluster scale-out and scale-in operations by deleting stale keys directly instead of cleaning them up through SST file ingestion, thereby reducing the impact on online request latency [#18042](https://github.com/tikv/tikv/issues/18042) @[LykxSassinator](https://github.com/LykxSassinator)
    - Support collecting TiKV network traffic and logical I/O metrics for Top SQL, which helps you diagnose SQL performance issues more accurately [#18815](https://github.com/tikv/tikv/issues/18815) @[yibin87](https://github.com/yibin87)

+ PD

    - Return `404` instead of `200` when deleting a non-existent label [#10089](https://github.com/tikv/pd/issues/10089) @[lhy1024](https://github.com/lhy1024)
    - Reduce unnecessary error logs [#9370](https://github.com/tikv/pd/issues/9370) @[bufferflies](https://github.com/bufferflies)

+ Tools

    + TiDB Data Migration (DM)

        - Add foreign key causal dependency support in DM syncer to ensure parent-to-child execution order of row changes in multi-worker scenarios [#12350](https://github.com/pingcap/tiflow/issues/12350) @[OliverS929](https://github.com/OliverS929)

## Bug fixes

+ TiDB

    - Fix the issue that upgrading from `release-8.5-20250606-v8.5.2` to the upstream `release-8.5` might skip the PITR metadata upgrade and cause PITR operations to fail [#66994](https://github.com/pingcap/tidb/issues/66994) @[fzzf678](https://github.com/fzzf678)
    - Fix the issue that after executing `EXCHANGE PARTITION`, non-unique global indexes or nullable unique global indexes on non-clustered partitioned tables might become inconsistent and return incomplete results [#65289](https://github.com/pingcap/tidb/issues/65289) @[mjonss](https://github.com/mjonss)
    - Fix the issue that `KILL QUERY` might incorrectly terminate idle connections [#65447](https://github.com/pingcap/tidb/issues/65447) @[gengliqi](https://github.com/gengliqi)
    - Fix the issue that the value of `tidb_service_scope` is not converted to lowercase when set [#66749](https://github.com/pingcap/tidb/issues/66749) @[D3Hunter](https://github.com/D3Hunter)
    - Fix the issue that affinity tables are not displayed after TiDB restarts [#66284](https://github.com/pingcap/tidb/issues/66284) @[lcwangchao](https://github.com/lcwangchao)
    - Fix the issue that the Stats Healthy metric displays inaccurately because system tables are not excluded from the stats cache [#64080](https://github.com/pingcap/tidb/issues/64080) @[0xPoe](https://github.com/0xPoe)
    - Fix the issue that statistics might not be updated due to abnormal updates of `modify_count` [#65426](https://github.com/pingcap/tidb/issues/65426) @[0xPoe](https://github.com/0xPoe)
    - Fix the issue that a pessimistic transaction might be unexpectedly rolled back due to a keep-alive mechanism failure when its first statement acquires locks in fair locking mode [#66571](https://github.com/pingcap/tidb/issues/66571) @[MyonKeminta](https://github.com/MyonKeminta)

+ TiKV

    - Fix the memory leak issue in crossbeam skiplist [#19285](https://github.com/tikv/tikv/issues/19285) @[ekexium](https://github.com/ekexium)
    - Fix the issue that global indexes on non-unique columns of partitioned tables might become inconsistent and return incorrect results in some cases [#19262](https://github.com/tikv/tikv/issues/19262) @[mjonss](https://github.com/mjonss)
    - Fix the issue that stalled coprocessor snapshot retrieval might occupy unified read pool workers until request deadlines expire, delaying other read requests [#18491](https://github.com/tikv/tikv/issues/18491) @[AndreMouche](https://github.com/AndreMouche)
    - Fix the issue that follower reads might remain blocked on disk-full TiKV nodes by rejecting read-index requests on disk-full followers [#19201](https://github.com/tikv/tikv/issues/19201) @[glorv](https://github.com/glorv)
    - Fix the issue that resolved-ts task backlogs might cause OOM when the resolved-ts worker is busy [#18359](https://github.com/tikv/tikv/issues/18359) @[overvenus](https://github.com/overvenus)
    - Fix the issue that long-tail follower read latency might occur during leader transfer by retrying read-index requests earlier and adding a dedicated retry interval setting [#18417](https://github.com/tikv/tikv/issues/18417) @[gengliqi](https://github.com/gengliqi)
    - Fix the rare data inconsistency issue when retrying a prewrite request in pessimistic transactions [#11187](https://github.com/tikv/tikv/issues/11187) @[wk989898](https://github.com/wk989898)

+ PD

    - Fix a panic issue that might occur when executing `DISTRIBUTE TABLE` in scenarios with a large number of Merge Region operators [#10293](https://github.com/tikv/pd/issues/10293) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that configuring Store Limit might not take effect immediately [#10108](https://github.com/tikv/pd/issues/10108) @[okJiang](https://github.com/okJiang)

+ TiFlash

    - Fix a potential data inconsistency issue between TiFlash and TiKV after executing a DDL statement to remove the `NOT NULL` constraint of a column [#10680](https://github.com/pingcap/tiflash/issues/10680) @[JaySon-Huang](https://github.com/JaySon-Huang)
    - Fix the issue that the Raft throughput metric in the Grafana dashboard might display an abnormally large value [#10701](https://github.com/pingcap/tiflash/issues/10701) @[CalvinNeo](https://github.com/CalvinNeo)
    - Fix the issue that the Join result might be incorrect when the Runtime Filter is enabled and the Join Keys have inconsistent data types [#10699](https://github.com/pingcap/tiflash/issues/10699) @[ChangRui-Ryan](https://github.com/ChangRui-Ryan)

+ Tools

    + Backup & Restore (BR)

        - Fix the issue that `flush_ts` might be `0` in log backup [#19406](https://github.com/tikv/tikv/issues/19406) @[YuJuncen](https://github.com/YuJuncen)
        - Fix the issue that BR might fail during multipart uploads when accessing Google Cloud Storage via Amazon S3-compatible APIs with S3-style credentials, due to a missing Content-Length header [#19352](https://github.com/tikv/tikv/issues/19352) @[Leavrth](https://github.com/Leavrth)
        - Fix the issue that the BR `restore point` might remain stuck in the `waiting for schema info finishes reloading` state for a long time and then fail due to timeout after 15 minutes [#66110](https://github.com/pingcap/tidb/issues/66110) @[kennytm](https://github.com/kennytm)
        - Fix the issue that BR cannot correctly pre-split Regions when restoring tables with the `SHARD_ROW_ID_BITS`, `PRE_SPLIT_REGIONS`, and `merge_option` attributes [#65060](https://github.com/pingcap/tidb/issues/65060) @[JoyC-dev](https://github.com/JoyC-dev)

    + TiCDC

        - Fix the issue that changefeeds might repeatedly create invalid dispatchers after the server restarts [#4452](https://github.com/pingcap/ticdc/issues/4452) @[wlwilliamx](https://github.com/wlwilliamx)
        - Fix the issue that TiCDC fails to replicate table renaming operations correctly when the upstream TiDB version is v8.1.x or earlier [#4392](https://github.com/pingcap/ticdc/issues/4392) @[lidezhu](https://github.com/lidezhu)
        - Fix the issue that TiKV might crash during data scanning when TiCDC is enabled [#19404](https://github.com/tikv/tikv/issues/19404) @[wk989898](https://github.com/wk989898)
        - Support Azure Managed Identity authentication for Azure Blob Storage and fix the issue that uploads to cloud storage might get stuck [#3093](https://github.com/pingcap/ticdc/issues/3093) @[wlwilliamx](https://github.com/wlwilliamx)

    + TiDB Data Migration (DM)

        - Fix the issue that DM does not advance the global checkpoint position after an upstream binlog file rotation [#12339](https://github.com/pingcap/tiflow/issues/12339) @[OliverS929](https://github.com/OliverS929)
        - Fix the issue that, when processing updates on tables with foreign key constraints in safe mode, DM might still incorrectly trigger foreign key cascades and cause unintended data deletion even if the primary key or unique key is not modified [#12350](https://github.com/pingcap/tiflow/issues/12350) @[OliverS929](https://github.com/OliverS929)
        - Fix the issue that DM validator incorrectly returns validation errors when processing `UNSIGNED` columns [#12178](https://github.com/pingcap/tiflow/issues/12178) @[OliverS929](https://github.com/OliverS929)
