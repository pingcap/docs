---
title: TiDB 7.6.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 7.6.0.
---

# TiDB 7.6.0 Release Notes

Release date: xx xx, 202x

TiDB version: 7.6.0

Quick access: [Quick start](https://docs.pingcap.com/tidb/v7.6/quick-start-with-tidb) | [Installation packages](https://www.pingcap.com/download/?version=v7.6.0#version-list)

7.6.0 introduces the following key features and improvements:

<table>
<thead>
  <tr>
    <th>Category</th>
    <th>Feature/Enhancement</th>
    <th>Description</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="4">Scalability and Performance<br></td>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/sql-plan-management#cross-database-binding">Cross-database SQL binding</a> {/* tw@Oreoxmt */}</td>
    <td>When managing hundreds of databases with the same schema, it is often necessary to apply SQL bindings across these schemas. For example, in SaaS or PaaS data platforms, each user typically operates separate databases with the same schema and runs similar SQL queries on them. In this case, it is impractical to bind SQL for each schema one by one. TiDB v7.6.0 introduces cross-database SQL bindings that enable matching bindings across all schema-equivalent databases.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/br-snapshot-guide#restore-cluster-snapshots">Achieve up to 10 times faster for snapshot restore (experimental)</a> {/* tw@Oreoxmt */}</td>
    <td>BR v7.6.0 introduces an experimental two-phase Region scatter algorithm to prepare snapshot restores for clusters. In clusters with many TiKV nodes, this algorithm significantly improves cluster resource efficiency by more evenly distributing load across nodes and better utilizing per-node network bandwidth. In several real-world cases, this improvement accelerates restore speed by about up to 10 times.</td>
  </tr>
  <tr>
    <td><a href="">Achieve up to 10 times faster for creating tables in batch (experimental)</a>  {/* tw@hfxsd */}</td>
    <td>With the implementation of the new DDL architecture in v7.6.0, the performance of batch table creation has witnessed a remarkable improvement, up to 10 times faster. This substantial enhancement drastically reduces the time needed for creating numerous tables. This acceleration is particularly noteworthy in SaaS scenarios, where the prevalence of high volumes of tables, ranging from tens to hundreds of thousands, is a common challenge.</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service">Use the Active PD Follower feature to enhance the scalability of PD's Region information query service (experimental)</a>  {/* tw@Oreoxmt */}</td>
    <td>TiDB v7.6.0 introduces an experimental feature "Active PD Follower", which allows PD followers to provide Region information query services. This feature improves the capability of the PD cluster to handle GetRegion and ScanRegions requests in clusters with a large number of TiDB nodes and Regions, thereby reducing the CPU pressure on the PD leader.</td>
  </tr>
  <tr>
    <td rowspan="2">Reliability and Availability<br></td>
    <td><a href="https://docs.pingcap.com/tidb/v7.6/tiproxy/tiproxy-overview">Support TiProxy (experimental)</a>  {/* tw@ran-huang */}</td>
    <td>Full support for the TiProxy service, easily deployable via deployment tooling, to manage and maintain connections to TiDB so that they live through rolling restarts, upgrades, or scaling events.</td>
  </tr>
  <tr>
    <td><a href="">Data Migration (DM) officially supports MySQL 8.0 (GA)</a>  {/* tw@hfxsd */}</td>
    <td>Previously, using DM to migrate data from MySQL 8.0 is an experimental feature and is not available for production environments. TiDB v7.6.0 enhances the stability and compatibility of this feature to help you smoothly and quickly migrate data from MySQL 8.0 to TiDB in production environments. In v7.6.0, this feature becomes generally available (GA).</td>
  </tr>
</tbody>
</table>

## Feature details

### Scalability

* Use the Active PD Follower feature to enhance the scalability of PD's Region information query service (experimental) [#7431](https://github.com/tikv/pd/issues/7431) @[CabinfeverB](https://github.com/CabinfeverB) **tw@Oreoxmt** <!--1667-->
    
    In a TiDB cluster with a large number of Regions, the PD leader might experience high CPU load due to the increased overhead of handling heartbeats and scheduling tasks. If the cluster has many TiDB instances, and there is a high concurrency of requests for Region information, the CPU pressure on the PD leader increases further and might cause PD services to become unavailable.
    
    To ensure high availability, TiDB v7.6.0 supports using the Active PD Follower feature to enhance the scalability of PD's Region information query service. You can enable the Active PD Follower feature by setting the system variable [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760) to `ON`. After this feature is enabled, TiDB evenly distributes Region information requests to all PD servers, and PD followers can also directly handle Region requests, thereby reducing the CPU pressure on the PD leader.

    For more information, see [documentation](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service).

### Performance

* BR improves snapshot restore speed by up to 10 times (experimental) [#33937](https://github.com/pingcap/tidb/issues/33937) @[3pointer](https://github.com/3pointer) **tw@Oreoxmt** <!--1647-->

    As a TiDB cluster scales up, it becomes increasingly crucial to quickly restore the cluster from failures to minimize business downtime. Before v7.6.0, the Region scattering algorithm is a primary bottleneck in performance restoration. In v7.6.0, BR optimizes the Region scattering algorithm, which quickly splits the restore task into a large number of small tasks and scatters them to all TiKV nodes in batches. The new parallel recovery algorithm fully utilizes the resources of each TiKV node, thereby achieving a rapid parallel recovery. In several real-world cases, the snapshot restore speed of the cluster is improved by about 10 times in large-scale Region scenarios.

    The new parallel recovery algorithm is experimental. To use it, you can configure the `--granularity=coarse-grained` parameter in the `br` command. You can also control the concurrency of download tasks on each TiKV node by setting the `--tikv-max-restore-concurrency` parameter. For example:

    ```bash
    br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}" \
    --s3.region "${region}" \
    --granularity "coarse-grained" \
    --tikv-max-restore-concurrency 128 \
    --send-credentials-to-tikv=true \
    --log-file restorefull.log
    ```

    For more information, see [documentation](/br/br-snapshot-guide.md#restore-cluster-snapshots).

* Support pushing down the following string functions to TiKV [#48170](https://github.com/pingcap/tidb/issues/48170) @[gengliqi](https://github.com/gengliqi) **tw@qiancai** <!--1607-->

    * `LOWER()`
    * `UPPER()`

    For more information, see [documentation](/functions-and-operators/expressions-pushed-down.md).

* Support pushing down the following JSON functions to TiFlash [#48350](https://github.com/pingcap/tidb/issues/48350) [#48986](https://github.com/pingcap/tidb/issues/48986) [#48994](https://github.com/pingcap/tidb/issues/48994) [#49345](https://github.com/pingcap/tidb/issues/49345) [#49392](https://github.com/pingcap/tidb/issues/49392) @[SeaRise](https://github.com/SeaRise) @[yibin87](https://github.com/yibin87) **tw@qiancai** <!--1608-->

    * `JSON_UNQUOTE()`
    * `JSON_ARRAY()`
    * `JSON_DEPTH()`
    * `JSON_VALID()`
    * `JSON_KEYS()`
    * `JSON_CONTAINS_PATH()`

    For more information, see [documentation](/tiflash/tiflash-supported-pushdown-calculations.md).

* Improve the performance of creating tables by 10 times (experimental) [#49752](https://github.com/pingcap/tidb/issues/49752) @[gmhdbjd](https://github.com/gmhdbjd) **tw@hfxsd** <!--1408-->

    In previous versions, when migrating tens of thousands of tables from the upstream database to TiDB, it is time-consuming and inefficient for TiDB to create these tables. Starting from v7.6.0, TiDB introduces a new TiDB DDL V2 architecture. You can enable it by configuring the system variable [`tidb_ddl_version`](/system-variables.md#tidb_ddl_version-new-in-v760). Compared with previous versions, the new version of the DDL improves the performance of creating batch tables by 10 times, and significantly reduces time for creating tables.

    For more information, see [documentation](/ddl-v2.md).

* The optimizer enhances support for multi-valued indexes [#47759](https://github.com/pingcap/tidb/issues/47759) [#46539](https://github.com/pingcap/tidb/issues/46539) @[Arenatlx](https://github.com/Arenatlx) @[time-and-fate](https://github.com/time-and-fate) **tw@ran-huang** <!--1405/1584-->

    Starting from v6.6.0, TiDB introduced [multi-value indexes](/sql-statements/sql-statement-create-index.md#multi-valued-indexes) to improve query performance for JSON data types. In v7.6.0, the optimizer enhances its support for multi-valued indexes and can correctly identify and utilize them to optimize queries in complex scenarios.

    * Statistics on multi-valued indexes are collected and applied by the optimizer for estimation. When a SQL statement might select multiple multi-valued indexes, the optimizer can identify the index with lower cost.
    * When there are multiple `member of` conditions connected by `OR`, the optimizer is able to match an effective index partial path for each DNF item (a `member of` condition) and combine multiple paths using Union to form an `Index Merge`. This allows more efficient condition filtering and data querying.

    For more information, see [documentation](/sql-statements/sql-statement-create-index.md#multi-valued-indexes).

### Reliability

* Cross-database execution plan binding [#48875](https://github.com/pingcap/tidb/issues/48875) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1613-->

    When running SaaS services on TiDB, it is common practice to store data for each tenant in separate databases for easier data maintenance and management. This results in hundreds of databases with the same table and index definitions, and similar SQL statements. In such scenario, when you create an execution plan binding for a SQL statement, this binding usually applies to the SQL statements in other databases as well.

    For this scenario, TiDB v7.6.0 introduces the cross-database binding feature, which supports binding the same execution plan to SQL statements with the same schema, even if they are in different databases. When creating a cross-database binding, you need to use the wildcard `*` to represent the database name, as shown in the following example. After the binding is created, regardless of which database the tables `t1` and `t2` are in, TiDB will try to use this binding to generate an execution plan for any SQL statement with the same schema, which saves your effort to create a binding for each database.

    ```sql
    CREATE GLOBAL BINDING FOR
    USING
        SELECT /*+ merge_join(t1, t2) */ t1.id, t2.amount FROM *.t1, *.t2 WHERE t1.id = t2.id;
    ```

    In addition, cross-database binding can effectively mitigate SQL performance issues caused by uneven distribution and rapid changes in user data and workload. SaaS providers can use cross-database binding to fix execution plans validated by users with large data volumes, thereby fixing execution plans for all users. For SaaS providers, this feature provides significant convenience and experience improvements.

    Due to the system overhead (less than 1%) introduced by cross-database binding, TiDB disables this feature by default. To use cross-database binding, you need to first enable the [`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-new-in-v760) system variable.

    For more information, see [documentation](/sql-plan-management.md#cross-database-binding).

### Availability

* Support the proxy component TiProxy (experimental) [#413](https://github.com/pingcap/tiproxy/issues/413) @[djshow832](https://github.com/djshow832) @[xhebox](https://github.com/xhebox) **tw@ran-huang** <!--1596-->

    TiProxy is the official proxy component of TiDB, located between the client and TiDB server. It provides load balancing and connection persistence functions for TiDB, making the workload of the TiDB cluster more balanced and not affecting user access to the database during maintenance operations.

    - During maintenance operations such as rolling restarts, rolling upgrades, and scaling-in in a TiDB cluster, changes occur in the TiDB servers which result in interruptions in connections between clients and the TiDB servers. By using TiProxy, connections can be smoothly migrated to other TiDB servers during these maintenance operations so that clients are not affected.
    - Client connections to a TiDB server cannot be dynamically migrated to other TiDB servers. When the workload of multiple TiDB servers is unbalanced, it might result in a situation where the overall cluster resources are sufficient, but certain TiDB servers experience resource exhaustion leading to a significant increase in latency. To address this issue, TiProxy provides dynamic migration for connection, which allows connections to be migrated from one TiDB server to another without any impact on the clients, thereby achieving load balancing for the TiDB cluster.

    TiProxy has been integrated into TiUP, TiDB Operator, and TiDB Dashboard, making it easy to configure, deploy and maintain.

    For more information, see [documentation](/tiproxy/tiproxy-overview.md).

### SQL

* `LOAD DATA` supports explicit transactions and rollbacks [#49079](https://github.com/pingcap/tidb/pull/49079) @[ekexium](https://github.com/ekexium) **tw@Oreoxmt** <!--1422-->

    Compared with MySQL, the transactional behavior of the`LOAD DATA` statement varies in different TiDB versions before v7.6.0, so you might need to make additional adjustments when using this statement. Specifically, before v4.0.0, `LOAD DATA` commits every 20000 rows. From v4.0.0 to v6.6.0, TiDB commits all rows in one transaction by default and also supports committing every fixed number of rows by setting the [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) system variable. Starting from v7.0.0, `tidb_dml_batch_size` no longer takes effect on `LOAD DATA` and TiDB commits all rows in one transaction.

    Starting from v7.6.0, TiDB processes `LOAD DATA` in transactions in the same way as other DML statements, especially in the same way as MySQL. The `LOAD DATA` statement in a transaction no longer automatically commits the current transaction or starts a new transaction. Moreover, you can explicitly commit or roll back the `LOAD DATA` statement in a transaction. Additionally, the `LOAD DATA` statement is affected by the TiDB transaction mode setting (optimistic or pessimistic transaction). These improvements simplify the migration process from MySQL to TiDB and offer a more unified and controllable experience for data import.

    For more information, see [documentation](/sql-statements/sql-statement-load-data.md).

### DB operations

* `FLASHBACK CLUSTER` supports specifying a precise TSO [#48372](https://github.com/pingcap/tidb/issues/48372) @[BornChanger](https://github.com/BornChanger/BornChanger) **tw@qiancai** <!--1615-->

    In TiDB v7.6.0, the flashback feature is more powerful and precise. It not only supports rolling back a cluster to a specified historical timestamp but also enables you to specify a precise recovery [TSO](/tso.md) using `FLASHBACK CLUSTER TO TSO`, thereby increasing flexibility in data recovery. For example, you can use this feature with TiCDC. After pausing data replication and conducting pre-online read-write tests in your downstream TiDB cluster, this feature allows the cluster to gracefully and quickly roll back to the paused TSO and continue to replicate data using TiCDC. This streamlines the pre-online validation process and simplifies data management.

    ```sql
    FLASHBACK CLUSTER TO TSO 445494839813079041;
    ````

    For more information, see [documentation](/sql-statements/sql-statement-flashback-cluster.md).

* Support automatically terminating long-running idle transactions [#48714](https://github.com/pingcap/tidb/pull/48714) @[crazycs520](https://github.com/crazycs520) **tw@Oreoxmt** <!--1598-->

    In scenarios where network disconnection or application failure occurs, `COMMIT`/`ROLLBACK` statements might fail to be transmitted to the database. This could lead to delayed release of database locks, causing transaction lock waits and a rapid increase in database connections. Such issues are common in test environments but can also occur occasionally in production environments, and they are sometimes difficult to diagnose promptly. To avoid these issues, TiDB v7.6.0 introduces the [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760) system variable, which automatically terminates long-running idle transactions. When a user session in a transactional state remains idle for a duration exceeding the value of this variable, TiDB will terminate the database connection of the transaction and roll back it.

    For more information, see [documentation](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760).

* Simplify the syntax for creating execution plan bindings [#48876](https://github.com/pingcap/tidb/issues/48876) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1613-->

    TiDB v7.6.0 simplifies the syntax for creating execution plan bindings. When creating an execution plan binding, you no longer need to provide the original SQL statement. TiDB identifies the original SQL statement based on the statement with hints. This improvement enhances the convenience of creating execution plan bindings. For example:

    ```sql
    CREATE GLOBAL BINDING
    USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
    ```

    For more information, see [documentation](/sql-plan-management.md#create-a-binding-according-to-a-sql-statement).

* Support dynamically modifying the size limit of a single row record in TiDB [#49237](https://github.com/pingcap/tidb/pull/49237) @[zyguan](https://github.com/zyguan) **tw@Oreoxmt** <!--1452-->

    Before v7.6.0, the size of a single row record in a transaction is limited by the TiDB configuration item [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50). If the size limit is exceeded, TiDB returns the `entry too large` error. In this case, you need to manually modify the TiDB configuration file and restart TiDB to make the modification take effect. To reduce your management overhead, TiDB v7.6.0 introduces the system variable [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760), which supports dynamically modifying the value of the `txn-entry-size-limit` configuration item. The default value of this variable is `0`, which means that TiDB uses the value of the configuration item `txn-entry-size-limit` by default. When this variable is set to a non-zero value, TiDB limits the size of a row record in transactions to the value of this variable. This improvement enhances the flexibility for you to adjust system configurations without restarting TiDB.

    For more information, see [documentation](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760).


* The global sort feature becomes generally available (GA), improving the performance and stability of `ADD INDEX` and `IMPORT INTO` [#45719](https://github.com/pingcap/tidb/issues/45719) @[wjhuang2016](https://github.com/wjhuang2016) @[D3Hunter](https://github.com/D3Hunter) **tw@ran-huang** <!--1580/1579-->

    Prior to v7.4.0, when executing tasks such as `ADD INDEX` or `IMPORT INTO` using the [Distributed eXecution Framework (DXF)](/tidb-distributed-execution-framework.md), due to limited local storage space in TiDB, only a portion of the data could be sorted locally before importing it into TiKV. The data imported into TiKV had a significant overlap range and required additional resources for processing, which reduced the performance and stability of TiKV.

    With the introduction of the global sort feature in v7.4.0, data can be temporarily stored in external storage (such as S3) for global sorting before being imported into TiKV. This improvement reduces resource consumption of TiKV and significantly improves the performance and stability of operations such as `ADD INDEX` and `IMPORT INTO`. This feature becomes GA in v7.6.0.

    For more information, see [documentation](/tidb-global-sort.md).

* BR restores system tables by default, such as user data [#48567](https://github.com/pingcap/tidb/issues/48567) @[BornChanger](https://github.com/BornChanger) **tw@Oreoxmt** <!--1570/1628-->

    Starting from v5.1.0, when you back up snapshots, BR automatically backs up system tables in the `mysql` schema, but does not restore these system tables by default. In v6.2.0, BR adds the parameter `--with-sys-table` to support restoring data in some system tables, providing more flexibility in operations.

    To further reduce your management overhead and provide more intuitive default behavior, starting from v7.6.0, BR enables the parameter `--with-sys-table` by default and supports restoring user data for the `cloud_admin` user. This means that BR restores some system tables by default during restoration, especially user account and table statistics data. This improvement makes backup and restore operations more intuitive, thereby reducing the burden of manual configuration and improving the overall operation experience.

    For more information, see [documentation](/br/br-snapshot-guide.md).

### Observability

* Enhance observability related to resource control [#49318](https://github.com/pingcap/tidb/issues/49318) @[glorv](https://github.com/glorv) @[bufferflies](https://github.com/bufferflies) @[nolouch](https://github.com/nolouch) **tw@hfxsd** <!--1668-->

    As more and more users use resource groups to isolate application workloads, Resource Control provides enhanced data based on resource groups. This helps you monitor resource group workloads and settings, ensuring that you can quickly identify and accurately diagnose problems, including:

    * [Slow Queries](/identify-slow-queries.md): add the resource group name, RU consumption, and time for waiting for resources.
    * [Statement Summary Tables](/statement-summary-tables.md): add the resource group name, RU consumption, and time for waiting for resources.
    * In the system variable [`tidb_last_query_info`](/system-variables.md#tidb_last_query_info-new-in-v4014), add a new entry `ru_consumption` to indicate the consumed [RU](/tidb-resource-control.md#what-is-request-unit-ru) by SQL statements. You can use this variable to get the resource consumption of the last statement in the session.
    * Add database metrics based on resource groups: QPS/TPS, execution time (P999/P99/P95), number of failures, number of connections.
    * Add the system table [`request_unit_by_group`](/mysql-schema.md#system-tables-related-to-resource-control) to record the history records of daily consumed resource units (RUs) of all resource groups.

    For more information, see [Identify Slow Queries](/identify-slow-queries.md), [Statement Summary Tables](/statement-summary-tables.md), and [Key Monitoring Metrics of Resource Control](/grafana-resource-control-dashboard.md).

### Data migration

* Data Migration (DM) support for migrating MySQL 8.0 becomes generally available (GA) [#10405](https://github.com/pingcap/tiflow/issues/10405) @[lyzx2001](https://github.com/lyzx2001) **tw@hfxsd** <!--1617-->

    Previously, using DM to migrate data from MySQL 8.0 is an experimental feature and is not available for production environments. TiDB v7.6.0 enhances the stability and compatibility of this feature to help you smoothly and quickly migrate data from MySQL 8.0 to TiDB in production environments. In v7.6.0, this feature becomes generally available (GA).

    For more information, see [documentation](/dm/dm-compatibility-catalog.md).

* TiCDC supports replicating DDL statements in bi-directional replication (BDR) mode (experimental) [#10301](https://github.com/pingcap/tiflow/issues/10301) [#48519](https://github.com/pingcap/tidb/issues/48519) @[okJiang](https://github.com/okJiang) @[asddongmen](https://github.com/asddongmen) **tw@hfxsd** <!--1521/1525/1460-->

    Starting from v7.6.0, TiCDC supports replication of DDL statements with bi-directional replication configured. Previously, replicating DDL statements was not supported by TiCDC, so users of TiCDC's bi-directional replication had to apply DDL statements to both TiDB clusters separately. With this feature, TiCDC allows for a cluster to be assigned the `PRIMARY` BDR role, and enables the replication of DDL statements from that cluster to the downstream cluster.

    For more information, see [documentation](/ticdc/ticdc-bidirectional-replication.md).

* TiCDC supports querying the downstream synchronization status of a changefeed [#10289](https://github.com/pingcap/tiflow/issues/10289) @[hongyunyan](https://github.com/hongyunyan) **tw@qiancai** <!--1627-->

    Starting from v7.6.0, TiCDC introduces a new API `GET /api/v2/changefeed/{changefeed_id}/synced` to query the downstream synchronization status of a specified replication task (changefeed). By using this API, you can determine whether the upstream data received by TiCDC has been synchronized to the downstream system completely.

    For more information, see [documentation](/ticdc/ticdc-open-api-v2.md#query-whether-a-specific-replication-task-is-completed).

* TiCDC adds support for three-character delimiters with CSV output protocol [#9969](https://github.com/pingcap/tiflow/issues/9969) @[zhangjinpeng1987](https://github.com/zhangjinpeng1987) **tw@hfxsd** <!--1653-->

    Starting from v7.6.0, you can specify the CSV output protocol delimiters as 1 to 3 characters long. With this change, you can configure TiCDC to generate file output using two character delimiters (such as `||` or `$^`) or three character delimiters (such as `|@|`) to separate fields in the output.

    For more information, see [documentation](/ticdc/ticdc-csv.md).

## Compatibility changes

> **Note:**
>
> This section provides compatibility changes you need to know when you upgrade from v7.5.0 to the current version (v7.6.0). If you are upgrading from v7.4.0 or earlier versions to the current version, you might also need to check the compatibility changes introduced in intermediate versions.

### Behavior changes

### System variables

| Variable name | Change type | Description |
|--------|------------------------------|------|
| [`tidb_analyze_distsql_scan_concurrency`](/system-variables.md#tidb_analyze_distsql_scan_concurrency-new-in-v760)       |    Newly added       |    Sets the concurrency of the `scan` operation when executing the `ANALYZE` operation. The default value is `4`.  | 
| [`tidb_ddl_version`](/system-variables.md#tidb_ddl_version-new-in-v760)  |  Newly added  | Controls whether to enable [TiDB DDL V2](/ddl-v2.md). Set the value to `2` to enable it and `1` to disable it. The default value is `1`. When TiDB DDL V2 is enabled, DDL statements will be executed using TiDB DDL V2. The execution speed of DDL statements for creating tables is increased by 10 times compared with TiDB DDL V1. |
| [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-new-in-v760)  |  Newly added   | Controls whether to support creating `Global indexes` for partitioned tables. The default value is `OFF`. `Global index` is currently in the development stage. **It is not recommended to modify the value of this system variable**. |
| [`tidb_idle_transaction_timeout`](/system-variables.md#tidb_idle_transaction_timeout-new-in-v760) | Newly added | Controls the idle timeout for transactions in a user session. When a user session is in a transactional state and remains idle for a duration exceeding the value of this variable, TiDB will terminate the session. The default value `0` means unlimited. |
| [`tidb_txn_entry_size_limit`](/system-variables.md#tidb_txn_entry_size_limit-new-in-v760) | Newly added | Dynamically modifies the TiDB configuration item [`performance.txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50). It limits the size of a single row of data in TiDB. The default value of this variable is `0`, which means that TiDB uses the value of the configuration item `txn-entry-size-limit` by default. When this variable is set to a non-zero value, `txn-entry-size-limit` is also set to the same value. |

### Configuration file parameters

| Configuration file | Configuration parameter | Change type | Description |
| -------- | -------- | -------- | -------- |
| TiKV | [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression) | Modified | The algorithm used for compressing values in Titan, which takes value as the unit. Starting from TiDB v7.6.0, the default compression algorithm is `zstd`. |
| TiKV | [`rocksdb.titan.enabled`](/tikv-configuration-file.md#enabled) | Modified  |  Enables or disables Titan. For v7.5.0 and earlier versions, the default value is `false`. Starting from v7.6.0, the default value is `true` for only new clusters. Existing clusters upgraded to v7.6.0 or later versions will retain the original configuration. |
| TiKV | [`raftstore.periodic-full-compact-start-times`](/tikv-configuration-file.md#periodic-full-compact-start-times-new-in-v760) | Newly added | Sets the specific times that TiKV initiates periodic full compaction. The default value `[]` means periodic full compaction is disabled by default. |
| TiKV | [`raftstore.periodic-full-compact-start-max-cpu`](/tikv-configuration-file.md#periodic-full-compact-start-max-cpu-new-in-v760) | Newly added | Limits the maximum CPU usage rate for TiKV periodic full compaction. The default value is `0.1`. |
| TiKV | [`zstd-dict-size`](/tikv-configuration-file.md#zstd-dict-size) |  Newly added | Specifies the `zstd` dictionary compression size. The default value is `"0KB"`, which means to disable the `zstd` dictionary compression. |

### System tables

- Add a new system table [`INFORMATION_SCHEMA.KEYWORDS`](/information-schema/information-schema-keywords.md) to display the information of all keywords supported by TiDB. **tw@Oreoxmt**
- In the system table [`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md), add the following fields related to Resource Control:
    - `Resource_group`: the resource group that the statement is bound to.
    - `Request_unit_read`: the total read RUs consumed by the statement.
    - `Request_unit_write`: the total write RUs consumed by the statement.
    - `Time_queued_by_rc`: the total time that the statement waits for available resources.

## Offline package changes

## Deprecated features

* 实验特性 [执行计划的自动演进绑定](https://docs.pingcap.com/zh/tidb/stable/sql-plan-management#%E8%87%AA%E5%8A%A8%E6%BC%94%E8%BF%9B%E7%BB%91%E5%AE%9A-baseline-evolution) 将在 v8.0.0 被废弃，等同的功能将会在后续版本被重新设计。

* 废弃功能 2

## Improvements

+ TiDB

    - When a non-binary collation is set and the query condition includes `LIKE`, the optimizer generates an `IndexRangeScan` to improve the execution efficiency [#48181](https://github.com/pingcap/tidb/issues/48181) @[time-and-fate](https://github.com/time-and-fate)

## Bug fixes

## Contributors
