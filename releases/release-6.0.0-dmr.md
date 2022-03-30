---
title: TiDB 6.0.0 Release Notes
---

# TiDB 6.0.0 Release Notes

Release date: x x, 2022

TiDB version: 6.0.0-DMR

In 6.0.0-DMR, the key new features or improvements are as follows:

* Support placement rules in SQL
* Add a check for data index consistency at the kernel level
* Enhance Raft Engine
* Accelerate leader balancing after restarting TiKV nodes
* Support canceling the automatic update of statistics
* Optimize the overhead of obtaining TSO at the Read Committed isolation level
* Enhance prepared statements to share execution plans
* Enhance function queries
* TiKV 过载资源保护增强（实验特性)
* Cache hotspot small tables
* 批量更新热点索引
* Optimize in-memory pessimistic locking
* TiEM 图形化管理界面
* Provide PingCAP Clinic, the automatic diagnosis tool for TiDB
* Top SQL becomes generally available (GA)
* HTAP capabilities improve by x times
* Strengthen disaster recovery

Also, as a core component of TiDB’s HTAP solution, TiFlash<sup>TM</sup> is officially open source in this release. For details, see [TiFlash repository](https://github.com/pingcap/tiflash).

## Release strategy changes

Starting from TiDB 6.0.0, TiDB provides two types of releases:

* Long-Term Support Releases

    Long-Term Support (LTS) releases are released approximately every six months. An LTS release introduces new features and improvements, and accepts patch releases within its release lifecycle. For example, v5.4.0 is an LTS release.

* Development Milestone Releases

    Development MileStone Releases (DMR) are released approximately every two months. A DMR introduces new features and improvements, but does not accept patch releases. It is not recommended for on-premises users to use DMR in production environments. For example, v6.0.0-DMR is a DMR.

TiDB 6.0.0 is a DMR, and its version is 6.0.0-DMR.

## Compatibility changes

> **Note:**
>
> When upgrading from an earlier TiDB version to v6.0.0, if you want to know the compatibility change notes of all intermediate versions, you can check the [Release Notes](/release/release-notes.md) of the corresponding version.

### System variables

| Variable name | Change type | Description |
|---|---|---|
| `tidb_enable_mutation_checker` | Newly added | Controls whether to enable the mutation checker. The default value is `ON`. |
| `tidb_ignore_prepared_cache_close_stmt` | Newly added | Controls whether to ignore the command that closes Prepared Statement. The default value is `OFF`. |
| `tidb_mem_quota_binding_cache` | Newly added | Set the memory usage threshold for the cache holding `binding`. The default value is `67108864` (64 MiB). |
| `tidb_placement_mode` | Newly added | Controls whether DDL statements ignore the placement rules specified by [Placement Rules in SQL](/placement-rules-in-sql.md). The default value is `strict`, which means that DDL statements do not ignore placement rules. |
| `tidb_rc_read_check_ts` | Newly added | - Optimizes read statement latency within a transaction. If read/write conflicts are more severe, turning this variable on will add additional overhead and latency, causing regressions in performance. The default value is `off`.<br/>- This variable is not yet compatible with [replica-read](#tidb_replica_read-new-in-v40). If a read request has `tidb_rc_read_check_ts` on, it might not be able to use replica-read. Do not turn on both variables at the same time. |
| `tidb_sysdate_is_now` | Newly added | Controls whether `SYSDATE` can be replaced by `NOW`. This configuration has the same effect as MySQL option [`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now). The default value is `OFF`. |
| `tidb_table_cache_lease` | Newly added | Controls the lease time of [table cache](/table-cache.md), in seconds. The default value is `3`. |
| `tidb_top_sql_max_meta_count` | Newly added | Controls the maximum number of SQL statement types that are collected by [Top SQL](/dashboard/top-sql.md) every minute. The default is `5000`. |
| `tidb_top_sql_max_time_series_count` | Newly added | Controls how many of the top SQL statements that consume the most resources are saved in [Top SQL](/dashboard/top-sql.md) every minute. The default is `100`. |
| `tidb_txn_assertion_level` | Newly added | Controls the assertion level. The assertion is a data index consistency check performed during the transaction commit process. By default, the check has only minor impact on performance and includes most of the check items.  |
| `placement_checks` | Deleted | Controls whether the DDL statement validates the placement rules specified by [Placement Rules in SQL](/placement-rules-in-sql.md). Replaced by `tidb_placement_mode`. |
| `tidb_enable_alter_placement` | Deleted | Controls whether to enable [placement rules in SQL](/placement-rules-in-sql.md). |
| `tidb_mem_quota_hashjoin`<br/>`tidb_mem_quota_indexlookupjoin`<br/>`tidb_mem_quota_indexlookupreader` <br/>`tidb_mem_quota_mergejoin`<br/>`tidb_mem_quota_sort`<br/>`tidb_mem_quota_topn` | Deleted | Since v5.0, these variables have been replaced by `tidb_mem_quota_query` and removed from the [system variables](/system-variables.md) document. To ensure compatibility, these variables were kept in source code. Since TiDB 6.0.0, these variables are removed from the code, too. |

## Configuration file parameters

| Configuration file | Configuration | Change type | Description |
|---|---|---|---|
| TiDB | `pessimistic-txn.pessimistic-auto-commi`t | Newly added | Determines the transaction mode that the auto-commit transaction uses when the pessimistic transaction mode is globally enabled (`tidb_txn_mode='pessimistic'`). |
| TiDB | `new_collations_enabled_on_first_bootstrap` | Modified | Controls whether to enable support for the new collation. Since v6.0, the default value is changed from `false` to `true`. This configuration item only takes effect when the cluster is initialized for the first time. After the first bootstrap, you cannot enable or disable the new collation framework using this configuration item. |
| TiDB | `stmt-summary.enable` <br/> `stmt-summary.enable-internal-query` <br/> `stmt-summary.history-size` <br/> `stmt-summary.max-sql-length` <br/> `stmt-summary.max-stmt-count` <br/> `stmt-summary.refresh-interval` <br/> `pessimistic-txn.in-memory` | Deleted | Configuration related to the [statement summary tables](/statement-summary-tables.md). All these configuration items are removed. You need to use SQL variables to control the statement summary tables. |
| TiKV |  | Newly added | Controls whether to enable the in-memory pessimistic lock. With this feature enabled, pessimistic transactions store pessimistic locks in TiKV memory as much as possible, instead of writing pessimistic locks to disks or replicating to other replicas. This improves the performance of pessimistic transactions; however, there is a low probability that a pessimistic lock will be lost, which might cause the pessimistic transaction to fail to commit. The default value is `true`. |
| TiKV | `quota` | Newly added | Add configuration items related to Quota Limiter, which limit the resources occupied by frontend requests. Quota Limiter is an experimental feature and is disabled by default. New configuration items are `foreground-cpu-time`, `foreground-write-bandwidth`, `foreground-read-bandwidth`, and `max-delay-duration`. |
| TiKV | `rocksdb.enable-pipelined-write` | Modified | Change the default value from `true` to `false`. When this configuration is enabled, the previous Pipelined Write is used. When this configuration is disabled, the new Pipelined Commit mechanism is used. |
| TiKV | `rocksdb.max-background-flushes` | Modified | - When the number of CPU cores is 10, the default value is `3`.<br/>- When the number of CPU cores is 8, the default value is `2`. |
| TiKV | `rocksdb.max-background-jobs` | Modified | + When the number of CPU cores is 10, the default value is `9`.<br/>+ When the number of CPU cores is 8, the default value is `7`. |
| TiKV | [`raft-engine.enable`](/tikv-configuration-file.md#raft-engine) | Modified | The default value is changed from `false` to `true`, which uses Raft Engine to store raft logs. When it is enabled, configurations of `raftdb` are ignored. |
| TiKV | `raftstore.apply-max-batch-size` | Modified | Chang the maximum value to `10240`. |
| TiKV | `backup.num-threads` | Modified | Modify the adjustable range to `[1, CPU]`.  |
| TiKV | `readpool.unified.max-thread-count` | Modified | Modify the adjustable range to `[min-thread-count, MAX(4, CPU)]`. |
| TiKV | `raft-max-size-per-msg` | Modified | - Change the minimum value from `0` to larger than `0`.<br/>- Add a maximum value of `3 GB`.<br/>- Change the unit from `MB` to `KB\|MB\|GB`. |
| TiKV | `store-max-batch-size` | Modified | Add a maximum value of `10240`. |
| TiKV | `enable-io-snoop` | Deleted | Remove the `enable-io-snoop` configuration item. |
| TiFlash | `profiles.default.dt_compression_method` | Newly added | Specifies the compression algorithm for TiFlash. The optional values are `LZ4`, `zstd` and `LZ4HC`, all case insensitive. The default value is `LZ4`. |
| TiFlash | `profiles.default.dt_compression_level` | Newly added | Specifies the compression level of TiFlash. The default value is `1`. |
| TiFlash | `profiles.default.dt_enable_logical_split` | Modified | Determines whether the segment of DeltaTree Storage Engine uses logical split. The default value is changed from `true` to `false`. |
| TiFlash | `profiles.default.enable_elastic_threadpool` | Modified | Controls whether to enable the elastic thread pool. The default value is changed from `false` to `true`. |
| TiFlash | `storage.format_version` | Modified | Controls the data validation feature of TiFlash. The default value is changed from `2` to `3`.<br/>When `format_version` is set to `3`, consistency check is performed on the read operations for all TiFlash data to avoid incorrect read due to hardware failure.<br/>Note that the new format version cannot be downgraded in place to versions earlier than v5.4. |
| DM | `loaders.<name>.import-mode` | Newly added | The import mode during the full import phase. Since v6.0, DM uses TiDB Lightning’s TiDB-backend mode to import data during the full import phase; the previous Loader component is no longer used. This is an internal replacement and has no obvious impact on daily operations.<br/>The default value is set to `sql`, which means using `tidb-backend` mode. In some rare cases, `tidb-backend` might not be fully compatible. You can fall back to Loader mode by configuring this parameter to `loader`. |
| DM | `loaders.<name>.on-duplicate` | Newly added | Specifies the methods to resolve conflicts during the full import phase. The default value is `replace`, which means using the new data to replace the existing data. |
| TiCDC | `read-timeout` | Newly added | The timeout in getting a response returned by the downstream Kafka. The default value is `10s`. |
| TiCDC | `write-timeout` | Newly added | The timeout in sending a request to the downstream Kafka. The default value is `10s`. |
| TiCDC | `dial-timeout` | Newly added | The timeout in establishing a connection with the downstream Kafka. The default value is `10s`. |

### Others

* The data placement policy has the following compatibility changes:
    * Binding is not supported. The direct placement option is removed from the syntax.
    * The `CREATE PLACEMENT POLICY` and `ALTER PLACEMENT POLICY` statements no longer support the `VOTERS` and `VOTER_CONSTRAINTS` placement options.
    * TiDB ecosystem tools (TiDB Binlog, TiCDC, and BR) are now compatible with placement rules. The placement option is moved to a special comment in TiDB Binlog.
    * The `information_schema.placement_rules` system table is renamed to `information_schema.placement_policies`. This table now only displays information about placement policies.
    * The `placement_checks` system variable is replaced by `tidb_placement_mode`.
    * It is prohibited to add partitions with placement rules to tables that have TiFlash replicas.
    * Remove the `TIDB_DIRECT_PLACEMENT` column from the `INFORMATION_SCHEMA` table.
* The `status` value of SQL plan management (SPM) binding is modified:
    * Remove `using`.
    * Add `enabled` (available) to replace `using`.
    * Add `disabled` (unavailable).
* DM modifies the OpenAPI interface
    * Because of internal mechanism changes, the interface related to task management cannot be compatible with the previous experimental version. You need to refer to the new [DM OpenAPI documentation](/dm/dm-open-api.md) for adaptation.
* DM changes the methods to resolve conflicts during the full import phase
    * A `loader.&lt;name>.on-duplicate` parameter is added. The default value is `replace`, which means using the new data to replace the existing data. If you want to keep the previous behavior, you can set the value to `error`. This parameter only controls the behavior during the full import phase.
* In v5.4 (v5.4 only), TiDB allows incorrect values for some noop system variables. Since v6.0.0, TiDB disallows setting incorrect values for system variables.

## New features

### SQL

* SQL-based placement rules for data

    TiDB is a distributed database with excellent scalability. Usually, data is deployed across multiple servers or even multiple data centers. Therefore, data scheduling management is one of the most important basic capabilities of TiDB. In most cases, customers do not need to care about how to schedule and manage data. However, with the increasing application complexity, deployment changes caused by isolation and access latency have become new challenges for TiDB. Since v6.0.0, TiDB officially provides data scheduling and management capabilities based on SQL interfaces. It supports flexible scheduling and management in dimensions such as replica counts, role types, and placement locations for any data. TiDB also supports more flexible management for data placement in multi-service shared clusters and cross-AZ deployments. 

    [user document](/placement-rules-in-sql.md)

* Support building TiFlash replicas by databases. To add TiFlash replicas for all tables in a database, you only need to use a single SQL statement, which greatly saves operation and maintenance costs. 

    [user document]()

### Transaction

* Add a check for data index consistency at the kernel level

    Add a check for data index consistency when a transaction is executed, which improves system stability and robustness, with only very low resource overhead. You can control the check behavior using the `tidb_enable_mutation_checker` and `tidb_txn_assertion_level` variables. With the default configuration, the QPS drop is controlled within 2% in most scenarios. For the error description of the consistency check, see [user document](/data-inconsistency-errors.md).

### Observability

* ​​General availability (GA) of Top SQL

    Top SQL is a self-service database performance monitoring and diagnosis feature provided in TiDB Dashboard for DBAs and app developers. With this feature, you can easily locate SQL queries that contribute to a high load of a TiDB or TiKV node in a specified time range. Unlike existing diagnostic features provided in TiDB Dashboard for database experts, Top SQL is designed for non-experts. You do not need to observe thousands of monitoring charts to find correlations or understand TiDB internal mechanisms such as Raft Snapshot, RocksDB, MVCC, and TSO. With basic database concepts such as index, lock conflict, and execution plans, you can use Top SQL to analyze database load quickly and improve application performance.

    Top SQL is disabled by default and can be enabled with a single click. When enabled, Top SQL provides you with the CPU load of each TiKV or TiFlash node within the last 30 days, so you can intuitively see which SQL statements cause high CPU loads and quickly analyze the issues such as database hotspots and sudden load increases.

    For example, you can use Top SQL to locate an analytic query that consumes 99% of the load for a low-load database.

    [User documentation](/dashboard/top-sql.md)

* General availability (GA) of Continuous Profiling

    TiDB Dashboard introduces the Continuous Profiling feature, providing the ability to automatically save instance performance analysis results as the cluster is running, improving the observability of TiDB cluster performance and helping to reduce troubleshooting time.
    
    With Continuous Profiling, you can collect continuous performance data of TiDB, TiKV, and PD instances, and view the profiling results in flame graphs.
    
    This feature is applicable to TiDB clusters deployed or upgraded using TiUP of v1.9.0 or later or TiDB Operator of v1.3.0 or later.
    
    This feature is not enabled by default. You can enable it in TiDB Dashboard.
    
    [User document](/dashboard/continuous-profiling.md)

### Performance

* Enhanced Raft Engine

    By default, [Raft Engine](https://github.com/tikv/raft-engine) is used as the storage engine for TiKV logs. Compared with RocksDB, Raft Engine can reduce TiKV I/O write traffic by up to 40% and CPU usage by 10%. At the same time, under certain loads, Raft Engine improves foreground throughput by about 5% and reduces long-tail latency by 20%.

    [User document](/tikv-configuration-file#raft-engine)，[issue 号]()

* Cache hotspot small tables

    For customer applications in scenarios where hotspot small tables are accessed, TiDB supports explicitly caching the hotspot tables in memory, which greatly improves the access performance, improves the throughput, and reduces access latency. This solution can effectively avoid introducing a third-party cache middleware, reduce the complexity of the architecture, and cut the cost of operation and maintenance management. The solution is suitable for scenarios where small tables are frequently accessed and rarely updated, such as the configuration tables or exchange rate tables.

    [User document]()，[issue 号]()

* In-memory pessimistic locking

    Since TiDB v6.0.0, in-memory pessimistic locking is enabled by default. After enabling this feature, pessimistic transaction locks are managed in memory. This avoids persisting pessimistic locks and the Raft replication of the lock information, and greatly reduces the overhead of managing pessimistic transaction locks. Under the performance bottleneck caused by pessimistic locks, memory optimization for pessimistic locks can effectively reduce latency by 10% and increase QPS by 10%.

    [User document]()，[issue 号]()

* Optimization to get TSO at the Read Committed isolation level

    To reduce query latency, when read-write conflicts are rare, TiDB adds the `tidb_rc_read_check_ts` system variable at the [Read Committed isolation level](/transaction-isolation-levels.md#read-committed-isolation-level) to get less unnecessary TSO. This variable is disabled by default. When the variable is enabled, this optimization can almost help avoid getting duplicated TSO to reduce latency in scenarios with no read-write conflict. However, in scenarios with frequent read-write conflicts, enabling this variable might cause a performance regression. Do not use it before checking.

    [User docs]()，[issue 号]()

* Enhance prepared statements to share execution plans

    Reusing SQL execution plans can effectively reduce the time for parsing SQL statements, lessen CPU resource consumption, and improve SQL execution efficiency. One of the important methods of SQL tuning is to reuse SQL execution plans effectively. TiDB has supported sharing execution plans with prepared statements. However, when the prepared statements are closed, TiDB automatically clears the corresponding plan cache. After that, TiDB might unnecessarily parse the repeated SQL statements, affecting the execution efficiency. Since v6.0, TiDB supports controlling whether to ignore the `COM_STMT_CLOSE` directive through the `tidb_ignore_clost_stmt_cmd` parameter (disabled by default). When the parameter is enabled, TiDB ignores the directive of closing prepared statements and keeps the execution plan in the cache, improving the reuse rate of the execution plan.

    [User doc]()，[issue]()

* Enhanced function queries

    With its native architecture of separating computing from storage, TiDB supports filtering out invalid data by pushing down operators, which greatly reduces the data transmission between TiDB and TiKV and thereby improves the query efficiency. In v6.0, TiDB supports pushing down more expressions and the `BIT` data type to TiKV, improving the query efficiency when computing those expressions and data types.

    [User document](/functions-and-operators/expressions-pushed-down.md#add-to-the-blocklist), [#12037](https://github.com/tikv/tikv/pull/12037)

* Support the dynamic pruning mode for partitioned tables in TiFlash MPP engine (experimental feature)

    In this mode, TiDB can read and compute the data on partitioned tables using the MPP engine of TiFlash, which greatly improves the query performance of partitioned tables.

    [User docs]()，[issue 号]()

* Improve the computing performance of the MPP engine

    - Support pushing down more functions and operators to the MPP engine

        - Logical functions: `IS`, `IS NOT`
        - String functions: `REGEXP()`, `NOT REGEXP()`
        - Mathmatical functions: `GREATEST(int/real)`, `LEAST(int/real)`
        - Date functions: `DAYOFNAME()`, `DAYOFMONTH()`, `DAYOFWEEK()`, `DAYOFYEAR()`, `LAST_DAY()`, `MONTHNAME()`
        - Operators: Anti Left Outer Semi Join, Left Outer Semi Join

    - Introduce the dynamic thread pool (enabled by default) to improve the CPU utilization

    [User docs]()，[issue 号]()

### Stability

* Enhance baseline capturing of execution plans

    Enhance the usability of baseline capturing of execution plans by adding a blocklist with such dimensions as table name, frequency, and user name. Introduce a new algorithm to optimize memory management for caching bindings. After baseline capturing is enabled, the system automatically creates bindings for most OLTP queries. Execution plans of bound statements are fixed, avoiding performance problems due to any change in the execution plans. Baseline capturing is applicable to scenarios such as major version upgrades and cluster migration, and helps reduce performance problems caused by rollback of execution plans.

    [User document](/sql-plan-management.md)

* Quota Limiter (experimental)

    If your machine deployed with TiKV has limited resources and the foreground is burdened by an excessively large amount of requests, background CPU resources are occupied by the foreground, causing TiKV performance to degrade. In TiDB v6.0, you can use the quota-related configuration items to limit the resources used by the foreground, including CPU and read/write bandwidth. This greatly improves stability of clusters under long-term heavy workloads.

    [User document](/tikv-configuration-file.md#quota)

* Support the zstd compression algorithm

    TiFlash introduces two parameters, profiles.default.dt_compression_method and profiles.default.dt_compression_level, which allows users to select the optimal compression algorithm based on performance and capacity balance.

    [User document](/tiflash-configuration.md#configure-the-tiflashtoml-file)

* Enable all I/O checks (Checksum) by default

    This feature was introduced in v5.4.0 as experimental. It enhances data accuracy and security without imposing an obvious impact on users’ businesses.

    Warning: Newer version of data format cannot be downgraded in place to versions earlier than v5.4.0. During such a downgrade, you need to delete TiFlash replicas and replicate data after the downgrade. Alternatively, you can perform a downgrade by referring to [dttool migrate](/tiflash-command-line-flags.md#dttool-migrate).

    [User document](/use-tiflash.md#use-data-validation)

* Improve thread utilization

    TiFlash introduces asynchronous GRPC and Min-TSO scheduling mechanisms. Such mechanisms ensure more efficient use of threads and avoids system crashes caused by excessive threads.

    [User document](/monitor-tiflash.md#coprocessor)

### TiDB Data Migration (DM)

* Add WebUI (experimental)

    On the newly introduced WebUI, you can easily manage a large number of migration tasks. The WebUI supports:

    * Dashboard
    * Migration task management
    * Upstream configuration
    * Replication status query
    * Master and Worker management

    WebUI is still experimental and needs improvement. Therefore, it is recommended only for trial. A known issue is that problems might occur if you use WebUI and dmctl  to operate the same task. This issue will be resolved in later versions.

    [User document](/dm/dm-webui-guide.md)

* Add an error handling mechanism

    More commands are introduced to address problems that interrupt a migration task. For example:

* In case of a schema error, you can update the schema file by using the `--from-source/--from-target` parameter of the binlog-schema update, instead of editing the schema file separately.
* You can specify a binlog position to inject, replace, skip, or revert a DDL statement.

    [User document](/dm/dm-manage-schema.md)

* Support full data storage to Amazon S3

    When DM performs all or full data migration tasks, sufficient hard disk space is required for storing full data from upstream. Compared with EBS, Amazon S3 has nearly infinite storage at lower costs. Now, DM supports configuring Amazon S3 as the dump directory. That means you can use S3 to store full data when you perform all or full data migration tasks.

    [User document](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)

* Support starting a migration task from specified time

    A new parameter `--start-time` is added to migration tasks. You can define time in the format of '2021-10-21 00:01:00' or '2021-10-21T00:01:00'.

    This feature is particularly useful in scenarios where you migrate and merge incremental data from shard mysql instances. Specifically, you do not need to set a binlog start point for each incremental migration task. Instead, you can complete an incremental migration task faster by using the `--start-time` parameter in `safe-mode`.

    [User document](/dm/dm-create-task.md#flags-description)

### TiDB Lightning

* Maximum tolerable error

    Added a configuration item `max-error`. The default value is 0. When the value is greater than 0, the max-error function is enabled. If an error occurs in a row during encoding, a record containing this row is added to `type_error_v1` and this row is ignored. When rows with errors exceed the threshold, TiDB Lightning exits immediately.

    Matching the `max-error` configuration, the `lightning_task_info` configuration item records the name of the database that reports a data saving error.

    This feature does not cover all types of errors, for example, syntax errors are not applicable.

    [User document](/tidb-lightning/tidb-lightning-error-resolution.md#type-error)

### Data sharing and subscription

* Support replicating 100K tables simultaneously

    By optimizing the data processing flow, TiCDC reduces the resource consumption of processing incremental data for each table, which greatly improves the replication stability and efficiency when replicating data in large clusters. The result of an internal test shows that TiCDC can stably support replicating 100,000 tables simultaneously.

    [User document]()

### Deployment and maintenance

* Enable new collation rules by default

    TiDB has supported new collation rules since v4.0, which behave the same as MySQL in the case-insensitive, accent-insensitive, and padding rules. The new collation rules are controlled by the `new_collations_enabled_on_first_bootstrap` parameter, which was disabled by default. Since v6.0, TiDB enables new collation rules by default. Note that this configuration takes effect only for the TiDB clusters first initialized.

    [User documentation](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)

* ​​Accelerate leader balancing after restarting TiKV nodes

    After a restart, TiKV nodes need to redistribute the unevenly scattered leaders for load balance. In large-scale clusters, leader balancing time is positively correlated with the number of Regions. For example, the leader balancing of 100K Regions can take 20-30 minutes, which is prone to performance issues and stability risks due to uneven load. TiDB 6.0 provides a parameter to control the balancing concurrency and adjusts the default value to 4 times of the original, which greatly shortens the leader rebalancing time and accelerates the business recovery after a restart of TiKV nodes.

    [User documentation](/pd-control.md#scheduler-show--add--remove--pause--resume--config)

* Support canceling the automatic update of statistics

    Statistics are one of the most important basic data that affects SQL performance. To ensure the completeness and timeliness of statistics, TiDB updates statistics periodically. Since v6.0, you can cancel the automatic update of statistics manually, which avoids any SQL performance impact caused by resource contention of the automatic update task.

    [user documentation](/statistics.md#automatic-update)

## Improvements

* TiDB

    * Clear the placement rule information of a table automatically after restoring the table using the `FLASHBACK` or `RECOVER` statement  [#31668](https://github.com/pingcap/tidb/issues/31668)
    * Add a performance overview monitoring dashboard to show core performance metrics on typical critical paths, making metrics analysis on TiDB easier  [#31676](https://github.com/pingcap/tidb/issues/31676)
    * Support using the `REPLACE` keyword in the `LOAD DATA LOCAL INFILE` statement [#24515](https://github.com/pingcap/tidb/issues/24515)
    * (dup: release-5.1.4.md > Improvements> TiDB)- Support partition pruning for the built-in `IN` expression in Range partition tables [#26739](https://github.com/pingcap/tidb/issues/26739)
    * Improve query efficiency by eliminating potentially redundant Exchange operations in MPP aggregation queries  [#31762](https://github.com/pingcap/tidb/issues/31762)
    * Improve compatibility with MySQL by allowing duplicate partition names in the `TRUNCATE PARTITION` and `DROP PARTITION` statements [#31681](https://github.com/pingcap/tidb/issues/31681)
    * Support showing the `CREATE_TIME` information in the results of the `ADMIN SHOW DDL JOBS` statement [#23494](https://github.com/pingcap/tidb/issues/23494)
    * Support a new built-in function `CHARSET()` [#3931](https://github.com/pingcap/tidb/issues/3931)
    * Support filtering the automatically captured blacklist by usernames [#32558](https://github.com/pingcap/tidb/issues/32558)
    * Optimize the results of `ADMIN SHOW DDL JOBS` and `SHOW TABLE STATUS` statement by displaying the time according to the current `time_zone` [#26642](​​https://github.com/pingcap/tidb/issues/26642)
    * Supports pushing down the `DAYNAME()` and `MONTHNAME()` functions to TiFlash [#32594](https://github.com/pingcap/tidb/issues/32594)
    * Support pushing down the `REGEXP` function to TiFlash [#32637](https://github.com/pingcap/tidb/issues/32637)
    * Support tracking the execution of the `UnionScan` operator [#32631](https://github.com/pingcap/tidb/issues/32631)
    * Support pushing down the `GREATEST` and `LEAST` functions to TiFlash [#32787](https://github.com/pingcap/tidb/issues/32787)
    * Support using the PointGet plan for queries that read the `_tidb_rowid` column [#31543](https://github.com/pingcap/tidb/issues/31543)
    * Support using wildcards in the automatically captured blacklist [#32714](https://github.com/pingcap/tidb/issues/32714)
    * Support showing the original partition name in the output of the `EXPLAIN` statement without converting the name to lowercase [#32719](https://github.com/pingcap/tidb/issues/32719)
    * Enable partition pruning for RANGE COLUMNS partitionings on IN conditions and string type columns [#32626](https://github.com/pingcap/tidb/issues/32626)
    * Return an error message when you set a system variable to NULL [#32850](https://github.com/pingcap/tidb/issues/32850)
    * Remove Broadcast Join from the non-MPP mode [#31465](https://github.com/pingcap/tidb/issues/31465)
    * Support pushing down the ` DAYOFMONTH()` and ` LAST_DAY()` functions to TiFlash [#33012](https://github.com/pingcap/tidb/issues/33012)
    * Support pushing down the `DAYOFWEEK()` and `DAYOFYEAR()` functions to TiFlash [#33130](https://github.com/pingcap/tidb/issues/33130)
    * Support pushing down the `IS_TRUE`, `IS_FALSE`, and `IS_TRUE_WITH_NULL` functions to TiFlash [#33047](https://github.com/pingcap/tidb/issues/33047)
    * Support executing MPP plans on partitioned tables in dynamic pruning mode [#32347](https://github.com/pingcap/tidb/issues/32347)
    * 支持 read-consistency 读取可在 `READ-COMMITTED` 隔离级别下打开优化事务内读语句延迟  Support enabling the switch to reduce read latency in transaction at the `READ-COMMITTED` isolation level for the read-consistency read [#33159](https://github.com/pingcap/tidb/issues/33159)
    * Support pushing down predicates for common table expressions (CTEs) [#28163](https://github.com/pingcap/tidb/issues/28163)
    * Simplify the configurations of `Statement Summary` and `Capture Plan Baselines` to be available on a global basis only [#30557](https://github.com/pingcap/tidb/issues/30557)
    * Update gopsutil to v3.21.12 to address alarms reported when building binary on macOS 12 [#31607](https://github.com/pingcap/tidb/issues/31607)

* TiKV

    * (dup: release-5.4.0.md > Improvements> TiKV)- Support archiving and rotating logs [#11651](https://github.com/tikv/tikv/issues/11651)
    * Improve the Raftstore sampling accuracy for large key range batches [#11039](https://github.com/tikv/tikv/pull/11039)
    * Add the correct "Content-Type" for `debug/pprof/profile` to make the Profile more easily identified [#11521](https://github.com/tikv/tikv/issues/11521)
    * Renew the lease time of the leader infinitely when the Raftstore has heartbeats or handles read requests, which helps reduce latency jitter [#11579](https://github.com/tikv/tikv/pull/11579)
    * Choose the store with the least cost when switching the leader, which helps improve performance stability [#10602](https://github.com/tikv/tikv/issues/10602)
    * Fetch Raft logs asynchronously to reduce the performance jitter caused by blocking the Raftstore [#11320](https://github.com/tikv/tikv/issues/11320)
    * Support the `QUARTER` function in vector calculation [#5751](https://github.com/tikv/tikv/issues/5751)
    * Support pushing down the `BIT` data type to TiKV [#12037](https://github.com/tikv/tikv/pull/12037)
    * Support pushing down the `MOD` function and the `SYSDATE` function to TiKV [#11916](https://github.com/tikv/tikv/issues/11916)
    * (dup: release-5.3.1.md > Improvements> TiKV)- Reduce the TiCDC recovery time by reducing the number of the Regions that require the Resolve Locks step [#11993](https://github.com/tikv/tikv/issues/11993)
    * Support dynamically modifying `raftstore.raft-max-inflight-msgs` [#11865](https://github.com/tikv/tikv/issues/11865)
    * Support `EXTRA_PHYSICAL_TABLE_ID_COL_ID` to enable dynamic pruning mode [#11888](https://github.com/tikv/tikv/issues/11888)
    * Support calculation in buckets [#11759](https://github.com/tikv/tikv/issues/11759)
    * Encode the keys of RawKV API V2 as `user-key` + `memcomparable-padding` + `timestamp` [#11965](https://github.com/tikv/tikv/issues/11965)
    * Encode the values of RawKV API V2 as `user-value` + `ttl` + `ValueMeta` and encode `delete` in `ValueMeta` [#11965](https://github.com/tikv/tikv/issues/11965)
    * TiKV Coprocessor supports the Projection operator [#12114](https://github.com/tikv/tikv/issues/12114)
    * Support dynamically modifying `raftstore.raft-max-size-per-msg` [#12017](https://github.com/tikv/tikv/issues/12017)
    * Support monitoring multi-k8s in Grafana [#12014](https://github.com/tikv/tikv/issues/12014)
    * Transfer the leadership to CDC observer to reduce latency jitter [#12111](https://github.com/tikv/tikv/issues/12111)
    * Support dynamically modifying `raftstore.apply_max_batch_size` and `raftstore.store_max_batch_size` [#11982](https://github.com/tikv/tikv/issues/11982)
    * RawKV V2 returns the latest version upon receiving the `raw_get` or `raw_scan` request [#11965](https://github.com/tikv/tikv/issues/11965)
    * Support the RCCheckTS consistency reads [#12097](https://github.com/tikv/tikv/issues/12097)
    * Support dynamically modifying  `storage.scheduler-worker-pool-size`(the thread count of the Scheduler pool) [#12067](https://github.com/tikv/tikv/issues/12067)
    * Control the use of CPU and bandwidth by using the global foreground flow controller to improve the performance stability of TiKV [#11855](https://github.com/tikv/tikv/issues/11855)
    * Support dynamically modifying `readpool.unified.max-thread-count` (the thread count of the UnifyReadPool)  [#11781](https://github.com/tikv/tikv/issues/11781)
    * Use the TiKV internal pipeline to replace the RocksDB pipeline and deprecate the `rocksdb.enable-multibatch-write` parameter [#12059](https://github.com/tikv/tikv/issues/12059)

* PD

    * Support automatically selecting the fastest object for transfer when evicting the leader, which helps speed up the eviction process  [#4229](https://github.com/tikv/pd/issues/4229)
    * Forbid deleting a voter from a 2-replica Raft group in case that the Region becomes unavailable [#4564](https://github.com/tikv/pd/issues/4564)
    * Speed up the scheduling of the balance leader [#4652](https://github.com/tikv/pd/issues/4652)

* TiFlash

    * Forbid the logical splitting of TiFlash files (by adjusting the default value of `profiles.default.dt_enable_logical_split` to `false`. See [user document](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters) for details) and improve the space usage efficiency of the TiFlash columnar storage so that the space occupation of a table synchronized to TiFlash is similar to the space occupation of the table in TiKV.
    * Optimize the cluster management and replica replication mechanism for TiFlash by integrating the previous cluster management module into TiDB, which accelerates replica creation for small tables. [#29924](https://github.com/pingcap/tidb/issues/29924)

* Tools

    * Backup & Restore (BR)

        * Improve the speed of restoring the backup data. In the simulation test when BR restores 16 TB data to a TiKV cluster with 15 nodes (each node has 16 CPU cores), the throughput reaches 2.66 GiB/s. [#27036](https://github.com/pingcap/tidb/issues/27036)

        * Support importing and exporting placement rules. Add a `--with-tidb-placement-mode` parameter to control whether to ignore the placement rules when importing data. [#32290](https://github.com/pingcap/tidb/issues/32290)

    * TiCDC

        * Add a `Lag analyze` panel in Grafana [#4891](https://github.com/pingcap/tiflow/issues/4891)
        * Support placement rules [#4846](https://github.com/pingcap/tiflow/issues/4846)
        * Synchronize HTTP API handling [#1710](https://github.com/pingcap/tiflow/issues/1710)
        * (dup) Add the exponential backoff mechanism for restarting a changefeed [#3329](https://github.com/pingcap/tiflow/issues/3329)
        * Set the default isolation level of MySQL sink to read-committed to reduce deadlocks in MySQL [#3589](https://github.com/pingcap/tiflow/issues/3589)
        * Validate changefeed parameters upon creation and refine error messages [#1716](https://github.com/pingcap/tiflow/issues/1716) [#1718](https://github.com/pingcap/tiflow/issues/1718) [#1719](https://github.com/pingcap/tiflow/issues/1719) [#4472](https://github.com/pingcap/tiflow/issues/4472)
        * (dup) Expose configuration parameters of the Kafka producer to make them configurable in TiCDC [#4385](https://github.com/pingcap/tiflow/issues/4385)

    * TiDB Data Migration (DM)

        * Support starting a task when upstream table schemas are inconsistent and in optimistic mode [#3903](https://github.com/pingcap/tiflow/pull/3903)
        * Support creating a task in the `stopped` state [#4510](https://github.com/pingcap/tiflow/pull/4510)
        * Support Syncer using the working directory of the DM-worker rather than `/tmp` to write internal files, and cleaning the directory after the task is stopped [#4732](https://github.com/pingcap/tiflow/pull/4732)
        * Precheck has improved. Some important checks are no longer skipped. [#3608](https://github.com/pingcap/tiflow/issues/3608)

    * TiDB Lightning

        * Add more retryable error types [#31484](https://github.com/pingcap/tidb/pull/31484)
        * Tolerate TiKV node address changes during importing [#32876](https://github.com/pingcap/tidb/pull/32876)
        * Support the base64 format password string [#31194](https://github.com/pingcap/tidb/issues/31194)
        * Standardize error codes and error outputs [#32239](https://github.com/pingcap/tidb/issues/32239)

## Bug Fixes

* TiDB

    * Fix the bug that the placement rule reports an error when `SCHEDULE = majority_in_primary`, and `PrimaryRegion` and `Regions` are of the same value [#31271](https://github.com/pingcap/tidb/issues/31271)
    * (dup: release-5.3.1.md > Bug fixes> TiDB)- Fix the `invalid transaction` error when executing a query using index lookup join [#30468](https://github.com/pingcap/tidb/issues/30468)
    * Fix the bug that `show grants` returns incorrect results when two or more privileges are granted [#30855](https://github.com/pingcap/tidb/issues/30855)
    * Fix the bug that `INSERT INTO t1 SET timestamp_col = DEFAULT` would set the timestamp to the zero timestamp for the field defaulted to CURRENT_TIMESTAMP [#29966](https://github.com/pingcap/tidb/pull/29966))
    * ​Fix errors reported in reading the results by avoiding encoding the maximum value and minimum non-null value of the string type [#31721](https://github.com/pingcap/tidb/issues/31721)
    * Fix load data panic if the data is broken at an escape character [#31589](https://github.com/pingcap/tidb/issues/31589)
    * (dup: release-5.3.1.md > Bug fixes> TiDB)- Fix the issue that the `greatest` or `least` function with collation gets a wrong result [#31789](https://github.com/pingcap/tidb/issues/31789)
    * Fix the bug that the date_add and date_sub functions may return incorrect data types [#31809](https://github.com/pingcap/tidb/issues/31809)
    * Fix possible panic when inserting data to virtually generated columns using an insert statement [#31735](https://github.com/pingcap/tidb/issues/31735)
    * Fix the bug that no error is reported when duplicate columns are present in the created list partition [#31784](https://github.com/pingcap/tidb/issues/31784)
    * Fix wrong results returned when `select for update union select` uses incorrect snapshots [#31530](https://github.com/pingcap/tidb/issues/31530)
    * (dup: release-5.3.1.md > Bug fixes> Tools> Backup & Restore (BR))- Fix the potential issue that Regions might be unevenly distributed after a restore operation is finished [#31034](https://github.com/pingcap/tidb/issues/31034)
    * Fix the bug that COERCIBILITY is wrong for the `json` type [#31541](https://github.com/pingcap/tidb/issues/31541)
    * Fix wrong collation of the `json` type when this type is processed using builtin-func [#31320](https://github.com/pingcap/tidb/issues/31320)
    * Fix the bug that PD rules are not deleted when the count of TiFlash replicas is set to 0 [#32190](https://github.com/pingcap/tidb/issues/32190)
    * (dup: release-5.3.1.md > Bug fixes> TiDB)- Fix the issue that `alter column set default` wrongly updates the table schema [#31074](https://github.com/pingcap/tidb/issues/31074)
    * (dup: release-5.3.1.md > Bug fixes> TiDB)- Fix the issue that `date_format` in TiDB handles in a MySQL-incompatible way [#32232](https://github.com/pingcap/tidb/issues/32232)
    * Fix the bug that errors may occur when updating partitioned tables using join [#31629](https://github.com/pingcap/tidb/issues/31629)
    * Fix wrong range calculation for Nulleq function on Enum values [#32428](https://github.com/pingcap/tidb/issues/32428)
    * Fix possible panic in `upper()` and `lower()` functions [#32488](https://github.com/pingcap/tidb/issues/32488)
    * Fix time zone problems encountered when changing the other type columns to timestamp type columns [#29585](https://github.com/pingcap/tidb/issues/29585)
    * Fix TiDB OOM when exporting data using ChunkRPC [#31981](https://github.com/pingcap/tidb/issues/31981) [#30880](https://github.com/pingcap/tidb/issues/30880)
    * Fix the bug that sub SELECT LIMIT does not work as expected in dynamic partition pruning mode [#32516](https://github.com/pingcap/tidb/issues/32516)
    * Fix wrong or inconsistent format of bit default value on INFORMATION_SCHEMA.COLUMNS [#32655](https://github.com/pingcap/tidb/issues/32655)
    * Fix the bug that partition table pruning might not work for listing partition tables after server restart [#32416](https://github.com/pingcap/tidb/issues/32416)
    * Fix the bug that  `add column` may use wrong default timestamp after executing `SET timestamp` [#31968](https://github.com/pingcap/tidb/issues/31968)
    * Fix the bug that connecting to a TiDB passwordless account from MySQL 5.5 or 5.6 client may fail [#32334](https://github.com/pingcap/tidb/issues/32334)
    * Fix wrong results when reading partitioned tables in dynamic mode in transactions [#29851](https://github.com/pingcap/tidb/issues/29851)
    * Fix the bug that TiDB may dispatch duplicate tasks to TiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)
    * Fix wrong results returned when the `timdiff` function contains a millisecond [#31680](https://github.com/pingcap/tidb/issues/31680)
    * Fix wrong results when explicitly reading partitions and using the IndexJoin plan [#32007](https://github.com/pingcap/tidb/issues/32007)
    * Fix the bug that "rename column" fails when changing column type concurrently [#31075](https://github.com/pingcap/tidb/issues/31075)
    * Fix the bug that the formula for calculating net cost for TiFlash plans is not aligned with TiKV plans [#30103](https://github.com/pingcap/tidb/issues/30103)
    * Fix the bug that `KILL TIDB` cannot take effect immediately on idle links [#24031](https://github.com/pingcap/tidb/issues/24031)
    * Fix the bug that reading from a table with generated columns  may get wrong results [#33038](https://github.com/pingcap/tidb/issues/33038)
    * Fix wrong results of deleting data of multiple tables using `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)
    * Fix the bug that the `SUBTIME` function returns a wrong result in case of overflow [#31868](https://github.com/pingcap/tidb/issues/31868)
    * Fix the bug that the selection operator can not be pushed down when an  aggregation contains the having condition [#33166](https://github.com/pingcap/tidb/issues/33166)
    * Fix the bug that CTE may be blocked when a query reports errors [#31302](https://github.com/pingcap/tidb/issues/31302)
    * Fix the bug that excessive length of varbinary or varchar columns when creating tables in non-strict mode may result in errors [#30328](https://github.com/pingcap/tidb/issues/30328)
    * Fix the wrong number of followers in `information_schema.placement_policies`when no follower is specified [#31702](https://github.com/pingcap/tidb/issues/31702)
    * Fix the issue that TiDB allows to specify column prefix length as 0 when an index is created [#31972](https://github.com/pingcap/tidb/issues/31972)
    * Fix the issue that TiDB allows partition names ending with spaces [#31535](https://github.com/pingcap/tidb/issues/31535)
    * Fix the wrong message of the `RENAME TABLE` statement [#29893](https://github.com/pingcap/tidb/issues/29893)

* TiKV

    * (dup: release-5.3.1.md > Bug fixes> TiKV)- Fix the panic issue caused by deleting snapshot files when the peer status is `Applying` [#11746](https://github.com/tikv/tikv/issues/11746)修复 Peer 状态为 Applying 时快照文件被删除会造成 Panic 的问题 [#11746](https://github.com/tikv/tikv/issues/11746)
    * (dup: release-5.3.1.md > Bug fixes> TiKV)- Fix the issue of QPS drop when flow control is enabled and `level0_slowdown_trigger` is set explicitly [#11424](https://github.com/tikv/tikv/issues/11424)修复开启流量控制且显式设置 level0_slowdown_trigger 时出现 QPS 下降的问题 [#11424](https://github.com/tikv/tikv/issues/11424)
    * (dup: release-5.3.1.md > Bug fixes> TiKV)- Fix the issue that destroying a peer might cause high latency [#10210](https://github.com/tikv/tikv/issues/10210)修复删除 Peer 可能造成高延迟的问题 [#10210](https://github.com/tikv/tikv/issues/10210)
    * (dup: release-5.3.1.md > Bug fixes> TiKV)- Fix a bug that TiKV cannot delete a range of data (`unsafe_destroy_range` cannot be executed) when the GC worker is busy [#11903](https://github.com/tikv/tikv/issues/11903)
    * Fix a bug that TiKV panics when the data in `StoreMeta` is accidentally deleted in some corner cases [#11852](https://github.com/tikv/tikv/issues/11852)
    * Fix a bug that TiKV panics when performing profiling on ARM platform [#10658](https://github.com/tikv/tikv/issues/10658)
    * Fix a bug that TiKV might panic when running 2 years or more [#11940](https://github.com/tikv/tikv/issues/11940)
    * Fix the compilation issue on the ARM64 architecture caused by missing SSE instruction set [#12034](https://github.com/tikv/tikv/issues/12034)
    * (dup: release-5.3.1.md > Bug fixes> TiKV)- Fix the issue that deleting an uninitialized replica might cause an old replica to be recreated [#10533](https://github.com/tikv/tikv/issues/10533)
    * Fix the bug that stale messages causes TiKV to panic [#12023](https://github.com/tikv/tikv/issues/12023)
    * Fix the issue that undefined behavior (UB) might occur in TsSet conversions [#12070](https://github.com/tikv/tikv/issues/12070)
    * Fix a bug that replica reads might violate the linearizability [#12109](https://github.com/tikv/tikv/issues/12109)
    * Fix the potential panic issue that occurs when TiKV performs profiling on Ubuntu 18.04 [#9765](https://github.com/tikv/tikv/issues/9765)
    * Fix the issue that tikv-ctl returns an incorrect result due to its wrong string match [#12049](https://github.com/tikv/tikv/pull/12049)
    * Fix the issues of intermittent packet loss and out of memory (OOM) caused by the overflow of memory metrics [#12160](https://github.com/tikv/tikv/issues/12160)
    * Fix the potential issue of reporting TiKV panics when exiting TiKV [#12231](https://github.com/tikv/tikv/issues/12231)

* PD

    * Fix the issue that the operator creates steps with meaningless Joint Consensus [#4534](https://github.com/tikv/pd/pull/4534)
    * Fix a bug that the TSO revoking might get stuck when closing the PD client [#4550](https://github.com/tikv/pd/pull/4550)
    * Fix the issue that the Region scatterer scheduling might cause lost peers [#4570](https://github.com/tikv/pd/pull/4570)
    * Fix the issue that `Duration` fields of `dr-autosync` cannot be dynamically configured [#4653](https://github.com/tikv/pd/pull/4653)

* TiFlash

    * Fix the issue of TiFlash panic when the memory limit is enabled [#3902](https://github.com/pingcap/tiflash/issues/3902)
    * Fix the issue that expired data is recycled slowly [#4146]([https://github.com/pingcap/tiflash/issues/](https://github.com/pingcap/tiflash/issues/3902)4146)
    * Fix the potential issue of TiFlash panic when `Snapshot` is applied simultaneously with multiple DDL operations [#4072]([https://github.com/pingcap/tiflash/issues/](https://github.com/pingcap/tiflash/issues/3902)4072)
    * Fix the potential query error after adding columns under heavy read workload [https://github.com/pingcap/tiflash/issues/3967](https://github.com/pingcap/tiflash/issues/3967)
    * Fix the issue that the `SQRT` function with a negative argument returns `NaN` instead of `Null` [#3598] [https://github.com/pingcap/tiflash/issues/3598](https://github.com/pingcap/tiflash/issues/3598)
    * Fix the issue that casting `INI` to `DECIMAL` might cause overflow [#3920](https://github.com/pingcap/tiflash/issues/3920)
    * Fix the issue that the result of `IN` is incorrect in multi-value expressions [#4016](https://github.com/pingcap/tiflash/issues/4016)
    * Fix the issue that the date format identifies `'\n'` as an invalid separator [#4036](https://github.com/pingcap/tiflash/issues/4036)
    * Fix the issue that the learner-read process takes too much time under high concurrency scenarios [#3555](https://github.com/pingcap/tiflash/issues/3555)
    * Fix the wrong result that occurs when casting `DATETIME` to `DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)
    * Fix the issue of memory leak that occurs when a query is canceled [#4098](https://github.com/pingcap/tiflash/issues/4098)
    * Fix bug that enabling the elastic thread pool might introduce memory leak [#4098](https://github.com/pingcap/tiflash/issues/4098)
    * Fix a bug that canceled MPP queries might cause tasks to hang forever when the local tunnel is enabled [#4229](https://github.com/pingcap/tiflash/issues/4229)
    * Fix a bug that the failure of HashJoin build side might cause MPP queries to hang forever [#4195](https://github.com/pingcap/tiflash/issues/4195)
    * Fix a bug that MPP tasks might leak threads forever [https://github.com/pingcap/tiflash/issues/4238](https://github.com/pingcap/tiflash/issues/4238)

* Tools

    * Backup & Restore (BR)

        * Fix a bug that BR gets stuck when the restore operation meets some unrecoverable errors [#33200](https://github.com/pingcap/tidb/issues/33200)
        * Fix a bug that causes the restore operation to fail when the encryption information is lost during backup retry [#32423](https://github.com/pingcap/tidb/issues/32423)

    * TiCDC

        * (dup: release-5.3.1.md > Bug fixes> Tools> TiCDC)- Fix a bug that MySQL sink generates duplicated `replace` SQL statements when`batch-replace-enable` is disabled [#4501](https://github.com/pingcap/tiflow/issues/4501)
        * (dup: release-5.3.1.md > Bug fixes> Tools> TiCDC)- Fix a bug that a TiCDC node exits abnormally when a PD leader is killed [#4248](https://github.com/pingcap/tiflow/issues/4248)
        * Fix the error `Unknown system variable 'transaction_isolation'` for some MySQL versions [#4504](https://github.com/pingcap/tiflow/issues/4504)
        * Fix the TiCDC panic issue that might occur when `Canal-JSON` incorrectly handles `string` [#4635](https://github.com/pingcap/tiflow/issues/4635)
        * Fix a bug that sequence is incorrectly replicated in some cases [#4563](https://github.com/pingcap/tiflow/issues/4552)
        * Fix the TiCDC panic issue that might occur because `Canal-JSON` does not support nil [#4736](https://github.com/pingcap/tiflow/issues/4736)
        * Fix the wrong data mapping for avro codec of type `Enum/Set` and `TinyText/MediumText/Text/LongText` [#4454](https://github.com/pingcap/tiflow/issues/4454)
        * Fix a bug that Avro converts a `NOT NULL` column to a nullable field [#4818](https://github.com/pingcap/tiflow/issues/4818)
        * Fix an issue that TiCDC cannot exit [#4699](https://github.com/pingcap/tiflow/issues/4699)

    * TiDB Data Migration (DM)

        * (dup: release-5.4.0.md > Bug fixes> Tools> TiDB Data Migration (DM))- Fix the issue that syncer metrics are updated only when querying the status [#4281](https://github.com/pingcap/tiflow/issues/4281)
        * (dup: release-5.3.1.md > Bug fixes> Tools> TiCDC)- Fix the issue that execution errors of the update statement in safemode may cause the DM-worker panic [#4317](https://github.com/pingcap/tiflow/issues/4317)
        * (dup: release-5.3.1.md > Bug fixes> Tools> TiCDC)- Fix a bug that long varchars report an error `Column length too big` [#4637](https://github.com/pingcap/tiflow/issues/4637)
        * Fix the conflict issue caused by multiple DM-workers writing data from the same upstream [#3737](https://github.com/pingcap/tiflow/issues/3737)
        * Fix the issue that hundreds of "checkpoint has no change, skip sync flush checkpoint" print in the log and the replication is very slow [#4619](https://github.com/pingcap/tiflow/issues/4619)
        * Fix the DML loss issue when merging shards and replicating incremental data from upstream in the pessimistic mode [#5002](https://github.com/pingcap/tiflow/issues/5002)

    * TiDB Lightning

        * (dup: release-5.3.1.md > Bug fixes> Tools> TiDB Lightning)- Fix the bug that TiDB Lightning may not delete the metadata schema when some import tasks do not contain source files [#28144](https://github.com/pingcap/tidb/issues/28144)
        * Fix the panic that occurs when the table names in the source file and in the target cluster are different [#31771](https://github.com/pingcap/tidb/issues/31771)
        * Fix the checksum error “GC life time is shorter than transaction duration” [#32733](https://github.com/pingcap/tidb/issues/32733)
        * Fix the issue that TiDB Lightning gets stuck when it fails to check empty tables [#31797](https://github.com/pingcap/tidb/issues/31797)

    * Dumpling

        * Fix the issue that the displayed progress is not accurate when running `dumpling --sql $query` [#30532](https://github.com/pingcap/tidb/issues/30532)
        * Fix the issue that Amazon S3 cannot correctly calculate the size of compressed data [#30534](https://github.com/pingcap/tidb/issues/30534)

    * TiDB Binlog

        * Fix the issue that TiDB Binlog might be skipped when large upstream write transactions are replicated to Kafka. [#1136](https://github.com/pingcap/tidb-binlog/issues/1136)
