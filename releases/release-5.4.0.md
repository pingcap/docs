---
title: TiDB 5.4 Release Notes
---

# TiDB 5.4 Release Notes

Release date：February xx, 2022

TiDB version: 5.4.0

In v5.4, the key new features or improvements are as follows:

- Support the GBK character set
- Support using Index Merge to access data, which merges the filtering results of indexes on multiple columns
- Support reading stale data using a session variable
- Support persisting the configuration for collecting statistics
- Support using Raft Engine as the log storage engine of TiKV (experimental)
- Optimize the impact of backup on the cluster
- Support using Azure Blob storage as the target storage for backup
- Continuouly improve the stability and performance of TiFlash and the MPP engine
- Add a switch in TiDB Lightning to determine whether to allow importing an existing table
- Optimize the Continuous Profiling feature (experimental)
- TiSpark supports user identification and authentication

## Compatibility changes

> **Note:**
>
> When upgrading from an earlier TiDB version to v5.4.0, if you want to know the compatibility change notes of all intermediate versions, you can check the [Release Notes](/releases/release-notes.md) of the corresponding version.

### System variables

| Variable name | Change type | Description |
| :---------- | :----------- | :----------- |
|  [`tidb_backoff_lock_fast`](/system-variables.md#tidb_backoff_lock_fast) | Modified | The default value is changed from `100` to `10`. |
|  [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-new-in-v50) | Newly added | Controls whether allow TiDB to collect `PREDICATE COLUMNS`. The default value is `OFF`. |
| [`tidb_enable_index_merge`](/system-variables.md#tidb_enable_index_merge-new-in-v40) | Modified | The default value is changed from `OFF` to `ON`. <br/><ul><li>If you upgrade a TiDB cluster from versions earlier than v4.0.0 to v5.4.0 or later, this variable is `OFF` by default. </li><li>If you upgrade a TiDB cluster from v4.0.0 or later to v5.4.0 or later, this variable remains the same as before the upgrade. </li><li>For TiDB clusters of v5.4.0 and later, this variable is `ON` by default.</li></ul> |
| [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-new-in-v540)  | Newly added | This variable controls whether to use the method of paging to send coprocessor requests in `IndexLookUp` operator. The default value is `OFF`. <br/> For read queries that use `IndexLookup` and `Limit` and that `Limit` cannot be pushed down to `IndexScan`, there might be high latency for the read queries and high CPU usage for TiKV's `unified read pool`. In such cases, because the `Limit` operator only requires a small set of data, if you set `tidb_enable_paging` to `ON`, TiDB processes less data, which reduces query latency and resource consumption. |
| [`tidb_enable_top_sql`](/system-variables.md#tidb_enable_top_sql-new-in-v540) | Newly added | Controls whether to enable the Top SQL feature. The default value is `OFF`. |
| [`tidb_persist_analyze_options`](/system-variables.md#tidb_persist_analyze_options-new-in-v540) | Newly added | Controls whether to enable the [ANALYZE configuration persistence](/statistics.md#persist-analyze-configurations) feature. The default value is `OFF`. |
| [`tidb_read_staleness`](/system-variables.md#tidb_read_staleness-new-in-v540) | Newly added | Controls the range of historical data that can be read in the current session. The default value is `0`.|
| [`tidb_regard_null_as_point `](/system-variables.md#tidb_regard_null_as_point-new-in-v540) | Newly added | Controls whether the optimizer can treat `null` as a point value and uses it as a prefix condition to access the index 用于控制优化器是否可以把 null 值当做点值并作为前缀条件来访问索引 |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540) | Newly added | This variable controls whether to enable the synchronously loading statistics feature. (The default value `0` means that the feature is disabled and that the statistics is asynchronously loaded.) When the feature is enabled, this variable controls the maximum time that SQL optimization can wait for synchronously loading statistics before timeout. |
| [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540) | Newly added | This variable controls when synchronously loading statistics reaches timeout, whether SQL fails (`OFF`) or falls back to using pseudo statistics. The default value is `ON`. |
| [`tidb_store_limit`](/system-variables.md#tidb_store_limit-new-i-v304-and-v40) | Modified | Before v5.4.0, this variabe can be configured at instance level and globally. Starting from v5.4.0, this variable only supports global configuration. |

### Configuration file parameters

|  Configuration file    |  Configuration |  Change type  | Description    |
| :---------- | :----------- | :----------- | :----------- |
| TiDB | [`stats-load-concurrency`](/tidb-configuration-file.md#stats-load-concurrency-new-in-v540) | Newly added |  Controls the maximum number of columns that the TiDB synchronously loading statistics feature can process concurrently. The default value is `5`  |
| TiDB | [`stats-load-queue-size`](/tidb-configuration-file.md#stats-load-queue-size-new-in-v540)   | Newly added |  Controls the maximum number of column requests that the TiDB synchronously loading statistics feature can cache. The default value is`1000`.  |
| TiKV | [`snap-generator-pool-size`](/tidb-configuration-file.md#snap-generator-pool-size) | Newly added | The size of `snap-generator` thread pool. The default value is `2`. |
| TiKV | `log.file.max-size`、`log.file.max-days`、`log.file.max-backups` | Newly added  | For details, see [TiKV Configuration File - log.file](/tikv-configuration-file.md#logfile-new-in-v540). |
| TiKV | `raft-engine` | Newly added | Includes `enable`, `dir`, `batch-compression-threshold`, `bytes-per-sync`, `target-file-size`, `purge-threshold`, `recovery-mode`, `recovery-read-block-size`, `recovery-read-block-size`, `recovery-threads`. For details, see [TiKV Configuration File - Raft-engine](/tikv-configuration-file.md#raft-engine).|
| TiKV | [`backup.enable-auto-tune`](/tikv-configuration-file.md#enable-auto-tune-new-in-v540) | Newly added | In v5.3.0, the default value is `false`. Since v5.4.0, the default value is changed to `true`. This parameter controls whether to limit the resources used by backup tasks to reduce the impact on the cluster when the cluster resource utilization is high. In the default configuration, the speed of backup task might slow down. |
| TiKV | `log-level`, `log-format`, `log-file`, `log-rotation-size` | Modified | The names of TiKV log parameters are replaced with the names that are same as TiDB log parameters, which are `log.level`, `log.format`, `log.file.filename`, `log.enable-timestamp`. If you only set the old parameters, and their values are set to non-default values, the old parameters remain compatible with the new parameters. If both old and new parameters are set, the new parameters take effect. For details, see [TiKV Configuration File - log](/tikv-configuration-file.md#log-new-in-v540). |
| TiKV  |  `log-rotation-timespan`  | Deleted |  The timespan between log rotations. When this timespan passes, log files are rotated, that is, a timestamp is appended to the file name of the current log file, and a new file is created. |
| TiKV | `allow-remove-leader` | Deleted  | Determines whether to allow deleting the main switch. |
| TiKV | `raft-msg-flush-interval` | Deleted | Determines the interval at which Raft messages are sent in batches. The Raft messages in batches are sent at every interval specified by this configuration item.  |
| PD | [`log.level`](/pd-configuration-file.md#level) | Modified | The default value is changed from "INFO" to "info", guaranteed to be case in-sensitive. |
| TiFlash | [`profile.default.enable_elastic_threadpool`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Newly added  |  Determines whether to enable or disable the elastic thread pool function. Enabling this configuration item can significantly improve TiFlash CPU utilization in high concurrency scenarios. The default value is `false`. |
| TiFlash | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Newly added | Specifies the version of DTFile. The default value is `2`, under which hashes are embedded in the data file. You can also set the value to `3`. When it is `3`, the data file contains metadata and token data checksum, and supports multiple hash algorithms. |
| TiFlash | [`logger.count`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Modified | The default value is changed to `10`. |
| TiFlash | [`status.metrics_port`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file) | Modified | The default value is changed to `8234`. |
| TiFlash | [`raftstore.apply-pool-size`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file) | Newly added | The allowable number of threads in the pool that flushes Raft data to storage. The default value is `4`. |
| TiFlash | [`raftstore.store-pool-size`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file) | Newly added | The allowable number of threads that process Raft, which is the size of the Raftstore thread pool. The default value is `4`. |
| TiDB Data Migration (DM)  | [`collation_compatible`](/dm/task-configuration-file-full.md##task-configuration-file-template-advanced) | Newly added | The mode to sync the default collation in `CREATE` SQL statements. The supported values are "loose" (by default) or "strict".  |
| TiCDC | `max-message-bytes` | Modified| Change the default value of `max-message-bytes` in Kafka sink to `104857601` (10MB)  |
| TiCDC | `partition-num`     | Modified | Change the default value of `partition-num` in Kafka Sink from `4` to `3`. It makes TiCDC send messages to Kafaka partitions more evenly. |
| TiDB Lightning | `meta-schema-name` | Modified | Specifies the schema name for the metadata in the target TiDB. From v5.4.0, this schema is created only if you have enabled [parallel import](/tidb-lightning/tidb-lightning-distributed-import) (the corresponding parameter is `tikv-importer.incremental-import = true`). |
| TiDB Lightning | `task-info-schema-name` |  Newly added  | Specifies the name of the database where duplicated data is stored when Lightning detects conflicts. By default, the value is "lightning_task_info". Specify this parameter only if you have enabled the "duplicate-resolution" feature. |
| TiDB Lightning | `incremental-import` | Newly added | Whether to allow importing data to tables where data already exists. The default value is `false`. |


### Others

- TiDB Dashboard, by default, does not permit using `root` + empty password for login.
    Since v5.4.0, it is recommended to use `start --initial` when you use TiUP to start a TiDB cluster. Then, a random password is generated for the `root` account to log into TiDB Dashboard.

- An interface is added between TiDB and PD. When using the `information_schema.TIDB_HOT_REGIONS_HISTORY` system table, TiDB needs to use the PD in a matching version.
- TiDB Server, PD Server, and TiKV Server start using a unified naming method for the log-related parameters to manage log names, output formats, the rules of rotation and expiration. For details, see [TiKV configuration file - log](/tikv-configuration-file.md#log-new-in-v540).
- Since v5.4.0, if you create a SQL binding for an execution plan that has been cached via Plan Cache, the binding invalidates the plan already cached for the corresponding query. Before v5.4.0, the new binding does not affect any execution plans that have been already cached.

## New features

### SQL

- **TiDB supports GBK since v5.4.0**

    Before v5.4.0, TiDB supports `ascii`, `binary`, `latin1`, `utf8`, and `utf8mb4` character sets.

    To better support Chinese users, TiDB supports the GBK character set since v5.4.0. After enabling the [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) option in the TiDB configuration file when initializing a TiDB cluster for the first time, the TiDB GBK character set supports both `gbk_bin` and `gbk_chinese_ci` collations.

    When using the GBK character set, you need to pay attention to the compatibility restrictions. For details, see [Character Set and Collation - GBK](/character-set-gbk.md).

### Security

- **TiSpark supports user authentication and authorization**

    Since TiSpark 2.5.0, TiSpark supports both database user authentication and read/write authorization at a database or table level. After enabling this feature, you can prevent the business from running unauthorized batch tasks such as draws to obtain data, which improves the stability and data security of online clusters.

    This feature is disabled by default. When it is enabled, if a user operating through TiSpark does not have the needed permissions, the user gets an exception from TiSpark.

    [User document](/tispark-overview.md#security)

### Performance

- **Continue improving the stability and performance of the column-wise storage engine and the MPP computing engine for TiFlash**

    - Support more functions to be pushed down to the MPP engine:
        - String functions: `LPAD()`, `RPAD()`, `STRCMP()`
        - Date functions: `ADDDATE()`, `DATE_ADD()`, `DATE_SUB()`, `SUBDATE()`, `QUARTER()`
    - Introduce the elastic thread pool function to improve resource utilization (experimental feature)
    - Accelerate row-column data conversion when replicating data from TiKV. This improves overall replication performance by 50%.
    - Improve TiFlash performance and stability by adjusting the default value of some configuration items, yielding up to 20% performance improvement in simple queries per table.

    User documents: [Supported push-down calculations](/tiflash/use-tiflash.md#supported-push-down-calculations), [Configure the tiflash.toml file](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

- **Read expired data within a specified time range through a session variable**

    TiDB is a multi-replica distributed database that uses the Raft protocol. In the high concurrency and high throughput business scenarios, TiDB can make  read performance scalable through follower nodes and build a read-write separation architecture.

    For different business scenarios, the follower provides two read modes: strongly consistent read and weakly consistent expired read. The strongly consistent read mode is suitable for use in business scenarios with strict data real-time requirements. However, when this mode is used, especially in the geo-distributed deployment, there will be latency issue due to the data replication latency and the reduced throughput of the leader and the follower.

    For the business scenarios that do not require high real-time performance, the expired read mode can be used. This mode can reduce latency and improve throughput. TiDB currently supports the expired read by displaying read-only transactions or SQL statements. Both methods support reading the historical data of a specific point in time or within a specified time range. For details, please refer to [Read Historical Data through session variable `tidb_snapshot`](/read-historical-data.md).

    Since v5.4.0, TiDB supports reading historical data within a specified time range a through session variable, which further improves usability, reduces the difficulty of development, and meets the business requirements of low latency and high throughput of data access in quasi-real-time scenarios. You can set the variable as following example:

    ```sql
    set @@tidb_replica_read=leader_and_follower
    set @@tidb_read_staleness="-5"
    ```

    By this setting, TiDB can select the nearest leader or follower node and read the latest historical data within 5 seconds.

    [User document](/read-historical-data.md)

- **GA for Index Merge**

    _Index Merge_ is introduced in TiDB v4.0 as an experimental feature to access tables. This method greatly accelerates condition filtering when a query requires scanning of multiple columns of data. Take the following query as an example. In the `WHERE` statement, the filtering conditions connected by `OR` have their respective indexes in columns _key1_ and _key2_. Based on the indexes in the two columns, the Index Merge feature filters and merges the query results, and returns the merged result.

    ```sql
    SELECT * FROM table WHERE key1 <= 100 OR key2 = 200;
    ```

   Before TiDB v4.0, a query in a table uses only one not multiple indexes for filtering. If you want to query multiple columns of data, you can enable _Inex Merge_ to get the exact query result in short time by using the indexes in individual columns. _Inex Merge_ avoids unnecessary full table scans and does not require establishing large number of composite indexes.

    In v5.4.0, _Inex Merge_ is a GA feature. However, you still need to pay attention to the following restrictions:

    - _Inex Merge_ supports only disjunctive normal form (X<sub>1</sub> ⋁ X<sub>2</sub> ⋁ …X<sub>n</sub>). That is, to use this feature, filtering conditions in a `WHERE` clause should be connected by `OR`.

    - This feature is enabled by default for TiDB clusters of v5.4.0 or later. For v5.4.0 or later TiDB clusters upgraded from versions earlier than v5.4.0, this feature inherits the setting before the upgrade and you can change the setting as required (in TiDB clusters earlier than v4.0, this feature does not exist and is disabled by default).

    [User document](/explain-index-merge.md)

- **Add Raft Engine (experimental)**

    Support using [Raft Engine](https://github.com/tikv/raft-engine) as the log storage engine in TiKV. Compared with RocksDB, Raft Engine can reduce TiKV I/O write traffic by up to 40% and CPU usage by 10%, while improving foreground throughput by about 5% and reducing tail latency by 20% under certain loads. In addition, Raft Engine improves the efficiency of log recycling and fixes the issue of log accumulation in extreme conditions.

    Raft Engine is still an experimental feature and is disabled by default. Note that the data format of Raft Engine in v5.4.0 is not compatible with previous versions. Before upgrading or downgrading the cluster, you need to make sure that Raft Engine on all TiKV nodes is disabled. It is recommended to use Raft Engine only in v5.4.0 or a later version.

- **Support collecting statistics for `PREDICATE COLUMNS` (experimental)**

    In most cases, when executing SQL statements, the optimizer only uses statistics of some columns (such as columns in the `WHERE`, `JOIN`, `ORDER BY`, and `GROUP BY` statements). These used columns are called `PREDICATE COLUMNS`.

    Since v5.4.0, you can set the value of the [`tidb_enable_column_tracking`](/system-variables.md#tidb_enable_column_tracking-introduced-from-v540-version) system variable to `ON` to enable TiDB to collect `PREDICATE COLUMNS`.

    After the setting, TiDB writes the `PREDICATE COLUMNS` information to the `mysql.column_stats_usage` system table every 100 * [`stats-lease`](/tidb-configuration-file.md#stats-lease). When the query pattern of your business is stable, you can use the `ANALYZE TABLE TableName PREDICATE COLUMNS` syntax to collect statistics on the `PREDICATE COLUMNS` columns only, which can greatly reduce the overhead of collecting statistics.

    [User document](/statistics.md#collect-statistics-for-some-columns)

- **Support synchronously loading statistics (experimental)**

    Since v5.4.0, TiDB introduces the synchronously loading statistics feature. The feature is disabled by default. After enabling the feature, TiDB can synchronously load statistics with a large space consumption (such as histogram, TopN, and Count-Min Sketch statistics) into memory when you execute SQL statements, which improves the completeness of statistics for SQL optimization.

    [[User document](/statistics.md#load-statistics)

### Stability

- **Support persisting ANALYZE configurations**

    Statistics are one type of the basic information that the optimizer refers to when generating execution plans. The accuracy of the statistics directly affects whether the generated execution plans are reasonable. To ensure the accuracy of the statistics, sometimes it is necessary to set different collection configurations for different tables, partitions, and indexes.

    Since v5.4.0, TiDB supports persisting some `ANALYZE` configurations. With this feature, the existing configurations can be easily reused for future statistics collection.

    The `ANALYZE` configuration persistence feature is enabled by default (the system variable `tidb_analyze_version` is `2` and `tidb_persist_analyze_options` is `ON` by default). You can use this feature to record the persistence configurations specified in the `ANALYZE` statement when executing the statement manually. Once recorded, the next time TiDB automatically updates statistics or you manually collect statistics without specifying these configuration, TiDB will collect statistics according to the recorded configurations.

    [User document](/statistics.md#persist-analyze-configurations)

## High availability and disaster recovery

- **Reduce the impact of backup tasks on the cluster**

    Backup & Restore (BR) introduces the auto-tune feature (enabled by default). This feature monitors the cluster resource usage and adjusts the number of threads used by the backup tasks to reduce the impact of backup tasks on the cluster. In some cases, if you increase the cluster resources for backup and enable the auto-tune feature, it is possible to limit the impact of backup tasks on the cluster to 10% or less.

    [User document](/br/br-auto-tune.md)

- **Support Azure Blob Storage as a target storage for backup**

    Backup & Restore (BR) supports Azure Blob Storage as a remote target storage for backup. If you deploy TiDB in Azure Cloud, you can back up the cluster data to the Azure Blob Storage service.

    [User document](/br/backup-and-restore-azblob.md)

### Data migration

- **TiDB Lightning introduces a new feature to determine whether to allow importing data to tables with data**

    TiDB Lightning introduces a new feature `incremental-import`. It determines whether to allow importing data to tables with data. The default value is `false`. When using parallel import mode, you must set it to `true`.

    [User document](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

- **TiDB Lightning introduces the schema name that stores the meta information for parallel import**

    TiDB Lightning introduces `meta-schema-name`. In parallel import mode, this parameter specifies the schema name that stores the meta information for each TiDB Lightning instance in the target cluster. By default, the value is "lightning_metadata". The value set for this parameter must be the same for each TiDB Lightning instance that participates in the same parallel import; otherwise, the correctness of the imported data can not be ensured.

    [User document](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task)

- **TiDB Lightning introduces duplicate resolution**

    In Local-backend mode, TiDB Lightning outputs duplicated data before the data import is completed, and then removes that duplicated data from the database. You can resolve the duplicated data after the import is completed and select suitable data to insert according to business rules. It is recommended to clean upstream data sources based on duplicated data to avoid data inconsistency caused by duplicated data encountered in the subsequent incremental data migration phase.

    [User document](tidb-lightning/tidb-lightning-error-resolution.md)

- **Optimize the usage of relay log in TiDB Data Migration (DM)**

    - Recover the `enable-relay` switch in the `source` configuration.
    - Support dynamically enabling or disabling relay log in the `start-relay` or `stop-relay` command.
    - Bind the status of relay log to `source`. `source` keeps its original status of being enabled or disabled after it is migrated to any DM-worker.
     - Move the storage path of relay log to the DM-worker configuration file.

     [User document](/dm/relay-log.md)

- **Optimize the processing of [collation](/character-set-and-collation.md) in DM**

    Add the `collation_compatible` configuration item. The value options are `loose` (default) and `strict`:

    - If your application does not have strict requirements on collation, and the collation of query results can be different between the upstream and downstream, you can use the default `loose` mode to avoid reporting errors.
    - If your application has strict requirements on collation, and the collation must be consistent between the upstream and downstream, you can use the `strict` mode. However, if the downstream does not support the upstream's default collation, the data replication might report errors.

    [User document](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)

- **Optimize `transfer source` in DM to support smooth execution of replication tasks**

    When the DM-worker nodes have unbalanced load, the `transfer source` command can be used to manually transfer the configuration of a `source` to another load. After the optimization, the `transfer source` command simplifies the manual operation. You can smoothly transfer the source instead of pausing all related tasks; DM completes other operations internally.

- **DM OpenAPI becomes generally available (GA)**

    DM supports daily management via API, including adding data sources and managing tasks. In v5.4.0, DM OpenAPI becomes GA.

    [User document](/dm/dm-open-api.md)

### Diagnostic efficiency

- **Top SQL (experimental feature)**

    A new experimental feature, Top SQL (turned off by default), is introduced to help you easily find queries that consume more resources.

    [User document](/dashboard/top-sql.md)

### TiDB data share subscription

- **Optimize the impact of TiCDC on clusters**

    Significantly reduces the performance impact on TiDB clusters when you use TiCDC. In the test environment, the performance impact of TiCDC on TiDB can be reduced to less than 5%.

### Deployment and maintenance

- **Enhance Continuous Profiling (experimental feature)**

    - More components supported: Besides TiDB, PD, and TiKV, TiDB v5.4.0 also supports CPU profiling of TiFlash.
    - More forms of profiling display: Supports display of CPU profiling and Goroutine results on flame charts.
    - More deployment environments supported: Continuous Profiling is applicable to clusters deployed using TiDB Operator.

    Continuous Profiling is disabled by default and can be enabled on TiDB Dashboard. 

    Continuous Profiling is available to clusters deployed or upgraded using TiUP of v1.9.0 or later or TiDB Operator of v1.3.0 or later.

    [User document](/dashboard/continuous-profiling.md)

## Improvements

+ TiDB

    - Add a new system variable `tidb_enable_paging. For read requests in which `IndexLookUp` and `Limit` are used and `Limit` cannot be pushed down to `IndexScan`, setting this variable to `ON` can significantly reduce the latency and the resource consumption [#30578](https://github.com/pingcap/tidb/issues/30578)
    - Support the `ADMIN {SESSION | INSTANCE | GLOBAL} PLAN_CACHE` syntax to clear the cached query plan [#30370](https://github.com/pingcap/tidb/pull/30370)

+ TiKV

    - Coprocessor supports paging API to process requests in a stream-like way [#11448](https://github.com/tikv/tikv/issues/11448)
    - Support `read-through-lock` so that read operations do not need to wait for secondary locks to be resolved [#11402](https://github.com/tikv/tikv/issues/11402)
    - Add a disk protection mechanism to avoid panic caused by disk space drainage [#10537](https://github.com/tikv/tikv/issues/10537)
    - Support archiving and rotating logs [#11651](https://github.com/tikv/tikv/issues/11651)
    - Reduce the system call by the Raft client and increase CPU efficiency [#11309](https://github.com/tikv/tikv/issues/11309)
    - Coprocessor supports pushing down substring to TiKV [#11495](https://github.com/tikv/tikv/issues/11495)
    - Improve the scan performance by skip reading locks in the Read Committed isolation level [#11485](https://github.com/tikv/tikv/issues/11485)
    - Reduce the default thread pool size used by backup operations and limit the use of thread pool when the stress is high [#11000](https://github.com/tikv/tikv/issues/11000)
    - Support dynamically adjusting the sizes of Apply thread pool and Store thread pool [#11159](https://github.com/tikv/tikv/issues/11159)
    - Support configuring the size of the `snap-generator` thread pool [#11247](https://github.com/tikv/tikv/issues/11247)
    - Optimize the issue of global lock race that occurs when there are many files with frequent reads and writes [#250](https://github.com/tikv/rocksdb/pull/250)

+ PD

    - Record the historic hotspot information by default [#25281](https://github.com/pingcap/tidb/issues/25281)
    - Add signature for the HTTP component to identify the request source [#4490](https://github.com/tikv/pd/issues/4490)
    - Update TiDB Dashboard to v2021.12.31 [#4257](https://github.com/tikv/pd/issues/4257)

+ TiFlash

    - Optimize the communication of local operators
    - Increase the non-temporary thread count of gRPC to avoid the frequent creation or destroy of threads

+ Tools

    + Backup & Restore (BR)

        - Add a validity check for the key when BR performs encrypted backup [#29794](https://github.com/pingcap/tidb/issues/29794)

    + TiCDC

        - Reduce the count of "EventFeed retry rate limited" logs [#4006](https://github.com/pingcap/tiflow/issues/4006)
        - Reduce the replication latency when replicating many tables [#3900](https://github.com/pingcap/tiflow/issues/3900)
        - Reduce the time for the KV client to recover when a TiKV store is down [#3191](https://github.com/pingcap/tiflow/issues/3191)

    + TiDB Data Migration (DM)

        - Lower the usage rate of CPU when relay is enabled [#2214](https://github.com/pingcap/dm/issues/2214)

    + TiDB Lightning

        - Use optimistic transactions to write data to improve performance in TiDB-backend mode [#30953](https://github.com/pingcap/tidb/pull/30953)

    + Dumpling

        - Improve compatibility when Dumpling checks the data version [#29500](https://github.com/pingcap/tidb/pull/29500)
        - Add a default collation when dumping `CREATE DATABASE` and `CREATE TABLE` [#3420](https://github.com/pingcap/tiflow/issues/3420)

## Bug fixes

+ TiDB

    - Fix the issue of the `tidb_analyze_version` value change that occurs when upgrading the cluster from v4.x to v5.x [#25422](https://github.com/pingcap/tidb/issues/25422)
    - Fix the issue of wrong result that occurs when using different collations in a subquery [#30748](https://github.com/pingcap/tidb/issues/30748)
    - Fix the issue that the result of `concat(ifnull(time(3))` in TiDB is different from that in MySQL [#29498](https://github.com/pingcap/tidb/issues/29498)
    - Fix the issue of potential data index inconsistency in optimistic transaction mode [#30410](https://github.com/pingcap/tidb/issues/30410)
    - Fix the issue that the query execution plan of IndexMerge is wrong when an expression cannot be pushed down to TiKV [#30200](https://github.com/pingcap/tidb/issues/30200)
    - Fix the issue that concurrent column type change causes inconsistency between the schema and the data [#31048](https://github.com/pingcap/tidb/issues/31048)
    - Fix the issue that the IndexMerge query result is wrong that occurs when there is a subquery [#30913](https://github.com/pingcap/tidb/issues/30913)
    - Fix the panic issue that occurs when the FetchSize is set too large in the client [#30896](https://github.com/pingcap/tidb/issues/30896)
    - Fix the issue that LEFT JOIN might be mistakenly converted to INNER JOIN [#20510](https://github.com/pingcap/tidb/issues/20510)
    - Fix the issue that panic might occur when the `CASE-WHEN` expression and collation are used together [#30245](https://github.com/pingcap/tidb/issues/30245)
    - Fix the issue of wrong query result that occurs when the `IN` value contains a binary constant [#31261](https://github.com/pingcap/tidb/issues/31261)
    - Fix the issue of wrong query result that occurs when CTE has a subquery [#31255](https://github.com/pingcap/tidb/issues/31255)
    - Fix the issue that executing the `INSERT ... SELECT ... ON DUPLICATE KEY UPDATE` statement get panic [#28078](https://github.com/pingcap/tidb/issues/28078)
    - Fix the issue that INDEX HASH JOIN returns the `send on closed channel` error [#31129](https://github.com/pingcap/tidb/issues/31129)

+ TiKV

    - Fix the issue that the MVCC deletion records are not cleared by GC [#11217](https://github.com/tikv/tikv/issues/11217)
    - Fix the issue that retrying prewrite requests in the pessimistic transaction mode might cause the risk of data inconsistency in rare cases [#11187](https://github.com/tikv/tikv/issues/11187)
    - Fix the issue that GC scan causes memory overflow [#11410](https://github.com/tikv/tikv/issues/11410)
    - Fix the issue that RocksDB flush or compaction causes panic when the disk capacity is full [#11224](https://github.com/tikv/tikv/issues/11224)

+ PD

    - Fix the issue that Region statistics are not affected by `flow-round-by-digit` [#4295](https://github.com/tikv/pd/issues/4295)
    - Fix the issue that the scheduling operator cannot fail fast because the target store is down [#3353](https://github.com/tikv/pd/issues/3353)
    - Fix the issue that Regions on offline stores cannot be merged [#4119](https://github.com/tikv/pd/issues/4119)
    - Fix the issue that the cold hotspot data cannot be deleted from the hotspot statistics [#4390](https://github.com/tikv/pd/issues/4390)

+ TiFlash

    - Fix the issue that the `Tree struct based executor must have executor id` error is returned in the query result
    - Fix the issue that the `Illegal column type UInt32 for the second argument of function tidbRoundWithFrac` error is returned in the query result
    - Fix the issue that the `Unexpected type of column: Nullable(Nothing)` error is returned in the query result
    - Fix the issue that the `source region at right may be considered at left when merging` error is returned in the query result
    - Fix the issue that collation does not take effect on the `nullable` type
    - Fix the issue that `coalesce` mistakenly deletes the `nullable` identifier from the result columns
    - Fix the issue that TiFlash might panic when a MPP query is stopped
    - Fix the issue that queries with the `where <string>` clause return wrong result 
    - Fix the potential issue of data inconsistency that might occur when setting the column type of an integer primary key to a larger range
    - Fix the issue that when an input time is earlier than 1970-01-01 00:00:01 UTC, the behavior of `unix_timestamp` is inconsistent with that of TiDB or MySQL
    - Fix the issue that TiFlash might return the `EstablishMPPConnection` error after it is retarted
    - Fix the issue that the `CastStringAsDecimal` bahavior is inconsitent in TiFlash and in TiDB/TiKV
    - Fix the issue that the `DB::Exception: Encode type of coprocessor response is not CHBlock` error is returned in the query result
    - Fix the issue that the `castStringAsReal` bahavior is inconsitent in TiFlash and in TiDB/TiKV
    - Fix the issue that the returned result of the `date_add_string_xxx` function in TiFlash is inconsistent with that in MySQL

+ Tools

    + Backup & Restore (BR)

        - Fix the potential issue that Region distribution might be uneven after a restore operation is finished [#30425](https://github.com/pingcap/tidb/issues/30425)
        - Fix the issue that `'/'` cannot be specified in endpoint when `minio` is used as the backup storage [#30104](https://github.com/pingcap/tidb/issues/30104)
        - Fix the issue that system tables cannot be restored because concurrently backing up system tables makes the table name fail to update [#29710](https://github.com/pingcap/tidb/issues/29710)

    + TiCDC

        - Fix the issue that replication cannot be performed when `min.insync.replicas` is smaller than `replication-factor` [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - Fix the issue that the `cached region` monitoring metric is negative [#4300](https://github.com/pingcap/tiflow/issues/4300)
        - Fix the issue that `mq sink write row` does not have monitoring data [#3431](https://github.com/pingcap/tiflow/issues/3431)
        - Fix the compatibility issue of `sql mode` [#3810](https://github.com/pingcap/tiflow/issues/3810)
        - Fix the potential panic issue that occurs when a replication task is removed [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - Fix the issue of panic and data inconsistency that occurs when outputting the default column value [#3929](https://github.com/pingcap/tiflow/issues/3929)
        - Fix the issue that default values cannot be replicated [#3793](https://github.com/pingcap/tiflow/issues/3793)
        - Fix the potential issue that the deadlock causes a replication task to gets stuck [#4055](https://github.com/pingcap/tiflow/issues/4055)
        - Fix the issue that no log is output when the disk is fully written [#3362](https://github.com/pingcap/tiflow/issues/3362)
        - Fix the issue that special comments in DDL statements cause the replication task to stop [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - Fix the issue that the service cannot be started because of a timezone issue in the RHEL release [#3584](https://github.com/pingcap/tiflow/issues/3584)
        - Fix the issue of potential data loss caused by inaccurate checkpoint [#3545](https://github.com/pingcap/tiflow/issues/3545)
        - Fix the OOM issue in the container environment [#1798](https://github.com/pingcap/tiflow/issues/1798)
        - Fix the issue of replication stop caused by the incorrect configuration of `config.Metadata.Timeout` [#3352](https://github.com/pingcap/tiflow/issues/3352)

    + TiDB Data Migration (DM)

        - Fix the issue that the `CREATE VIEW` statement interrupts data replication [#4173](https://github.com/pingcap/tiflow/issues/4173)
        - Fix the issue the schema needs to be reset after a DDL statement is skipped [#4177](https://github.com/pingcap/tiflow/issues/4177)
        - Fix the issue that the table checkpoint is not updated in time after a DDL statement is skipped [#4184](https://github.com/pingcap/tiflow/issues/4184)
        - Fix a compatibility issue of the TiDB version with the parser version [#4298](https://github.com/pingcap/tiflow/issues/4298)
        - Fix the issue that syncer metrics are updated only when querying the status [#4281](https://github.com/pingcap/tiflow/issues/4281)

    + TiDB Lightning

        - Fix the issue of wrong import result that occurs when TiDB Lightning does not have the priviledge to access the `mysql.tidb` table [#31088](https://github.com/pingcap/tidb/issues/31088)
        - Fix the issue that some checks are skipped when TiDB Lightning is restarted [#30772](https://github.com/pingcap/tidb/issues/30772)
        - Fix the issue that TiDB Lighting fails to report the error when the S3 path does not exist [#30674](https://github.com/pingcap/tidb/pull/30674)

    + TiDB Binlog

        - Fix the issue that Drainer fails because it is incompatible with the `CREATE PLACEMENT POLICY` statement [#1118](https://github.com/pingcap/tidb-binlog/issues/1118)
